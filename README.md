# 🕵️‍♂️ Virtual Host Scanner

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A simple, fast, and flexible subdomain scanner for security researchers and bug bounty hunters. Supports both wordlist-based brute force and certificate transparency (crt.sh) enumeration.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Wordlist Mode](#wordlist-mode)
  - [crt.sh Mode](#crtsh-mode)
- [Example Output](#example-output)
- [Notes](#notes)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- 🔎 **Wordlist Mode:** Brute-force subdomains using any wordlist (e.g., rockyou.txt)
- 🌐 **crt.sh Mode:** Enumerate subdomains from certificate transparency logs
- 🧠 **Smart Encoding:** Automatically handles UTF-8 and latin-1 wordlists
- 🖥️ **CLI:** Simple command-line interface
- 📝 **No dependencies except `requests`**

---

## Installation

1. **Clone the repository:**
   ```sh
git clone https://github.com/yourusername/virtual-host-scanner.git
cd virtual-host-scanner/Virual\ Host\ Scanner
   ```
2. **Install dependencies:**
   ```sh
pip install requests
   ```

---

## Usage

### Wordlist Mode
Scan a domain for subdomains using a wordlist:
```sh
python vhost.py <domain> <wordlist>
```
**Example:**
```sh
python vhost.py example.com /path/to/wordlist.txt
```

### crt.sh Mode
Fetch subdomains from crt.sh (no wordlist needed):
```sh
python vhost.py <domain> --mode crtsh
```
**Example:**
```sh
python vhost.py example.com --mode crtsh
```

---

## Example Output
```
[+] Scanning 1000 subdomains for example.com...
[FOUND] test.example.com -> 93.184.216.34
[FOUND] dev.example.com -> 93.184.216.34
...
[+] Scan complete. 2 valid subdomains found.
```

---

## Notes
- For large wordlists (like rockyou.txt), scanning may take a long time.
- If your wordlist is not UTF-8 encoded, the script will automatically retry with latin-1 encoding.
- If crt.sh mode fails, check your network connection or try again later.
- KeyboardInterrupt (Ctrl+C) will stop the scan at any time.

---

## Contributing
Pull requests and suggestions are welcome! For major changes, please open an issue first to discuss what you would like to change.

---
