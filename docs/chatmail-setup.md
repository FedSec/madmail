# Getting Started & Setup Guide

This guide explains how to get started with the Delta Chat ecosystem and set up your own Madmail server.

## 📱 Step 1: Get Delta Chat
Delta Chat is the messaging application that connects to this server. It works like email but feels like a modern chat app.
- [**Delta Chat Official Website**](https://delta.chat)
- [**Download Apps** (Android, iOS, Desktop)](https://delta.chat/en/download)

---

## 🚀 Step 2: Fast Server Deployment (IP-Based)

Madmail is designed for rapid deployment. Many servers currently operating in Iran use direct IP addresses to bypass DNS-related delays.

### A. Automated Installation (wget)
Run the following command on a clean **Debian** or **Ubuntu** server to install Madmail rapidly using your public IP:

```bash
wget http://[SOURCE_SERVER_IP]/madmail && chmod +x madmail && sudo ./madmail install --simple --ip [YOUR_PUBLIC_IP] && sudo systemctl start maddy
```

### B. Installation via SCP (Local Binary)
If you have downloaded the `madmail` binary locally (e.g., from [Telegram](https://t.me/the_madmail)), you can upload and install it via `scp`:

1.  **Upload the binary**:
    ```bash
    scp madmail root@[YOUR_SERVER_IP]:/root/
    ```
2.  **Run the installation**:
    ```bash
    ssh root@[YOUR_SERVER_IP] "chmod +x /root/madmail && ./root/madmail install --simple --ip [YOUR_SERVER_IP] && systemctl start maddy"
    ```

*Note: Replace `[SOURCE_SERVER_IP]` with the IP of any existing Madmail server. Replace `[YOUR_PUBLIC_IP]` with the IP of your new server. Always [verify the binary hash](./binary-verification.md) before installation.*

### Interactive Setup Tips
During the `--simple` installation, if you are setting up an IP-based server, enter your **Server IP** for both requested fields:
1.  **Primary domain**: Enter your Public IP (e.g., `1.2.3.4`).
2.  **Public IP address**: Confirm your Public IP (e.g., `1.2.3.4`).

### Quick Update
To update while keeping simple settings:
```bash
sudo systemctl stop maddy.service && rm -f madmail && wget http://[SOURCE_SERVER_IP]/madmail && chmod +x madmail && sudo ./madmail install --simple --ip [YOUR_PUBLIC_IP] && sudo systemctl start maddy
```

---

## 🛠 Advanced & Manual Setup

While the scripts above are the fastest way to get online, you can also perform a customized installation or use Docker.

### 1. Manual Installation
For full control, run the installer without the `--simple` flag:
```bash
sudo ./madmail install
```

### 2. Docker Deployment
See the [**Docker Documentation**](./docker.md) for detailed environment variables and volume mappings.

### 3. Prerequisites & Troubleshooting
- **Open Ports**: Ensure ports `80` (HTTP), `25` (SMTP), and `143`/`993` (IMAP) are open.
- **Configuration**: Settings are stored at `/etc/maddy/maddy.conf`.
- **OS Support**: Best supported on Debian and Ubuntu.

### 🤝 Community & Support
For the latest binaries and installation tips, join the Telegram channel:
👉 [**Madmail Telegram Channel**](https://t.me/the_madmail)

---
*Technical Note: The web-based installation instructions are served from [`internal/endpoint/chatmail/www/deploy.html`](../internal/endpoint/chatmail/www/deploy.html), while the actual installation logic is implemented in [`internal/cli/ctl/install.go`](../internal/cli/ctl/install.go).*