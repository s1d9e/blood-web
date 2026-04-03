# Blood-Web Honeypot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Educational%20Purpose-Yes-red.svg" alt="Educational">
</p>

> *"All that and a bag of chips..."*

**Blood-Web** est un honeypot modulaire et réaliste conçu pour la formation en pentesting et la détection d'attaques réseau.

## Avertissement

⚠️ **Ce projet est à usage éducatif uniquement.** Utilisez Blood-Web uniquement sur votre propre réseau ou dans un environnement de laboratoire isolé. Toute utilisation malveillante est strictement interdite.

## Fonctionnalités

- **7 services simulés** : SSH, FTP, HTTP, Telnet, SMB, MySQL, RDP
- **Détection d'attaques en temps réel** : brute force, SQL injection, XSS, etc.
- **Logging structuré** : fichiers JSON pour analyse
- **Dashboard web** : interface de monitoring en temps réel
- **Personnalisation** : ports configurables, services optionnels

## Installation

```bash
# Cloner le repository
git clone https://github.com/s1d9e/blood-web.git
cd blood-web

# Aucune dépendance externe requise (Python 3.8+)
```

## Utilisation Rapide

```bash
# Lancer avec les services de base (ports non-privilégiés)
python3 blood-web.py

# Lancer avec le dashboard web
python3 blood-web.py --web-monitor

# Activer tous les services
python3 blood-web.py --ssh --ftp --http --telnet --smb --mysql --rdp

# Ports personnalisés
python3 blood-web.py --smb --mysql --rdp --custom-ports 2222 2121 8080 2323 445 3306 3389
```

## Services

| Service | Port (privilégié) | Port (non-privilégié) | Détecte |
|---------|-------------------|------------------------|---------|
| SSH | 22 | 2222 | Brute force, username enum |
| FTP | 21 | 2121 | Creds, directory traversal |
| HTTP | 80 | 8080 | SQLi, XSS, path traversal, dirbusting |
| Telnet | 23 | 2323 | Shell commands, offensive tools |
| SMB | 445 | 4445 | NTLM auth, file shares |
| MySQL | 3306 | 33306 | SQL injection, enumeration |
| RDP | 3389 | 33890 | Usernames, connections |

## Dashboard Web

Lancez le dashboard pour visualiser les attaques en temps réel :

```bash
# Option 1: Via blood-web.py
python3 blood-web.py --web-monitor --monitor-port 8081

# Option 2: Dashboard autonome
python3 web_monitor.py --port 8081 --log-dir logs
```

Accédez à `http://localhost:8081` pour voir :
- Nombre total d'attaques
- Répartition par sévérité (Critical/High/Medium/Low)
- Feed en temps réel des attaques
- Top attackers (IPs les plus actives)
- Stats par service

## Structure du Projet

```
blood-web/
├── blood-web.py       # Honeypot principal
├── web_monitor.py     # Dashboard de monitoring
├── logs/              # Logs d'attaques
└── README.md
```

## Format des Logs

Les attaques sont journalisées dans `logs/attacks_YYYYMMDD_HHMMSS.log` :

```
2026-04-03 12:15:19 | 192.168.1.100:54321 -> ssh | SSH_AUTH_BRUTE_FORCE | User: admin | Severity: HIGH | Payload: 61646d696e...
```

## Exemples d'Attaques Détectées

### SSH Brute Force
```bash
hydra -l admin -P wordlist.txt ssh://target:2222
```

### FTP Directory Traversal
```bash
ftp target 2121
USER anonymous
PASS anonymous
CWD ../../../etc
LIST
```

### HTTP SQL Injection
```bash
curl "http://target:8080/login?id=1' OR '1'='1"
```

### Telnet Offensive Commands
```
login: admin
password: admin123
$ nmap -sV target
$ msfconsole
```

### SMB NTLM Capture
```bash
smbclient //target/share -U admin
```

### MySQL Enumeration
```bash
mysql -h target -u root -p
SHOW DATABASES;
SELECT * FROM mysql.user;
```

### RDP Username Enum
```bash
rdesktop -u admin target:3389
```

## Personnalisation

### Modifier les Fake Credentials

Dans `blood-web.py`, modifiez les dictionnaires :

```python
# SSH fake users
self.fake_users = {
    "admin": {"pass": "yourpassword", ...},
    ...
}

# FTP fake filesystem
self.fake_files = {
    "/home/admin": [".ssh/id_rsa", "credentials.txt"],
    ...
}
```

### Ajouter de Nouveaux Services

```python
class CustomHoneypot(HoneypotService):
    def __init__(self, port: int = 9999):
        super().__init__(ServiceType.CUSTOM, port)
        
    def _handle_connection(self, client, addr):
        # Votre logique personnalisée
        self.log_attack(addr, "CUSTOM_ATTACK", "description", "HIGH")
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Soumettre des pull requests

## Licence

MIT License - Voir [LICENSE](LICENSE)

---

<p align="center">
  <sub>Blood-Web Honeypot - For Educational Purposes Only</sub>
</p>
