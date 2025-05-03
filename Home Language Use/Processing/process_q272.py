import pandas as pd
from mapping import country_dict, language_dict  # Import the mappings

# Load the WVS Wave 7 dataset
df = pd.read_csv("../WVS_Cross-National_Wave_7_csv_v6_0.csv", low_memory=False)

# Keep only the columns we care about
df = df[['B_COUNTRY', 'Q272']]

# Filter out invalid or missing language codes
df = df[df['Q272'] > 0]

# Count how many people in each country speak each language
language_counts = df.groupby(['B_COUNTRY', 'Q272']).size().reset_index(name='count')

# Count how many people were surveyed in each country
country_totals = df.groupby('B_COUNTRY').size().reset_index(name='total')

# Merge the counts and totals, then calculate percentages
merged = language_counts.merge(country_totals, on='B_COUNTRY')
merged['percent'] = (merged['count'] / merged['total']) * 100

# Convert numeric codes to readable names
merged['country'] = merged['B_COUNTRY'].map(country_dict)
merged['language'] = merged['Q272'].map(language_dict)

# Check for any missing language codes in the dictionary and label them
missing_codes = df.loc[~df['Q272'].isin(language_dict.keys()), 'Q272'].unique()
if len(missing_codes) > 0:
    print("Missing language codes:", missing_codes)
merged['language'] = merged['language'].fillna("Unlisted Language")

# Save final data to CSV
merged[['country', 'language', 'count', 'percent']].to_csv("spoken_languages_by_country.csv", index=False)

print("Done! File saved as 'spoken_languages_by_country.csv'")
