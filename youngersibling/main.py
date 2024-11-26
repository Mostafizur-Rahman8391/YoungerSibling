import requests
from bs4 import BeautifulSoup
from terminaltables import SingleTable
from colorama import Fore, Style, init
import dns.resolver
import exifread
from tqdm import tqdm
import json
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

print(Fore.CYAN + r"""
 __   __                          ___ _ _    _ _           
 \ \ / /__ _  _ _ _  __ _ ___ _ _/ __(_) |__| (_)_ _  __ _ 
  \ V / _ \ || | ' \/ _` / -_) '_\__ \ | '_ \ | | ' \/ _` |
   |_|\___/\_,_|_||_\__, \___|_| |___/_|_.__/_|_|_||_\__, |
                    |___/                            |___/ Version: 1.1
                                                        Developer: Mostafizur Rahman
                                                        Github: Mostafizur-Rahman8391
      """)

def google_search(query):
    print(Fore.CYAN + "\n[+] Performing Google Search...")
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for g in soup.find_all("div", class_="tF2Cxc"):
            title = g.find("h3").text if g.find("h3") else "No title"
            link = g.find("a", href=True)["href"] if g.find("a", href=True) else "No link"
            snippet = (
                g.find("span", class_="aCOpRe").text
                if g.find("span", class_="aCOpRe")
                else "No description"
            )
            results.append([title, link, snippet])

        return results if results else [["No results found.", "N/A", "N/A"]]
    except Exception as e:
        return [["Error occurred", str(e), "N/A"]]

def ip_lookup(ip):
    print(Fore.CYAN + "\n[+] Performing IP Lookup...")
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "IP": ip,
                "Country": data.get("country", "N/A"),
                "Region": data.get("regionName", "N/A"),
                "City": data.get("city", "N/A"),
                "ISP": data.get("isp", "N/A"),
                "Lat/Lon": f"{data.get('lat', 'N/A')}/{data.get('lon', 'N/A')}"
            }
        else:
            return {"Error": f"Failed to fetch data (Status code: {response.status_code})"}
    except Exception as e:
        return {"Error": str(e)}
def username_lookup(username, json_file="data.json", threads=10):
    print(Fore.CYAN + f"\n[+] Performing Username Lookup for '{username}'...\n" + Style.RESET_ALL)
    
    # Load platforms from Sherlock's JSON
    try:
        with open(json_file, "r") as file:
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


def email_lookup(email):
    print(Fore.CYAN + "\n[+] Performing Email Lookup...")
    try:
        domain = email.split("@")[-1]
        answers = dns.resolver.resolve(domain, 'MX')
        return {
            "Email": email,
            "MX Records": ", ".join([str(r.exchange) for r in answers]),
            "Domain": domain
        }
    except Exception as e:
        return {"Error": str(e)}

def exif_data_extraction(image_path):
    print(Fore.CYAN + "\n[+] Extracting Exif Data...")
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            return {tag: str(tags[tag]) for tag in tags.keys()}
    except Exception as e:
        return {"Error": str(e)}

def display_table(title, data, headers):
    table_data = [headers] + data
    table = SingleTable(table_data, title)
    print(Fore.YELLOW + table.table)

def main():
    while True:
        print(Fore.GREEN + "\nChoose an option:")
        print("1. Google Search")
        print("2. IP Lookup")
        print("3. Email Lookup")
        print("4. Username Lookup(Enhanced)")
        print("5. Exif Data Extraction")
        print("6. Exit")

        choice = input(Fore.BLUE + "Enter your choice: ")

        if choice == "1":
            query = input("Enter the search query: ")
            results = google_search(query)
            display_table("Google Search Results", results, ["Title", "URL", "Snippet"])

        elif choice == "2":
            ip = input("Enter the IP address: ")
            results = ip_lookup(ip)
            display_table("IP Lookup Results", [[k, v] for k, v in results.items()], ["Field", "Value"])

        elif choice == "3":
            email = input("Enter the email address: ")
            results = email_lookup(email)
            display_table("Email Lookup Results", [[k, v] for k, v in results.items()], ["Field", "Value"])
            
        elif choice == "4":
            username = input("Enter the username: ")
            username_lookup(username)

        elif choice == "5":
            image_path = input("Enter the image path: ")
            results = exif_data_extraction(image_path)
            display_table("Exif Data Results", [[k, v] for k, v in results.items()], ["Tag", "Value"])

        elif choice == "6":
            print(Fore.MAGENTA + "Exiting the tool.")
            break

        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
