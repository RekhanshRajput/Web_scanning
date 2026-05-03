import requests
import re

#  fetch from wayback
def from_wayback(domain):
    urls = set()
    try:
        api = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&collapse=urlkey"
        r = requests.get(api, timeout=10)

        data = r.json()

        for row in data[1:]:
            urls.add(row[2])
    except:
        pass
    return urls


#  fetch from gau-like api
def from_gau(domain):
    urls = set()
    try:
        r = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=10)
        for line in r.text.splitlines():
            urls.add(line.split(",")[0])
    except:
        pass
    return urls


#  extract params
def extract_params(urls):
    params = set()
    for u in urls:
        if "?" in u:
            parts = u.split("?")[1]
            for p in parts.split("&"):
                key = p.split("=")[0]
                params.add(key + "=")
    return params


#  filter interesting files
def filter_urls(urls):
    interesting = []
    for u in urls:
        if any(ext in u for ext in [".php", ".json", ".aspx", ".jsp", ".zip", ".bak"]):
            interesting.append(u)
    return interesting


#  MAIN FUNCTION
def get_wayback_data(domain):
    print("\n[+] Fetching historical URLs...\n")

    all_urls = set()

    print("[*] Wayback...")
    all_urls.update(from_wayback(domain))

    print("[*] Other sources...")
    all_urls.update(from_gau(domain))

    print(f"\n[+] Total URLs collected: {len(all_urls)}")

    #  extract
    params = extract_params(all_urls)
    interesting = filter_urls(all_urls)

    return list(all_urls), list(params), list(interesting)