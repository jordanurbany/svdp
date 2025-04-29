import pandas as pd
from datetime import datetime, timedelta

def analyze_marykrosalie_data(csv_file="MaryKRosalie.csv"):
    """
    Analyzes MaryKRosalie.csv data to extract information for 2024,
    categorizes by gender, adult/child status, calculates average stay
    for adults (maximum stay 90 days), categorizes ethnicity, and
    calculates age range percentages (0-18, 19-50 and 50+). Also,
    calculates the percentage of each ethnicity category.

    Args:
        csv_file (str): Path to the CSV file.  Defaults to "MaryKRosalie.csv".

    Returns:
        None. Prints results to the terminal.
    """

    try:
        df = pd.read_csv(csv_file)
        print("CSV file loaded successfully.")
    except FileNotFoundError:
        print(f"Error: File not found: {csv_file}")
        return

    # Data Cleaning and Preparation
    df.dropna(subset=["Entry Date", "Exit Date", "Age"], inplace=True)  # Include 'Age' in dropna

    # Convert "Entry Date" and "Exit Date" to datetime objects, handling errors
    df["Entry Date"] = pd.to_datetime(df["Entry Date"], errors='coerce')
    df["Exit Date"] = pd.to_datetime(df["Exit Date"], errors='coerce')

    # Drop rows where date conversion failed
    df.dropna(subset=["Entry Date", "Exit Date"], inplace=True)

    df['Age'] = pd.to_numeric(df['Age'], errors='coerce') #force numeric
    df.dropna(subset=["Entry Date", "Exit Date", "Age"], inplace=True) # Drop again after type conversion

    # Filter for 2024 data
    df_2024 = df[(df["Entry Date"].dt.year == 2024) | (df["Exit Date"].dt.year == 2024)]

    # Categorize adults and children based on Age
    df_2024["Category"] = df_2024["Age"].apply(lambda age: "adult" if age >= 18 else "child")

    # Separate by gender
    male_df = df_2024[df_2024["Gender"] == "Male"]
    female_df = df_2024[df_2024["Gender"] == "Female"]

    # Separate adults and children
    adult_df = df_2024[df_2024["Category"] == "adult"]
    child_df = df_2024[df_2024["Category"] == "child"]

    # Calculate average length of stay for adults
    if not adult_df.empty:
        adult_df.loc[:, "Length of Stay"] = (adult_df["Exit Date"] - adult_df["Entry Date"]).dt.days
        adult_df.loc[:, "Length of Stay"] = adult_df["Length of Stay"].clip(upper=90)  # Cap at 90 days
        avg_stay = adult_df["Length of Stay"].mean()
    else:
        avg_stay = None

   # DEBUGGING - Print counts and basic info
    print(f"\nTotal records in df_2024: {len(df_2024)}")
    print(f"Number of adults: {len(adult_df)}")
    print(f"Number of children: {len(child_df)}")
    print(f"Sum of adults and children: {len(adult_df) + len(child_df)}") #SHOULD match total
    print(f"Adult ages: \n{adult_df['Age'].describe()}") #Basic stats on adult ages
    print(f"Child ages: \n{child_df['Age'].describe()}") #Basic stats on child ages
    # Debug this to help with the results
    print(f"Total Record of age 0 to 18 with {df_2024[(df_2024['Age'] >= 0) & (df_2024['Age'] <= 18)]}")




    # Calculate age range counts using a single loop
    age_0_18_count = 0
    age_19_50_count = 0
    age_50_plus_count = 0

    for age in df_2024["Age"]:
        if 0 <= age <= 18:
            age_0_18_count += 1
        elif 19 <= age <= 50:
            age_19_50_count += 1
        elif age >= 50:
            age_50_plus_count += 1

    # Calculate age range percentages and use a more robust approach
    if len(df_2024) > 0:
        total_records_with_valid_age = len(df_2024)
        percent_0_18 = (age_0_18_count / total_records_with_valid_age) * 100
        percent_19_50 = (age_19_50_count / total_records_with_valid_age) * 100
        percent_50_plus = (age_50_plus_count / total_records_with_valid_age) * 100

    else:
        # Handle the edge case when df_2024 is empty
        percent_0_18 = 0.0
        percent_19_50 = 0.0
        percent_50_plus = 0.0

    print("Values are set, let's show results with new set values:")

    print(f"age_0_18_count = {age_0_18_count} ,Percent_0_18 {percent_0_18} , number people {total_records_with_valid_age}")


    # Categorize Ethnicity (incorporating Race)
    def categorize_ethnicity(ethnicity, race):
        if pd.notnull(race):
            race = str(race).lower()
            if "white" in race and "hispanic" not in race:
                return "White"
            elif "black" in race or "african american" in race or "african" in race:
                return "Black/African American"
            elif "asian" in race:
                return "Asian"
            elif "native american" in race or "alaskan native" in race:
                return "Native American/Indigenous"
            elif "hawaiian native" in race or "pacific islander" in race:
                return "Pacific Islander"
            elif "middle eastern" in race or "west african" in race or "north african" in race:
                return "Middle Eastern/North African"
            elif "multi-racial" in race or "two or more races" in race:
                return "Multi-Racial"
            elif "unknown" in race or "data not collected" in race:
                return "Unknown"
            elif "other" in race:
                return "Other"
        if pd.isnull(ethnicity):
            return "Unknown"
        ethnicity = str(ethnicity).lower()
        if "hispanic" in ethnicity or "puerto rican" in ethnicity or "honduran" in ethnicity or "guatemalan" in ethnicity or "salvadorean" in ethnicity or "peruvian" in ethnicity:
            return "Hispanic/Latino"
        elif "chinese" in ethnicity:
            return "Asian"
        elif "american indian" in ethnicity or "alaskan native" in ethnicity:
            return "Native American/Indigenous"
        elif "afghan" in ethnicity or "turkish" in ethnicity or "indian" in ethnicity:
            return "Asian"
        elif "samoan" in ethnicity:
            return "Pacific Islander"
        elif "american" in ethnicity:
            return "Other"
        else:
            return "Other"

    df_2024["Ethnicity Category"] = df_2024.apply(lambda row: categorize_ethnicity(row["Nationality/Race/Ethnicity"], row["Race"]), axis=1)

    # Print Results
    print("Analysis Results for 2024 Data:\n")

    print(f"Total Records in 2024: {len(df_2024)}")
    print(f"Number of Male Records: {len(male_df)}")
    print(f"Number of Female Records: {len(female_df)}")
    print(f"Number of Adult Records: {len(adult_df)}")
    print(f"Number of Child Records: {len(child_df)}\n")

    if avg_stay is not None:
        print(f"Average Length of Stay for Adults (capped at 90 days): {avg_stay:.2f} days\n")
    else:
        print("No adult records found to calculate average stay.\n")

    if percent_0_18 is not None and percent_19_50 is not None and percent_50_plus is not None:
        print(f"Percentage of individuals aged 0-18: {percent_0_18:.2f}%\n")
        print(f"Percentage of individuals aged 19-50: {percent_19_50:.2f}%\n")
        print(f"Percentage of individuals aged 50 and older: {percent_50_plus:.2f}%\n")
    else:
        print("Age range percentages could not be calculated (missing age data).\n")

    print("Ethnicity Categories:")
    ethnicity_counts = df_2024["Ethnicity Category"].value_counts()
    total_ethnicity_records = len(df_2024) #Total here

    for category, count in ethnicity_counts.items():
        percentage = (count / total_ethnicity_records) * 100 #Percent here
        print(f"- {category}: {percentage:.2f}%")

# Example Usage:
analyze_marykrosalie_data()