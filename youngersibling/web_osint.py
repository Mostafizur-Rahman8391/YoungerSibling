import requests
from bs4 import BeautifulSoup
import socket
import whois
import dns.resolver
import textwrap
from colorama import init, Fore, Back, Style
import datetime

# Initialize colorama
init(autoreset=True)

# Function to wrap text within a cell and break lines to fit
def wrap_text(text, width=50):
    return '\n'.join(textwrap.wrap(text, width))

# Function to get WHOIS data of a website
def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        # Formatting WHOIS data in a cleaner manner
        formatted_whois = {
            "Domain Name": w.domain_name,
            "Registrar": w.registrar,
            "Creation Date": w.creation_date,
            "Expiration Date": w.expiration_date,
            "Updated Date": w.updated_date,
            "Name Servers": w.name_servers,
            "Status": w.status,
            "Emails": w.emails,
            "Country": w.country,
            "Registrant Organization": w.org,
        }
        return formatted_whois
    except Exception as e:
        return {"Error": str(e)}

# Function to get DNS records (A, AAAA, MX, CNAME) for a domain
def get_dns_info(domain):
    try:
        records = {}
        # A record (IPv4)
        a_records = dns.resolver.resolve(domain, 'A')
        records['A'] = [r.to_text() for r in a_records]
        
        # AAAA record (IPv6)
        try:
            aaaa_records = dns.resolver.resolve(domain, 'AAAA')
            records['AAAA'] = [r.to_text() for r in aaaa_records]
        except dns.resolver.NoAnswer:
            records['AAAA'] = "No IPv6 records"
        
        # MX records (Mail servers)
        mx_records = dns.resolver.resolve(domain, 'MX')
        records['MX'] = [r.to_text() for r in mx_records]
        
        # CNAME record (Canonical Name)
        try:
            cname_records = dns.resolver.resolve(domain, 'CNAME')
            records['CNAME'] = [r.to_text() for r in cname_records]
        except dns.resolver.NoAnswer:
            records['CNAME'] = "No CNAME records"
        
        return records
    except Exception as e:
        return {"Error": str(e)}

# Function to get geolocation of the domain's IP address
def get_ip_geolocation(ip_address):
    try:
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'fail':
            return {"Error": "Unable to fetch geolocation data"}
        return {
            "Country": data.get("country"),
            "Region": data.get("regionName"),
            "City": data.get("city"),
            "ZIP": data.get("zip"),
            "Latitude": data.get("lat"),
            "Longitude": data.get("lon"),
            "ISP": data.get("isp"),
            "Organization": data.get("org"),
            "AS": data.get("as")
        }
    except Exception as e:
        return {"Error": str(e)}

# Function to extract metadata from a webpage
def get_metadata(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.title.string if soup.title else "No title"
        description = soup.find("meta", {"name": "description"}) or soup.find("meta", {"property": "og:description"})
        description = description["content"] if description else "No description"

        return {
            "Title": title,
            "Description": description
        }
    except Exception as e:
        return {"Error": str(e)}

# Main function to gather all web OSINT information
def get_web_osint_info(domain):
    # Get WHOIS information
    whois_info = get_whois_info(domain)
    
    # Get DNS information (A, AAAA, MX, CNAME records)
    dns_info = get_dns_info(domain)
    
    # Get IP address and geolocation of the domain
    ip_address = dns_info.get("A", ["No A records"])[0]
    geolocation_info = get_ip_geolocation(ip_address)
    
    # Get Website Metadata
    metadata_info = get_metadata(f"http://{domain}")
    
    # Combine all information
    web_osint_data = {
        "WHOIS Info": whois_info,
        "DNS Info": dns_info,
        "Geolocation Info": geolocation_info,
        "Metadata Info": metadata_info
    }
    
    return web_osint_data

def wrap_text(text, width=80):
    """
    Wraps the given text to the specified width.
    """
    return '\n'.join(textwrap.wrap(text, width))

def display_web_osint_info(data):
    for category, info in data.items():
        print(Fore.YELLOW + f"--- {category} ---")
        
        # If the info is a dictionary, format it
        if isinstance(info, dict):
            for key, value in info.items():
                # If value is a list, format it to show each item in a new line
                if isinstance(value, list):
                    formatted_info = f"{key}:\n" + '\n'.join([f"  {v}" for v in value])
                # If the value is a datetime, format it to make it more readable
                elif isinstance(value, datetime):
                    formatted_info = f"{key}: {value.strftime('%Y-%m-%d %H:%M:%S')}"
                else:
                    formatted_info = f"{key}: {value}"
        else:
            formatted_info = str(info)

        # Wrap text to ensure it doesn't overflow and stays readable
        wrapped_info = wrap_text(formatted_info)

        # Display the wrapped info with color
        print(Fore.GREEN + wrapped_info)
        print("\n")  # Separate sections with a newline for better readability
# Integration with the original menu system

def run_osint_choice():
    while True:
        domain = input("Enter the domain or website URL (e.g., example.com): ")
        results = get_web_osint_info(domain)

        # Loop through each category in the OSINT results
        display_web_osint_info(results)

        # Exiting the loop, no back option anymore
        print(Fore.GREEN + "Returning to main menu...")  # End of this category info display

# Call the main function to start the OSINT process
if __name__ == "__main__":
    run_osint_choice()
