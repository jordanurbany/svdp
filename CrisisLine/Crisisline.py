import csv
from datetime import datetime

def count_calls_in_date_range(filename="CrisisLineReport.csv"):
    """
    Reads a CSV file, counts the number of crisis line calls within a specified date range
    (March 18, 2025 to today), and returns the count.

    Args:
        filename (str, optional): The name of the CSV file to read.
                                  Defaults to "CrisisLineReport.csv".

    Returns:
        int: The number of crisis line calls within the date range.
    """

    start_date = datetime(2025, 3, 18)  # March 18, 2025
    today = datetime.now()
    call_count = 0

    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Skip the header row

            # Check if the "Assessment Date" column exists in the header. if not we can't proceed
            if "Assessment Date" not in header:
                print("Error: 'Assessment Date' column not found in CSV file.")
                return 0

            date_column_index = header.index("Assessment Date")

            for row in reader:
                try:
                    # Extract the date from the first column
                    date_string = row[date_column_index]
                    assessment_date = datetime.strptime(date_string, '%m/%d/%Y')  # Parse date

                    # Check if the date is within the specified range
                    if start_date <= assessment_date <= today:
                        call_count += 1
                except ValueError as e:
                    print(f"Skipping row due to invalid date format: {row}. Error: {e}") # Print errors if there are any with date format
                except IndexError as e:
                    print(f"Skipping row due to missing data: {row}. Error: {e}") # Print errors if there is any other missing data


    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return 0
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 0

    return call_count

# Example usage:
if __name__ == "__main__":
    call_count = count_calls_in_date_range()
    print(f"Number of crisis line calls between March 18, 2025 and today: {call_count}")