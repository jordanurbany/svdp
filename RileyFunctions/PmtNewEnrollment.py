import pandas as pd

def analyze_enrollment(file="PmtNewEnrollment.csv"):
    try:
        df = pd.read_csv(file)
        df = df.dropna(how='all')

        # --- Analyze All Data ---
        print("--- All Data ---")
        num_rows_before = len(df)
        print(f"Number of rows before handling missing data: {num_rows_before}")
        num_rows_after = len(df)
        print(f"Number of rows *AFTER* dropping rows with all NaN values: {num_rows_after}")
        total = len(df)
        print(f"Total: {total}")
        print("\nEthnicity:")
        for k, v in df['Ethnicity'].value_counts().items(): print(f"{k}: {v}")
        age_groups = {"0-12": 0, "13-17": 0, "18-24": 0, "25-59": 0, "60+": 0}
        for age in df['Age']:
            if 0 <= age <= 12: age_groups["0-12"] += 1
            elif 13 <= age <= 17: age_groups["13-17"] += 1
            elif 18 <= age <= 24: age_groups["18-24"] += 1
            elif 25 <= age <= 59: age_groups["25-59"] += 1
            else: age_groups["60+"] += 1
        print("\nAges:")
        for k, v in age_groups.items(): print(f"{k}: {v}")

        brennen_total = 0
        riley_total = 0
        for bed in df['Bed Assignment Name']:
            bed_upper = str(bed).upper()
            if "BH" in bed_upper:
                brennen_total += 1
            elif "RH" in bed_upper:
                riley_total += 1
        print("\nPrograms:")
        print(f"Brennen: {brennen_total}")
        print(f"Riley: {riley_total}")

        # --- Analyze Riley House Data ---
        print("\n--- Riley House ---")
        riley_df = df[df['Bed Assignment Name'].astype(str).str.upper().str.contains("RH")]
        riley_total = len(riley_df)
        print(f"Total: {riley_total}")
        print("\nEthnicity:")
        for k, v in riley_df['Ethnicity'].value_counts().items(): print(f"{k}: {v}")
        riley_age_groups = {"0-12": 0, "13-17": 0, "18-24": 0, "25-59": 0, "60+": 0}
        for age in riley_df['Age']:
            if 0 <= age <= 12: riley_age_groups["0-12"] += 1
            elif 13 <= age <= 17: riley_age_groups["13-17"] += 1
            elif 18 <= age <= 24: riley_age_groups["18-24"] += 1
            elif 25 <= age <= 59: riley_age_groups["25-59"] += 1
            else: riley_age_groups["60+"] += 1
        print("\nAges:")
        for k, v in riley_age_groups.items(): print(f"{k}: {v}")
        print("\nPrograms:") # Program analysis will always show Riley for this subset.
        print(f"Riley: {len(riley_df)}")

        # --- Analyze Brennen House Data ---
        print("\n--- Brennen House ---")
        brennen_df = df[df['Bed Assignment Name'].astype(str).str.upper().str.contains("BH")]
        brennen_total = len(brennen_df)
        print(f"Total: {brennen_total}")
        print("\nEthnicity:")
        for k, v in brennen_df['Ethnicity'].value_counts().items(): print(f"{k}: {v}")
        brennen_age_groups = {"0-12": 0, "13-17": 0, "18-24": 0, "25-59": 0, "60+": 0}
        for age in brennen_df['Age']:
            if 0 <= age <= 12: brennen_age_groups["0-12"] += 1
            elif 13 <= age <= 17: brennen_age_groups["13-17"] += 1
            elif 18 <= age <= 24: brennen_age_groups["18-24"] += 1
            elif 25 <= age <= 59: brennen_age_groups["25-59"] += 1
            else: brennen_age_groups["60+"] += 1
        print("\nAges:")
        for k, v in brennen_age_groups.items(): print(f"{k}: {v}")
        print("\nPrograms:") # Program analysis will always show Brennen for this subset.
        print(f"Brennen: {len(brennen_df)}")

    except FileNotFoundError:
        print(f"Error: '{file}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_enrollment()