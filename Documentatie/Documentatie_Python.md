# Documentație Proiect: Analiză Financiară CD PROJEKT RED
**Seminar: Pachete Software**  
**Tehnologii: Python, Streamlit, Pandas, SAS**

---

## 1. Descrierea Proiectului
Acest proiect reprezintă o soluție completă de analiză a performanței financiare pentru grupul polonez **CD PROJEKT RED** pe o perioadă de 9 ani (2017–2025). Aplicația integrează tehnici de procesare a datelor (ETL), vizualizare interactivă și modele econometrice/statistice avansate.

## 2. Structura Sistemului
Proiectul este organizat modular pentru a asigura o mentenanță ușoară și o separare clară între logică și prezentare:

*   **`Python_Project/`**: Conține codul sursă al aplicației Streamlit.
    *   `app.py`: Punctul central al aplicației, gestionează navigarea și interfața principală.
    *   `pages_config.py`: Gestionează tema vizuală (Cyberpunk), stilizarea CSS și încărcarea securizată a datelor.
    *   `pages_part1.py`: Implementează vizualizările de bază, hărțile geografice și tehnicile de curățare/scalare a datelor.
    *   `pages_part2.py`: Conține analizele avansate (Grupări Pandas, Regresii și Clusterizare).
    *   `clean_data.py`: Scriptul de tip ETL (Extract, Transform, Load) care extrage datele din rapoartele Excel oficiale.
*   **`Data_Source/`**: Depozitul central de date (fișiere Excel brute și fișierul CSV procesat).
*   **`SAS_Project/`**: Scripturile pentru analiza statistică realizată în mediul SAS.

## 3. Metodologie și Implementare (Cele 9 Cerințe)

### C1. Metode Streamlit (Interfață și Grafice)
Utilizarea componentelor `st.metric` pentru KPI-uri financiare și `plotly.express` pentru grafice de evoluție (Revenue, Profit Net). Interfața este personalizată cu CSS pentru o experiență de utilizator premium.

### C2. Utilizarea Geopandas
Analiza distribuției geografice a vânzărilor prin hărți coropletice. Datele procesate permit vizualizarea ponderii piețelor din America de Nord, Europa și Asia.

### C3. Tratarea Valorilor Lipsă și Extreme
Implementarea metodelor statistice de detecție a anomaliilor:
*   **IQR (Interquartile Range)** pentru identificarea anilor atipici (ex: anul lansării Cyberpunk 2077).
*   **Heatmap-uri** pentru identificarea vizuală a lipsei datelor.

### C4 & C5. Preprocesarea Datelor (Encoding și Scaling)
Transformarea datelor pentru algoritmii de Machine Learning:
*   **Label/One-Hot Encoding**: Clasificarea perioadelor strategice (Era Witcher vs Era Cyberpunk).
*   **StandardScaler/RobustScaler**: Normalizarea veniturilor și a datoriilor pentru a permite compararea lor pe aceeași scală.

### C6. Prelucrări Pandas Avansate
Utilizarea funcțiilor `groupby`, `agg` și `pivot_table` pentru a calcula rentabilitatea investițiilor în marketing (ROI) și performanța medie pe cicluri de dezvoltare.

### C7. Regresie Logistică (Predicție)
Utilizarea `sklearn.LogisticRegression` pentru a clasifica anii ca având profitabilitate ridicată sau scăzută în funcție de cheltuielile de marketing și active.

### C8. Regresie Liniară Multiplă
Analiza econometrică folosind `statsmodels.OLS`. Modelul determină impactul direct al veniturilor și al costurilor de marketing asupra profitului net, oferind indicatori de precizie (R-squared, P-values).

### C9. Clusterizare K-Means
Segmentarea automată a anilor de performanță financiară în 3 grupuri distincte (Lansare, Dezvoltare, Recuperare), facilitând înțelegerea macro-tendințelor companiei.

## 4. Instrucțiuni de Utilizare
Pentru a rula proiectul pe un sistem local:
1.  Asigurați-vă că aveți Python instalat (>= 3.9).
2.  Navigați în folderul proiectului: `cd Python_Project`
3.  Instalați dependențele: `pip install streamlit pandas plotly geopandas scikit-learn statsmodels`
4.  Lansați aplicația: `streamlit run app.py`

---
*Documentație generată automat pentru Proiectul de Seminar Pachete Software.*
