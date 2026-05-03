import requests
import subprocess

def from_crtsh(domain):
    subs = set()
    try:
        r = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=10)
        data = r.json()
        for entry in data:
            for sub in entry.get("name_value", "").split("\n"):
                if domain in sub:
                    subs.add(sub.strip())
    except:
        pass
    return subs


def from_hackertarget(domain):
    subs = set()
    try:
        r = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=10)
        for line in r.text.splitlines():
            subs.add(line.split(",")[0])
    except:
        pass
    return subs


def from_bufferover(domain):
    subs = set()
    try:
        r = requests.get(f"https://dns.bufferover.run/dns?q=.{domain}", timeout=10)
        data = r.json()

        for entry in data.get("FDNS_A", []):
            subs.add(entry.split(",")[1])

        for entry in data.get("RDNS", []):
            subs.add(entry.split(",")[1])
    except:
        pass
    return subs


def from_threatcrowd(domain):
    subs = set()
    try:
        r = requests.get(f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}", timeout=10)
        data = r.json()
        for sub in data.get("subdomains", []):
            subs.add(sub)
    except:
        pass
    return subs


def from_subfinder(domain):
    subs = set()
    try:
        output = subprocess.getoutput(f"subfinder -d {domain} -silent 2>nul")
        for sub in output.splitlines():
            subs.add(sub.strip())
    except:
        pass
    return subs


def find_subdomains(domain):
    print("\n[+] Collecting subdomains from multiple sources...\n")

    all_subs = set()

    print("[*] crt.sh...")
    all_subs.update(from_crtsh(domain))

    print("[*] hackertarget...")
    all_subs.update(from_hackertarget(domain))

    print("[*] bufferover...")
    all_subs.update(from_bufferover(domain))

    print("[*] threatcrowd...")
    all_subs.update(from_threatcrowd(domain))

    print("[*] subfinder (optional)...")
    all_subs.update(from_subfinder(domain))

    return sorted(all_subs)