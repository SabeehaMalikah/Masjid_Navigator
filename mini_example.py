'''
Task: Start by building a tiny Python program containing 5-10 mosques and their facilities (hardcoded JSON), and allow the user to search/filter them.

'''
from datetime import datetime


masjid1 = {
    "name" : "Al Istiqamah Community Center",
    "address" : "1835 Bay Ridge Pkwy, Brooklyn, NY 11204",
    "womens_section" : True,
    "denomination" : "Sunni",
    "open" : "4:45",
    "close" : "21:25",
    "rating" : 4.9
}
masjid2 = {
    "name" : "Islamic Society of Bay Ridge",
    "address" : "6807 5th Ave a1, Brooklyn, NY 11220",
    "womens_section" : True,
    "denomination" : "Sunni",
    "open" : "11:30",
    "close" : "21:30",
    "rating" : 4.8
}
masjid3 = {
    "name" : "Islamic Mission of America/Dawood Mosque",
    "address" : "143 State St, Brooklyn, NY 11201",
    "womens_section" : True,
    "denomination" : "Sunni",
    "open" : "4:45",
    "close" : "21:25",
    "rating" : 4.9
}
masjid4 = {
    "name" : "Al-Farooq Mosque",
    "address" : "554 Atlantic Ave, Brooklyn, NY 11217",
    "womens_section" : True,
    "denomination" : "Sunni",
    "open" : "12:00",
    "close" : "21:00",
    "rating" : 4.8
}
masjid5 = {
    "name" : "North Bronx Islamic Center",
    "address" : "261 E 206th St, Bronx, NY 10467",
    "womens_section" : False,
    "denomination" : "Sunni",
    "open" : "9:00",
    "close" : "18:00",
    "rating" : 4.6
}
masjid6 = {
    "name" : "Al-Mahdi Foundation",
    "address" : "779 Coney Island Ave, Brooklyn, NY 11218",
    "womens_section" : False,
    "denomination" : "Shia",
    "open" : "0:00",
    "close" : "0:00",
    "rating" : 4.8
}
masjids = [masjid1, masjid2, masjid3, masjid4, masjid5, masjid6]

def has_womens_section(masjids, masjid_name):
    for masjid in masjids:
        if masjid_name.lower() == masjid["name"].lower():
            return masjid["womens_section"]
    return "Masjid not found."

def filter_womens_section(masjids):
    result = [masjid for masjid in masjids if masjid["womens_section"]]
    return result

def filter_sunni(masjids):
    result = [masjid for masjid in masjids if masjid["denomination"] == "Sunni"]
    return result

def filter_shia(masjids):
    result = [masjid for masjid in masjids if masjid["denomination"] == "Shia"]
    return result

def filter_open(masjids):
    current_time = datetime.now().strftime("%H:%M")
    result = [masjid for masjid in masjids if masjid["open"] < current_time and masjid["close"] > current_time]
    return result

def filter_borough(masjids, target_borough):
    result = [masjid for masjid in masjids if target_borough in masjid["address"]]
    return result

def print_directory(masjids_list=masjids):
    i = 0
    for masjid in masjids_list:
        print(
            f"{i}. {masjid["name"]}\n" \
            f"{masjid["address"]}\n" \
            f"Hours: {masjid["open"]} - {masjid["close"]}"
        )
        print()
        i += 1

def main():
    print(
        "Welcome to Masjid Navigator!\n" \
        "Please see the list of masaajid below:\n"
    )
    print_directory()
    
    while True:
        filter_option = input(
            "\nPlease choose from the following filtering options: \n" \
            "'W' -- for masaajid with womens' prayer area \n" \
            "'SN' -- for Sunni masaajid\n" \
            "'SH' -- for Shia masaajid\n" \
            "'B' -- for masaajid in Brooklyn\n" \
            "'Q' -- for masaajid in Queens\n" \
            "'M' -- for masaajid in Manhattan\n" \
            "'BR' for masaajid in the Bronx\n" \
            "'SI' -- for masaajid in Staten Island\n" \
            "'X' -- to exit the menu\n\n"
        )
        if filter_option.upper() == 'W':
            print_directory(filter_womens_section(masjids))
        elif filter_option.upper() == 'SN':
            print_directory(filter_sunni(masjids))
        elif filter_option.upper() == 'SH':
            print_directory(filter_shia(masjids))
        elif filter_option.upper() == 'B':
            print_directory(filter_borough(masjids, "Brooklyn"))
        elif filter_option.upper() == 'Q':
            print_directory(filter_borough(masjids, "Queens"))
        elif filter_option.upper() == 'M':
            print_directory(filter_borough(masjids, "New York"))
        elif filter_option.upper() == 'BR':
            print_directory(filter_borough(masjids, "Bronx"))
        elif filter_option.upper() == 'SI':
            print_directory(filter_borough(masjids, "Staten Island"))
        elif filter_option.upper() == 'X':
            print("Thank you for choosing Masjid Navigator!")
            exit()
        else:
            print("Please choose from the given filter options.")

main()


