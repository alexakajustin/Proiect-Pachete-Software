import pandas as pd
excel_path = 'c:/Users/Justin/Desktop/Pachete Software/Data_Source/CDPR Data/key-financial-data-fy-2025.xlsx'
xl = pd.ExcelFile(excel_path)
print("Available years (sheets):", xl.sheet_names)
