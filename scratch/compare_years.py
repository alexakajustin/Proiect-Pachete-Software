import pandas as pd
excel_path = 'c:/Users/Justin/Desktop/Pachete Software/Data_Source/CDPR Data/key-financial-data-fy-2025.xlsx'
xl = pd.ExcelFile(excel_path)
with open('c:/Users/Justin/Desktop/Pachete Software/scratch/compare_utf8.txt', 'w', encoding='utf-8') as f:
    for year in ['2017', '2020', '2025']:
        f.write(f"\n--- SCANNING YEAR {year} ---\n")
        df = pd.read_excel(xl, sheet_name=year)
        for i, row in df.iterrows():
            label = str(row.iloc[0]).lower()
            if 'asset' in label or 'equit' in label or 'liabilit' in label or 'aktywa' in label or 'kapita' in label or 'zobow' in label:
                val = "N/A"
                for col in range(1, min(6, df.shape[1])):
                    if pd.notna(row.iloc[col]) and isinstance(row.iloc[col], (int, float)):
                        val = row.iloc[col]
                        break
                f.write(f"Row {i}: {row.iloc[0]} | Value: {val}\n")
