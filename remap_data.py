import pandas as pd
import os

# Read files
latest_df = pd.read_csv('latest_t.csv', encoding='latin-1')
xlsx_df = pd.read_excel('STORE_LIST MAPPING.xlsx', sheet_name='Sheet2')

# Create mapping from XLSX using Store Name as key
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

print(f'Created mapping for {len(store_mapping)} stores from XLSX')

# Map the data
latest_df['State'] = ''
latest_df['City'] = ''
latest_df['Tier'] = ''
latest_df['Mall_HS_Mapped'] = ''

mapped_count = 0
for idx, row in latest_df.iterrows():
    store_code = str(row['Store Code']).strip()
    
    if store_code in store_mapping:
        mapping = store_mapping[store_code]
        latest_df.at[idx, 'State'] = mapping['state']
        latest_df.at[idx, 'City'] = mapping['city']
        latest_df.at[idx, 'Tier'] = mapping['tier']
        latest_df.at[idx, 'Mall_HS_Mapped'] = mapping['mallhs']
        mapped_count += 1

print(f'Mapped {mapped_count} records with State, City, Tier from XLSX')

# Save with UTF-8 encoding
latest_df.to_csv('latest_t_mapped.csv', index=False, encoding='utf-8')
print('Saved latest_t_mapped.csv with UTF-8 encoding')

print('\nSample output:')
print(latest_df[['Store Code', 'State', 'City', 'Tier', 'Zone']].head(10))
