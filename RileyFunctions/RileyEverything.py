import pandas as pd
from datetime import datetime
import re

def calculate_occupancy(occupancy_file, start_date_str, end_date_str):
    """
    Calculates and prints bed and bedroom occupancy statistics for Brennen and Rosalie Houses
    from a combined CSV file.  Includes people whose entry OR exit dates are within the period.
    """

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD.")
        return

    try:
        df = pd.read_csv(occupancy_file, encoding='utf-8')
        df = df.rename(columns={
            'Bed: Bed Number': 'bed_name',
            'Full Name': 'full_name',
            'Program Enrollment Name': 'program_name',
            'Bed Assignment Name': 'bed_assignment_name',
            'Age': 'age',
            'Sexual Orientation': 'sexual_orientation',
            'Other Exit Reason': 'other_exit_reason',
            'Nationality/Race/Ethnicity': 'ethnicity',
            'Gender': 'gender',
            'Entry Date': 'entry_date',
            'Exit Date': 'exit_date',
            'Exit Reason': 'exit_reason',
            'Race': 'race',
            'Start Date/Time': 'start_time',
            'Bed Transfer': 'bed_transfer'
        })
        df['entry_date'] = pd.to_datetime(df['entry_date'], errors='coerce')
        df['exit_date'] = pd.to_datetime(df['exit_date'], errors='coerce')
        df['is_adult'] = df['age'] >= 18
        df = df.dropna(subset=['entry_date', 'exit_date'])

    except FileNotFoundError:
        print(f"Error: File not found: {occupancy_file}")
        return
    except Exception as e:
        print(f"Error processing {occupancy_file}: {e}")
        return

    # --- Constants ---
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    total_days = (end_date - start_date).days + 1

    rh_total_beds = 18  # Rosalie House
    bh_total_beds = 32  # Brennen House
    rh_total_rooms = 6   # Rosalie has 6 rooms
    bh_total_rooms = 12  # Brennen has 12 rooms. Room #'s 5-16

    rh_total_bed_nights = rh_total_beds * total_days
    bh_total_bed_nights = bh_total_beds * total_days

    rh_total_room_nights = rh_total_rooms * total_days
    bh_total_room_nights = bh_total_rooms * total_days

    # --- Initialize tracking variables ---
    rh_occupied_bed_days = 0
    rh_adult_bed_nights = 0
    rh_child_bed_nights = 0
    rh_occupied_room_days = 0
    
    bh_occupied_bed_days = 0
    bh_adult_bed_nights = 0
    bh_child_bed_nights = 0
    bh_occupied_room_days = 0
    
    # --- Track unique people at the RECORD level, not day level ---
    rh_unique_adults = set()
    rh_unique_children = set()
    bh_unique_adults = set()
    bh_unique_children = set()
    
    # --- Process data for counting unique individuals first ---
    # This counts people before day-by-day iteration
    for index, row in df.iterrows():
        bed_name = row['bed_name']
        entry_date = row['entry_date']
        exit_date = row['exit_date']
        is_adult = row['is_adult']
        full_name = row['full_name']
        
        # Check if this stay overlaps with our analysis period
        if not (exit_date < start_date or entry_date > end_date):
            # This person stayed during our analysis period
            if "RH" in bed_name:
                if is_adult:
                    rh_unique_adults.add(full_name)
                else:
                    rh_unique_children.add(full_name)
            elif "BH" in bed_name:
                if is_adult:
                    bh_unique_adults.add(full_name)
                else:
                    bh_unique_children.add(full_name)

    #---- Set for holding data ------
    rh_adult_bed_room = [set() for _ in range(total_days)]
    bh_adult_bed_room = [set() for _ in range(total_days)]

    # --- Now process data for occupancy calculations ---
    for index, row in df.iterrows():
        bed_name = row['bed_name']
        entry_date = row['entry_date']
        exit_date = row['exit_date']
        is_adult = row['is_adult']

        # Check if this stay overlaps with our analysis period
        if not (exit_date < start_date or entry_date > end_date):
            # Adjust entry and exit dates to be within the analysis period
            entry_date = max(entry_date, start_date)
            exit_date = min(exit_date, end_date)
            
            occupancy_duration = (exit_date - entry_date).days + 1

            # Iterate each day in duration
            for day in range(occupancy_duration):
                current_date = entry_date + pd.Timedelta(days=day)
                day_index = (current_date - start_date).days
                
                # --- Rosalie House (RH) ---
                if "RH" in bed_name:
                    rh_occupied_bed_days += 1
                    
                    if is_adult:
                        rh_adult_bed_nights += 1
                        try:
                            match = re.search(r'Rm (\d+)', bed_name)
                            if match:
                                room_number = int(match.group(1))
                                rh_adult_bed_room[day_index].add(room_number)
                                rh_occupied_room_days += 1
                        except Exception as e:
                            pass
                    else:
                        rh_child_bed_nights += 1

                # --- Brennen House (BH) ---
                elif "BH" in bed_name:
                    bh_occupied_bed_days += 1
                    
                    if is_adult:
                        bh_adult_bed_nights += 1
                        try:
                            match = re.search(r'Rm (\d+)', bed_name)
                            if match:
                                room_number = int(match.group(1))
                                if 5 <= room_number <= 16:
                                    bh_adult_bed_room[day_index].add(room_number)
                                    bh_occupied_room_days += 1
                        except Exception as e:
                            pass
                    else:
                        bh_child_bed_nights += 1

    # --- Calculate Percentages ---
    rh_bed_occupancy_percentage = (rh_occupied_bed_days / rh_total_bed_nights) * 100 if rh_total_bed_nights > 0 else 0.0
    bh_bed_occupancy_percentage = (bh_occupied_bed_days / bh_total_bed_nights) * 100 if bh_total_bed_nights > 0 else 0.0

    rh_room_occupancy_percentage = (rh_occupied_room_days / rh_total_room_nights) * 100 if rh_total_room_nights > 0 else 0.0
    bh_room_occupancy_percentage = (bh_occupied_room_days / bh_total_room_nights) * 100 if bh_total_room_nights > 0 else 0.0

    # --- Print Results ---
    print("----- Occupancy Statistics -----")
    print(f"Analysis Period: {start_date_str} to {end_date_str}")
    print(f"Total Days: {total_days}")

    print("\n----- Rosalie House -----")
    print(f"Bed Occupancy Percentage: {rh_bed_occupancy_percentage:.2f}%")
    print(f"Total Available Bed Nights: {rh_total_bed_nights}")
    print(f"Total Adult Bed Nights: {rh_adult_bed_nights}")
    print(f"Total Child Bed Nights: {rh_child_bed_nights}")
    print(f"Bedroom Occupancy Percentage: {rh_room_occupancy_percentage:.2f}%")
    print(f"Total Available Bedroom Nights: {rh_total_room_nights}")
    print(f"Total Room Occupancy: {rh_occupied_room_days}")

    print("\n----- Brennen House -----")
    print(f"Bed Occupancy Percentage: {bh_bed_occupancy_percentage:.2f}%")
    print(f"Total Available Bed Nights: {bh_total_bed_nights}")
    print(f"Total Adult Bed Nights: {bh_adult_bed_nights}")
    print(f"Total Child Bed Nights: {bh_child_bed_nights}")
    print(f"Bedroom Occupancy Percentage: {bh_room_occupancy_percentage:.2f}%")
    print(f"Total Available Bedroom Nights: {bh_total_room_nights}")
    print(f"Total Room Occupancy: {bh_occupied_room_days}")
    
    # --- Print People Served Statistics at the end ---
    print("\n----- People Served (Year Total) -----")
    print("\nRosalie House:")
    print(f"Total Unique Adults Served: {len(rh_unique_adults)}")
    print(f"Total Unique Children Served: {len(rh_unique_children)}")
    
    print("\nBrennen House:")
    print(f"Total Unique Adults Served: {len(bh_unique_adults)}")
    print(f"Total Unique Children Served: {len(bh_unique_children)}")

# --- Example Usage ---
if __name__ == "__main__":
    occupancy_file_path = r"C:\Users\jurbany\Desktop\BrennenBedPercent\RileyEverything.csv"
    start_date = "2024-01-01"
    end_date = "2024-12-31"
    calculate_occupancy(occupancy_file_path, start_date, end_date)