# NIRA-X-Guardian Chrome Extension

## Installation (Developer Mode)

1. Open Chrome and navigate to `chrome://extensions`.
2. Enable "Developer mode" in the top right.
3. Click "Load unpacked".
4. Select the `extension` directory from this repository.

## Configuration

1. Click the extension icon.
2. Enter your Family ID (from the Dashboard URL, e.g., `/family/1` -> ID is 1).
3. Click Save.
4. The extension will fetch policies from `http://localhost:8000` and block domains.

## Architecture

- Uses Manifest V3 `declarativeNetRequest` to block/redirect requests.
- Polls the backend API every minute for policy updates.
