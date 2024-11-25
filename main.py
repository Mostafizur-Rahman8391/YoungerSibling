import requests
from bs4 import BeautifulSoup
from terminaltables import SingleTable
from colorama import Fore, Style, init
import dns.resolver
import exifread

init(autoreset=True)

print(Fore.RED + r"""
 __   __                          ___ _ _    _ _           
 \ \ / /__ _  _ _ _  __ _ ___ _ _/ __(_) |__| (_)_ _  __ _ 
  \ V / _ \ || | ' \/ _` / -_) '_\__ \ | '_ \ | | ' \/ _` |
   |_|\___/\_,_|_||_\__, \___|_| |___/_|_.__/_|_|_||_\__, |
                    |___/                            |___/ Version: 1.0
                                                        Developer: Mostafizur Rahman
                                                        Github: Mostafizur-Rahman8391
      """)

# Function: Google Search
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

# Function: IP Geolocation
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
def username_lookup(username):
    print(Fore.CYAN + f"\n[+] Performing Username Lookup for '{username}'...\n" + Style.RESET_ALL)

    platforms = {
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "Facebook": f"https://facebook.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "LinkedIn": f"https://www.linkedin.com/in/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "YouTube": f"https://www.youtube.com/@{username}"
    }

    results = []
    for platform, url in platforms.items():
        try:
            response = requests.get(url, timeout=5)
            status = "Found" if response.status_code == 200 else "Not Found"
        except requests.RequestException:
            status = "Error"
        results.append([platform, url, status])

    # If no results, show a message
    if not results:
        results.append(["N/A", "N/A", "No Results"])

    # Use `display_table` for consistent output
    headers = ["Platform", "URL", "Status"]
    display_table("Username Lookup Results", results, headers)


# Function: Email Lookup
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

# Function: Exif Data Extraction
def exif_data_extraction(image_path):
    print(Fore.CYAN + "\n[+] Extracting Exif Data...")
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            return {tag: str(tags[tag]) for tag in tags.keys()}
    except Exception as e:
        return {"Error": str(e)}

# Display Table
def display_table(title, data, headers):
    table_data = [headers] + data
    table = SingleTable(table_data, title)
    print(Fore.YELLOW + table.table)

# Main Function
def main():
    while True:
        print(Fore.GREEN + "\nChoose an option:")
        print("1. Google Search")
        print("2. IP Lookup")
        print("3. Email Lookup")
        print("4. Username Lookup")
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
