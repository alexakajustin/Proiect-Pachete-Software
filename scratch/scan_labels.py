import pandas as pd
excel_path = 'c:/Users/Justin/Desktop/Pachete Software/Data_Source/CDPR Data/key-financial-data-fy-2025.xlsx'
xl = pd.ExcelFile(excel_path)
df = pd.read_excel(xl, sheet_name='2025')
with open('c:/Users/Justin/Desktop/Pachete Software/scratch/labels_utf8.txt', 'w', encoding='utf-8') as f:
    f.write("--- ALL LABELS IN 2025 SHEET ---\n")
    for i, row in df.iterrows():
        label = str(row.iloc[0])
        if len(label) > 3:
            val = "N/A"
            for col in range(1, min(6, df.shape[1])):
                if pd.notna(row.iloc[col]) and isinstance(row.iloc[col], (int, float)):
                    val = row.iloc[col]
                    break
            f.write(f"Row {i}: {label} | Value: {val}\n")
