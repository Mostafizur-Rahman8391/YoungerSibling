from tqdm import tqdm
import json
import os
from colorama import Fore, Style
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
try:
    from display_table import display_table
except ImportError:
        from youngersibling.display_table import display_table
        
def username_lookup(username, json_file="data.json", threads=10):
    print(Fore.CYAN + f"\n[+] Performing Username Lookup for '{username}'...\n" + Style.RESET_ALL)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    json_path = os.path.join(current_dir, json_file)
                                  
    # Load platforms from Sherlock's JSON
    try:
        with open(json_path, "r") as file:
            platforms = json.load(file)
    except FileNotFoundError:
        print(Fore.RED + "Error: JSON file not found!" + Style.RESET_ALL)
        return
    except json.JSONDecodeError:
        print(Fore.RED + "Error: Invalid JSON file format!" + Style.RESET_ALL)
        return

    found_results = []
    total_checked = 0
    platform_items = list(platforms.items())  # Convert dict to list for iteration

    # Not found phrases
    not_found_keywords = [
        "not found",
        "this page doesn't exist",
        "user not found",
        "404",
        "page not found",
        "no user",
        "account not found",
        "oops",
        "not a registered member",
        "Why not register it?",
        "centralauth-admin-nonexistent",
        "нет такого участника",
        "is still available",
        "This account may have been banned or the username is incorrect.",
        "doesn't exist",
        
    ]

    # Progress bar for tracking
    progress_bar = tqdm(total=len(platform_items), desc="Checking platforms")

    def check_platform(platform_item):
        nonlocal total_checked
        platform_name, platform_data = platform_item
        if isinstance(platform_data, dict):
            url = platform_data.get("url", "").format(username)
            if not url:
                progress_bar.update(1)
                return

            try:
                response = requests.get(url, timeout=5)
                total_checked += 1

                if response.status_code == 200:
                    # Parse the page content with BeautifulSoup
                    soup = BeautifulSoup(response.text, "html.parser")
                    page_text = soup.get_text().lower()

                    # Check if the username or relevant information is present
                    if username.lower() in page_text:
                        # Check if any "not found" keyword is present
                        if any(keyword in page_text for keyword in not_found_keywords):
                            progress_bar.update(1)
                            return
                        found_results.append([platform_name, url])

            except requests.RequestException:
                pass  # Ignore errors (timeout, connection issues)

        progress_bar.update(1)  # Update progress bar

    # Use ThreadPoolExecutor to make requests concurrently
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(check_platform, platform_items)

    progress_bar.close()

    # Display results
    if found_results:
        print(Fore.GREEN + f"\n[+] Found {len(found_results)} accounts for '{username}':" + Style.RESET_ALL)
        headers = ["Platform", "URL"]
        display_table("Available Accounts", found_results, headers)
    else:
        print(Fore.YELLOW + f"\n[!] No accounts found for '{username}'." + Style.RESET_ALL)

    print(Fore.CYAN + f"\n[+] Checked {total_checked} platforms." + Style.RESET_ALL)
