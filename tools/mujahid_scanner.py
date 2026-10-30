import re
import json
import argparse
import ipaddress
from datetime import datetime
from urllib.parse import urlparse

# ==================================
# MUJAHID SECURITY SCANNER
# PROFESSIONAL ADVANCED EDITION
# VERSION 2.0
# ==================================

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

SHORTENERS = [
    "bit.ly", "tinyurl.com", "t.co",
    "is.gd", "cutt.ly", "rb.gy"
]

KEYWORDS = [
    "login", "verify", "password",
    "account", "secure", "update",
    "banking", "signin", "wallet"
]


def banner():
    print(CYAN + """
========================================
       MUJAHID SECURITY SCANNER
          PROFESSIONAL V2.0
========================================
     LEARN | PRACTISE | SECURE
========================================
""" + RESET)


def scan_url(url):

    warnings = []
    score = 0

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        parsed = urlparse(url)
        domain = parsed.hostname

        if not domain:
            print(RED + "[ERROR] Invalid URL" + RESET)
            return None

        domain = domain.lower()

    except ValueError:
        print(RED + "[ERROR] Invalid URL format" + RESET)
        return None

    # HTTPS CHECK
    if parsed.scheme == "https":
        print(GREEN + "[+] HTTPS enabled" + RESET)
    else:
        warnings.append("Website does not use HTTPS")
        score += 15

    # IP ADDRESS CHECK
    try:
        ipaddress.ip_address(domain)
        warnings.append("URL uses an IP address")
        score += 20
    except ValueError:
        pass

    # SUSPICIOUS CHARACTERS
    if "@" in parsed.netloc:
        warnings.append("URL contains @ character")
        score += 20

    if "%" in url:
        warnings.append("URL contains encoded characters")
        score += 5

    # PUNYCODE CHECK
    if "xn--" in domain:
        warnings.append("Domain contains Punycode")
        score += 20

    # DOMAIN ANALYSIS
    if domain.count(".") >= 4:
        warnings.append("Unusually many subdomains")
        score += 10

    if domain.count("-") >= 3:
        warnings.append("Domain contains many hyphens")
        score += 10

    # URL LENGTH
    if len(url) > 100:
        warnings.append("Unusually long URL")
        score += 10

    # SHORTENED URL CHECK
    if domain in SHORTENERS:
        warnings.append("URL uses a shortening service")
        score += 15

    # KEYWORD CHECK
    for word in KEYWORDS:
        if word in url.lower():
            warnings.append(
                "Suspicious keyword detected: " + word
            )
            score += 5

    # FINAL RISK SCORE
    score = min(score, 100)

    if score >= 60:
        risk = "HIGH"
        colour = RED
    elif score >= 30:
        risk = "MEDIUM"
        colour = YELLOW
    else:
        risk = "LOW"
        colour = GREEN

    # RESULTS
    print("\n" + CYAN + "======= SCAN RESULTS =======" + RESET)

    print("Domain:", domain)
    print("Risk Score:", score, "/100")

    print(colour + "Risk Level:", risk + RESET)

    print("\nWarnings:")

    if warnings:
        for warning in warnings:
            print(YELLOW + "[!] " + warning + RESET)
    else:
        print(GREEN + "[+] No configured warning patterns found" + RESET)

    print("\n" + CYAN + "============================" + RESET)

    print(YELLOW + "[!] This is a heuristic assessment.")
    print("[!] A low score does not prove a website is safe.")
    print("[!] No website was visited during this scan." + RESET)

    return {
        "url": url,
        "domain": domain,
        "risk_score": score,
        "risk_level": risk,
        "warnings": warnings,
        "scan_date": datetime.now().isoformat()
    }


def main():

    parser = argparse.ArgumentParser(
        description="Mujahid Security Scanner V2.0"
    )

    parser.add_argument(
        "url",
        nargs="?",
        help="Website URL to analyse"
    )

    parser.add_argument(
        "--json",
        help="Save scan report as JSON"
    )

    args = parser.parse_args()

    banner()

    url = args.url

    if not url:
        url = input("Enter website URL: ").strip()

    if not url:
        print(RED + "[ERROR] No URL provided" + RESET)
        return

    result = scan_url(url)

    if result and args.json:
        with open(args.json, "w") as file:
            json.dump(result, file, indent=4)

        print(GREEN + "\n[+] Report saved successfully!" + RESET)


if __name__ == "__main__":
    main()
