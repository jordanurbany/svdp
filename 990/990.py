import pandas as pd

def analyze_brennen_data(csv_file="BrennanAll.csv", output_file="brennen_filtered_data.csv", house_name="Brennen House"):
    """
    Reads a CSV file, filters records based on Entry Date and Exit Date falling within a
    specified range, removes duplicate entries based on 'Full Name', calculates total and filtered
    counts, and exports the filtered data to a new CSV file.

    Args:
        csv_file (str, optional): The path to the input CSV file.
            Defaults to "BrennanAll.csv".
        output_file (str, optional): The path to the output CSV file for filtered data.
        house_name (str, optional): The name of the house for the output description.
            Defaults to "Brennen House".

    Returns:
        None. Prints total and filtered counts to the console, and exports filtered data to a CSV file.
    """

    try:
        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(csv_file)

        # Convert 'Entry Date' and 'Exit Date' to datetime objects, handling errors
        df['Entry Date'] = pd.to_datetime(df['Entry Date'], errors='coerce')
        df['Exit Date'] = pd.to_datetime(df['Exit Date'], errors='coerce')

        # Define the date range
        start_date = pd.to_datetime('07/01/2023')
        end_date = pd.to_datetime('06/30/2025')

        # Store the total number of people before filtering (before removing duplicates)
        total_people = len(df)

        # Filter the DataFrame based on the specified date range
        filtered_df = df[
            ((df['Entry Date'] >= start_date) & (df['Entry Date'] <= end_date)) |
            ((df['Exit Date'] >= start_date) & (df['Exit Date'] <= end_date))
        ]

        # Remove duplicate rows based on 'Full Name'.  Keep the first occurrence.
        filtered_df = filtered_df.drop_duplicates(subset=['Full Name'], keep='first')  # Removes duplicates based on 'Full Name'

        # Calculate the total number of people after filtering and removing duplicates
        filtered_people = len(filtered_df)

        # Print the results
        print(f"--- {house_name} ---") #added house name
        print(f"Total number of people in the CSV: {total_people}")
        print(f"Number of people with Entry or Exit Date between 07/01/2023 and 06/30/2025 (duplicates removed based on 'Full Name'): {filtered_people}")

        # Export the filtered data to a new CSV file
        filtered_df.to_csv(output_file, index=False)
        print(f"Filtered data exported to: {output_file}")

    except FileNotFoundError:
        print(f"Error: File not found at path: {csv_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


def analyze_rosalie_data(csv_file="RosalieAll.csv", output_file="rosalie_filtered_data.csv"):
    """
    Analyzes Rosalie House data with the same filtering logic as Brennen House.
    """
    analyze_brennen_data(csv_file=csv_file, output_file=output_file, house_name="Rosalie House")


# Example usage:
analyze_brennen_data()  # Processes Brennan House
analyze_rosalie_data()   # Processes Rosalie House