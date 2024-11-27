from colorama import Fore
import exifread
from terminaltables import SingleTable

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
