# SQLHOUND (v1.0)

A lightweight multithreaded SQL Injection (SQLi) vulnerability scanner using Bing dorking, subdomain enumeration, and custom URL lists.  
It detects common SQLi error messages by injecting typical SQL payloads into URLs.

---

## Features

- Search Bing using custom dorks to find URLs.
- Enumerate subdomains using [crt.sh](https://crt.sh) for a target domain.
- Scan URLs from a file or directly from dork results.
- Supports multithreaded scanning for speed.
- Filter search results by specific domain.
- Saves vulnerable URLs to a file.
- Simple detection using common SQLi error strings.
- User-agent rotation and randomized delays for stealth.

---

## Requirements

- Python 3.6+
- Packages:
  - `requests`
  - `beautifulsoup4`

Install dependencies with:

```bash
pip install requests beautifulsoup4
````

---

## Usage

```bash
python3 sqli_scanner.py [OPTIONS]
```

### Options

| Option                  | Description                                          |
| ----------------------- | ---------------------------------------------------- |
| `--dorks <dork> [...]`  | List of Bing search dorks to find URLs               |
| `--urls <file>`         | Path to a file containing URLs to scan directly      |
| `--limit <number>`      | Limit number of links to scan per dork (default: 10) |
| `--threads <number>`    | Number of concurrent threads (default: 5)            |
| `--output <file>`       | Save vulnerable URLs found to the specified file     |
| `--domain <domain>`     | Enumerate subdomains of a domain and scan them       |
| `--dorkdomain <domain>` | Restrict Bing dork search results to this domain     |

---

## Examples

### Scan URLs from a file

```bash
python3 sqli_scanner.py --urls urls.txt --threads 10 --output vulnerable.txt
```

### Search Bing with dorks and scan top 20 results per dork

```bash
python3 sqli_scanner.py --dorks "inurl:index.php?id=" "inurl:product.php?id=" --limit 20 --threads 8
```

### Enumerate subdomains for example.com and scan

```bash
python3 sqli_scanner.py --domain example.com --threads 10
```

### Search Bing dorks restricted to a specific domain

```bash
python3 sqli_scanner.py --dorks "inurl:page.php?id=" --dorkdomain example.com --limit 15
```

---

## How It Works

1. **Dorking**: Uses Bing search with your provided dorks to collect URLs.
2. **Subdomain Enumeration**: Queries crt.sh to find active subdomains for a given domain.
3. **Scanning**: Injects SQL payloads into URLs and checks for known SQL error messages in the HTTP response.
4. **Multithreading**: Speeds up scanning by running multiple checks concurrently.

---

## Notes

* Make sure to use this tool responsibly and only scan domains and URLs you have permission to test.
* Some SQL injection error messages may be customized or hidden by web applications, causing false negatives.
* Requests verify SSL by default is disabled to avoid issues with invalid certificates.

---

## License

This project is provided as-is under the MIT License.

---

## Author

MikiVirus

---

