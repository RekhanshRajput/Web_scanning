from rich import print
from modules.tech import detect_tech
from modules.subdomain import find_subdomains
from modules.alive import alive_hosts
from modules.dirscan import dir_scan
from modules.jsanalyzer import find_js_files, save_js_list, download_js, analyze_js
from utils.report import save_report
from modules.wayback import get_wayback_data
from modules.paramminer import param_miner


def menu():
    while True:
        print("\n[bold cyan]========================================[/bold cyan]")
        print("[bold cyan]🔥 SNIPER RECON TOOL v1.0[/bold cyan]")
        print("[bold cyan]========================================[/bold cyan]")

        print("[1] Tech Finding")
        print("[2] Subdomain Finding")
        print("[3] Alive Host Detection")
        print("[4] Directory & Endpoint Discovery")
        print("[5] JavaScript Analysis")
        print("[6] Wayback + Historical URLs")
        print("[7] Parameter Mining")
        print("[8] Full Report (All Modules)")
        print("[9] Exit")

        choice = input("\nEnter Option > ")

        #  TECH
        if choice == "1":
            target = input("Enter Target > ")
            print("\n[green][+] Running Tech Detection...[/green]\n")

            result = detect_tech(target)
            print("[bold yellow]=== RESULT ===[/bold yellow]\n")
            print(result)

            r = input("\nReport Format (1=HTML, 2=TXT) > ")
            file = save_report(target, result, "html" if r == "1" else "txt")
            print(f"\n[bold green][+] Report Saved: {file}[/bold green]")

        #  SUBDOMAIN
        elif choice == "2":
            target = input("Enter Target > ")
            print("\n[green][+] Running Subdomain Scan...[/green]\n")

            subs = find_subdomains(target)

            if not subs:
                print("[red]No subdomains found[/red]")
                continue

            print(f"\n[bold yellow]=== FOUND {len(subs)} SUBDOMAINS ===[/bold yellow]\n")

            for sub in subs:
                print(sub)

            result = "\n".join(subs)

            r = input("\nReport Format (1=HTML, 2=TXT) > ")
            file = save_report(target + "_subs", result, "html" if r == "1" else "txt")

            print(f"\n[bold green][+] Report Saved: {file}[/bold green]")

        #  ALIVE
        elif choice == "3":
            file_path = input("Enter subdomain file path > ")

            print("\n[green][+] Running Alive Host Detection...[/green]\n")

            results, err = alive_hosts(file_path)

            if err:
                print(f"[red]{err}[/red]")
                continue

            if not results:
                print("[red]No alive hosts found[/red]")
                continue

            print(f"\n[bold yellow]=== ALIVE HOSTS ({len(results)}) ===[/bold yellow]\n")

            output_lines = []

            for r in results:
                url = r["url"]
                status = r["status"]
                title = r["title"]

                color = "green" if status == 200 else "yellow" if status == 403 else "cyan" if status in [301,302] else "red"

                line = f"{url} [{status}] - {title}"
                output_lines.append(line)

                print(f"[{color}]{line}[/{color}]")

            result_text = "\n".join(output_lines)

            output_file = file_path.replace(".txt", "_alive.txt")

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result_text)

            print(f"\n[bold green][+] Saved: {output_file}[/bold green]")

        #  DIRECTORY SCAN
        elif choice == "4":
            target = input("Enter target domain (no http) > ")

            print("\nSelect Scan Mode:")
            print("1. Common Paths")
            print("2. Extended Scan")
            print("3. File Fuzzing")
            print("4. Custom Wordlist")

            mode = input("Enter choice > ")

            custom_wordlist = None
            if mode == "4":
                custom_wordlist = input("Enter wordlist file/folder path > ")

            print("\nFilter Status Codes (e.g. 200,403) or press enter:")
            fc = input("> ")
            filter_codes = [int(x) for x in fc.split(",")] if fc else None

            print("\nEnable Recursion? (y/n): ")
            recursive = input("> ").lower() == "y"

            depth = 1
            if recursive:
                depth = int(input("Enter depth > "))

            print("\n[green][+] Running Directory Scan...[/green]\n")

            results = dir_scan(target, mode, custom_wordlist, filter_codes, recursive, depth)

            if not results:
                print("[red]No endpoints found[/red]")
                continue

            print(f"\n[bold yellow]=== FOUND {len(results)} ENDPOINTS ===[/bold yellow]\n")

            for r in results:
                url = r["url"]
                status = r["status"]
                size = r["size"]
                title = r["title"]

                color = "green" if status == 200 else "yellow" if status == 403 else "cyan" if status in [301,302] else "red"

                print(f"[{color}]{url} [{status}] [{size}B] - {title}[/{color}]")

        #  JS MODULE  
        elif choice == "5":

            print("\nSelect JS Mode:")
            print("1. Find & Download JS Files")
            print("2. Analyze Downloaded JS")

            mode = input("Enter choice > ")

            #  MODE 1
            if mode == "1":
                target = input("Enter Target > ")

                print("\n[+] Finding JS files...\n")

                js_files = find_js_files(target)

                if not js_files:
                    print("[red]No JS files found[/red]")
                    continue

                print(f"[green]Found {len(js_files)} JS files[/green]\n")

                for js in js_files:
                    print(js)

                file_path = save_js_list(js_files, target)
                print(f"\n[+] Saved list: {file_path}")

                print("\n[+] Downloading JS files...\n")

                saved = download_js(js_files)

                print(f"[green]Downloaded {len(saved)} JS files[/green]")

            #  MODE 2
            elif mode == "2":
                folder = input("Enter JS folder path > ")

                print("\n[+] Analyzing JS files...\n")

                endpoints, secrets = analyze_js(folder)

                print(f"\n[bold yellow]=== ENDPOINTS ({len(endpoints)}) ===[/bold yellow]\n")
                for e in endpoints:
                    print(e)

                print(f"\n[bold red]=== SECRETS ({len(secrets)}) ===[/bold red]\n")
                for s in secrets:
                    print(s)

                result = "ENDPOINTS:\n" + "\n".join(endpoints) + "\n\nSECRETS:\n" + "\n".join(secrets)

                r = input("\nReport Format (1=HTML, 2=TXT) > ")

                file = save_report("js_analysis", result, "html" if r == "1" else "txt")

                print(f"[green][+] Report Saved: {file}[/green]")

        #  FUTURE
        #  WAYBACK + HISTORICAL URLS 
        elif choice == "6":
            target = input("Enter Target > ")

            urls, params, interesting = get_wayback_data(target)

            if not urls:
                print("[red]No historical data found[/red]")
                continue

            print(f"\n[bold yellow]=== ALL URLS ({len(urls)}) ===[/bold yellow]\n")

    #  sirf first 50 show (spam avoid)
            for u in urls[:50]:
                print(u)

            print(f"\n[bold cyan]=== PARAMETERS ({len(params)}) ===[/bold cyan]\n")
            for p in params:
                print(p)

            print(f"\n[bold red]=== INTERESTING FILES ({len(interesting)}) ===[/bold red]\n")
            for i in interesting:
                print(i)

            result = (
                "ALL URLS:\n" + "\n".join(urls) +
                "\n\nPARAMETERS:\n" + "\n".join(params) +
                "\n\nINTERESTING FILES:\n" + "\n".join(interesting)
            )

            print("\nSelect Report Format:")
            print("1. HTML")
            print("2. TXT")

            r = input("Enter choice > ")

            file = save_report(target + "_wayback", result, "html" if r == "1" else "txt")

            print(f"[bold green][+] Report Saved: {file}[/bold green]")

        #  PARAMETER MINING 
        elif choice == "7":
            file_path = input("Enter URL list file (wayback output) > ")

            try:
                with open(file_path, "r") as f:
                    urls = [line.strip() for line in f if line.strip()]
            except:
                print("[red]File not found[/red]")
                continue

            print("\n[green][+] Extracting parameters...[/green]\n")

            params, xss, sqli, ssrf = param_miner(urls)

            if not params:
                print("[red]No parameters found[/red]")
                continue

            print(f"\n[bold yellow]=== ALL PARAMS ({len(params)}) ===[/bold yellow]\n")
            for p in params:
                print(p)

            print(f"\n[bold cyan]=== XSS PARAMS ({len(xss)}) ===[/bold cyan]\n")
            for p in xss:
                print(p)

            print(f"\n[bold red]=== SQLi PARAMS ({len(sqli)}) ===[/bold red]\n")
            for p in sqli:
                print(p)

            print(f"\n[bold magenta]=== SSRF PARAMS ({len(ssrf)}) ===[/bold magenta]\n")
            for p in ssrf:
                print(p)

            result = (
                "ALL:\n" + "\n".join(params) +
                "\n\nXSS:\n" + "\n".join(xss) +
                "\n\nSQLI:\n" + "\n".join(sqli) +
                "\n\nSSRF:\n" + "\n".join(ssrf)
            )

            print("\nSelect Report Format:")
            print("1. HTML")
            print("2. TXT")

            r = input("Enter choice > ")

            file = save_report("param_mining", result, "html" if r == "1" else "txt")

            print(f"[green][+] Report Saved: {file}[/green]")

#  FULL AUTOMATION 
        elif choice == "8":
            target = input("Enter Target Domain > ")

            print("\n[bold green][+] Starting Full Recon Pipeline...[/bold green]\n")

    #  STEP 1: Subdomain
            print("[cyan][1] Subdomain Enumeration...[/cyan]")
            subs = find_subdomains(target)

            if not subs:
                print("[red]No subdomains found[/red]")
                continue

            print(f"[green]Found {len(subs)} subdomains[/green]")

    #  STEP 2: Save subs
            sub_file = f"output/{target}_subs.txt"
            with open(sub_file, "w") as f:
                f.write("\n".join(subs))

    #  STEP 3: Alive check
            print("\n[cyan][2] Checking Alive Hosts...[/cyan]")
            alive_results, _ = alive_hosts(sub_file)

            alive_urls = []
            for r in alive_results:
                alive_urls.append(r["url"])

            print(f"[green]Alive Hosts: {len(alive_urls)}[/green]")

    #  STEP 4: Wayback
            print("\n[cyan][3] Fetching Wayback URLs...[/cyan]")
            all_urls, params, interesting = get_wayback_data(target)

            print(f"[green]Collected URLs: {len(all_urls)}[/green]")

    # STEP 5: Param Mining
            print("\n[cyan][4] Extracting Parameters...[/cyan]")
            params_all, xss, sqli, ssrf = param_miner(all_urls)

            print(f"[green]Params Found: {len(params_all)}[/green]")

    #  FINAL REPORT
            print("\n[bold yellow][+] Generating Final Report...[/bold yellow]\n")

            result = (
        "SUBDOMAINS:\n" + "\n".join(subs) +
        "\n\nALIVE HOSTS:\n" + "\n".join(alive_urls) +
        "\n\nWAYBACK URLS:\n" + "\n".join(all_urls) +
        "\n\nPARAMETERS:\n" + "\n".join(params_all) +
        "\n\nXSS:\n" + "\n".join(xss) +
        "\n\nSQLI:\n" + "\n".join(sqli) +
        "\n\nSSRF:\n" + "\n".join(ssrf)
        )

            print("Select Report Format:")
            print("1. HTML")
            print("2. TXT")

            r = input("Enter choice > ")

            file = save_report(target + "_full_recon", result, "html" if r == "1" else "txt")

            print(f"\n[bold green][+] Full Recon Report Saved: {file}[/bold green]")

        elif choice == "9":
            print("[red]Exiting...[/red]")
            break

        else:
            print("[red]Invalid Option[/red]")


if __name__ == "__main__":
    menu()