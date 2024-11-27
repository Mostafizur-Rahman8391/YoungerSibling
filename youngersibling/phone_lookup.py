import phonenumbers
from phonenumbers import geocoder, carrier, timezone, phonenumberutil
from phonenumbers import PhoneNumberType
from colorama import Fore
try:
    # Try importing normally if it's during development
    from display_table import display_table
except ImportError:
    # Fallback to the fully-qualified import if packaged
    from youngersibling.display_table import display_table
    
def phone_lookup(phone_number):
    """Function to perform detailed phone lookup using libphonenumber"""
    print(Fore.CYAN + "\n[+] Performing Phone Lookup...")

    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number)

        # Check if the phone number is possible
        is_possible = phonenumbers.is_possible_number(parsed_number)

        # Validate if the phone number is valid
        is_valid = phonenumbers.is_valid_number(parsed_number)

        # Get the number type (e.g., mobile, fixed-line, etc.)
        number_type = phonenumbers.number_type(parsed_number)
        number_type_str = {
            PhoneNumberType.MOBILE: "Mobile",
            PhoneNumberType.FIXED_LINE: "Fixed Line",
            PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
            PhoneNumberType.TOLL_FREE: "Toll Free",
            PhoneNumberType.PREMIUM_RATE: "Premium Rate",
            PhoneNumberType.SHARED_COST: "Shared Cost",
            PhoneNumberType.VOIP: "VoIP",
            PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
            PhoneNumberType.PAGER: "Pager",
            PhoneNumberType.UAN: "UAN",
            PhoneNumberType.VOICEMAIL: "Voicemail",
            PhoneNumberType.UNKNOWN: "Unknown"
        }.get(number_type, "Unknown")

        # Get country and carrier details
        country = geocoder.description_for_number(parsed_number, "en")
        carrier_name = carrier.name_for_number(parsed_number, "en")

        # Get the timezone of the phone number
        time_zones = timezone.time_zones_for_number(parsed_number)

        # Get the region code for country-specific details
        region_code = phonenumbers.region_code_for_number(parsed_number)

        # Prepare the results to be displayed in table format
        results = [
            ["Phone Number", phone_number],
            ["Country", country],
            ["Carrier", carrier_name],
            ["Is Possible", is_possible],
            ["Is Valid", is_valid],
            ["Number Type", number_type_str],
            ["Time Zones", ", ".join(time_zones) if time_zones else "N/A"],
            ["Region Code", region_code]
        ]

        # Display the results in a table
        display_table("Phone Lookup Results", results, ["Field", "Value"])

    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(Fore.RED + f"Error: Failed to parse phone number: {str(e)}")
