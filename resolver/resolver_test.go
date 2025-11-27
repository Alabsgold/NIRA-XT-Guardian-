package main

import (
	"testing"
)

func TestIsBlocked(t *testing.T) {
	policy := &Policy{
		BlockAdult:    true,
		BlockPhishing: true,
		Blocklist:     []string{"bad.com", "evil.com"},
		Whitelist:     []string{"good.com"},
	}

	tests := []struct {
		domain  string
		blocked bool
	}{
		{"bad.com", true},
		{"sub.bad.com", true}, // Contains check
		{"evil.com", true},
		{"good.com", false},
		{"google.com", false},
		{"porn.com", true}, // Category check stub
	}

	for _, tt := range tests {
		if got := isBlocked(tt.domain, policy); got != tt.blocked {
			t.Errorf("isBlocked(%q) = %v, want %v", tt.domain, got, tt.blocked)
		}
	}
}
