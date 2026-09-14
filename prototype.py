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
    "close" : "23:59",
    "rating" : 4.8
}
masjid7 = {
    "name" : "Islamic Cultural Center of New York",
    "address" : "1711 3rd Ave, New York, NY 10029",
    "womens_section" : True,
    "denomination" : "Sunni",
    "open" : "10:00",
    "close" : "17:00",
    "rating" : 4.7
}
masjid8 = {
    "name" : "Masjid Manhattan",
    "address" : "30 Cliff St, New York, NY 10038",
    "womens_section" : True,
    "denomination" : "Sunni",
    "open" : "4:00",
    "close" : "22:30",
    "rating" : 4.8
}
masjid9 = {
    "name" : "An-Noor Masjid",
    "address" : "70-13 37 Avenue,(Basement, Jackson Heights, NY 11372",
    "womens_section" : False,
    "denomination" : "Sunni",
    "open" : None,
    "close" : None,
    "rating" : 4.4
}
masjid10 = {
    "name" : "MAS Staten Island Center (MASSI Center)",
    "address" : "180 Burgher Ave, Staten Island, NY 10304",
    "womens_section" : True,
    "denomination" : "Sunni",
    "open" : "6:00",
    "close" : "22:30",
    "rating" : 4.8
}
masjids = [masjid1, masjid2, masjid3, masjid4, masjid5, masjid6, masjid7, masjid8, masjid9, masjid10]

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
    if target_borough == "Queens:":
        result = []
        for masjid in masjids:
            if masjid["address"][:-5][:3] == "110" or masjid["address"][:-5][:3] == "111" or \
                masjid["address"][:-5][:3] == "113" or masjid["address"][:-5][:3] == "114" or \
                masjid["address"][:-5][:3] == "116":
                result.append(masjid)
    return result

def print_directory(masjids_list=masjids):
    i = 1
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

    # prompt the user
    filter_options = input(
            "\nPlease choose from the following filtering options: \n" \
            "'W' -- for masaajid with womens' prayer area \n" \
            "'SN' -- for Sunni masaajid\n" \
            "'SH' -- for Shia masaajid\n" \
            "'B' -- for masaajid in Brooklyn\n" \
            "'M' -- for masaajid in Manhattan\n" \
            "'Q' -- for masaajid in Queens\n" \
            "'BR' for masaajid in the Bronx\n" \
            "'SI' -- for masaajid in Staten Island\n" \
            "'X' -- to exit\n\n" \
            "Enter your response as a list of all the filters you would like to apply.\n" \
            "If you would like to see sunni masjids in Brooklyn, you would enter 'SN B'.\n"
        )
    valid_filters = ["W", "SN", "SH", "B", "M", "Q", "BR", "SI", "X"]
    filter_options = filter_options.split()
    valid = True
    for f in filter_options:
        if f.upper() not in valid_filters:
            valid = False
    if not valid:
        filter = input(
            "\nInvalid filter entered. \nPlease choose from the following filtering options: \n" \
            "'W' -- for masaajid with womens' prayer area \n" \
            "'SN' -- for Sunni masaajid\n" \
            "'SH' -- for Shia masaajid\n" \
            "'B' -- for masaajid in Brooklyn\n" \
            "'M' -- for masaajid in Manhattan\n" \
            "'Q' -- for masaajid in Queens\n" \
            "'BR' for masaajid in the Bronx\n" \
            "'SI' -- for masaajid in Staten Island\n" \
            "'X' -- to exit the menu\n\n"
        )
    result = masjids
    for filter in filter_options:
        if filter.upper() == 'W':
            result = filter_womens_section(result)
        elif filter.upper() == 'SN':
            result = filter_sunni(result)
        elif filter.upper() == 'SH':
            result = filter_shia(result)
        elif filter.upper() == 'B':
            result = filter_borough(result, "Brooklyn")
        elif filter.upper() == 'Q':
            result = filter_borough(result, "Queens")
        elif filter.upper() == 'M':
            result = filter_borough(result, "New York")
        elif filter.upper() == 'BR':
            result = filter_borough(result, "Bronx")
        elif filter.upper() == 'SI':
            result = filter_borough(result, "Staten Island")
        elif filter.upper() == 'X':
            print("Thank you for choosing Masjid Navigator!")
            exit()
        else:
            print("Please choose from the given filter options.")
    if result == []:
        print("Sorry, no masjids found.")

    print("\n\nFiltered Masjids:")
    print_directory(result)
    print("Thank you for choosing Masjid Navigator!")


main()


