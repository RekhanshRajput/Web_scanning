import re

#  extract params from URLs
def extract_params(urls):
    params = set()

    for u in urls:
        if "?" in u:
            query = u.split("?")[1]

            for p in query.split("&"):
                key = p.split("=")[0]
                if key:
                    params.add(key + "=")

    return list(params)


#  categorize params
def categorize(params):
    xss = []
    sqli = []
    ssrf = []

    for p in params:
        key = p.lower()

        if any(k in key for k in ["q", "search", "msg", "comment", "text"]):
            xss.append(p)

        if any(k in key for k in ["id", "uid", "user", "item", "number"]):
            sqli.append(p)

        if any(k in key for k in ["url", "redirect", "link", "callback"]):
            ssrf.append(p)

    return xss, sqli, ssrf


#  MAIN FUNCTION
def param_miner(urls):
    params = extract_params(urls)

    xss, sqli, ssrf = categorize(params)

    return params, xss, sqli, ssrf