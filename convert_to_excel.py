import pandas as pd

# อ่านไฟล์ CSV ด้วย UTF-8-SIG encoding
csv_file = r'.\data\ckan_data.csv'
excel_file = r'.\data\ckan_data.xlsx'

print(f"Reading CSV file: {csv_file}")
df = pd.read_csv(csv_file, encoding='utf-8-sig')

print(f"Total rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

# บันทึกเป็น Excel
print(f"\nSaving to Excel: {excel_file}")
df.to_excel(excel_file, index=False, engine='openpyxl')

print("\n✅ Success! Excel file created with proper Thai encoding.")
print(f"Open '{excel_file}' to see Thai text correctly displayed.")
