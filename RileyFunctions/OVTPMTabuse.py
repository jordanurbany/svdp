import pandas as pd
from collections import Counter

def analyze_violence_from_csv(csv_filename):
    """
    Analyzes a CSV file (OVTPMT.csv) to count occurrences of different violence types
    in the "History of Violence" column.

    Args:
        csv_filename (str): The path to the CSV file.

    Returns:
        tuple: A tuple containing:
            - A Counter object with the counts of each violence type.
            - The total count of all violence instances.
    """

    # Define all possible violence types
    all_violence_types = [
        "Physical Violence", "Physical Abuse", "Emotional Abuse", "Other/Unknown", "Sexual Assault",
        "Neglect", "Witnessed Violence", "Elder Abuse", "Trafficked"
    ]

    violence_counts = Counter()
    total_violence_count = 0

    try:
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        print(f"Error: File '{csv_filename}' not found.")
        return violence_counts, total_violence_count  # Return empty results
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return violence_counts, total_violence_count

    for history_of_violence in df['History of Violence'].astype(str): #Iterate the rows and use str to catch problems
        if history_of_violence:
            violence_types = [vt.strip() for vt in history_of_violence.split(';') if vt.strip()]  # Clean and split.

            for violence_type in violence_types:
                if violence_type in all_violence_types:
                    violence_counts[violence_type] += 1
                    total_violence_count += 1

    return violence_counts, total_violence_count


def main():
    csv_filename = "OVTPMTabuse.csv"  # List of CSV filenames
    analysis_results, total_count = analyze_violence_from_csv(csv_filename)

    print(f"\nAnalysis Results for {csv_filename}:")
    for violence_type, count in analysis_results.items():
        print(f"{violence_type}: {count}")

    print(f"Total Violence Count for {csv_filename}: {total_count}")


if __name__ == "__main__":
    main()