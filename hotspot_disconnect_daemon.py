#!/usr/bin/env python3
import subprocess
import time
import sys
import os
import signal
import Quartz

# Configuration
CHECK_INTERVAL = 5  # seconds
WIFI_DEVICE = "en0"  # default Wi-Fi interface on MacBooks

wifi_disabled_by_script = False  # flag: was Wi-Fi disabled by this script?

def disconnect_wifi():
    global wifi_disabled_by_script
    try:
        subprocess.run([
            "networksetup", "-setairportpower", WIFI_DEVICE, "off"
        ], check=True)
        wifi_disabled_by_script = True  # mark Wi-Fi as disabled
    except Exception:
        pass

def enable_wifi():
    global wifi_disabled_by_script
    try:
        subprocess.run([
            "networksetup", "-setairportpower", WIFI_DEVICE, "on"
        ], check=True)
        wifi_disabled_by_script = False  # mark Wi-Fi as enabled
    except Exception:
        pass

def is_connected_to_hotspot():
    # Check if connected to iPhone hotspot (by SSID or IP range)
    ssid = None
    ip = None
    try:
        output = subprocess.check_output([
            "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport",
            "-I"
        ]).decode()
        for line in output.splitlines():
            if " SSID:" in line:
                ssid = line.split(":", 1)[1].strip()
                break
    except Exception:
        pass
    try:
        output = subprocess.check_output(["ifconfig", WIFI_DEVICE]).decode()
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("inet "):
                ip = line.split()[1]
                break
    except Exception:
        pass
    if ssid and "iphone" in ssid.lower():
        return True
    if ip and ip.startswith("172.20.10."):
        return True
    return False

def is_screen_locked():
    # Check if the screen is currently locked (using Quartz API)
    try:
        locked = Quartz.CGSessionCopyCurrentDictionary().get("CGSSessionScreenIsLocked", False)
        return locked
    except Exception:
        pass
    return False

def main():
    # Main loop: disconnect Wi-Fi on lock, enable on unlock
    while True:
        hotspot = is_connected_to_hotspot()
        locked = is_screen_locked()
        if hotspot and locked:
            disconnect_wifi()
            time.sleep(10)
        elif not locked and wifi_disabled_by_script:
            enable_wifi()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0) 