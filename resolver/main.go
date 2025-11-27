package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"os/signal"
	"strings"
	"sync"
	"syscall"
	"time"

	"github.com/miekg/dns"
)

var (
	backendURL      string
	resolverMapping map[string]int // IP -> FamilyID
	cache           sync.Map
	cacheTTL        = 5 * time.Second
)

type Policy struct {
	FamilyID      int      `json:"family_id"`
	BlockAdult    bool     `json:"block_adult"`
	BlockPhishing bool     `json:"block_phishing"`
	BlockScam     bool     `json:"block_scam"`
	Blocklist     []string `json:"blocklist"`
	Whitelist     []string `json:"whitelist"`
}

type CacheEntry struct {
	Policy    *Policy
	ExpiresAt time.Time
}

func main() {
	backendURL = os.Getenv("BACKEND_URL")
	if backendURL == "" {
		backendURL = "http://localhost:8000"
	}

	// Parse mapping: 127.0.0.1:1,192.168.1.50:2
	resolverMapping = make(map[string]int)
	mappingEnv := os.Getenv("RESOLVER_MAPPING")
	if mappingEnv != "" {
		parts := strings.Split(mappingEnv, ",")
		for _, part := range parts {
			kv := strings.Split(part, ":")
			if len(kv) == 2 {
				var id int
				fmt.Sscanf(kv[1], "%d", &id)
				resolverMapping[kv[0]] = id
			}
		}
	}

	// Handle TCP and UDP
	go func() {
		srv := &dns.Server{Addr: ":5353", Net: "udp"}
		srv.Handler = dns.HandlerFunc(handleRequest)
		log.Printf("Starting UDP listener on :5353")
		if err := srv.ListenAndServe(); err != nil {
			log.Fatalf("Failed to set up UDP listener %s\n", err.Error())
		}
	}()

	go func() {
		srv := &dns.Server{Addr: ":5353", Net: "tcp"}
		srv.Handler = dns.HandlerFunc(handleRequest)
		log.Printf("Starting TCP listener on :5353")
		if err := srv.ListenAndServe(); err != nil {
			log.Fatalf("Failed to set up TCP listener %s\n", err.Error())
		}
	}()

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
	s := <-sig
	log.Printf("Signal (%v) received, stopping\n", s)
}

func handleRequest(w dns.ResponseWriter, r *dns.Msg) {
	m := new(dns.Msg)
	m.SetReply(r)
	m.Compress = false

	switch r.Opcode {
	case dns.OpcodeQuery:
		parseQuery(m, w.RemoteAddr())
	}

	w.WriteMsg(m)
}

func parseQuery(m *dns.Msg, remoteAddr net.Addr) {
	for _, q := range m.Question {
		name := strings.ToLower(q.Name)
		// Remove trailing dot
		name = strings.TrimSuffix(name, ".")

		clientIP, _, _ := net.SplitHostPort(remoteAddr.String())
		// Determine Family ID
		familyID, ok := resolverMapping[clientIP]
		if !ok {
			// Default or fallback logic. For MVP, if not mapped, allow all or map to default.
			// Let's assume default family ID 1 for localhost if not explicitly mapped, or just allow.
			if clientIP == "127.0.0.1" || clientIP == "::1" {
				familyID = 1 // Default dev family
			} else {
				// Allow if unknown
				resolveExternal(m, q)
				continue
			}
		}

		policy := getPolicy(familyID)
		if policy != nil {
			if isBlocked(name, policy) {
				logEvent(familyID, name, true, "Policy Block", clientIP)
				// Return NXDOMAIN
				m.Rcode = dns.RcodeNameError
				continue
			}
		}

		// Not blocked, resolve normally
		resolveExternal(m, q)
	}
}

func getPolicy(familyID int) *Policy {
	// Check cache
	if val, ok := cache.Load(familyID); ok {
		entry := val.(CacheEntry)
		if time.Now().Before(entry.ExpiresAt) {
			return entry.Policy
		}
	}

	// Fetch from backend
	resp, err := http.Get(fmt.Sprintf("%s/api/policy/%d", backendURL, familyID))
	if err != nil {
		log.Printf("Error fetching policy: %v", err)
		return nil
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return nil
	}

	var policy Policy
	if err := json.NewDecoder(resp.Body).Decode(&policy); err != nil {
		return nil
	}

	cache.Store(familyID, CacheEntry{
		Policy:    &policy,
		ExpiresAt: time.Now().Add(cacheTTL),
	})

	return &policy
}

func isBlocked(domain string, policy *Policy) bool {
	// Whitelist check
	for _, w := range policy.Whitelist {
		if strings.Contains(domain, w) {
			return false
		}
	}

	// Blocklist check
	for _, b := range policy.Blocklist {
		if strings.Contains(domain, b) {
			return true
		}
	}

	// Category check (stub - in real app would check domain categorization service)
	if policy.BlockAdult && (strings.Contains(domain, "porn") || strings.Contains(domain, "xxx")) {
		return true
	}

	return false
}

func resolveExternal(m *dns.Msg, _ dns.Question) {
	c := new(dns.Client)
	in, _, err := c.Exchange(m, "8.8.8.8:53") // Forward to Google DNS
	if err != nil {
		log.Printf("Error resolving external: %v", err)
		return
	}
	m.Answer = append(m.Answer, in.Answer...)
}

func logEvent(familyID int, domain string, blocked bool, reason string, clientIP string) {
	go func() {
		payload := map[string]interface{}{
			"family_id": familyID,
			"domain":    domain,
			"blocked":   blocked,
			"reason":    reason,
			"client_ip": clientIP,
		}
		jsonPayload, _ := json.Marshal(payload)
		http.Post(fmt.Sprintf("%s/api/events/", backendURL), "application/json", bytes.NewBuffer(jsonPayload))
	}()
}
