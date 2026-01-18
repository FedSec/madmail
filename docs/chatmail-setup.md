# Chatmail Server Setup Guide

This guide explains how to set up a Madmail server. Madmail is designed for rapid deployment, especially in environments where speed and IP-based access are priorities (e.g., in Iran).

## 🚀 Fast Deployment (IP-Based)

Many Madmail servers currently operating in Iran use direct IP addresses to bypass DNS-related delays and issues. Each server provides an automated installation script through its own web interface at `http://[YOUR_SERVER_IP]/deploy.html`.

### Automated Installation Command

Run the following command on a clean **Debian** or **Ubuntu** server to install Madmail rapidly using your public IP:

```bash
wget http://[SOURCE_SERVER_IP]/madmail && chmod +x madmail && sudo ./madmail install --simple --ip [YOUR_PUBLIC_IP] && sudo systemctl start maddy
```

*Note: Replace `[SOURCE_SERVER_IP]` with the IP of any existing Madmail server. Replace `[YOUR_PUBLIC_IP]` with the IP of your new server. If you cannot reach a server directly, you can download the latest `madmail` binary and its SHA256 hash from our [**Telegram Channel**](https://t.me/the_madmail). Always [verify the binary hash](./binary-verification.md) before installation.*

### Interactive Setup
During the `--simple` installation, you will be asked two key questions. If you are setting up an IP-based server, enter your **Server IP** for both:

1.  **Primary domain**: Enter your Public IP (e.g., `1.2.3.4`).
2.  **Public IP address**: Confirm your Public IP (e.g., `1.2.3.4`).

### Quick Update
To update an existing installation to the latest version while keeping simple settings and your current IP:

```bash
sudo systemctl stop maddy.service && rm -f madmail && wget http://[SOURCE_SERVER_IP]/madmail && chmod +x madmail && sudo ./madmail install --simple --ip [YOUR_PUBLIC_IP] && sudo systemctl start maddy
```

---

## 🛠 Advanced & Manual Setup

While the script above is the fastest way to get online, you can also perform a more customized installation or use Docker for better isolation.

### 1. Manual Installation
For full control over the installation process, run the installer without the `--simple` flag:

```bash
sudo ./madmail install
```
This will allow you to configure specific storage paths, custom domains, and more.

### 2. Docker Deployment
If you prefer containerization, you can use the official Docker image. See the [**Docker Documentation**](./docker.md) for detailed environment variables and volume mappings.

### 3. Prerequisites & Troubleshooting
- **Open Ports**: Ensure the following ports are open in your firewall:
  - `80` (HTTP)
  - `25` (SMTP)
  - `143` & `993` (IMAP)
- **Configuration File**: After installation, your settings are stored at `/etc/maddy/maddy.conf`. You can edit this file to close registration, change rate limits, or add domains.
- **OS Support**: Best supported on Debian-based distributions (Debian, Ubuntu, etc.).

### 🤝 Community & Support
For the latest binaries, installation tips, and community support, join the Telegram channel:
👉 [**Madmail Telegram Channel**](https://t.me/the_madmail)

---
*Technical Note: The fast-install logic is implemented in [`internal/endpoint/chatmail/www/deploy.html`](../internal/endpoint/chatmail/www/deploy.html) and the [`madmail` CLI tool](../).*