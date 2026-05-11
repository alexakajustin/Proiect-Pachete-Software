import pandas as pd
excel_path = 'c:/Users/Justin/Desktop/Pachete Software/Data_Source/CDPR Data/key-financial-data-fy-2025.xlsx'
xl = pd.ExcelFile(excel_path)
df = pd.read_excel(xl, sheet_name='2024')
with open('c:/Users/Justin/Desktop/Pachete Software/scratch/scan_2024.txt', 'w', encoding='utf-8') as f:
    for i, row in df.iterrows():
        label = str(row.iloc[0])
        if len(label) > 3:
            f.write(f"Row {i}: {label}\n")
