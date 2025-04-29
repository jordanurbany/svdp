import csv
from datetime import datetime

def sort_uav_data(filename="UAV.csv"):
    january_data = []
    february_data = []
    march_data = []
    total_lines = 0
    unique_entries = {}  # Dictionary to track unique entries

    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                total_lines += 1
                try:
                    start_date_str = row["Start Date/Time"]
                    date_format = '%m/%d/%Y, %I:%M %p'
                    start_date = datetime.strptime(start_date_str, date_format)
                    month = start_date.month

                    # Deduplicate based on "Full Name"
                    full_name = row["Full Name"]

                    if full_name not in unique_entries:
                        # Store ONLY the Full Name and Exit Reason
                        unique_entries[full_name] = {"Full Name": row["Full Name"], "Exit Reason": row["Exit Reason"]}

                        if month == 1:
                            january_data.append(unique_entries[full_name])
                        elif month == 2:
                            february_data.append(unique_entries[full_name])
                        elif month == 3:
                            march_data.append(unique_entries[full_name])

                except ValueError as e:
                    print(f"ValueError: Could not parse date '{start_date_str}' in row: {row}. Error: {e}")
                except KeyError as e:
                    print(f"KeyError: Missing column in CSV: {e}")
                    return None

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None

    print(f"Total lines in CSV: {total_lines}")
    return january_data, february_data, march_data

def write_to_csv(data, filename="unique_uav_data.csv"):
    """Writes the unique data to a CSV file, including the 'Exit Reason'."""
    if not data:
        print("No data to write to CSV.")
        return

    fieldnames = ["Full Name", "Exit Reason"]  # Only these two columns

    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Successfully wrote unique data to '{filename}'")
    except Exception as e:
        print(f"Error writing to CSV: {e}")


def main():
    data = sort_uav_data()
    if data is not None:
        january_data, february_data, march_data = data

        print(f"Number of entries in January: {len(january_data)}")
        print(f"Number of entries in February: {len(february_data)}")
        print(f"Number of entries in March: {len(march_data)}")

        all_unique_data = january_data + february_data + march_data
        print(f"Total number of unique entries: {len(all_unique_data)}")

        write_to_csv(all_unique_data)


if __name__ == "__main__":
    main()