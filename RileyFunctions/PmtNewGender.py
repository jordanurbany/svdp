import pandas as pd

def analyze_gender_by_house(file="PmtNewGender.csv"):
    """
    Analyzes gender distribution for Brennen and Riley Houses from a CSV file.

    Args:
        file (str): The path to the CSV file containing the enrollment data.
                      It MUST have "Bed Assignment Name" and "Gender" columns.

    Returns:
        None. Prints the analysis results to the console.
    """

    try:
        df = pd.read_csv(file)
        df = df.dropna(how='all') # Remove rows that are completely empty

        # --- Analyze All Data ---
        print("--- All Data ---")
        total = len(df)
        print(f"Total: {total}")

        # Gender Analysis
        print("\nGender:")
        for k, v in df['Gender'].value_counts().items(): print(f"{k}: {v}")

        # --- Brennen House Gender Analysis ---
        print("\n--- Brennen House ---")
        brennen_df = df[df['Bed Assignment Name'].astype(str).str.upper().str.contains("BH")]
        brennen_total = len(brennen_df)
        print(f"Total: {brennen_total}")

        print("\nGender:")
        for k, v in brennen_df['Gender'].value_counts().items(): print(f"{k}: {v}")

        # --- Riley House Gender Analysis ---
        print("\n--- Riley House ---")
        riley_df = df[df['Bed Assignment Name'].astype(str).str.upper().str.contains("RH")]
        riley_total = len(riley_df)
        print(f"Total: {riley_total}")

        print("\nGender:")
        for k, v in riley_df['Gender'].value_counts().items(): print(f"{k}: {v}")

    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_gender_by_house()