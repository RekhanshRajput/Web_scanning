import requests
import warnings
from Wappalyzer import Wappalyzer, WebPage

warnings.filterwarnings("ignore")  #  remove Wappalyzer warnings

def wappalyzer_scan(target):
    try:
        webpage = WebPage.new_from_url(target)
        wappalyzer = Wappalyzer.latest()
        return wappalyzer.analyze_with_versions(webpage)
    except:
        return {}

def detect_tech(target):
    if not target.startswith("http"):
        target = "http://" + target

    result = []

    try:
        r = requests.get(target, timeout=5)
        headers = r.headers
        html = r.text.lower()
    except:
        return "Error connecting to target"

    #  Server
    result.append(f"Server: {headers.get('Server', 'Unknown')}")

    #  Language
    if "x-powered-by" in headers:
        result.append(f"Language: {headers['x-powered-by']}")

    if "php" in html:
        result.append("Language: PHP")
    elif "asp.net" in html:
        result.append("Language: ASP.NET")
    elif "node.js" in html:
        result.append("Language: Node.js")

    #  CMS
    if "wp-content" in html:
        result.append("CMS: WordPress")
    elif "drupal" in html:
        result.append("CMS: Drupal")

    #  Framework
    if "laravel" in html:
        result.append("Framework: Laravel")
    if "react" in html:
        result.append("Frontend: React")
    if "angular" in html:
        result.append("Frontend: Angular")

    #  CDN / WAF
    if "cloudflare" in headers.get("Server", "").lower():
        result.append("CDN/WAF: Cloudflare")

    #  Security Headers
    if "x-frame-options" in headers:
        result.append("Security: X-Frame-Options Enabled")
    else:
        result.append("Security: Missing X-Frame-Options")

    #  Wappalyzer
    techs = wappalyzer_scan(target)
    result.append("\n[Wappalyzer Detection + Versions]")

    if isinstance(techs, dict) and techs:
        for tech, data in techs.items():
            versions = ", ".join(data.get("versions", []))
            if versions:
                result.append(f"- {tech} ({versions})")
            else:
                result.append(f"- {tech}")
    else:
        result.append("No technologies detected")

    return "\n".join(result)