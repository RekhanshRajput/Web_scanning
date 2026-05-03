import requests
import re
import os
from urllib.parse import urljoin

# 🔹 regex patterns
JS_REGEX = r'src=["\'](.*?\.js)["\']'
ENDPOINT_REGEX = r'["\'](\/api\/.*?|\/v\d+\/.*?|\/.*?\.php|\/.*?\.json)["\']'
SECRET_REGEX = r'(api_key|apikey|token|secret|auth|password)[\'"\s:=]+([A-Za-z0-9_\-]{6,})'

#  STEP 1: FIND JS FILES
def find_js_files(target):
    if not target.startswith("http"):
        target = "http://" + target

    js_files = set()

    try:
        r = requests.get(target, timeout=5)

        matches = re.findall(JS_REGEX, r.text)

        for m in matches:
            full_url = urljoin(target, m)
            js_files.add(full_url)

    except:
        pass

    return list(js_files)


#  STEP 2: SAVE JS FILES LIST
def save_js_list(js_files, target):
    os.makedirs("output/js", exist_ok=True)

    file_path = f"output/js/{target}_js.txt"

    with open(file_path, "w") as f:
        for js in js_files:
            f.write(js + "\n")

    return file_path


#  STEP 3: DOWNLOAD JS FILES
def download_js(js_files):
    os.makedirs("output/js/files", exist_ok=True)

    saved_files = []

    for i, url in enumerate(js_files):
        try:
            r = requests.get(url, timeout=5)

            file_path = f"output/js/files/file_{i}.js"

            with open(file_path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(r.text)

            saved_files.append(file_path)

        except:
            continue

    return saved_files


#  STEP 4: ANALYZE JS FILES
def analyze_js(folder_path):
    endpoints = set()
    secrets = set()

    for file in os.listdir(folder_path):
        if file.endswith(".js"):
            full_path = os.path.join(folder_path, file)

            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                    # endpoints
                    ep = re.findall(ENDPOINT_REGEX, content)
                    for e in ep:
                        endpoints.add(e)

                    # secrets
                    sec = re.findall(SECRET_REGEX, content)
                    for s in sec:
                        secrets.add(s[1])

            except:
                continue

    return list(endpoints), list(secrets)