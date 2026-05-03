import requests
from concurrent.futures import ThreadPoolExecutor
from rich import print
import re
import random
import time
import os

#  random user agents
USER_AGENTS = [
    "Mozilla/5.0",
    "Chrome/110.0",
    "Safari/537.36",
    "Edge/90.0"
]

#  extract title
def get_title(html):
    try:
        match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
        return match.group(1).strip() if match else "No Title"
    except:
        return "No Title"


#  LOAD WORDLIST (FILE + FOLDER SUPPORT)
def load_wordlist(mode, custom_path=None):
    words = set()

    #  Folder support
    if custom_path and os.path.isdir(custom_path):
        try:
            for file in os.listdir(custom_path):
                if file.endswith(".txt"):
                    with open(os.path.join(custom_path, file), "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            word = line.strip()
                            if word:
                                words.add(word)
        except:
            pass

        return list(words)

    #  Single file
    if custom_path and os.path.isfile(custom_path):
        try:
            with open(custom_path, "r", encoding="utf-8", errors="ignore") as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return []

    #  Default modes
    if mode == "1":
        return ["admin", "login", "dashboard", "api", "test"]

    elif mode == "2":
        return ["admin", "login", "dashboard", "api", "test", "backup", "config", "private"]

    elif mode == "3":
        return ["admin.php", "login.php", ".env", "config.json", "backup.zip"]

    return []


#  REQUEST FUNCTION
def scan_url(base, path, delay):
    for scheme in ["https://", "http://"]:
        url = f"{scheme}{base}/{path}"

        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS)
            }

            r = requests.get(url, headers=headers, timeout=5, allow_redirects=True)

            time.sleep(delay)

            return {
                "url": url,
                "status": r.status_code,
                "size": len(r.content),
                "title": get_title(r.text)
            }

        except:
            continue

    return None


#  MAIN SCAN FUNCTION
def dir_scan(target, mode, custom_wordlist=None, filter_codes=None, recursive=False, depth=1):
    words = load_wordlist(mode, custom_wordlist)

    print(f"\n[+] Loaded {len(words)} words\n")

    results = []
    visited = set()

    def scan(base, current_depth):
        if current_depth > depth:
            return

        with ThreadPoolExecutor(max_workers=30) as executor:
            futures = [executor.submit(scan_url, base, word, 0.1) for word in words]

            for future in futures:
                res = future.result()

                if not res:
                    continue

                status = res["status"]

                #  filter
                if filter_codes and status not in filter_codes:
                    continue

                if res["url"] not in visited:
                    visited.add(res["url"])
                    results.append(res)

                    #  recursion (only on valid dirs)
                    if recursive and status == 200:
                        try:
                            new_path = res["url"].replace("https://", "").replace("http://", "")
                            scan(new_path, current_depth + 1)
                        except:
                            pass

    scan(target, 1)

    return results