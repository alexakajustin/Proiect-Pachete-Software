import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.cluster import KMeans
from sklearn.preprocessing import RobustScaler, StandardScaler
import os
import warnings
warnings.filterwarnings('ignore')

def generate_complex_analysis():
    base_path = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base_path, "..", "Data_Source", "cdpr_cleaned.csv"))
    
    output_file = os.path.join(base_path, "..", "Documentatie", "Analiza_Complexa_Rezultate.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RAPORT DE ANALIZĂ DATĂ COMPLEXĂ: CD PROJEKT RED (2010 - 2025)\n")
        f.write("="*80 + "\n\n")
        
        # 1. STATISTICI DESCRIPTIVE ȘI ANALIZA PANDAS (Cerința 6)
        f.write("1. STATISTICI DESCRIPTIVE & PANDAS (Analiză Exploratorie)\n")
        f.write("-" * 50 + "\n")
        f.write(f"Număr total de ani analizați: {len(df)}\n")
        f.write(f"Venituri Totale (2010-2025): {df['Revenue'].sum():,.0f} PLN\n")
        f.write(f"Profit Net Total: {df['NetProfit'].sum():,.0f} PLN\n")
        f.write(f"Media Anuală a Profitului: {df['NetProfit'].mean():,.0f} PLN\n")
        f.write(f"Anul cu cel mai mare profit: {df.loc[df['NetProfit'].idxmax()]['Year']} ({df['NetProfit'].max():,.0f} PLN)\n")
        
        # Grupari istorice (Era)
        df['Era'] = np.where(df['Year'] < 2015, 'Pre-Witcher 3', 
                    np.where(df['Year'] < 2020, 'Golden Era (W3)', 'Cyberpunk Era'))
        era_stats = df.groupby('Era')['NetProfit'].mean().sort_values()
        f.write("\nProfit Mediu pe Epoci Istorice (Groupby):\n")
        for era, profit in era_stats.items():
            f.write(f" - {era}: {profit:,.0f} PLN\n")
        f.write("\n")
        
        # 2. ANALIZA OUTLIER-ILOR (Cerința 3)
        f.write("2. ANALIZA ANOMALIILOR (Outlier Detection prin IQR)\n")
        f.write("-" * 50 + "\n")
        Q1 = df['NetProfit'].quantile(0.25)
        Q3 = df['NetProfit'].quantile(0.75)
        IQR = Q3 - Q1
        upper_bound = Q3 + 1.5 * IQR
        lower_bound = Q1 - 1.5 * IQR
        outliers = df[(df['NetProfit'] > upper_bound) | (df['NetProfit'] < lower_bound)]
        
        f.write(f"Prag inferior IQR: {lower_bound:,.0f} | Prag superior IQR: {upper_bound:,.0f}\n")
        if not outliers.empty:
            f.write("Anomalii detectate (Ani atipici):\n")
            for _, row in outliers.iterrows():
                f.write(f" - Anul {int(row['Year'])}: Profit {row['NetProfit']:,.0f} PLN (Depășește limitele statistice)\n")
        f.write("\n")

        # 3. REGRESIE LOGISTICĂ - CLASIFICARE (Cerința 7 - SUPERVISED LEARNING)
        f.write("3. MACHINE LEARNING SUPERVIZAT: Regresie Logistică\n")
        f.write("-" * 50 + "\n")
        f.write("Concept (Ce înseamnă Supervised?):\n")
        f.write("Învățarea supervizată presupune că modelul are un 'profesor'. Îi oferim variabile independente (Cheltuieli Marketing, Active) și îi dăm răspunsul corect (A fost anul profitabil sau nu? Da=1, Nu=0). Modelul învață relația dintre ele pentru a face predicții viitoare.\n\n")
        
        df_log = df[['NetProfit', 'MarketingCosts', 'Assets']].dropna()
        median_profit = df_log['NetProfit'].median()
        df_log['HighProfit'] = (df_log['NetProfit'] > median_profit).astype(int)
        
        X_log = df_log[['MarketingCosts', 'Assets']]
        y_log = df_log['HighProfit']
        scaler_rob = RobustScaler()
        X_log_scaled = scaler_rob.fit_transform(X_log)
        
        log_reg = LogisticRegression(random_state=42)
        log_reg.fit(X_log_scaled, y_log)
        y_pred_log = log_reg.predict(X_log_scaled)
        
        acc = log_reg.score(X_log_scaled, y_log)
        cm = confusion_matrix(y_log, y_pred_log)
        
        f.write("Rezultate Model:\n")
        f.write(f"Acuratețe globală: {acc*100:.2f}%\n")
        f.write("Matricea de Confuzie (Confusion Matrix):\n")
        f.write(f" [ {cm[0][0]} (True Negatives)  |  {cm[0][1]} (False Positives) ]\n")
        f.write(f" [ {cm[1][0]} (False Negatives) |  {cm[1][1]} (True Positives)  ]\n")
        f.write("\nInterpretare Matrice:\n")
        f.write(f"- A ghicit corect {cm[0][0]} ani slabi și {cm[1][1]} ani profitabili.\n")
        f.write(f"- A greșit la {cm[0][1] + cm[1][0]} ani.\n")
        f.write(f"Coeficienți învățați: Marketing = {log_reg.coef_[0][0]:.4f}, Active = {log_reg.coef_[0][1]:.4f}\n\n")

        # 4. REGRESIE LINIARĂ MULTIPLĂ (Cerința 8)
        f.write("4. ANALIZĂ ECONOMETRICĂ: Regresie Liniară Multiplă (OLS)\n")
        f.write("-" * 50 + "\n")
        df_ols = df[['NetProfit', 'Revenue', 'AdminExpenses', 'MarketingCosts']].dropna()
        X_ols = df_ols[['Revenue', 'MarketingCosts']]
        X_ols = sm.add_constant(X_ols) # Adăugăm constanta
        y_ols = df_ols['NetProfit']
        
        model_ols = sm.OLS(y_ols, X_ols).fit()
        
        f.write(f"Coeficient de Determinare (R-squared): {model_ols.rsquared:.4f} ({model_ols.rsquared*100:.1f}%)\n")
        f.write(f"R-squared ajustat (Adj. R-squared): {model_ols.rsquared_adj:.4f}\n")
        f.write(f"F-statistic (Test de validitate globală): {model_ols.fvalue:.4f} (Prob: {model_ols.f_pvalue:.4e})\n\n")
        
        f.write("Analiza Variabilelor (P-values și Coeficienți):\n")
        f.write("1. Venituri (Revenue):\n")
        f.write(f"   - Coeficient: {model_ols.params['Revenue']:.4f}\n")
        f.write(f"   - P-value: {model_ols.pvalues['Revenue']:.4e}\n")
        if model_ols.pvalues['Revenue'] < 0.05:
            f.write("   -> Semnificativ statistic! Are un impact dovedit asupra profitului.\n")
        else:
            f.write("   -> Nesemnificativ statistic (Posibil coliniaritate sau date insuficiente).\n")
            
        f.write("2. Costuri Marketing:\n")
        f.write(f"   - Coeficient: {model_ols.params['MarketingCosts']:.4f}\n")
        f.write(f"   - P-value: {model_ols.pvalues['MarketingCosts']:.4e}\n\n")
        
        # 5. CLUSTERIZARE K-MEANS (Cerința 9 - UNSUPERVISED LEARNING)
        f.write("5. MACHINE LEARNING NESUPERVIZAT: Clusterizare K-Means\n")
        f.write("-" * 50 + "\n")
        f.write("Concept (Ce înseamnă Unsupervised?):\n")
        f.write("Învățarea nesupervizată înseamnă că algoritmul NU are 'profesor'. Îi dăm datele brute (fără să-i spunem ce ani au fost buni sau răi) și îi cerem să găsească el singur tipare (pattern-uri) ascunse, formând grupuri de ani care seamănă între ei.\n\n")
        
        cols_km = ['Revenue', 'NetProfit', 'MarketingCosts']
        df_km = df[cols_km].dropna()
        scaler_std = StandardScaler()
        X_km_scaled = scaler_std.fit_transform(df_km)
        
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_km_scaled)
        
        df_km_results = df.loc[df_km.index].copy()
        df_km_results['Cluster'] = clusters
        
        f.write("Rezultate Clusterizare (K=3 grupuri):\n")
        # Inversăm transformarea centroizilor pentru a-i vedea în valorile reale (PLN)
        centroids = scaler_std.inverse_transform(kmeans.cluster_centers_)
        
        for i in range(3):
            years_in_cluster = df_km_results[df_km_results['Cluster'] == i]['Year'].tolist()
            f.write(f"\nCLUSTERUL {i}:\n")
            f.write(f"- Ani incluși: {years_in_cluster}\n")
            f.write(f"- Caracteristicile centroidului (media grupului):\n")
            f.write(f"    * Venituri Medii: {centroids[i][0]:,.0f} PLN\n")
            f.write(f"    * Profit Net Mediu: {centroids[i][1]:,.0f} PLN\n")
            f.write(f"    * Cost Marketing Mediu: {centroids[i][2]:,.0f} PLN\n")
            
            # Interpretare automata
            if centroids[i][0] > 1.5e6:
                f.write("-> INTERPRETARE: Aceștia sunt anii excepționali ('Blockbuster Releases' gen Cyberpunk), cu venituri uriașe și costuri de marketing colosale.\n")
            elif centroids[i][0] > 5e5:
                f.write("-> INTERPRETARE: Anii de dezvoltare stabilă / Long-tail sales (Vânzări susținute post-lansare, profit mare cu efort de marketing redus).\n")
            else:
                f.write("-> INTERPRETARE: Anii de construcție/dezvoltare. Venituri mici, profit mic sau pierderi, timp dedicat creării următoarelor mari titluri.\n")
                
    print(f"Raportul detaliat a fost generat in: {output_file}")

if __name__ == "__main__":
    generate_complex_analysis()
