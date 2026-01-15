import pandas as pd

# Read the XLSX file
xlsx_file = 'STORE_LIST MAPPING.xlsx'
xlsx_df = pd.read_excel(xlsx_file, sheet_name='Sheet2')

# Define corrections
corrections = {
    'Bangaluru': 'Bengaluru',
    'BERHAMPUR': 'Berhampur',
    'BHILWARA': 'Bhilwara',
    'Calicut': 'Kozhikode',
    'Belgaum': 'Belagavi',
    'Bellary': 'Ballari',
    'JAIPUR': 'Jaipur',
    'JHARSUGUDA': 'Jharsuguda',
    'MALAPPURAM ': 'Malappuram',
    'Palakkad ': 'Palakkad',
    'PORVORIM': 'Porvorim',
    'ROURKRLA': 'Rourkela',
    'TIRUPATI': 'Tirupati',
    'Nasik': 'Nashik',
    'Shivmogga': 'Shivamogga',
    'Thanjauvar': 'Thanjavur',
    'Trissur': 'Thrissur',
    'Trivandrum': 'Thiruvananthapuram',
    'Trichy': 'Tiruchirappalli',
}

# Apply corrections to City column
for wrong, correct in corrections.items():
    mask = xlsx_df['City'] == wrong
    if mask.any():
        xlsx_df.loc[mask, 'City'] = correct
        print(f"Fixed {mask.sum()} rows: {wrong} -> {correct}")

# Save the corrected XLSX
xlsx_df.to_excel(xlsx_file, sheet_name='Sheet2', index=False)
print(f"\nSaved corrected XLSX to {xlsx_file}")

# Now regenerate the mapped CSV
latest_df = pd.read_csv('latest_t.csv', encoding='latin-1')

store_mapping = {}
for idx, row in xlsx_df.iterrows():
    store_name = str(row.get('Store Name', '')).strip()
    if store_name:
        store_mapping[store_name] = {
            'state': str(row.get('State', '')),
            'city': str(row.get('City', '')),
            'tier': str(row.get('Tier', '')),
            'zone': str(row.get('Zone', '')),
            'mallhs': str(row.get('Mall/HS', ''))
        }

latest_df['State'] = ''
latest_df['City'] = ''
latest_df['Tier'] = ''
latest_df['Mall_HS_Mapped'] = ''

for idx, row in latest_df.iterrows():
    store_code = str(row['Store Code']).strip()
    if store_code in store_mapping:
        mapping = store_mapping[store_code]
        latest_df.at[idx, 'State'] = mapping['state']
        latest_df.at[idx, 'City'] = mapping['city']
        latest_df.at[idx, 'Tier'] = mapping['tier']
        latest_df.at[idx, 'Mall_HS_Mapped'] = mapping['mallhs']

latest_df.to_csv('latest_t_mapped.csv', index=False, encoding='utf-8')
print(f"Regenerated latest_t_mapped.csv with corrected city spellings")
