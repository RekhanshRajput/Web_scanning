import requests
from concurrent.futures import ThreadPoolExecutor
from rich import print
import re

def get_title(html):
    try:
        title = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
        return title.group(1).strip() if title else "No Title"
    except:
        return "No Title"


def check_host(host):
    for scheme in ["https://", "http://"]:  
        url = scheme + host

        try:
            r = requests.get(url, timeout=3, allow_redirects=True)

            status = r.status_code
            title = get_title(r.text)

            return {
                "url": url,
                "status": status,
                "title": title
            }

        except:
            continue

    return None


def alive_hosts(file_path):
    results = []

    try:
        with open(file_path, "r") as f:
            targets = [line.strip() for line in f if line.strip()]
    except:
        return [], "File not found!"

    print(f"\n[+] Checking {len(targets)} hosts...\n")

    with ThreadPoolExecutor(max_workers=30) as executor:
        output = executor.map(check_host, targets)

    for res in output:
        if res:
            results.append(res)

    return results, None