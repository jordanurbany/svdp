import pandas as pd
from datetime import datetime

def calculate_rh_room_occupancy(occupancy_file, start_date_str, end_date_str):
    """
    Calculates room occupancy statistics for Rosalie House from a CSV file.

    Args:
        occupancy_file (str): Path to the occupancy CSV file.
        start_date_str (str): Start date for analysis (YYYY-MM-DD).
        end_date_str (str): End date for analysis (YYYY-MM-DD).

    Returns:
        tuple: (total_room_nights, occupied_room_nights, room_occupancy_percentage)
    """

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD.")
        return None, None, None

    try:
        df = pd.read_csv(occupancy_file, encoding='utf-8')  # Specify encoding
        df = df.rename(columns={
            'Program Enrollment Name': 'program_name',
            'Bed: Bed Number': 'bed_name',  # Updated column name
            'Sexual Orientation': 'sexual_orientation',
            'Entry Date': 'entry_date',
            'Exit Date': 'exit_date',
            'Age': 'age',
            'Program' : 'program'
        })
        df['entry_date'] = pd.to_datetime(df['entry_date'], errors='coerce')  # Handle parsing errors
        df['exit_date'] = pd.to_datetime(df['exit_date'], errors='coerce')    # Handle parsing errors
        df = df.dropna(subset=['entry_date', 'exit_date']) # Remove rows with invalid date
    except FileNotFoundError:
        print(f"Error: File not found: {occupancy_file}")
        return None, None, None
    except Exception as e:
        print(f"Error processing {occupancy_file}: {e}")
        return None, None, None

    total_days = (end_date - start_date).days + 1

    # Calculate room occupancy
    total_rooms = 6
    total_room_nights = total_rooms * total_days
    occupied_rooms_per_day = {}  # Dictionary to track occupied rooms for each day

    for index, row in df.iterrows():
        entry_date = row['entry_date']
        exit_date = row['exit_date']
        bed_name = row['bed_name']

        if pd.isna(exit_date):
            exit_date = end_date

        entry_date = max(entry_date, start_date)
        exit_date = min(exit_date, end_date)

        occupancy_duration = (exit_date - entry_date).days + 1
        if occupancy_duration > 0:

            # Extract the room number from the bed_name (Rosalie House format)
            try:
                room_number = bed_name.split('Rm ')[1].split('-')[0]  # Extract room number
                room_number = int(room_number)
            except:
                room_number = None

            if room_number is not None:
                for day in range(occupancy_duration):
                    current_date = entry_date + pd.Timedelta(days=day)
                    if current_date not in occupied_rooms_per_day:
                        occupied_rooms_per_day[current_date] = set()
                    occupied_rooms_per_day[current_date].add(room_number)

    # Calculate occupied room nights
    occupied_room_nights = sum(len(rooms) for rooms in occupied_rooms_per_day.values())
    room_occupancy_percentage = (occupied_room_nights / total_room_nights) * 100 if total_room_nights > 0 else 0.0

    return total_room_nights, occupied_room_nights, room_occupancy_percentage


# --- Example Usage ---
if __name__ == "__main__":
    occupancy_file_path = r"C:\Users\jurbany\Desktop\BrennenBedPercent\RH18-24LastYR.csv"  # Updated file path
    start_date = "2024-01-01"
    end_date = "2024-12-31"

    total_room_nights, occupied_room_nights, room_occupancy_percentage = calculate_rh_room_occupancy(occupancy_file_path, start_date, end_date)

    if total_room_nights is not None:
        print(f"Total Available Room Nights: {total_room_nights}")
        print(f"Total Occupied Room Nights: {occupied_room_nights}")
        print(f"Room Occupancy Percentage: {room_occupancy_percentage:.2f}%")