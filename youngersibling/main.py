import textwrap
import datetime
import os
from colorama import Fore, init
from terminaltables import SingleTable  # Import SingleTable
import datetime
try:
    # Try importing normally if it's during development
    from display_table import display_table
    from google_search import google_search
    from ip_lookup import ip_lookup
    from email_lookup import email_lookup
    from username_lookup import username_lookup
    from exif_data_extraction import exif_data_extraction
    from phone_lookup import phone_lookup
    from web_osint import get_web_osint_info  # Import the new web OSINT module
except ImportError:
    # Fallback to the fully-qualified import if packaged
    from youngersibling.display_table import display_table
    from youngersibling.google_search import google_search
    from youngersibling.ip_lookup import ip_lookup
    from youngersibling.email_lookup import email_lookup
    from youngersibling.username_lookup import username_lookup
    from youngersibling.exif_data_extraction import exif_data_extraction
    from youngersibling.phone_lookup import phone_lookup
    from youngersibling.web_osint import get_web_osint_info  # Import the new web OSINT module


init(autoreset=True)
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
current_time = datetime.datetime.now().strftime("%H:%M:%S")
print(Fore.CYAN + r"""
 __   __                          ___ _ _    _ _           
 \ \ / /__ _  _ _ _  __ _ ___ _ _/ __(_) |__| (_)_ _  __ _ 
  \ V / _ \ || | ' \/ _` / -_) '_\__ \ | '_ \ | | ' \/ _` |
   |_|\___/\_,_|_||_\__, \___|_| |___/_|_.__/_|_|_||_\__, |
                    |___/                            |___/
      """)
# Metadata
metadata = [
    f"Version: [1.2] - Stable",
    f"Date: {current_date} | Time: {current_time}",
    "Developer: Mostafizur Rahman",
    "Github: Mostafizur-Rahman8391",
]

# Create divider and welcome text
divider = "-" * 50
welcome_text = "\n" + "Welcome to the YoungerSibling OSINT Toolkit!\n" + "-" * 50

# Combine metadata with divider and welcome text
output = "\n".join(metadata) + "\n" + divider + welcome_text

# Print the final result
print( Fore.GREEN + output)


def wrap_text(text, width=100):
    return '\n'.join(textwrap.wrap(text, width))


def display_menu():
    """
    Displays the main menu as a table with input options.
    """
    table_data = [
        ["Option", "Description"],
        ["1", "Google Search"],
        ["2", "IP Lookup"],
        ["3", "Email Lookup"],
        ["4", "Username Lookup(Enhanced)"],
        ["5", "Exif Data Extraction"],
        ["6", "Phone Lookup"],
        ["7", "Web OSINT"],
        ["8", "Exit"]
    ]
    table = SingleTable(table_data)
    print(Fore.YELLOW + table.table)


def main():
    while True:
        display_menu()

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
            phone_number = input("Enter the phone number: ")
            results = phone_lookup(phone_number)          

        elif choice == "7":
            domain = input("Enter the domain or website URL (e.g., example.com): ")
            results = get_web_osint_info(domain)

            # Loop through each category in the OSINT results
            for category, info in results.items():
                print(Fore.YELLOW + f"--- {category} ---")

                # If the info is a dictionary, format it
                if isinstance(info, dict):
                    formatted_info = '\n'.join([f"{key}: {value}" for key, value in info.items()])
                else:
                    formatted_info = str(info)

                # Wrap text to fit the terminal or output space
                wrapped_info = wrap_text(formatted_info)

                # Print the wrapped info in color
                print(Fore.GREEN + wrapped_info)
                print("\n")  # Separate sections with a newline for better readability

        elif choice == "8":
            print(Fore.MAGENTA + "Exiting the tool.")
            break

        else:
            print(Fore.RED + "Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
