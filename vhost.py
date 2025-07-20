import socket
import sys
import argparse
import requests
import time


def scan_subdomains(domain, wordlist_path):
    valid_subdomains = []
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as file:
            words = [line.strip() for line in file if line.strip()]
    except UnicodeDecodeError:
        print(f"[!] UTF-8 decode error. Retrying with latin-1 encoding...")
        try:
            with open(wordlist_path, 'r', encoding='latin-1') as file:
                words = [line.strip() for line in file if line.strip()]
        except Exception as e:
            print(f"[!] Failed to read wordlist with latin-1 encoding: {e}")
            sys.exit(1)
    except FileNotFoundError:
        print(f"[!] Wordlist file not found: {wordlist_path}")
        sys.exit(1)

    print(f"[+] Scanning {len(words)} subdomains for {domain}...\n")
    for word in words:
        subdomain = f"{word}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            print(f"[FOUND] {subdomain} -> {ip}")
            valid_subdomains.append((subdomain, ip))
        except socket.gaierror:
            pass  # Not found, skip
    print(f"\n[+] Scan complete. {len(valid_subdomains)} valid subdomains found.")
    return valid_subdomains


def fetch_crtsh_subdomains(domain, retries=3, timeout=30):
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    print(f"[+] Fetching subdomains from crt.sh for {domain}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"https://crt.sh/?q=%.{domain}",
        "Connection": "keep-alive"
    }
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            break
        except Exception as e:
            print(f"[!] Attempt {attempt} failed: {e}")
            if attempt == retries:
                print(f"[!] Error fetching data from crt.sh after {retries} attempts.")
                sys.exit(1)
            else:
                print("[!] Retrying in 5 seconds...")
                time.sleep(5)
    subdomains = set()
    for entry in data:
        name_value = entry.get('name_value', '')
        for sub in name_value.split('\n'):
            if sub.endswith(domain):
                subdomains.add(sub.strip())
    print(f"[+] Found {len(subdomains)} unique subdomains:")
    for sub in sorted(subdomains):
        print(sub)
    return subdomains


def main():
    parser = argparse.ArgumentParser(description="Subdomain Scanner with wordlist or crt.sh mode")
    parser.add_argument("domain", help="Target domain (e.g. example.com)")
    parser.add_argument("wordlist", nargs="?", help="Path to wordlist file (if specified, wordlist mode is used)")
    parser.add_argument("--mode", choices=["crtsh"], help="If no wordlist is given, use --mode crtsh to fetch from crt.sh")
    args = parser.parse_args()

    if args.wordlist:
        scan_subdomains(args.domain, args.wordlist)
    elif args.mode == "crtsh":
        fetch_crtsh_subdomains(args.domain)
    else:
        print("[!] You must specify a wordlist for wordlist mode, or use --mode crtsh for crt.sh mode.")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
