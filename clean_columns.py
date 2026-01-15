import pandas as pd

# Read the CSV file
df = pd.read_csv('latest_t_mapped.csv', encoding='utf-8')

print("Original columns:")
print(f"Total: {len(df.columns)} columns")
print(df.columns.tolist())

# Remove the specified columns
columns_to_remove = ['Month_No.', 'Unnamed: 16']
df_cleaned = df.drop(columns=columns_to_remove)

print(f"\n\nRemoving columns: {columns_to_remove}")
print(f"\nFinal columns:")
print(f"Total: {len(df_cleaned.columns)} columns")
print(df_cleaned.columns.tolist())

# Save the cleaned CSV
df_cleaned.to_csv('latest_t_mapped.csv', index=False, encoding='utf-8')
print(f"\n\nSaved cleaned CSV to latest_t_mapped.csv")
print(f"File size: {len(df_cleaned)} rows x {len(df_cleaned.columns)} columns")

# Verify the save
df_verify = pd.read_csv('latest_t_mapped.csv', encoding='utf-8')
print(f"\nVerification - Columns in updated file:")
for i, col in enumerate(df_verify.columns, 1):
    print(f"  {i:2d}. {col}")
