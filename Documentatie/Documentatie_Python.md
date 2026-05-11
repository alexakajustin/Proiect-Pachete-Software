# Documentație Tehnică: Sistem Analitic de Gestiune și Predicție Financiară CD PROJEKT RED
**Seminar: Pachete Software**
**Tehnologii: Ecosistemul Python pentru Data Science**

---

## 1. Introducere și Obiectivele Proiectului
Prezentul proiect constituie un sistem complex de **Business Intelligence (BI)** și **Analiză Statistico-Financiară**, dezvoltat pentru evaluarea performanței economice a grupului **CD PROJEKT RED** pe un orizont temporal de 16 ani (2010–2025). Obiectivul fundamental al lucrării constă în integrarea metodelor cantitative de procesare a datelor cu tehnici avansate de vizualizare și modelare predictivă.

Sistemul permite monitorizarea indicatorilor de profitabilitate, analiza distribuției geografice a veniturilor și segmentarea strategică a exercițiilor financiare prin algoritmi de Machine Learning.

---

## 2. Arhitectura Sistemului și Componentele Software
Implementarea proiectului se bazează pe o arhitectură modulară, utilizând biblioteci software specializate:

*   **Pandas**: Utilizat pentru gestionarea structurilor de date tabelare (*DataFrames*). Permite operațiuni complexe de filtrare, agregare și curățare a datelor.
*   **Streamlit**: Framework utilizat pentru dezvoltarea interfeței grafice (Dashboard), facilitând interacțiunea utilizatorului cu modelele analitice.
*   **Scikit-Learn (Sklearn)**: Biblioteca centrală pentru implementarea modelelor de Machine Learning nesupervizat (K-Means) și supervizat (Regresie Logistică).
*   **Statsmodels**: Utilizată pentru modelarea econometrică riguroasă, oferind suport pentru inferența statistică prin metoda celor mai mici pătrate (OLS).
*   **Geopandas**: Utilizată pentru manipularea și randarea datelor geospațiale, necesare pentru generarea hărților financiare.

---

## 3. Metodologia de Prelucrare și Analiză a Datelor

### 3.1. Procesul de tip ETL (Extract, Transform, Load)
Datele financiare au fost preluate din rapoartele oficiale și procesate prin intermediul scriptului `clean_data.py`. Acesta asigură:
1.  **Extracția**: Parsarea automată a fișierelor Excel.
2.  **Transformarea**: Uniformizarea etichetelor contabile și calculul indicatorilor derivați (ex. Liabilities ca diferență între Assets și Equity).
3.  **Încărcarea**: Salvarea datelor într-un format interoperabil `.csv` (Single Source of Truth).

### 3.2. Managementul Valorilor Atipice și Lipsă
Integritatea statistică a fost asigurată prin:
*   **Analiza Valorilor Lipsă**: Utilizarea hărților termice pentru identificarea lacunelor informaționale.
*   **Metoda IQR (Interquartile Range)**: S-a utilizat pentru detecția punctelor de date atipice (Outliers), asigurând o scalare robustă a modelelor predictive.

---

## 4. Modele Analitice și Machine Learning

### 4.1. Regresia Logistică și Clasificarea Performanței
S-a implementat un model de clasificare binară pentru a estima probabilitatea de succes financiar (Profitabilitate Ridicată) în funcție de investițiile în Marketing și R&D. Validarea s-a realizat prin Matricea de Confuzie.

### 4.2. Regresia Liniară Multiplă (OLS)
S-a cuantificat relația de cauzalitate dintre variabilele independente (Venituri, Cheltuieli Administrative) și Profitul Net. S-au analizat pragurile de semnificație ($\alpha < 0.05$) și coeficientul de determinare ($R^2$).

### 4.3. Clusterizarea K-Means
S-a utilizat învățarea nesupervizată pentru a identifica automat tiparele de comportament financiar, grupând anii în clustere bazate pe centroizi.

---

## Anexă: Glosar Metodologic Detaliat

1.  **Business Intelligence (BI)**: Ansamblu de tehnologii și strategii utilizate pentru analiza datelor de afaceri în scopul fundamentării deciziilor manageriale.
2.  **KPI (Key Performance Indicator)**: Indicatori esențiali care măsoară gradul de atingere a obiectivelor strategice (ex. Profitul Net).
3.  **Intercuartilă (IQR)**: Diferența dintre al treilea și primul quartil ($Q3 - Q1$). Reprezintă zona în care se află 50% din datele centrale și este utilizată pentru eliminarea zgomotului statistic (anomaliilor).
4.  **RobustScaler**: Metodă de normalizare a datelor care utilizează mediana și IQR, fiind imună la influența valorilor extreme.
5.  **One-Hot Encoding**: Proces de transformare a categoriilor (ex. Epoci istorice) în coloane binare (0 sau 1), necesar pentru interpretarea datelor de către algoritmi.
6.  **Ordinary Least Squares (OLS)**: Metodă de estimare a parametrilor dintr-un model de regresie liniară prin minimizarea sumei pătratelor diferențelor dintre valorile observate și cele prezise.
7.  **R-squared ($R^2$)**: Statistică ce indică proporția de variație a variabilei dependente explicată de variabilele independente. O valoare de 1.0 indică o potrivire perfectă.
8.  **P-value**: Probabilitatea de a obține rezultatele observate (sau unele mai extreme) sub ipoteza nulă. O valoare sub 0.05 indică faptul că rezultatul este **statistic semnificativ**.
9.  **Centroizi**: Puncte centrale ale unui grup (cluster) în cadrul algoritmului K-Means, reprezentând media tuturor punctelor aparținând acelui grup.
10. **Matricea de Confuzie**: Instrument de evaluare a performanței unui model de clasificare, prezentând numărul de predicții corecte și eronate, divizate în categorii (Adevărat Pozitiv, Fals Pozitiv etc.).

---
*Acest document servește drept suport teoretic riguros pentru proiectul de seminar Pachete Software.*
