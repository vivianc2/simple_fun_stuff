import re
import csv


def parse_information(text):
    shows = []
    current_show = {}
    current_option = None
    lines = text.split("\n")

    for line in lines:
        if re.match(r"^[A-Z\s]+\(.*\)$", line):
            if current_show:
                shows.append(current_show)
                current_show = {}
            show_name, theater_info = re.findall(r"^([A-Z\s]+)\((.*)\)$", line)[0]
            current_show["Show"] = show_name.strip()
            current_show["Theatre"] = theater_info.strip()
        elif line.strip() in [
            "Standing Room",
            "Digital Lottery",
            "In-Person Lottery",
            "General Rush",
            "Digital Rush",
        ]:
            current_option = line.strip()
            current_show[current_option] = {}
        elif current_option:
            if line.strip() != "":
                matches = re.findall(r"^(.+): (.+)$", line)
                if matches:
                    key, value = matches[0]
                    if current_option in current_show:
                        current_show[current_option][key] = value

    if current_show:
        shows.append(current_show)

    return shows


def write_to_csv(shows, filename):
    fieldnames = [
        "Show",
        "Theatre",
        "Option",
        "Price",
        "How",
        "Where",
        "Time",
        "Payment Method",
        "ID",
        "Tickets Per Person",
        "Seat Locations",
        "Number of Tickets Available",
        "Special Policies",
    ]

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for show in shows:
            show_data = {}
            if "Show" in show:
                show_data["Show"] = show["Show"]
            if "Theatre" in show:
                show_data["Theatre"] = show["Theatre"]

            options = list(show.keys())[2:]
            for option in options:
                option_data = show[option]
                option_data["Option"] = option
                # Filter out any extra keys not present in fieldnames
                option_data_filtered = {
                    k: v for k, v in option_data.items() if k in fieldnames
                }
                writer.writerow({**show_data, **option_data_filtered})


filename = "raw.txt"

# Open the file in read mode
with open(filename, "r") as file:
    # Read the entire file contents as a single string
    information = file.read()
    show_list = parse_information(information)
    csv_filename = "shows.csv"
    write_to_csv(show_list, csv_filename)
    print(f"CSV file '{csv_filename}' has been created.")
