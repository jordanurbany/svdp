import csv
import pandas as pd

def find_dcpr_in_ce(ce_file="CE.csv", dcpr_file="DCPR.csv"):
    """
    Finds DCPR unique identifiers within the CE.csv file.  Returns only
    rows from CE.csv where the Unique Identifier is also present in DCPR.csv

    Args:
        ce_file (str, optional): Path to the CE.csv file. Defaults to "CE.csv".
        dcpr_file (str, optional): Path to the DCPR.csv file. Defaults to "DCPR.csv".

    Returns:
        pandas.DataFrame: A DataFrame containing rows from CE.csv where the unique identifiers
                          are also found in DCPR.csv.
                          Returns None if there are errors reading the CSV files.
    """

    try:
        # **Skip header rows and read CE.csv into a Pandas DataFrame**
        # Determine number of rows to skip
        with open(ce_file, 'r') as f:
            reader = csv.reader(f)
            header_rows = 0
            for row in reader:
                if not row or all(not cell.strip() for cell in row):  # Check for empty rows
                    header_rows += 1
                elif 'Unique Identifier' in ','.join(row):  # Check for the header row
                    break
                else:
                    header_rows += 1

        ce_df = pd.read_csv(ce_file, skiprows=header_rows, low_memory=False)  #Added low_memory=False to suppress DtypeWarning


        # Rename the 'Unique Identifier' column in CE.csv to match DCPR.csv
        ce_df.rename(columns={'Unique Identifier': 'Unique Identifier'}, inplace=True) #Ensure the header name is corrected



        # Read DCPR.csv into a Pandas DataFrame
        dcpr_df = pd.read_csv(dcpr_file)

        # Rename the 'Unique Identifier' column in DCPR.csv to match CE.csv
        dcpr_df.rename(columns={'Unique\nIdentifier': 'Unique Identifier'}, inplace=True) #Ensure the header name is corrected


        # Strip whitespace from Unique Identifier column in both dataframes (CRUCIAL)
        ce_df['Unique Identifier'] = ce_df['Unique Identifier'].str.strip()
        dcpr_df['Unique Identifier'] = dcpr_df['Unique Identifier'].str.strip()

        # Create a set of Unique Identifiers from DCPR for efficient lookup
        dcpr_identifiers = set(dcpr_df['Unique Identifier'])


        # Filter CE.csv DataFrame to include only rows where the Unique Identifier
        # is present in the DCPR identifiers set
        ce_filtered_df = ce_df[ce_df['Unique Identifier'].isin(dcpr_identifiers)]

        return ce_filtered_df

    except FileNotFoundError:
        print("Error: One or both CSV files not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: One or both CSV files are empty.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def main():
    """
    Example usage: Calls the matching function and prints the resulting DataFrame.
    """
    ce_data_with_dcpr_ids = find_dcpr_in_ce()

    if ce_data_with_dcpr_ids is not None:
        print("CE Data with DCPR Identifiers:\n", ce_data_with_dcpr_ids)
        # Save the filtered data to a new CSV file:
        ce_data_with_dcpr_ids.to_csv("ce_data_with_dcpr_ids.csv", index=False)
        print("Filtered CE data saved to ce_data_with_dcpr_ids.csv")

if __name__ == "__main__":
    main()