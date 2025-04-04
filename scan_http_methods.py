import requests
import os
from urllib.parse import urlparse
from colorama import init, Fore, Style
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# Banner
banner = f"""{Fore.CYAN}
  _  __          _           _   _ ____  _     
 | |/ /___ _   _| |__   ___ | | | |  _ \| |    
 | ' // _ \ | | | '_ \ / _ \| |_| | | | | |    
 | . \  __/ |_| | |_) | (_) |  _  | |_| | |___ 
 |_|\_\___|\__, |_.__/ \___/|_| |_|____/|_____|
           |___/           {Fore.YELLOW}By: kader11000
{Style.RESET_ALL}
"""
print(banner)

# Get URL
url = input(Fore.GREEN + "Enter the URL: ").strip()

# Get domain name for folder
parsed_url = urlparse(url)
domain = parsed_url.netloc or parsed_url.path.split('/')[0]
folder_name = domain.replace(":", "_")

# Create folder
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://google.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

methods = ["GET", "POST", "HEAD", "OPTIONS", "PUT"]
html_results = ""
headers_log = ""

for method in methods:
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(Fore.MAGENTA + f"\n[{method}] Sending request at {now}...")
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, data={})
        elif method == "HEAD":
            response = requests.head(url, headers=headers)
        elif method == "OPTIONS":
            response = requests.options(url, headers=headers)
        elif method == "PUT":
            response = requests.put(url, headers=headers, data={})
        else:
            continue

        status = response.status_code
        print(Fore.BLUE + f"[{method}] Status code: {status}")

        html_results += f"<h2>{method} - Status: {status} - {now}</h2>\n"

        if method in ["GET", "POST", "PUT"] and response.text:
            content = response.text[:1000]
            html_results += f"<pre>{content}</pre>\n"
        elif method in ["HEAD", "OPTIONS"]:
            html_results += f"<pre>{response.headers}</pre>\n"

        headers_log += f"\n--- {method} --- {now} ---\n"
        for key, value in response.headers.items():
            headers_log += f"{key}: {value}\n"

    except Exception as e:
        error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(Fore.RED + f"[{method}] Error at {error_time}: {e}")
        html_results += f"<h2>{method} - Error: {e} - {error_time}</h2>\n"
        headers_log += f"\n--- {method} --- {error_time} ---\nError: {e}\n"

# Save HTML
html_path = os.path.join(folder_name, "result.html")
with open(html_path, "w", encoding="utf-8") as file:
    file.write(f"<html><head><meta charset='utf-8'><title>Scan Results</title></head><body>{html_results}</body></html>")

# Save headers log
headers_path = os.path.join(folder_name, "headers.txt")
with open(headers_path, "w", encoding="utf-8") as file:
    file.write(headers_log)

print(Fore.GREEN + f"\nResults saved in folder: {folder_name}")
