import csv
from collections import Counter

def analyze_violence_from_csv(csv_filename, all_violence_types):
    """
    Analyzes a CSV file to count occurrences of different violence types in the "History of Violence" column.

    Args:
        csv_filename: The path to the CSV file.
        all_violence_types: A list of all possible violence types to count.

    Returns:
        A Counter object with the counts of each violence type, and the total count of all violence instances.
    """
    violence_counts = Counter()
    total_violence_count = 0

    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            history_of_violence = row.get('History of Violence', '')  # Safely get the value

            if history_of_violence:
                violence_types = [vt.strip() for vt in history_of_violence.split(';') if vt.strip()]  # Clean and split.

                for violence_type in violence_types:
                    if violence_type in all_violence_types:
                        violence_counts[violence_type] += 1
                        total_violence_count += 1

    return violence_counts, total_violence_count


def main():
    # Define all possible violence types
    all_violence_types = [
        "Physical Violence", "Physical Abuse", "Emotional Abuse", "Other/Unknown", "Sexual Assault",
        "Neglect", "Witnessed Violence", "Elder Abuse", "Trafficked"
    ]

    csv_filenames = ["RHHistoryOfViolence.csv", "BHHistoryOfViolence.csv"]  # List of CSV filenames

    for csv_filename in csv_filenames:
        analysis_results, total_count = analyze_violence_from_csv(csv_filename, all_violence_types)

        print(f"\nAnalysis Results for {csv_filename}:")
        for violence_type, count in analysis_results.items():
            print(f"{violence_type}: {count}")

        print(f"Total Violence Count for {csv_filename}: {total_count}")


if __name__ == "__main__":
    main()