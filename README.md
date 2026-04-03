# Blood-Web Honeypot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Stars-Open-blueviolet.svg" alt="Stars">
  <img src="https://img.shields.io/badge/Forks-Welcome-orange.svg" alt="Forks">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/s1d9e/blood-web/main/.assets/logo.svg" width="400" alt="Blood-Web Logo">
</p>

> *"All that and a bag of chips..."*

**Blood-Web** est un honeypot modulaire et réaliste conçu pour la formation en pentesting et la détection d'attaques réseau. Simulez des services vulnérables et analysez les techniques d'attaque en toute sécurité.

<p align="center">
  <a href="#avertissement---important">⚠️ Avertissement</a •
  <a href="#-installation">📦 Installation</a •
  <a href="#-utilisation-rapide">🚀 Utilisation</a •
  <a href="#-services">🔧 Services</a •
  <a href="#-dashboard-web">📊 Dashboard</a •
  <a href="#-contribuer">🤝 Contribuer</a>
</p>

---

## ⚠️ Avertissement - Important

> **AVERTISSEMENT LÉGAL**
>
> Blood-Web est un outil à **usage éducatif uniquement**.
>
> - ✅ Utilisez-le sur **votre propre infrastructure**
> - ✅ Utilisez-le dans un **environnement de laboratoire isolé**
> - ✅ Avec **autorisation explicite** du propriétaire du système
> - ❌ **Toute utilisation malveillante ou non autorisée est interdite**
>
> **L'auteur ne peut être tenu responsable de toute utilisation abusive. Voir [LEGAL.md](LEGAL.md)**

---

## ✨ Fonctionnalités

| Feature | Description |
|---------|-------------|
| 🛡️ **7 Services** | SSH, FTP, HTTP, Telnet, SMB, MySQL, RDP |
| 📊 **Dashboard Web** | Monitoring en temps réel avec interface dark theme |
| 📝 **Logs Structurés** | Fichiers de logs pour analyse forensique |
| 🎯 **Détection Intelligente** | SQLi, XSS, brute force, path traversal... |
| ⚙️ **Configurable** | Ports personnalisables, services optionnels |
| 🐍 **Zero Dépendance** | Python 3.8+ uniquement, pas de `pip install` |

---

## 📦 Installation

```bash
# Cloner le repo
git clone https://github.com/s1d9e/blood-web.git
cd blood-web

# C'est tout ! Aucune dépendance requise.
# Python 3.8+ suffit.

# Lancer directement
python3 blood-web.py
```

---

## 🚀 Utilisation Rapide

```bash
# === Mode basique (ports non-privilégiés) ===
python3 blood-web.py

# === Avec le dashboard web (http://localhost:8081) ===
python3 blood-web.py --web-monitor

# === Activer tous les services ===
python3 blood-web.py --ssh --ftp --http --telnet --smb --mysql --rdp

# === Mode paranoïaque - tous les services + dashboard ===
python3 blood-web.py --ssh --ftp --http --telnet --smb --mysql --rdp --web-monitor

# === Ports personnalisés ===
python3 blood-web.py --custom-ports 2222 2121 8080 2323 4445 33306 33890

# === Ports privilégiés (requiert sudo) ===
sudo python3 blood-web.py --ssh --ftp --http --telnet
```

---

## 🔧 Services

| Service | Port Standard | Port Alternatif | Attaques Détectées |
|---------|---------------|-----------------|---------------------|
| 🖥️ **SSH** | 22 | 2222 | Brute force, username enum, key exchange |
| 📁 **FTP** | 21 | 2121 | Creds, directory traversal, file access |
| 🌐 **HTTP** | 80 | 8080 | SQLi, XSS, path traversal, dirbusting |
| 📡 **Telnet** | 23 | 2323 | Shell commands, nmap, metasploit |
| 💾 **SMB** | 445 | 4445 | NTLM auth, shares, sensitive files |
| 🗄️ **MySQL** | 3306 | 33306 | SQL injection, enumeration, dumps |
| 🖥️ **RDP** | 3389 | 33890 | Usernames, connections |

---

## 📊 Dashboard Web

Lancez le dashboard et accédez à `http://localhost:8081` :

```bash
python3 blood-web.py --web-monitor --monitor-port 8081
```

### Ce que vous verrez :

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

## 🎯 Exemples d'Attaques Détectées

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

### Telnet avec Outils Offensifs
```
localhost:2323
login: admin
password: admin123
$ nmap -sV localhost
$ msfconsole
```

---

## 📝 Format des Logs

```log
2026-04-03 14:32:15 | 192.168.1.100:54321 -> ssh | SSH_AUTH_BRUTE_FORCE | User: admin | Severity: HIGH
2026-04-03 14:32:10 | 10.0.0.5:44321 -> http | SQL_INJECTION | /api/user?id=1' OR 1=1 | Severity: CRITICAL
2026-04-03 14:31:58 | 172.16.0.20:52341 -> ftp | FTP_CREDENTIALS | admin:password123 | Severity: HIGH
```

---

## 🏗️ Structure

```
blood-web/
├── blood-web.py       # Honeypot principal (1054 lignes)
├── web_monitor.py     # Dashboard de monitoring
├── logs/              # Logs générés automatiquement
├── .gitignore
├── LICENSE            # MIT License
├── README.md
└── LEGAL.md           # Mentions légales
```

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! 

1. **Fork** le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrez une **Pull Request**

---

## 📜 Licence

MIT License - Voir [LICENSE](LICENSE)

---

## 🙏 Remerciements

- Thème **Gothic** inspiré de Resident Evil Village ♡
- Développé pour la communauté cybersécurité française 🇫🇷

---

<p align="center">
  <sub>Made with 🩸 by <a href="https://github.com/s1d9e">s1d9e</a> | Blood-Web Honeypot - For Educational Purposes Only</sub>
</p>
