import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import RobustScaler
import os

def extract_results():
    base_path = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base_path, "..", "Data_Source", "cdpr_cleaned.csv"))
    
    output_file = os.path.join(base_path, "..", "Documentatie", "rezultate_analiza.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=== REZULTATE REALE PROIECT CDPR (2010-2025) ===\n\n")
        
        # 1. Regresie Multipla (OLS) - Curatam NaN
        cols_ols = ['NetProfit', 'Revenue', 'AdminExpenses']
        df_ols = df[cols_ols].dropna()
        
        X_ols = sm.add_constant(df_ols[['Revenue', 'AdminExpenses']])
        y_ols = df_ols['NetProfit']
        model_ols = sm.OLS(y_ols, X_ols).fit()
        
        f.write("1. REGRESIE MULTIPLA (Impact asupra Profitului):\n")
        f.write(f"   - Coeficient de determinare (R-squared): {model_ols.rsquared:.4f}\n")
        f.write(f"   - Coeficient Revenue (Impact vanzari): {model_ols.params['Revenue']:.4f}\n")
        f.write(f"   - P-value Revenue: {model_ols.pvalues['Revenue']:.4e} (Semnificativ daca < 0.05)\n")
        f.write(f"   - Interpretare: Modelul explica {model_ols.rsquared*100:.1f}% din variatia profitului.\n\n")
        
        # 2. Regresie Logistica
        df_log = df[['NetProfit', 'MarketingCosts', 'Assets']].dropna()
        df_log['HighProfit'] = (df_log['NetProfit'] > df_log['NetProfit'].median()).astype(int)
        
        X_log = df_log[['MarketingCosts', 'Assets']]
        scaler = RobustScaler()
        X_log_scaled = scaler.fit_transform(X_log)
        
        model_log = LogisticRegression()
        model_log.fit(X_log_scaled, df_log['HighProfit'])
        acc = model_log.score(X_log_scaled, df_log['HighProfit'])
        
        f.write("2. REGRESIE LOGISTICA (Predictie Performanta):\n")
        f.write(f"   - Acuratete Model: {acc*100:.1f}%\n")
        f.write(f"   - Intercept: {model_log.intercept_[0]:.4f}\n")
        f.write(f"   - Interpretare: Modelul clasifica corect {acc*100:.1f}% din ani ca fiind profitabili/slabi.\n\n")
        
        # 3. Clusterizare K-Means
        cols_km = ['Revenue', 'NetProfit', 'MarketingCosts']
        df_km = df[cols_km].dropna()
        X_km_scaled = scaler.fit_transform(df_km)
        
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_km_scaled)
        
        f.write("3. CLUSTERIZARE K-MEANS (Segmentare ani):\n")
        # Mapam clusterele inapoi pe anii originali (cei care nu erau NaN)
        df_km_results = df.loc[df_km.index].copy()
        df_km_results['Cluster'] = clusters
        
        for i in range(3):
            years = df_km_results[df_km_results['Cluster'] == i]['Year'].tolist()
            f.write(f"   - Cluster {i} (Ani): {years}\n")
            
    print(f"Succes! Rezultatele au fost salvate in {output_file}")

if __name__ == "__main__":
    extract_results()
