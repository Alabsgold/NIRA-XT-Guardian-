document.addEventListener('DOMContentLoaded', async () => {
    const { familyId, lastUpdate } = await chrome.storage.local.get(['familyId', 'lastUpdate']);

    if (familyId) {
        document.getElementById('familyIdInput').value = familyId;
        document.getElementById('statusText').textContent = `Active (Family ${familyId})`;
    } else {
        document.getElementById('statusText').textContent = 'Not Configured';
    }

    if (lastUpdate) {
        document.getElementById('lastUpdate').textContent = new Date(lastUpdate).toLocaleTimeString();
    }

    document.getElementById('saveBtn').addEventListener('click', async () => {
        const newId = document.getElementById('familyIdInput').value;
        if (newId) {
            await chrome.storage.local.set({ familyId: newId });
            alert('Saved! Policies will sync shortly.');
            // Trigger update immediately
            chrome.runtime.sendMessage({ action: "updateRules" }); // Need to handle this in background if we want immediate
        }
    });
});
