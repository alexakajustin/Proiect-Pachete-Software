import pandas as pd
import numpy as np
import os

def clean_financials():
    excel_path = 'CDPR Data/key-financial-data-fy-2025.xlsx'
    xl = pd.ExcelFile(excel_path)
    
    # We want to extract data from yearly sheets
    years = [str(y) for y in range(2017, 2026)]
    data_list = []
    
    for year in years:
        if year not in xl.sheet_names:
            continue
            
        df = pd.read_excel(xl, sheet_name=year)
        
        # Search for metrics in the first column
        # Standardizing row labels
        labels = {
            'Revenue': ['Sales revenue', 'Sales revenues'],
            'OperatingProfit': ['Operating profit'],
            'NetProfit': ['Net profit', 'Net profit (loss)'],
            'MarketingCosts': ['Selling expenses', 'Selling costs'],
            'Assets': ['TOTAL ASSETS'],
            'Equity': ['TOTAL EQUITY', 'Equity attributable to shareholders', 'Equity attributable to equity holders']
        }
        
        row_data = {'Year': int(year)}
        
        for key, possible_labels in labels.items():
            found = False
            for label in possible_labels:
                mask = df.iloc[:, 0].astype(str).str.contains(label, case=False, na=False)
                if mask.any():
                    idx = df[mask].index[0]
                    # The value is usually in the subsequent columns.
                    for col_idx in range(1, df.shape[1]):
                        val = df.iloc[idx, col_idx]
                        try:
                            # Try converting to float
                            num_val = float(val)
                            if not pd.isna(num_val) and num_val != 0:
                                row_data[key] = num_val
                                found = True
                                break
                        except (ValueError, TypeError):
                            continue
                if found: break
            if not found:
                row_data[key] = np.nan
        
        data_list.append(row_data)
        print(f"Processed year {year}")

    final_df = pd.DataFrame(data_list)
    
    # Fill in some missing data manually if needed (based on official reports)
    # CDPR Revenue 2025 was approx 866M PLN, Net Profit 470M PLN
    # Adding Geographic Sales (Percentages from IR 2025)
    # These will be used for the Geopandas map
    final_df['North_America_Pct'] = 0.755
    final_df['Europe_Pct'] = 0.115
    final_df['Asia_Pct'] = 0.093
    final_df['Poland_Pct'] = 0.033
    final_df['Other_Pct'] = 0.004
    
    # Export to CSV
    final_df.to_csv('cdpr_cleaned.csv', index=False)
    print("Exported to cdpr_cleaned.csv")

if __name__ == "__main__":
    clean_financials()
