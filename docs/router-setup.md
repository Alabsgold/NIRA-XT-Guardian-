# Router DNS Setup Guide

To protect your entire home network with NIRA-X-Guardian, you need to configure your router to use the NIRA-X-Guardian DNS Resolver.

## Prerequisites

- NIRA-X-Guardian Resolver running on your network (e.g., on a Raspberry Pi or Server).
- IP Address of the Resolver (e.g., `192.168.1.50`).

## General Steps

1.  Log in to your router's admin panel (usually `192.168.0.1` or `192.168.1.1`).
2.  Find the **DHCP** or **LAN** settings.
3.  Look for **Primary DNS** and **Secondary DNS**.
4.  Set **Primary DNS** to your Resolver's IP (e.g., `192.168.1.50`).
5.  Set **Secondary DNS** to a public resolver (e.g., `1.1.1.1`) as a fallback, OR leave empty to enforce blocking strictly (if Resolver goes down, internet goes down).
6.  Save and Reboot router.

## TP-Link

1.  Go to **Advanced** > **Network** > **DHCP Server**.
2.  Enter Resolver IP in **Primary DNS**.
3.  Click **Save**.

## D-Link

1.  Go to **Setup** > **Network Settings**.
2.  Under **Router Settings**, enter Resolver IP in **Primary DNS Server**.
3.  Click **Save Settings**.

## Testing

1.  Reconnect your device to Wi-Fi.
2.  Visit a blocked site (e.g., add `example.com` to blocklist).
3.  You should see the Block Page.
