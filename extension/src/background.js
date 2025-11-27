// background.js

const BACKEND_URL = "http://localhost:8000"; // In prod, this would be configurable
const POLL_INTERVAL = 1; // minutes

chrome.alarms.create("fetchPolicy", { periodInMinutes: POLL_INTERVAL });

chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === "fetchPolicy") {
        updateRules();
    }
});

chrome.runtime.onInstalled.addListener(() => {
    updateRules();
});

async function updateRules() {
    const { familyId } = await chrome.storage.local.get("familyId");
    if (!familyId) {
        console.log("No family ID set");
        return;
    }

    try {
        const response = await fetch(`${BACKEND_URL}/api/policy/${familyId}`);
        const policy = await response.json();

        const rules = [];
        let id = 1;

        // Blocklist rules
        if (policy.blocklist) {
            policy.blocklist.forEach(domain => {
                rules.push({
                    id: id++,
                    priority: 1,
                    action: {
                        type: "redirect",
                        redirect: { url: `${BACKEND_URL}/blockpage/${familyId}?domain=${domain}` }
                    },
                    condition: {
                        urlFilter: `||${domain}`,
                        resourceTypes: ["main_frame"]
                    }
                });
            });
        }

        // Category rules (stub)
        if (policy.block_adult) {
            rules.push({
                id: id++,
                priority: 1,
                action: { type: "block" },
                condition: { urlFilter: "porn", resourceTypes: ["main_frame"] }
            });
        }

        // Update dynamic rules
        const oldRules = await chrome.declarativeNetRequest.getDynamicRules();
        const oldRuleIds = oldRules.map(rule => rule.id);

        await chrome.declarativeNetRequest.updateDynamicRules({
            removeRuleIds: oldRuleIds,
            addRules: rules
        });

        console.log("Rules updated", rules);
        await chrome.storage.local.set({ lastUpdate: new Date().toISOString() });

    } catch (error) {
        console.error("Error updating rules", error);
    }
}
