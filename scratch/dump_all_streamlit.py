import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler, RobustScaler
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
import os
import warnings
warnings.filterwarnings('ignore')

def dump_all_results():
    base_path = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base_path, "..", "Data_Source", "cdpr_cleaned.csv"))
    
    # Pre-compute Eras
    df['Era'] = np.where(df['Year'] < 2015, 'Pre-Witcher 3', 
                np.where(df['Year'] < 2020, 'Witcher 3 Era', 'Cyberpunk Era'))
                
    median_profit = df['NetProfit'].median()
    df['Profitability'] = np.where(df['NetProfit'] > median_profit, 'High Profit', 'Low Profit')

    output_file = os.path.join(base_path, "..", "Documentatie", "Toate_Rezultatele_Streamlit.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("DUMP COMPLET: TOATE REZULTATELE APLICAȚIEI STREAMLIT CDPR\n")
        f.write("="*80 + "\n\n")

        # ---------------------------------------------------------
        f.write("--- 1. SUMAR EXECUTIV & EVOLUȚIA FINANCIARĂ ---\n")
        f.write("📈 Evoluție Venituri, Structura Profitabilității, Costuri vs Profit\n")
        f.write(df[['Year', 'Revenue', 'NetProfit', 'MarketingCosts', 'RD_Expenditure']].to_string(index=False) + "\n\n")
        
        f.write("--- TABEL COMPLET DATE FINANCIARE CDPR ---\n")
        f.write(df.to_string(index=False) + "\n\n")

        # ---------------------------------------------------------
        f.write("--- 2. DISTRIBUȚIA VENITURILOR PE REGIUNI ---\n")
        f.write("Structura Veniturilor (Procente):\n")
        f.write(df[['Year', 'North_America_Pct', 'Europe_Pct', 'Asia_Pct', 'Poland_Pct']].to_string(index=False) + "\n\n")

        # ---------------------------------------------------------
        f.write("--- 3. ANALIZA VALORILOR LIPSĂ & OUTLIERS ---\n")
        missing_data = df.isnull().sum()
        f.write("Analiza Valorilor Lipsă (Coloane și număr NaN):\n")
        f.write(missing_data[missing_data > 0].to_string() + "\n\n")
        
        Q1 = df['NetProfit'].quantile(0.25)
        Q3 = df['NetProfit'].quantile(0.75)
        IQR = Q3 - Q1
        f.write(f"Detectarea Valorilor Extreme (IQR NetProfit):\n")
        f.write(f"Q1: {Q1:,.0f}, Q3: {Q3:,.0f}, IQR: {IQR:,.0f}\n")
        outliers = df[(df['NetProfit'] > Q3 + 1.5 * IQR) | (df['NetProfit'] < Q1 - 1.5 * IQR)]
        f.write(f"Outliers detectați:\n{outliers[['Year', 'NetProfit']].to_string(index=False)}\n\n")

        # ---------------------------------------------------------
        f.write("--- 4. CODIFICAREA DATELOR (ENCODING) ---\n")
        le = LabelEncoder()
        
        df_enc = df.copy()
        df_enc['Era_LabelEncoded'] = le.fit_transform(df_enc['Era'])
        f.write("Codificare 1: Era de Dezvoltare (Label Encoding)\n")
        f.write(df_enc[['Year', 'Era', 'Era_LabelEncoded']].to_string(index=False) + "\n\n")
        
        df_enc['Profitability_LabelEncoded'] = le.fit_transform(df_enc['Profitability'])
        f.write("Codificare 2: Nivel de Profitabilitate (Label Encoding Ordinal)\n")
        f.write(df_enc[['Year', 'Profitability', 'Profitability_LabelEncoded']].to_string(index=False) + "\n\n")
        
        df_onehot = pd.get_dummies(df_enc, columns=['Era'], prefix='Era_OHE')
        ohe_cols = [c for c in df_onehot.columns if 'Era_OHE' in c]
        f.write("Codificare 3: One-Hot Encoding (Era)\n")
        f.write(df_onehot[['Year'] + ohe_cols].to_string(index=False) + "\n\n")

        # ---------------------------------------------------------
        f.write("--- 5. METODE DE SCALARE PENTRU TOATE VARIABILELE ---\n")
        num_cols = ['Revenue', 'NetProfit', 'MarketingCosts']
        
        std_scaler = StandardScaler()
        df_std = pd.DataFrame(std_scaler.fit_transform(df[num_cols]), columns=num_cols)
        f.write("StandardScaler (Media=0, Dev.Std=1):\n")
        f.write(pd.concat([df['Year'], df_std], axis=1).head(5).to_string(index=False) + "\n  ... (afișate primele 5 rânduri)\n\n")

        mm_scaler = MinMaxScaler()
        df_mm = pd.DataFrame(mm_scaler.fit_transform(df[num_cols]), columns=num_cols)
        f.write("MinMaxScaler (Între 0 și 1):\n")
        f.write(pd.concat([df['Year'], df_mm], axis=1).head(5).to_string(index=False) + "\n  ... (afișate primele 5 rânduri)\n\n")

        rob_scaler = RobustScaler()
        df_rob = pd.DataFrame(rob_scaler.fit_transform(df[num_cols]), columns=num_cols)
        f.write("RobustScaler (Ignoră Outliers):\n")
        f.write(pd.concat([df['Year'], df_rob], axis=1).head(5).to_string(index=False) + "\n  ... (afișate primele 5 rânduri)\n\n")

        # ---------------------------------------------------------
        f.write("--- 6. GRUPARE ȘI AGREGARI PANDAS ---\n")
        f.write("Grupare 1: Era Witcher vs. Era Cyberpunk (Medii)\n")
        f.write(df.groupby('Era')[['Revenue', 'NetProfit']].mean().to_string() + "\n\n")
        
        f.write("Grupare 2: Nivele de Profitabilitate (Medii)\n")
        f.write(df.groupby('Profitability')[['MarketingCosts', 'Assets']].mean().to_string() + "\n\n")
        
        f.write("Grupare 3: Statistici Descriptive Agregate (Suma, Media, Max)\n")
        agg_stats = df.groupby('Era').agg({
            'Revenue': ['sum', 'mean', 'max'],
            'NetProfit': ['mean', 'min']
        })
        f.write(agg_stats.to_string() + "\n\n")
        
        f.write("Pivot: Eficiența Marketingului pe Eră (NetProfit mediu per categorie)\n")
        df['Marketing_Level'] = pd.qcut(df['MarketingCosts'].fillna(df['MarketingCosts'].median()), q=3, labels=['Low', 'Medium', 'High'])
        pivot_df = pd.pivot_table(df, values='NetProfit', index='Era', columns='Marketing_Level', aggfunc='mean')
        f.write(pivot_df.to_string() + "\n\n")

        # ---------------------------------------------------------
        f.write("--- 7. REZULTATE REGRESIE LOGISTICĂ ---\n")
        df_log = df[['Year', 'NetProfit', 'MarketingCosts', 'Assets']].dropna()
        df_log['Target'] = (df_log['NetProfit'] > df_log['NetProfit'].median()).astype(int)
        
        X_log = df_log[['MarketingCosts', 'Assets']]
        y_log = df_log['Target']
        X_log_scaled = rob_scaler.fit_transform(X_log)
        
        log_reg = LogisticRegression()
        log_reg.fit(X_log_scaled, y_log)
        y_pred = log_reg.predict(X_log_scaled)
        y_prob = log_reg.predict_proba(X_log_scaled)[:, 1]
        
        f.write("Coeficienții Modelului:\n")
        f.write(f"Intercept: {log_reg.intercept_[0]:.4f}\n")
        f.write(f"MarketingCosts Coef: {log_reg.coef_[0][0]:.4f}\n")
        f.write(f"Assets Coef: {log_reg.coef_[0][1]:.4f}\n\n")
        
        f.write("Tabel Predicții vs. Realitate & Probabilitatea de profit ridicat pe an:\n")
        results_log_df = pd.DataFrame({
            'Year': df_log['Year'],
            'Real_Profit_Status': df_log['Target'],
            'Predicted_Status': y_pred,
            'Probability_of_High_Profit (%)': np.round(y_prob * 100, 2)
        })
        f.write(results_log_df.to_string(index=False) + "\n\n")

        # ---------------------------------------------------------
        f.write("--- 8. SUMAR MODEL OLS COMPLET ---\n")
        df_ols = df[['Year', 'NetProfit', 'Revenue', 'MarketingCosts']].dropna()
        X_ols = df_ols[['Revenue', 'MarketingCosts']]
        X_ols_sm = sm.add_constant(X_ols)
        y_ols = df_ols['NetProfit']
        
        model_ols = sm.OLS(y_ols, X_ols_sm).fit()
        f.write(model_ols.summary().as_text() + "\n\n")
        
        f.write("Tabel OLS: Predicții vs. Realitate (Eroare/Reziduri):\n")
        df_ols['Predicție_OLS'] = model_ols.predict(X_ols_sm)
        df_ols['Reziduuri (Eroare)'] = df_ols['NetProfit'] - df_ols['Predicție_OLS']
        f.write(df_ols[['Year', 'NetProfit', 'Predicție_OLS', 'Reziduuri (Eroare)']].to_string(index=False) + "\n\n")

        # ---------------------------------------------------------
        f.write("--- 9. CLUSTERIZARE K-MEANS ---\n")
        X_km = df[['Revenue', 'NetProfit', 'MarketingCosts']].dropna()
        X_km_scaled = std_scaler.fit_transform(X_km)
        
        f.write("Metoda Elbow — Determinarea k Optim (Inertia):\n")
        for k in range(1, 6):
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(X_km_scaled)
            f.write(f"K={k} -> Inertia: {km.inertia_:,.2f}\n")
        
        f.write("\nRezultatele Clusterizării (pentru k=3):\n")
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_km_scaled)
        
        df_km_res = df.loc[X_km.index].copy()
        df_km_res['Cluster'] = clusters
        
        f.write(df_km_res[['Year', 'Revenue', 'NetProfit', 'MarketingCosts', 'Cluster']].to_string(index=False) + "\n\n")
        
        f.write("Statistici Medii pe Cluster:\n")
        f.write(df_km_res.groupby('Cluster')[['Revenue', 'NetProfit', 'MarketingCosts']].mean().to_string() + "\n\n")

    print(f"GATA! Toate datele din Streamlit au fost salvate in {output_file}")

if __name__ == "__main__":
    dump_all_results()
