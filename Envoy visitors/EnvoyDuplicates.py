import csv
from datetime import datetime, date
import argparse

def process_envoy_data(csv_file_path, output_file_path, start_date, end_date):
    """
    Filters Envoy data by date, removes same-day duplicates, identifies non-DV entries,
    and saves the unique entries to a single output file.  Also prints relevant counts to
    the console.
    """

    processed_entries = set()  # Store (name, sign_in_date) tuples
    unique_rows = []  # Store unique rows within the date range
    non_dv_names = set() # Store names of people who said "No" to DV question

    total_rows = 0
    filtered_rows_count = 0
    duplicate_count = 0

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames  # Get column headers from the CSV

            for row in reader:
                total_rows += 1
                name = row.get('name')
                sign_in_time_str = row.get('sign_in_time')
                dv_status = row.get('Are you a Domestic Violence survivor?\xa0')  # Handles Unicode NBSP

                if not name or not sign_in_time_str:
                    print(f"Warning: Skipping row due to missing name or sign_in_time: {row}")
                    continue  # Skip rows with missing data

                # Parse sign-in time (handling multiple possible formats)
                try:
                    sign_in_time = datetime.fromisoformat(sign_in_time_str.replace('Z', '+00:00'))  # ISO format
                except ValueError:
                    try:
                        sign_in_time = datetime.strptime(sign_in_time_str, '%Y-%m-%d %H:%M:%S %Z%z')
                    except ValueError:
                        try:
                            sign_in_time = datetime.strptime(sign_in_time_str, '%m/%d/%Y %I:%M:%S %p %Z%z')  # '01/02/2024 10:30:00 AM EST'
                        except ValueError:
                            try:
                                sign_in_time = datetime.strptime(sign_in_time_str, '%Y-%m-%d %H:%M:%S')  # standard formatting
                            except ValueError:
                                try:
                                    sign_in_time = datetime.strptime(sign_in_time_str, '%m/%d/%Y %I:%M:%S %p')  # '01/02/2024 10:30:00 AM'
                                except ValueError:
                                    print(f"Warning: Could not parse sign-in time '{sign_in_time_str}'. Skipping row.")
                                    continue

                sign_in_date = sign_in_time.date()

                # Date filtering
                if not (start_date <= sign_in_date <= end_date):
                    continue

                filtered_rows_count += 1

                entry_key = (name, sign_in_date)

                if entry_key not in processed_entries:
                    processed_entries.add(entry_key)
                    unique_rows.append(row)

                    # Check Non-DV status
                    if dv_status and dv_status.lower() == 'no':
                        non_dv_names.add(name)
                else:
                    duplicate_count += 1



    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' was not found.")
        return None #Important to return none for correct terminal output

    print("Processing complete.\n")
    print("Filtered and unique entries saved to:", output_file_path)

    print(f"\nTotal number of rows in the original file: {total_rows}")
    print(f"Number of rows within the date range ({start_date} to {end_date}): {filtered_rows_count}")
    print(f"Number of duplicate entries removed: {duplicate_count}")
    print(f"Total number of unique entries within the date range: {len(unique_rows)}")
    print(f"Number of unique entries who answered 'No' to the DV question: {len(non_dv_names)}")

    # Write the unique rows to the output CSV file
    try:
        with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
            if unique_rows:
                fieldnames = unique_rows[0].keys()  # Get column headers from the first row
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(unique_rows)
            else:
                print("No data to write to CSV.")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

    return unique_rows #Important to return unique rows to not get errors in main

def main():
    """Parses command-line arguments and processes Envoy data."""
    parser = argparse.ArgumentParser(description="Process Envoy data: filter by date, remove duplicates, identify non-DV entries.")
    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("output_csv", help="Path to the output CSV file")
    parser.add_argument("start_date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("end_date", help="End date (YYYY-MM-DD)")

    args = parser.parse_args()

    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date() #Date Formatting
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d").date() #Date Formatting
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
        return

    unique_data = process_envoy_data(args.input_csv, args.output_csv, start_date, end_date) #get unique data

    if unique_data is None: #Catch File Not Found Error
        print("No data to write to CSV.")
        return

if __name__ == "__main__":
    main()

# This script is designed to be run from the command line.
# Example usage:
#python EnvoyDuplicates.py "C:\Users\jurbany\Desktop\Envoy visitors\V-Mar18-Apr23.csv" "UniqueEntries.csv" 2025-03-18 2025-04-23
#pythron run the file path, the export csv file path, start date, and end date