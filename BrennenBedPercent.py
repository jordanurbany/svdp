import pandas as pd
import os
from datetime import datetime, timedelta

def calculate_bed_occupancy(adults_file, children_file, start_date_str, end_date_str, total_beds, output_file="cleaned_data.csv"):
    """
    Calculates bed occupancy statistics and exports cleaned data with occupancy duration.

    Args:
        adults_file (str): Path to the adults CSV file.
        children_file (str): Path to the children CSV file.
        start_date_str (str): Start date for analysis (YYYY-MM-DD).
        end_date_str (str): End date for analysis (YYYY-MM-DD).
        total_beds (int): Total number of beds.
        output_file (str, optional): Path to save the cleaned data. Defaults to "cleaned_data.csv".

    Returns:
        tuple: (occupancy_percentage, total_bed_nights, adult_bed_nights, child_bed_nights)
    """

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD.")
        return None, None, None, None

    def process_file(file_path, is_adult):
        try:
            df = pd.read_csv(file_path)
            df = df.rename(columns={
                'Program Enrollment Name': 'program_name',
                'Bed Assignment Name': 'bed_name',
                'Sexual Orientation': 'sexual_orientation',
                'Entry Date': 'entry_date',
                'Exit Date': 'exit_date'
            })
            df['entry_date'] = pd.to_datetime(df['entry_date'])
            df['exit_date'] = pd.to_datetime(df['exit_date'], errors='coerce')
            df['is_adult'] = is_adult
            return df
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
            return None
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None

    adults_df = process_file(adults_file, True)
    children_df = process_file(children_file, False)

    if adults_df is None and children_df is None:
        print("Error: No valid data in adults or children files.")
        return None, None, None, None

    if adults_df is not None and children_df is not None:
        combined_df = pd.concat([adults_df, children_df], ignore_index=True)
    elif adults_df is not None:
        combined_df = adults_df
    else:
        combined_df = children_df

    total_days = (end_date - start_date).days + 1
    total_bed_nights = total_beds * total_days

    # Initialize lists to store occupancy duration values
    occupancy_durations = []
    adult_bed_nights = 0
    child_bed_nights = 0
    occupied_bed_days = 0

    for index, row in combined_df.iterrows():
        entry_date = row['entry_date']
        exit_date = row['exit_date']
        is_adult = row['is_adult']

        if pd.isna(exit_date):
            exit_date = end_date

        entry_date = max(entry_date, start_date)
        exit_date = min(exit_date, end_date)

        occupancy_duration = (exit_date - entry_date).days + 1
        if occupancy_duration > 0:
            occupied_bed_days += occupancy_duration
            if is_adult:
                adult_bed_nights += occupancy_duration
            else:
                child_bed_nights += occupancy_duration
        else:
            occupancy_duration = 0  # Ensure it's 0 if negative

        occupancy_durations.append(occupancy_duration)  # Append to the list

    occupancy_percentage = (occupied_bed_days / total_bed_nights) * 100 if total_bed_nights > 0 else 0.0

    # Add the calculated durations to the DataFrame
    combined_df['occupancy_duration'] = occupancy_durations

    columns_to_export = ['program_name', 'bed_name', 'sexual_orientation', 'entry_date', 'exit_date', 'is_adult', 'occupancy_duration']  #Include occupancy_duration
    try:
        combined_df[columns_to_export].to_csv(output_file, index=False)
        print(f"Cleaned data saved to: {output_file}")
    except Exception as e:
        print(f"Error saving cleaned data to CSV: {e}")

    return occupancy_percentage, total_bed_nights, adult_bed_nights, child_bed_nights


# --- Example Usage ---
if __name__ == "__main__":
    adults_file_path = "adults.csv"
    children_file_path = "children.csv"
    start_date = "2024-01-28"
    end_date = "2025-03-24"
    total_beds = 32
    output_csv_file = os.path.join(os.getcwd(), "cleaned_bed_data.csv")

    (occupancy_percentage, total_bed_nights, adult_bed_nights, child_bed_nights) = calculate_bed_occupancy(adults_file_path, children_file_path, start_date, end_date, total_beds, output_csv_file)

    if occupancy_percentage is not None:
        print(f"Bed Occupancy Percentage: {occupancy_percentage:.2f}%")
        print(f"Total Available Bed Nights: {total_bed_nights}")
        print(f"Total Adult Bed Nights: {adult_bed_nights}")
        print(f"Total Child Bed Nights: {child_bed_nights}")
        print(f"Combined Adult and Child Bed Nights: {adult_bed_nights + child_bed_nights}")