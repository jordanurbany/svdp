import pandas as pd
from datetime import datetime

def calculate_bed_occupancy(occupancy_file, start_date_str, end_date_str, total_beds, output_file="cleaned_data.csv"):
    """
    Calculates bed occupancy statistics from a single CSV file and exports cleaned data with occupancy duration.

    Args:
        occupancy_file (str): Path to the occupancy CSV file (BHoccupancy.csv).
        start_date_str (str): Start date for analysis (YYYY-MM-DD).
        end_date_str (str): End date for analysis (YYYY-MM-DD).
        total_beds (int): Total number of beds.
        output_file (str, optional): Path to save the cleaned data. Defaults to "cleaned_data.csv".

    Returns:
        tuple: (occupancy_percentage, total_bed_nights, adult_bed_nights, child_bed_nights, start_date_str, end_date_str)
    """

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD.")
        return None, None, None, None, None, None

    try:
        df = pd.read_csv(occupancy_file, encoding='utf-8')  # Specify encoding
        df = df.rename(columns={
            'Program Enrollment Name': 'program_name',
            'Bed: Bed Number': 'bed_name',  # Updated column name
            'Sexual Orientation': 'sexual_orientation',
            'Entry Date': 'entry_date',
            'Exit Date': 'exit_date',
            'Age': 'age'  # Map the Age
        })
        df['entry_date'] = pd.to_datetime(df['entry_date'], errors='coerce')  # Handle parsing errors
        df['exit_date'] = pd.to_datetime(df['exit_date'], errors='coerce')    # Handle parsing errors
        df['is_adult'] = df['age'] >= 18 # Create is_adult column.
        df = df.dropna(subset=['entry_date', 'exit_date']) # Remove rows with invalid date
    except FileNotFoundError:
        print(f"Error: File not found: {occupancy_file}")
        return None, None, None, None, None, None
    except Exception as e:
        print(f"Error processing {occupancy_file}: {e}")
        return None, None, None, None, None, None

    total_days = (end_date - start_date).days + 1
    total_bed_nights = total_beds * total_days

    # Initialize lists to store occupancy duration values
    occupancy_durations = []
    adult_bed_nights = 0
    child_bed_nights = 0
    occupied_bed_days = 0

    for index, row in df.iterrows():
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
    df['occupancy_duration'] = occupancy_durations

    columns_to_export = ['program_name', 'bed_name', 'sexual_orientation', 'entry_date', 'exit_date', 'is_adult', 'occupancy_duration']  #Include occupancy_duration
    try:
        df[columns_to_export].to_csv(output_file, index=False, encoding='utf-8') # added encoding
        print(f"Cleaned data saved to: {output_file}")
    except Exception as e:
        print(f"Error saving cleaned data to CSV: {e}")

    return occupancy_percentage, total_bed_nights, adult_bed_nights, child_bed_nights, start_date_str, end_date_str

# --- Example Usage ---
if __name__ == "__main__":
    occupancy_file_path = r"C:\Users\jurbany\Desktop\BrennenBedPercent\BHoccupancy.csv"  # Updated file path
    start_date = "2024-01-01"
    end_date = "2024-12-31"
    total_beds = 32 # Use your actual total number of beds
    output_csv_file = "cleaned_bed_data.csv"  # Simplify the output path

    (occupancy_percentage, total_bed_nights, adult_bed_nights, child_bed_nights, start_date_str, end_date_str) = calculate_bed_occupancy(occupancy_file_path, start_date, end_date, total_beds, output_csv_file)

    if occupancy_percentage is not None:
        print(f"Occupancy Data from: {start_date_str} to {end_date_str}")
        print(f"Bed Occupancy Percentage: {occupancy_percentage:.2f}%")
        print(f"Total Available Bed Nights: {total_bed_nights}")
        print(f"Total Adult Bed Nights: {adult_bed_nights}")
        print(f"Total Child Bed Nights: {child_bed_nights}")
        print(f"Combined Adult and Child Bed Nights: {adult_bed_nights + child_bed_nights}")