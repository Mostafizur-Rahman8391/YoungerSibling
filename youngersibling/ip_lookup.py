import requests
from colorama import Fore

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