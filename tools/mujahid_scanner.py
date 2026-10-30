from urllib.parse import urlparse
import re

# MUJAHID SECURITY SCANNER
# Version 1.0

def scan_url(url):

    print("\n===== MUJAHID SECURITY SCANNER =====")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    domain = parsed.hostname

    if not domain:
        print("[ERROR] Invalid URL")
        return

    warnings = []

    # Check HTTPS
    if parsed.scheme == "https":
        print("[+] HTTPS: Enabled")
    else:
        warnings.append("Website does not use HTTPS")

    # Check suspicious characters
    if "@" in url:
        warnings.append("URL contains @ character")

    # Check IP address
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain):
        warnings.append("URL uses an IP address instead of a domain")

    # Check suspicious words
    keywords = ["login", "verify", "password", "secure", "account"]

    for word in keywords:
        if word in domain.lower():
            warnings.append("Suspicious keyword: " + word)

    # Check punycode
    if "xn--" in domain.lower():
        warnings.append("Domain contains punycode")

    print("[+] Domain:", domain)

    print("\n===== SCAN RESULTS =====")

    if warnings:
        for warning in warnings:
            print("[!] WARNING:", warning)
    else:
        print("[+] No configured warning patterns detected.")

    print("\n[!] This is not proof that a website is safe.")
    print("[!] No website was visited during this scan.")
    print("====================================")


while True:

    url = input("\nEnter URL (or type exit): ")

    if url.lower() == "exit":
        print("Thank you for using Mujahid Security Scanner!")
        break

    scan_url(url)
