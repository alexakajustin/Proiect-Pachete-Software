import pandas as pd
excel_path = 'c:/Users/Justin/Desktop/Pachete Software/Data_Source/CDPR Data/key-financial-data-fy-2025.xlsx'
xl = pd.ExcelFile(excel_path)
print("Sheet names:", xl.sheet_names)
if '2025' in xl.sheet_names:
    df = pd.read_excel(xl, sheet_name='2025')
    print("\nFirst 10 rows of 2025 sheet:")
    print(df.head(10))
