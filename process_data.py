#!/usr/bin/env python3
"""
Automated Data Processing Pipeline for VOC Dashboard
Processes raw latest_t file and generates cleaned mapped CSV
"""
import pandas as pd
import os
import sys
from datetime import datetime

def load_store_mapping(mapping_file='STORE_LIST MAPPING.xlsx'):
    """Load store mapping from XLSX file"""
    try:
        xlsx_df = pd.read_excel(mapping_file, sheet_name='Sheet2')
        store_mapping = {}
        for idx, row in xlsx_df.iterrows():
            store_name = str(row.get('Store Name', '')).strip()
            if store_name:
                store_mapping[store_name] = {
                    'storeName': store_name,
                    'mallHS': str(row.get('Mall/HS', '')),
                    'state': str(row.get('State', '')),
                    'city': str(row.get('City', '')),
                    'tier': str(row.get('Tier', '')),
                    'zone': str(row.get('Zone', ''))
                }
        print(f"✓ Loaded {len(store_mapping)} store mappings")
        return store_mapping, xlsx_df
    except Exception as e:
        print(f"✗ Error loading store mapping: {e}")
        return {}, None

def fix_city_names(xlsx_df):
    """Fix common city name variations"""
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
    
    fixed_count = 0
    for wrong, correct in corrections.items():
        if 'City' in xlsx_df.columns:
            mask = xlsx_df['City'] == wrong
            if mask.any():
                xlsx_df.loc[mask, 'City'] = correct
                fixed_count += mask.sum()
    
    if fixed_count > 0:
        print(f"✓ Fixed {fixed_count} city name variations")
    return xlsx_df

def load_raw_data(input_file='latest_t.csv'):
    """Load raw data with multiple encoding attempts"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(input_file, encoding=encoding)
            print(f"✓ Loaded raw data from {input_file} (encoding: {encoding})")
            print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"  Error with {encoding}: {e}")
            continue
    
    raise Exception(f"Could not load {input_file} with any encoding")

def map_store_data(df, store_mapping):
    """Map store names and locations to the data"""
    print("\nMapping store data...")
    
    # Assume 'Store Name' column exists in the raw data
    if 'Store Name' not in df.columns:
        print("⚠ Warning: 'Store Name' column not found. Skipping mapping.")
        return df
    
    # Add mapped columns
    df['mallHS'] = df['Store Name'].map(lambda x: store_mapping.get(str(x).strip(), {}).get('mallHS', ''))
    df['state'] = df['Store Name'].map(lambda x: store_mapping.get(str(x).strip(), {}).get('state', ''))
    df['city'] = df['Store Name'].map(lambda x: store_mapping.get(str(x).strip(), {}).get('city', ''))
    df['tier'] = df['Store Name'].map(lambda x: store_mapping.get(str(x).strip(), {}).get('tier', ''))
    df['zone'] = df['Store Name'].map(lambda x: store_mapping.get(str(x).strip(), {}).get('zone', ''))
    
    print(f"✓ Mapped {len(df)} rows with store information")
    return df

def clean_columns(df):
    """Remove unnecessary columns"""
    columns_to_remove = ['Month_No.', 'Unnamed: 16']
    
    removed = []
    for col in columns_to_remove:
        if col in df.columns:
            df = df.drop(columns=[col])
            removed.append(col)
    
    if removed:
        print(f"✓ Removed columns: {removed}")
    
    return df

def process_data_pipeline():
    """Execute the complete data processing pipeline"""
    print("=" * 60)
    print("  VOC DASHBOARD - AUTOMATED DATA PROCESSING")
    print("=" * 60)
    print("")
    
    try:
        # Step 1: Load store mapping
        print("Step 1: Loading store mapping...")
        store_mapping, xlsx_df = load_store_mapping()
        
        # Step 2: Fix city names
        print("\nStep 2: Fixing city names...")
        xlsx_df = fix_city_names(xlsx_df)
        
        # Step 3: Load raw data
        print("\nStep 3: Loading raw data...")
        df = load_raw_data()
        
        # Step 4: Map store data
        print("\nStep 4: Mapping store data...")
        df = map_store_data(df, store_mapping)
        
        # Step 5: Clean columns
        print("\nStep 5: Cleaning columns...")
        df = clean_columns(df)
        
        # Step 6: Save outputs
        print("\nStep 6: Saving processed data...")
        
        # Save mapped version
        df.to_csv('latest_t_mapped.csv', index=False, encoding='utf-8')
        print(f"✓ Saved to latest_t_mapped.csv ({len(df)} rows)")
        
        # Save cleaned version
        df.to_csv('latest_t_mapped_clean.csv', index=False, encoding='utf-8')
        print(f"✓ Saved to latest_t_mapped_clean.csv ({len(df)} rows)")
        
        # Save XLSX mapping
        xlsx_df.to_excel('STORE_LIST MAPPING.xlsx', sheet_name='Sheet2', index=False)
        print(f"✓ Saved updated STORE_LIST MAPPING.xlsx")
        
        print("\n" + "=" * 60)
        print(f"  ✓✓✓ PROCESSING COMPLETE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print(f"\nSummary:")
        print(f"  - Processed {len(df)} rows")
        print(f"  - {len(df.columns)} columns in final output")
        print(f"  - Output files: latest_t_mapped.csv, latest_t_mapped_clean.csv")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"  ✗✗✗ ERROR - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = process_data_pipeline()
    sys.exit(0 if success else 1)
