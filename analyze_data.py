import pandas as pd
import numpy as np

# อ่านข้อมูล
df = pd.read_excel('data/ckan_data.xlsx')

print("=" * 80)
print("=== การวิเคราะห์ข้อมูลเพื่อ Data Cleansing ===")
print("=" * 80)

print(f"\n1. ข้อมูลพื้นฐาน:")
print(f"   - Total rows: {len(df)}")
print(f"   - Total columns: {len(df.columns)}")
print(f"   - Columns: {list(df.columns)}")

print(f"\n2. Data Types:")
print(df.dtypes)

print(f"\n3. Missing Values (ค่าว่าง):")
missing = df.isnull().sum()
print(missing[missing > 0])
print(f"   Total missing cells: {df.isnull().sum().sum()}")

print(f"\n4. รายการ (Categories) ที่มี:")
print(f"   จำนวน: {df['รายการ'].nunique()} ประเภท")
for i, item in enumerate(df['รายการ'].unique(), 1):
    count = len(df[df['รายการ'] == item])
    print(f"   {i}. {item} ({count} rows)")

print(f"\n5. สวนสัตว์ที่มี:")
print(f"   จำนวน: {df['สวนสัตว์'].nunique()} แห่ง")
for i, zoo in enumerate(df['สวนสัตว์'].unique(), 1):
    count = len(df[df['สวนสัตว์'] == zoo])
    print(f"   {i}. {zoo} ({count} rows)")

print(f"\n6. ตัวอย่างข้อมูลตัวเลข (ต.ค. 67):")
sample = df['ต.ค. 67'].head(10)
print(sample)
print(f"   Type: {df['ต.ค. 67'].dtype}")
print(f"   มีข้อมูลที่เป็น string: {df['ต.ค. 67'].apply(lambda x: isinstance(x, str)).sum()} rows")

print("\n" + "=" * 80)
print("=== คำแนะนำการ Cleansing ===")
print("=" * 80)

recommendations = """
1. ✅ ลบคอลัมน์ _id (ไม่จำเป็น)
2. ✅ แปลงค่าตัวเลขที่มี comma (เช่น " 174,614 ") เป็น integer
3. ✅ ลบช่องว่างหน้า-หลังใน string values
4. ✅ แทนค่า "-" ด้วย 0 หรือ NaN
5. ✅ เปลี่ยนชื่อคอลัมน์เดือนให้สั้นกระชับ (เช่น "ต.ค. 67" → "oct_67")
6. ✅ แยกข้อมูลแต่ละสวนสัตว์ออกเป็นไฟล์ต่างหาก (ถ้าต้องการ)
7. ✅ สร้าง summary data (รวมตัวเลขแต่ละเดือน)
8. ✅ ลบแถวที่มีข้อมูลว่างเกือบทั้งหมด
"""
print(recommendations)

print("\n7. แถวที่มีข้อมูลว่างมาก (แนะนำให้ลบ):")
# นับว่าแต่ละแถวมีค่าว่างกี่คอลัมน์
null_counts = df.isnull().sum(axis=1)
problematic_rows = df[null_counts > 8]  # มากกว่า 8 คอลัมน์ว่าง
if len(problematic_rows) > 0:
    print(f"   พบ {len(problematic_rows)} แถวที่มีข้อมูลว่างมาก:")
    print(problematic_rows[['_id', 'รายการ', 'สวนสัตว์']])
else:
    print("   ไม่มีแถวที่มีข้อมูลว่างมากผิดปกติ")
