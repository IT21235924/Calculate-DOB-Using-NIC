import re
from datetime import datetime, timedelta

def deriveDOBFromNIC(nic: str) -> str:
    """
    Returns the date of birth (DOB) in 'YYYY-MM-DD' format derived from a Sri Lankan NIC number.
    Returns None if the NIC is invalid.
    """

    # 1) Remove extra spaces at the start or end of the NIC
    nic = nic.strip()

    # 2) Validate NIC using a regular expression
    #    - Old NIC format: 9 digits followed by 'V' or 'v' (total length = 10)
    #    - New NIC format: 12 digits
    pattern = r'^\d{9}[Vv]$|^\d{12}$'
    if not re.match(pattern, nic):
        return None

    # 3) Extract the year and the dayOfYear part
    if len(nic) == 10:  # Old NIC format (e.g., 92xxxxxxxV -> 19 + '92' => 1992)
        year_str = "19" + nic[:2]
        day_of_year = int(nic[2:5])
    else:  # len(nic) == 12, New NIC format (e.g., 2000xxxxxxx -> year = '2000')
        year_str = nic[:4]
        day_of_year = int(nic[4:7])

    # 4) Check if dayOfYear > 500 (indicates female NIC). Subtract 500 if so.
    if day_of_year > 500:
        day_of_year -= 500

    # 5) Convert year_str to an integer
    year = int(year_str)

    # 6) Validate day_of_year range (1 to 366)
    if day_of_year < 1 or day_of_year > 366:
        return None

    # 7) Construct the date of birth using datetime
    try:
        # Start from January 1st of the given year, then add (day_of_year - 1) days
        dob = datetime(year, 1, 1) + timedelta(days=day_of_year - 1)
        # Convert to 'YYYY-MM-DD' format
        return dob.strftime('%Y-%m-%d')
    except ValueError:
        # This can happen if the day_of_year is 366 in a non-leap year
        return None

if __name__ == "__main__":
    # Prompt the user for their NIC
    nic_input = input("Please enter your NIC number: ")

    # Call the function
    dob = deriveDOBFromNIC(nic_input)

    # Print the result
    if dob is not None:
        print(f"Your date of birth is: {dob}")
    else:
        print("Invalid NIC format or day of year out of range.")
