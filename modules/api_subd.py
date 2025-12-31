from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
from threading import Lock
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, SpinnerColumn
import re
import os
import math
import time

console = Console()
file_write_lock = Lock()
session = requests.Session()
# Set User gent to prevent blocking
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
DEFAULT_TIMEOUT = 25

def get_files_dir():
    # Returns the path to the 'files' directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(current_dir) == 'modules':
        project_root = os.path.dirname(current_dir)
    else:
        project_root = current_dir
    
    files_dir = os.path.join(project_root, "files")
    if not os.path.exists(files_dir):
        os.makedirs(files_dir, exist_ok=True)
    return files_dir

def show_banner():
 
    os.system("clear") if os.name == "posix" else os.system("cls")
    banner_lines = [
        "AdwanceSNI - API Scanner",
        "v2.0.4",
        "Updated: 30 Dec 2025"
    ]
    console.rule("[bold cyan]" + " | ".join(banner_lines))

def validate_domain(domain):
    # Checks if domain format is valid
    domain_pattern = re.compile(
        r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,63}$"
    )
    return bool(domain_pattern.match(domain))

def clean_subdomain(subdomain):
    # Removes wildcards like *.example.com -> example.com
    subdomain = subdomain.strip()
    if subdomain.startswith("*."):
        subdomain = subdomain[2:]
    return subdomain

# --- APIs --

def crtsh_subdomains(domain):
    """Fetches subdomains for CRT.sh (JSON)."""
    subdomains = set()
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    
    for attempt in range(3):
        try:
            response = session.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    name_value = entry.get("name_value")
                    if name_value:
                        for sub in name_value.split("\n"):
                            sub = io_clean(sub, domain)
                            if sub: subdomains.add(sub)
                break
            elif response.status_code in [502, 503, 504]:
                time.sleep(2 * (attempt + 1))
            else:
                break
        except Exception:
            time.sleep(2)
    return subdomains

def hackertarget_subdomains(domain):
    """Fetches subdomains from HackerTarget."""
    subdomains = set()
    try:
        response = session.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=DEFAULT_TIMEOUT)
        if response.status_code == 200 and 'text' in response.headers.get('Content-Type', ''):
            for line in response.text.splitlines():
                parts = line.split(",")
                if parts:
                    sub = io_clean(parts[0], domain)
                    if sub: subdomains.add(sub)
    except Exception:
        pass
    return subdomains

def rapiddns_subdomains(domain):
    """Fetches subdomains from RapidDNS (with pagination)."""
    subdomains = set()
    try:
        url = f"https://rapiddns.io/subdomain/{domain}?full=1" 
        response = session.get(url, timeout=DEFAULT_TIMEOUT)
        if response.status_code != 200:
            return subdomains

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Page 1
        for link in soup.find_all('td'):
            sub = io_clean(link.get_text(strip=True), domain)
            if sub: subdomains.add(sub)

        # Pagination logic
        total_count = 0
        count_span = soup.find('span', style="color: #39cfca; ")
        if count_span:
            try:
                total_count = int(count_span.get_text(strip=True))
            except ValueError:
                pass
        
        if total_count > 100:
            total_pages = min(math.ceil(total_count / 100), 50) # Cap at 50 pages
            
            for page in range(2, total_pages + 1):
                try:
                    p_response = session.get(f"https://rapiddns.io/subdomain/{domain}?page={page}", timeout=20)
                    if p_response.status_code == 200:
                        p_soup = BeautifulSoup(p_response.text, 'html.parser')
                        for link in p_soup.find_all('td'):
                            sub = io_clean(link.get_text(strip=True), domain)
                            if sub: subdomains.add(sub)
                except Exception:
                    continue 
                time.sleep(0.5)
        
    except Exception:
        pass
    return subdomains

def anubisdb_subdomains(domain):
    """Fetches subdomains from AnubisDB."""
    subdomains = set()
    try:
        response = session.get(f"https://jldc.me/anubis/subdomains/{domain}", timeout=DEFAULT_TIMEOUT)
        if response.status_code == 200:
            try:
                data = response.json()
                for sub in data:
                    clean = io_clean(sub, domain)
                    if clean: subdomains.add(clean)
            except:
                pass
    except Exception:
        pass
    return subdomains

def webarchive_subdomains(domain):
    """Fetches subdomains from WebArchive."""
    subdomains = set()
    try:
        url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=text&fl=original&collapse=urlkey"
        response = session.get(url, timeout=40)
        if response.status_code == 200:
            for line in response.text.splitlines():
                if domain in line:
                    parts = re.findall(r'(?:[a-zA-Z0-9-]+\.)+' + re.escape(domain), line)
                    for part in parts:
                        sub = io_clean(part, domain)
                        if sub: subdomains.add(sub)
    except Exception:
        pass
    return subdomains

def io_clean(item, domain):
    """Helper to validate found items."""
    item = clean_subdomain(item)
    if item.endswith(f".{domain}") and validate_domain(item):
        return item
    return None

def process_domain(domain, sources, output_file, progress, task_id):
    # Runs all APIs in parallel for a domain
    all_subdomains = set()
    console.print(f"\n[bold yellow]Target:[/bold yellow] [bold cyan]{domain}[/bold cyan]")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_api = {executor.submit(source, domain): source.__name__ for source in sources}
        
        for future in as_completed(future_to_api):
            api_name = future_to_api[future].replace('_subdomains', '').title()
            try:
                results = future.result()
                count = len(results)
                all_subdomains.update(results)
                
                if count > 0:
                    console.print(f"  [green]✔ {api_name}: {count}[/green]")
                else:
                    console.print(f"  [dim]• {api_name}: 0[/dim]")
                    
                progress.update(task_id, advance=1)
            except Exception:
                console.print(f"  [red]✘ {api_name}: Failed[/red]")

    # Save to file
    if all_subdomains:
        with file_write_lock:
            try:
                with open(output_file, "a", encoding="utf-8") as file:
                    for subdomain in sorted(all_subdomains):
                        file.write(f"{subdomain}\n")
            except IOError:
                pass
                
    return len(all_subdomains)

def find_subdomains():
    show_banner()

    sources = [
        anubisdb_subdomains,
        hackertarget_subdomains,
        rapiddns_subdomains,
        crtsh_subdomains,
        webarchive_subdomains
    ]

    console.print("[yellow][1] Single Domain[/yellow]")
    console.print("[yellow][2] File List[/yellow]")
    choice = console.input("[green]Option: [/green]").strip()

    domains = []
    if choice == '1':
        domain = console.input("[green]Domain: [/green]").strip()
        if validate_domain(domain): domains = [domain]
    elif choice == '2':
        path = console.input("[green]File Path: [/green]").strip()
        if os.path.exists(path):
            with open(path, 'r') as f:
                domains = [l.strip() for l in f if l.strip()]
    else:
        return

    if not domains: return

    fname = console.input("[green]Output Filename (default: API_Results): [/green]").strip() or "API_Results"
    
    output_file = os.path.join(get_files_dir(), f"{fname}.txt")

    console.print(f"\n[bold]Scanning {len(domains)} targets...[/bold]")

    total_subs = 0
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[bold blue]{task.completed}/{task.total} APIs"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        
        for domain in domains:
            task_id = progress.add_task(f"Scanning {domain}...", total=len(sources), visible=True)
            subs = process_domain(domain, sources, output_file, progress, task_id)
            total_subs += subs
            progress.update(task_id, completed=len(sources))

    console.print(f"\n[bold green]Done! Total Found: {total_subs}[/bold green]")
    console.print(f"[bold yellow]Saved to: {output_file}[/bold yellow]")
    console.input("\nPress Enter to exit...")

if __name__ == "__main__":
    find_subdomains()
