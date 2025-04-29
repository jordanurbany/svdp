import pandas as pd

# Load the CSV
file_path = "MaryKBren.csv"
try:
    df = pd.read_csv(file_path)
    print("CSV file loaded successfully.")
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit()

# Filter 2024 data
df_2024 = df.copy()
print(f"Total records in df_2024: {len(df_2024)}")

# Classify Age Category
df_2024['Age Category'] = df_2024['Age'].apply(lambda x: 'child' if x < 18 else 'adult')

# Split adults and children
adults = df_2024[df_2024['Age Category'] == 'adult']
children = df_2024[df_2024['Age Category'] == 'child']

print(f"Number of adults: {len(adults)}")
print(f"Number of children: {len(children)}")
print(f"Sum of adults and children: {len(adults) + len(children)}")

# Display age statistics
print("Adult ages: \n", adults["Age"].describe())
print("Child ages:\n", children["Age"].describe())

# Show records of children
print("Total Record of age 0 to 18 with", children[["Bed: Bed Number", "Full Name", "Race", "Age Category"]])

# Normalize gender values
df_2024['Gender'] = df_2024['Gender'].astype(str).str.strip().str.lower()

# Gender counts
num_males = len(df_2024[df_2024['Gender'] == 'male'])
num_females = len(df_2024[df_2024['Gender'] == 'female'])

# Show results
print("Values are set, let's show results with new set values:")
age_0_18_count = len(children)
percent_0_18 = (age_0_18_count / len(df_2024)) * 100
print(f"age_0_18_count = {age_0_18_count} ,Percent_0_18 {percent_0_18} , number people {len(df_2024)}")

# Stay calculation (capped at 12 months)
if 'Entry Date' in df_2024.columns and 'Exit Date' in df_2024.columns:
    df_2024['Entry Date'] = pd.to_datetime(df_2024['Entry Date'], errors='coerce')
    df_2024['Exit Date'] = pd.to_datetime(df_2024['Exit Date'], errors='coerce')
    df_2024['Length of Stay'] = (df_2024['Exit Date'] - df_2024['Entry Date']).dt.days
    df_2024['Length of Stay'] = df_2024['Length of Stay'].clip(upper=360)  # cap at 12 months (360 days)
    avg_stay_adults = df_2024[df_2024['Age Category'] == 'adult']['Length of Stay'].mean()
else:
    avg_stay_adults = "Not available"

# Age brackets
age_0_18 = len(df_2024[df_2024["Age"] <= 18])
age_19_50 = len(df_2024[(df_2024["Age"] > 18) & (df_2024["Age"] <= 50)])
age_51_up = len(df_2024[df_2024["Age"] > 50])

# Percentages
total_people = len(df_2024)
pct_0_18 = round((age_0_18 / total_people) * 100, 2)
pct_19_50 = round((age_19_50 / total_people) * 100, 2)
pct_51_up = round((age_51_up / total_people) * 100, 2)

# Ethnicity breakdown
ethnicity_counts = df_2024['Race'].value_counts(normalize=True) * 100

# Final Report
print("\nAnalysis Results for 2024 Data:\n")
print(f"Total Records in 2024: {total_people}")
print(f"Number of Male Records: {num_males}")
print(f"Number of Female Records: {num_females}")
print(f"Number of Adult Records: {len(adults)}")
print(f"Number of Child Records: {len(children)}\n")
print(f"Average Length of Stay for Adults (capped at 12 months): {round(avg_stay_adults, 2) if isinstance(avg_stay_adults, float) else avg_stay_adults} days\n")

print(f"Percentage of individuals aged 0-18: {pct_0_18}%")
print(f"Percentage of individuals aged 19-50: {pct_19_50}%")
print(f"Percentage of individuals aged 50 and older: {pct_51_up}%\n")

print("Ethnicity Categories:")
for race, pct in ethnicity_counts.items():
    print(f"- {race}: {round(pct, 2)}%")
