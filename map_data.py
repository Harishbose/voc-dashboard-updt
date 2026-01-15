import pandas as pd
import re
import json
import openpyxl

# Read the CSV file - try different encodings
try:
    df = pd.read_csv('latest_t.csv', encoding='utf-8')
except UnicodeDecodeError:
    try:
        df = pd.read_csv('latest_t.csv', encoding='latin-1')
    except:
        df = pd.read_csv('latest_t.csv', encoding='cp1252')

# Read the XLSX file for detailed mapping
try:
    xlsx_df = pd.read_excel('STORE_LIST MAPPING.xlsx', sheet_name='Sheet2')
    # Create a mapping dictionary from XLSX using Store Name as key
    store_mapping_xlsx = {}
    for idx, row in xlsx_df.iterrows():
        store_name = row.get('Store Name', '').strip() if row.get('Store Name') else ''
        if store_name:
            store_mapping_xlsx[store_name] = {
                'storeName': store_name,
                'mallHS': row.get('Mall/HS', ''),
                'state': row.get('State', ''),
                'city': row.get('City', ''),
                'tier': row.get('Tier', ''),
                'zone': row.get('Zone', '')
            }
    print(f"Loaded {len(store_mapping_xlsx)} store mappings from XLSX")
except Exception as e:
    print(f"Could not read XLSX file: {e}")
    store_mapping_xlsx = {}

# Extract the mapping from the JavaScript file (fallback)
with open('store_mapping_complete.js', 'r') as f:
    content = f.read()

# Parse the JavaScript object manually
store_mapping_js = {}
entries = re.findall(r"'([A-Z0-9]+)':\s*{\s*storeName:\s*'([^']*)',\s*mallHS:\s*'([^']*)',\s*state:\s*'([^']*)'\s*}", content)
for store_code, name, mall_hs, state in entries:
    store_mapping_js[store_code] = {
        'storeName': name,
        'mallHS': mall_hs,
        'state': state
    }

print(f"Loaded {len(store_mapping_js)} store mappings from JS")

# City mapping based on state (for fallback)
city_tier_mapping = {
    'Delhi': {'city': 'Delhi', 'tier': 'Tier 1'},
    'Maharashtra': {'city': 'Maharashtra', 'tier': 'Tier 1'},
    'Karnataka': {'city': 'Karnataka', 'tier': 'Tier 1'},
    'Tamil Nadu': {'city': 'Tamil Nadu', 'tier': 'Tier 1'},
    'Telangana': {'city': 'Telangana', 'tier': 'Tier 1'},
    'West Bengal': {'city': 'West Bengal', 'tier': 'Tier 1'},
    'Punjab': {'city': 'Punjab', 'tier': 'Tier 2'},
    'Haryana': {'city': 'Haryana', 'tier': 'Tier 2'},
    'Rajasthan': {'city': 'Rajasthan', 'tier': 'Tier 2'},
    'Uttar Pradesh': {'city': 'Uttar Pradesh', 'tier': 'Tier 2'},
    'Madhya Pradesh': {'city': 'Madhya Pradesh', 'tier': 'Tier 2'},
    'Gujarat': {'city': 'Gujarat', 'tier': 'Tier 2'},
    'Odisha': {'city': 'Odisha', 'tier': 'Tier 2'},
    'Assam': {'city': 'Assam', 'tier': 'Tier 3'},
    'Chandigarh': {'city': 'Chandigarh', 'tier': 'Tier 2'},
    'Chhattisgarh': {'city': 'Chhattisgarh', 'tier': 'Tier 3'},
    'Jharkhand': {'city': 'Jharkhand', 'tier': 'Tier 3'},
    'Kerala': {'city': 'Kerala', 'tier': 'Tier 2'},
    'Uttarakhand': {'city': 'Uttarakhand', 'tier': 'Tier 3'},
    'Andhra Pradesh': {'city': 'Andhra Pradesh', 'tier': 'Tier 2'},
    'Goa': {'city': 'Goa', 'tier': 'Tier 2'},
    'Sikkim': {'city': 'Sikkim', 'tier': 'Tier 3'},
    'Meghalaya': {'city': 'Meghalaya', 'tier': 'Tier 3'},
    'Nagaland': {'city': 'Nagaland', 'tier': 'Tier 3'},
    'Manipur': {'city': 'Manipur', 'tier': 'Tier 3'},
    'Tripura': {'city': 'Tripura', 'tier': 'Tier 3'},
    'Jammu And Kashmir': {'city': 'Jammu And Kashmir', 'tier': 'Tier 3'},
    'Arunachal Pradesh': {'city': 'Arunachal Pradesh', 'tier': 'Tier 3'},
    'Puducherry': {'city': 'Puducherry', 'tier': 'Tier 2'},
    'Bihar': {'city': 'Bihar', 'tier': 'Tier 3'}
}

# Add new columns to the dataframe
df['City'] = ''
df['State'] = ''
df['Tier'] = ''
df['Store_Code'] = ''
df['Mall_HS_Mapped'] = ''

# Map the data - prioritize XLSX data over JS data
mapped_count = 0
for idx, row in df.iterrows():
    store_code = row['Store Code']
    
    # Try XLSX first
    if store_code in store_mapping_xlsx:
        mapping = store_mapping_xlsx[store_code]
        state = mapping.get('state', '')
        city = mapping.get('city', '')
        tier = mapping.get('tier', '')
        mall_hs = mapping.get('mallHS', '')
        
        df.at[idx, 'Store_Code'] = store_code
        df.at[idx, 'State'] = state
        df.at[idx, 'City'] = city
        df.at[idx, 'Tier'] = tier
        df.at[idx, 'Mall_HS_Mapped'] = mall_hs if mall_hs else ''
        mapped_count += 1
    # Fallback to JS mapping
    elif store_code in store_mapping_js:
        mapping = store_mapping_js[store_code]
        state = mapping['state']
        mall_hs = mapping['mallHS']
        
        df.at[idx, 'Store_Code'] = store_code
        df.at[idx, 'State'] = state
        df.at[idx, 'Mall_HS_Mapped'] = mall_hs if mall_hs else ''
        
        # Get city and tier info from fallback mapping
        if state in city_tier_mapping:
            city_info = city_tier_mapping[state]
            df.at[idx, 'City'] = city_info['city']
            df.at[idx, 'Tier'] = city_info['tier']
        mapped_count += 1
    else:
        df.at[idx, 'Store_Code'] = store_code
        df.at[idx, 'State'] = ''
        df.at[idx, 'City'] = ''
        df.at[idx, 'Tier'] = ''
        df.at[idx, 'Mall_HS_Mapped'] = ''

# Reorder columns to put the new columns after Store Code
columns = list(df.columns)
if 'City' in columns:
    columns.remove('City')
if 'State' in columns:
    columns.remove('State')
if 'Tier' in columns:
    columns.remove('Tier')
if 'Store_Code' in columns:
    columns.remove('Store_Code')
if 'Mall_HS_Mapped' in columns:
    columns.remove('Mall_HS_Mapped')

# Insert the new columns after Store Code
store_code_idx = columns.index('Store Code') if 'Store Code' in columns else 0
new_order = columns[:store_code_idx+1] + ['Store_Code', 'City', 'State', 'Tier', 'Mall_HS_Mapped'] + columns[store_code_idx+1:]
df = df[new_order]

# Save to CSV
df.to_csv('latest_t_mapped.csv', index=False)

print(f"\nMapping complete! File saved as 'latest_t_mapped.csv'")
print(f"Total records: {len(df)}")
print(f"Mapped records: {mapped_count}")
print(f"Unmapped records: {len(df) - mapped_count}")
print("\nSample of mapped data:")
print(df[['Store Code', 'Store_Code', 'City', 'State', 'Tier', 'Mall_HS_Mapped']].head(10))

