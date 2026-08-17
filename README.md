<div align="center">

# `BLOOD-WEB`

### Modular Honeypot for Pentesting Training

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-00ff88?style=flat-square)
![Stars](https://img.shields.io/github/stars/s1d9e/blood-web?style=flat-square&color=FFD700&logo=github)
![Services](https://img.shields.io/badge/Services-7-red?style=flat-square)

```
    ╔═══════════════════════════════════════════════════════╗
    ║              🩸 BLOOD-WEB HONEYPOT                   ║
    ╠═══════════════════════════════════════════════════════╣
    ║                                                       ║
    ║   SSH · FTP · HTTP · Telnet · SMB · MySQL · RDP       ║
    ║                                                       ║
    ║   ┌─────────┐    ┌──────────┐    ┌──────────────┐    ║
    ║   │ attacker │───▶│ honeypot │───▶│   dashboard  │    ║
    ║   └─────────┘    └──────────┘    └──────────────┘    ║
    ║                        │                               ║
    ║                   ┌────▼────┐                          ║
    ║                   │  logs   │                          ║
    ║                   └─────────┘                          ║
    ╚═══════════════════════════════════════════════════════╝
```

</div>

---

## What is Blood-Web?

Blood-Web is a **modular, realistic honeypot** designed for pentesting training and attack detection. It simulates 7 vulnerable services with fake filesystems, databases, and user accounts — all in a single Python file with **zero dependencies**.

> **Authorized use only.** Run on your own infrastructure or isolated lab environments. See [LEGAL.md](LEGAL.md).

---

## Features

| Feature | Description |
|---------|-------------|
| **7 Services** | SSH, FTP, HTTP, Telnet, SMB, MySQL, RDP |
| **Web Dashboard** | Real-time monitoring with dark theme UI |
| **Structured Logs** | Forensic-ready log files |
| **Smart Detection** | SQLi, XSS, brute force, path traversal, NTLM capture |
| **Configurable** | Custom ports, optional services |
| **Zero Dependencies** | Python 3.8+ only — no `pip install` needed |

---

## Quick Start

```bash
# Clone
git clone https://github.com/s1d9e/blood-web.git
cd blood-web

# Run (non-privileged ports)
python3 blood-web.py

# With dashboard
python3 blood-web.py --web-monitor

# All services + dashboard (paranoid mode)
python3 blood-web.py --ssh --ftp --http --telnet --smb --mysql --rdp --web-monitor
```

---

## Services

| Service | Default Port | Alt Port | Attacks Detected |
|---------|-------------|----------|------------------|
| **SSH** | 22 | 2222 | Brute force, username enum, key exchange |
| **FTP** | 21 | 2121 | Credentials, directory traversal, file access |
| **HTTP** | 80 | 8080 | SQLi, XSS, path traversal, dirbusting |
| **Telnet** | 23 | 2323 | Shell commands, nmap, metasploit |
| **SMB** | 445 | 4445 | NTLM auth, share enumeration, sensitive files |
| **MySQL** | 3306 | 33306 | SQL injection, enumeration, dumps |
| **RDP** | 3389 | 33890 | Username extraction, connection attempts |

---

## Dashboard

Launch with `--web-monitor` and open `http://localhost:8081`:

```
┌─────────────────────────────────────────────────────────────┐
│                    🩸 BLOOD-WEB MONITOR                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│   │   247    │ │    12    │ │    45    │ │    89    │     │
│   │  TOTAL   │ │ CRITICAL │ │   HIGH   │ │  MEDIUM  │     │
│   └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
│                                                             │
│   LIVE FEED:                          TOP ATTACKERS:        │
│   ┌─────────────────────────┐        185.220.101.34  89    │
│   │ 14:32:15 192.168.1.x   │        45.33.32.156    67    │
│   │ SQL_INJECTION          │        104.211.55.210   45    │
│   │───────────────────────│        89.248.165.52    34    │
│   │ 14:32:10 10.0.0.5      │                               │
│   │ SSH_BRUTE_FORCE        │        BY SERVICE:            │
│   │───────────────────────│        SSH    ████████ 89    │
│   │ 14:31:58 172.16.0.x   │        HTTP   ██████   67    │
│   │ FTP_TRAVERSAL          │        FTP    ████     45    │
│   └─────────────────────────┘        SMB    ██      23    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Attack Examples

### SSH Brute Force
```bash
hydra -l admin -P rockyou.txt ssh://localhost:2222
```

### HTTP SQL Injection
```bash
curl "http://localhost:8080/api/user?id=1' OR '1'='1"
```

### FTP Credential Stuffing
```bash
ftp localhost 2121
USER admin
PASS password123
```

### Telnet with Offensive Tools
```
localhost:2323
login: admin
password: admin123
$ nmap -sV localhost
$ msfconsole
```

---

## Log Format

```log
2026-04-03 14:32:15 | 192.168.1.100:54321 -> ssh | SSH_AUTH_BRUTE_FORCE | User: admin | Severity: HIGH
2026-04-03 14:32:10 | 10.0.0.5:44321 -> http | SQL_INJECTION | /api/user?id=1' OR 1=1 | Severity: CRITICAL
2026-04-03 14:31:58 | 172.16.0.20:52341 -> ftp | FTP_CREDENTIALS | admin:password123 | Severity: HIGH
```

---

## Architecture

```
blood-web/
├── blood-web.py       # Main honeypot (1500+ lines)
├── web_monitor.py     # Dashboard server
├── logs/              # Auto-generated attack logs
├── .assets/           # Logo and images
├── LICENSE            # MIT
├── LEGAL.md           # Legal disclaimer
└── README.md
```

---

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Open a Pull Request

---

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

> *"All that and a bag of chips..."*

Made with 🩸 by [s1d9e](https://github.com/s1d9e)

</div>
