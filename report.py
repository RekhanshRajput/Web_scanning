import os

def save_report(target, data, report_type):
    os.makedirs("output", exist_ok=True)

    safe_name = target.replace("http://", "").replace("https://", "").replace("/", "")

    if report_type == "html":
        content = f"""
        <html>
        <head>
        <title>Recon Report</title>
        <style>
        body {{ background:black; color:lime; font-family:monospace; }}
        h2 {{ color:cyan; }}
        </style>
        </head>
        <body>
        <h2>Target: {target}</h2>
        <pre>{data}</pre>
        </body>
        </html>
        """
        filename = f"output/{safe_name}_report.html"

    else:
        content = data
        filename = f"output/{safe_name}_report.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    return filename