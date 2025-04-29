import pandas as pd
from datetime import datetime

def calculate_rh_bed_occupancy(occupancy_file, start_date_str, end_date_str, total_beds=18):
    """
    Calculates bed occupancy statistics for Rosalie House from a CSV file.
    Only considers occupancy entirely within the specified date range.

    Args:
        occupancy_file (str): Path to the occupancy CSV file.
        start_date_str (str): Start date for analysis (YYYY-MM-DD).
        end_date_str (str): End date for analysis (YYYY-MM-DD).
        total_beds (int, optional): Total number of beds in Rosalie House. Defaults to 18.

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
        df = pd.read_csv(occupancy_file, encoding='utf-8')
        df = df.rename(columns={
            'Program Enrollment Name': 'program_name',
            'Bed: Bed Number': 'bed_name',
            'Sexual Orientation': 'sexual_orientation',
            'Entry Date': 'entry_date',
            'Exit Date': 'exit_date',
            'Age': 'age'
        })
        df['entry_date'] = pd.to_datetime(df['entry_date'], errors='coerce')
        df['exit_date'] = pd.to_datetime(df['exit_date'], errors='coerce')
        df['is_adult'] = df['age'] >= 18
        df = df.dropna(subset=['entry_date', 'exit_date'])
    except FileNotFoundError:
        print(f"Error: File not found: {occupancy_file}")
        return None, None, None, None, None, None
    except Exception as e:
        print(f"Error processing {occupancy_file}: {e}")
        return None, None, None, None, None, None

    total_days = (end_date - start_date).days + 1
    total_bed_nights = total_beds * total_days

    occupied_bed_days = 0
    adult_bed_nights = 0
    child_bed_nights = 0

    for index, row in df.iterrows():
        entry_date = row['entry_date']
        exit_date = row['exit_date']
        is_adult = row['is_adult']

        # Check if both entry and exit dates are within the analysis period.
        if start_date <= entry_date <= end_date and start_date <= exit_date <= end_date:
            occupancy_duration = (exit_date - entry_date).days + 1
            occupied_bed_days += occupancy_duration

            if is_adult:
                adult_bed_nights += occupancy_duration
            else:
                child_bed_nights += occupancy_duration

    occupancy_percentage = (occupied_bed_days / total_bed_nights) * 100 if total_bed_nights > 0 else 0.0

    return occupancy_percentage, total_bed_nights, adult_bed_nights, child_bed_nights, start_date_str, end_date_str


# --- Example Usage ---
if __name__ == "__main__":
    occupancy_file_path_2024 = r"C:\Users\jurbany\Desktop\BrennenBedPercent\RH18-24LastYR.csv"
    occupancy_file_path_2025 = r"C:\Users\jurbany\Desktop\BrennenBedPercent\RH2025.csv"

    total_beds = 18

    # --- 2024 Data (Sept 1 to December 31) ---
    start_date_2024 = "2024-09-01"
    end_date_2024 = "2024-12-31"
    (occupancy_percentage_2024, total_bed_nights_2024, adult_bed_nights_2024, child_bed_nights_2024, start_date_str_2024, end_date_str_2024) = \
        calculate_rh_bed_occupancy(occupancy_file_path_2024, start_date_2024, end_date_2024, total_beds)

    if occupancy_percentage_2024 is not None:
        print("----- 2024 Data (Sept 1 to December 31) -----")
        print(f"Rosalie House Occupancy Data from: {start_date_str_2024} to {end_date_str_2024}")
        print(f"Bed Occupancy Percentage: {occupancy_percentage_2024:.2f}%")
        print(f"Total Available Bed Nights: {total_bed_nights_2024}")
        print(f"Total Adult Bed Nights: {adult_bed_nights_2024}")
        print(f"Total Child Bed Nights: {child_bed_nights_2024}")
        print(f"Combined Adult and Child Bed Nights: {adult_bed_nights_2024 + child_bed_nights_2024}")

    # --- 2025 Data (First 6 Months) ---
    start_date_2025 = "2025-01-01"
    end_date_2025 = "2025-06-30"
    (occupancy_percentage_2025, total_bed_nights_2025, adult_bed_nights_2025, child_bed_nights_2025, start_date_str_2025, end_date_str_2025) = \
        calculate_rh_bed_occupancy(occupancy_file_path_2025, start_date_2025, end_date_2025, total_beds)

    if occupancy_percentage_2025 is not None:
        print("\n----- 2025 Data (First 6 Months) -----")
        print(f"Rosalie House Occupancy Data from: {start_date_str_2025} to {end_date_str_2025}")
        print(f"Bed Occupancy Percentage: {occupancy_percentage_2025:.2f}%")
        print(f"Total Available Bed Nights: {total_bed_nights_2025}")
        print(f"Total Adult Bed Nights: {adult_bed_nights_2025}")
        print(f"Total Child Bed Nights: {child_bed_nights_2025}")
        print(f"Combined Adult and Child Bed Nights: {adult_bed_nights_2025 + child_bed_nights_2025}")