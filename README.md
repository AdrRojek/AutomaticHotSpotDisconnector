# Automatic Hotspot Wi-Fi Disconnector for macOS

This script automatically turns off Wi-Fi when you lock your Mac while connected to a mobile hotspot (e.g., iPhone), and turns it back on after unlocking.

## Features
- Detects connection to a mobile hotspot (by SSID or IP range)
- Disables Wi-Fi immediately after screen lock
- Enables Wi-Fi automatically after unlocking
- Runs fully in the background, no Dock or menu bar icon

## Requirements
- macOS (tested on Sonoma and newer)
- Python 3
- `pyobjc-framework-Quartz` package (for screen lock detection)

## Installation

1. **Clone or copy the script to any folder, e.g.:**
   ```sh
   git clone <repo-url> ~/AutomaticHotSpotDisconnetor
   cd ~/AutomaticHotSpotDisconnetor
   ```

2. **Install required Python package:**
   ```sh
   pip3 install pyobjc-framework-Quartz
   ```

3. **Make the script executable:**
   ```sh
   chmod +x hotspot_disconnect_daemon.py
   ```

4. **(Recommended) Set up automatic start with macOS LaunchAgent:**
   - Edit the provided `com.user.hotspotdisconnect.plist` file:
     - Replace `__WORKSPACE__/hotspot_disconnect_daemon.py` with the full path to your script, e.g. `/Users/youruser/AutomaticHotSpotDisconnetor/hotspot_disconnect_daemon.py`
   - Copy the plist file to your LaunchAgents folder:
     ```sh
     cp com.user.hotspotdisconnect.plist ~/Library/LaunchAgents/
     ```
   - Load the agent:
     ```sh
     launchctl load ~/Library/LaunchAgents/com.user.hotspotdisconnect.plist
     ```

## Manual Start/Stop
- **Start manually:**
  ```sh
  python3 hotspot_disconnect_daemon.py &
  ```
- **Stop (if running in background):**
  ```sh
  pkill -f hotspot_disconnect_daemon.py
  ```

## Uninstall
- Remove the LaunchAgent:
  ```sh
  launchctl unload ~/Library/LaunchAgents/com.user.hotspotdisconnect.plist
  rm ~/Library/LaunchAgents/com.user.hotspotdisconnect.plist
  ```
- Delete the script folder.

## Notes
- The script only disables Wi-Fi if you are connected to a mobile hotspot (iPhone or similar).
- After unlocking, Wi-Fi is enabled and macOS will automatically reconnect to your preferred network.
- No logs or icons are created.
