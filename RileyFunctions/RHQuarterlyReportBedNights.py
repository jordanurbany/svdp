import pandas as pd

def calculate_rosalie_house_nights(filename="RHQuarterly.csv"):
    """
    Calculates bed nights and counts *unique* children and adults served at Rosalie House,
    handling cases where individuals may have multiple entries.

    Handles entries before Jan 1st, missing exit dates, and exits within the period.
    Assumes a maximum of 37 records.

    Args:
        filename (str, optional): The name of the CSV file to read. Defaults to "RHQuarterly.csv".

    Returns:
        tuple: A tuple containing the following values:
            - total_individual_nights (int): Total bed nights for all individuals (Adults and Children).
            - total_possible_bed_nights (int):  The total *possible* bed nights during the reporting period.
            - total_adult_nights (int): Total bed nights for adults.
            - total_child_nights (int): Total bed nights for children.
            - total_adults_served (int): Total number of *unique* adults served.
            - total_children_served (int): Total number of *unique* children served.
            - total_records (int): The number of records processed.
    """

    try:
        df = pd.read_csv(filename)
        if len(df) > 37:
            print(f"Warning: Found more than 37 records ({len(df)}).  Check your data for duplicates or errors.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return 0, 0, 0, 0, 0, 0, 0

    start_date = pd.to_datetime("2025-01-01")
    end_date = pd.to_datetime("2025-03-31")
    num_days_in_period = (end_date - start_date).days + 1
    total_possible_bed_nights = 35 * num_days_in_period # Assuming 35 physical beds at the house.

    # Convert 'Entry Date' and 'Exit Date' to datetime objects
    df['Entry Date'] = pd.to_datetime(df['Entry Date'])

    # Fill missing 'Exit Date' values with the end of the reporting period
    df['Exit Date'] = df['Exit Date'].fillna(end_date)

    # Now convert 'Exit Date' to datetime objects
    df['Exit Date'] = pd.to_datetime(df['Exit Date'])

     #Filter entries to ensure they entered date is before the end of date.
    df = df[df['Entry Date'] <= end_date]

    total_individual_nights = 0
    total_adult_nights = 0
    total_child_nights = 0
    total_records = 0

    # Use sets to track unique adults and children
    adults_served = set()
    children_served = set()

    for index, row in df.iterrows():
        total_records += 1

        arrival_date = row['Entry Date']
        departure_date = row['Exit Date']
        age = row['Age']
        full_name = row['Full Name'] # Use Full Name to track individuals

        # Clip the arrival date to the start date of the reporting period.
        arrival_date = max(arrival_date, start_date)

        # Ensure dates are within the reporting period (very important!)
        departure_date = min(departure_date, end_date)

        num_nights = (departure_date - arrival_date).days

        if num_nights < 0:
            print(f"Warning: Negative number of nights calculated for record {index}. Skipping.")
            continue

        if age >= 18:
            total_adult_nights += num_nights
            adults_served.add(full_name) # Add the full name to the set.
        else:
            total_child_nights += num_nights
            children_served.add(full_name) # Add the full name to the set.

        total_individual_nights += num_nights

    # Calculate the number of UNIQUE adults and children served
    total_adults_served = len(adults_served)
    total_children_served = len(children_served)

    # Print for verification and debugging
    print(f"Total records processed: {total_records}")
    print(f"Total possible bed nights: {total_possible_bed_nights}")
    print(f"Total Adult Nights: {total_adult_nights}")
    print(f"Total Child Nights: {total_child_nights}")
    print(f"Total Individual Nights: {total_individual_nights}")
    print(f"Total Adults Served: {total_adults_served}")
    print(f"Total Children Served: {total_children_served}")

    return total_individual_nights, total_possible_bed_nights, total_adult_nights, total_child_nights, total_adults_served, total_children_served, total_records


# Example usage
if __name__ == "__main__":
    individual_nights, possible_nights, adult_nights, child_nights, adults_served, children_served, record_count = calculate_rosalie_house_nights()
    print("\n--- Results ---")
    print(f"Total Individual Bed Nights (Jan 1 - Mar 31, 2025): {individual_nights}")
    print(f"Total Possible Bed Nights (Jan 1 - Mar 31, 2025): {possible_nights}")
    print(f"Total Bed Nights for Adults (Jan 1 - Mar 31, 2025): {adult_nights}")
    print(f"Total Bed Nights for Children (Jan 1 - Mar 31, 2025): {child_nights}")
    print(f"Total Adults Served: {adults_served}")
    print(f"Total Children Served: {children_served}")
    print(f"Total Records Processed: {record_count}")