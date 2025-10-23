import pandas as pd
import numpy as np
import re

print("=" * 80)
print("=== Data Cleansing Script ===")
print("=" * 80)

# 1. อ่านข้อมูล
print("\n[1/8] อ่านข้อมูลต้นฉบับ...")
df = pd.read_excel('data/ckan_data.xlsx')
print(f"   ✅ อ่านข้อมูลสำเร็จ: {len(df)} rows, {len(df.columns)} columns")

# 2. ลบคอลัมน์ _id
print("\n[2/8] ลบคอลัมน์ _id (ไม่จำเป็น)...")
df = df.drop(columns=['_id'])
print(f"   ✅ เหลือ {len(df.columns)} columns")

# 3. ทำความสะอาดข้อมูลตัวเลขในคอลัมน์เดือน
print("\n[3/8] แปลงค่าตัวเลขและทำความสะอาด...")
month_columns = ['ต.ค. 67', 'พ.ย. 67', 'ธ.ค. 67', 'ม.ค.68', 'ก.พ. 68', 
                 'มี.ค. 68', 'เม.ย. 68', 'พ.ค. 68', 'มิ.ย. 68', 
                 'ก.ค. 68', 'ส.ค. 68', 'ก.ย. 68']

def clean_number(value):
    """แปลงค่าที่มี comma และช่องว่างเป็นตัวเลข"""
    if pd.isna(value) or value == '-':
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    # ลบ comma และช่องว่าง
    cleaned = str(value).replace(',', '').replace(' ', '').strip()
    if cleaned == '' or cleaned == '-':
        return 0
    try:
        return int(float(cleaned))
    except:
        return 0

for col in month_columns:
    df[col] = df[col].apply(clean_number)
print(f"   ✅ แปลงข้อมูล {len(month_columns)} คอลัมน์เป็นตัวเลข")

# 4. ทำความสะอาดข้อมูล string (ลบช่องว่างหน้า-หลัง)
print("\n[4/8] ทำความสะอาดข้อมูล text...")
df['รายการ'] = df['รายการ'].str.strip()
df['สวนสัตว์'] = df['สวนสัตว์'].str.strip()
print("   ✅ ลบช่องว่างหน้า-หลังใน รายการ และ สวนสัตว์")

# 5. เปลี่ยนชื่อคอลัมน์ให้สั้นและเป็น English
print("\n[5/8] เปลี่ยนชื่อคอลัมน์...")
column_mapping = {
    'รายการ': 'category',
    'สวนสัตว์': 'zoo',
    'ปีงบประมาณ': 'fiscal_year',
    'ต.ค. 67': 'oct_67',
    'พ.ย. 67': 'nov_67',
    'ธ.ค. 67': 'dec_67',
    'ม.ค.68': 'jan_68',
    'ก.พ. 68': 'feb_68',
    'มี.ค. 68': 'mar_68',
    'เม.ย. 68': 'apr_68',
    'พ.ค. 68': 'may_68',
    'มิ.ย. 68': 'jun_68',
    'ก.ค. 68': 'jul_68',
    'ส.ค. 68': 'aug_68',
    'ก.ย. 68': 'sep_68'
}
df_clean = df.rename(columns=column_mapping)
print("   ✅ เปลี่ยนชื่อคอลัมน์เป็นภาษาอังกฤษ")

# 6. เพิ่มคอลัมน์ total (รวมทั้งปี)
print("\n[6/8] สร้างคอลัมน์ total...")
month_cols_clean = [col for col in df_clean.columns if col.endswith('_67') or col.endswith('_68')]
df_clean['total_visitors'] = df_clean[month_cols_clean].sum(axis=1)
print(f"   ✅ สร้างคอลัมน์ total_visitors (รวมจาก {len(month_cols_clean)} เดือน)")

# 7. จัดเรียงคอลัมน์
print("\n[7/8] จัดเรียงคอลัมน์...")
ordered_columns = ['zoo', 'category', 'fiscal_year'] + month_cols_clean + ['total_visitors']
df_clean = df_clean[ordered_columns]
print("   ✅ จัดเรียงคอลัมน์เรียบร้อย")

# 8. บันทึกข้อมูลที่ cleansing แล้ว
print("\n[8/8] บันทึกข้อมูล...")
# บันทึกเป็น CSV และ Excel
df_clean.to_csv('data/ckan_data_cleaned.csv', index=False, encoding='utf-8-sig')
df_clean.to_excel('data/ckan_data_cleaned.xlsx', index=False)
print("   ✅ บันทึกไฟล์:")
print("      - data/ckan_data_cleaned.csv")
print("      - data/ckan_data_cleaned.xlsx")

# แสดงสรุปข้อมูล
print("\n" + "=" * 80)
print("=== สรุปผลลัพธ์ ===")
print("=" * 80)
print(f"\n📊 ข้อมูลที่ cleansing แล้ว:")
print(f"   - จำนวนแถว: {len(df_clean)}")
print(f"   - จำนวนคอลัมน์: {len(df_clean.columns)}")
print(f"   - ค่าว่างทั้งหมด: {df_clean.isnull().sum().sum()}")

print(f"\n📝 รายการ (Categories) {df_clean['category'].nunique()} ประเภท:")
for cat in df_clean['category'].unique():
    total = df_clean[df_clean['category'] == cat]['total_visitors'].sum()
    print(f"   - {cat}: {total:,} คน")

print(f"\n🦁 สวนสัตว์ {df_clean['zoo'].nunique()} แห่ง:")
for zoo in df_clean['zoo'].unique():
    total = df_clean[df_clean['zoo'] == zoo]['total_visitors'].sum()
    print(f"   - {zoo}: {total:,} คน")

print(f"\n🎯 ผู้เข้าชมรวมทั้งหมด: {df_clean['total_visitors'].sum():,} คน")

print("\n" + "=" * 80)
print("=== ตัวอย่างข้อมูลที่ cleansing แล้ว (5 แถวแรก) ===")
print("=" * 80)
print(df_clean.head().to_string())

print("\n✅ Data Cleansing เสร็จสิ้น!")
