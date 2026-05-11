# Documentație Tehnică și Analitică: CD PROJEKT RED (2010 - 2025)
**Seminar: Pachete Software**
**Tehnologii: Ecosistemul Python pentru Data Science**

---

## Introducere și Ecosistemul Tehnologic
Prezentul proiect constituie un sistem complex de Business Intelligence (BI) și Analiză Statistico-Financiară, dezvoltat pentru evaluarea performanței economice a grupului CD PROJEKT RED. Obiectivul fundamental al lucrării constă în integrarea metodelor cantitative cu tehnici avansate de modelare predictivă (Machine Learning).

Pentru a realiza acest sistem, s-a utilizat ecosistemul Python, bazat pe următoarele pachete software:
*   **Pandas**: Reprezintă nucleul procesării datelor. Permite manipularea structurilor tabelare (*DataFrames*), curățarea valorilor lipsă, gruparea datelor (`groupby`) și crearea de tabele pivot multidimensionale.
*   **Streamlit**: Framework-ul utilizat pentru a transforma codul Python de analiză într-un Dashboard web interactiv, permițând utilizatorului să ajusteze parametrii modelelor în timp real.
*   **Scikit-Learn (Sklearn)**: Biblioteca esențială pentru Machine Learning. A fost utilizată pentru scalarea datelor (StandardScaler, RobustScaler), învățare supervizată (Regresie Logistică) și nesupervizată (Clusterizare K-Means).
*   **Statsmodels**: Utilizată pentru analiza econometrică tradițională, oferind statistici detaliate, coeficienți preciși și teste de ipoteză (P-values) imposibil de extras la fel de ușor din alte pachete.
*   **Geopandas & Plotly**: Instrumentele principale pentru generarea vizualizărilor interactive și a hărților coropletice pentru distribuția veniturilor globale.

---

## 1. Evoluția Financiară și Statistici Descriptive

**Concept Teoretic:** Statisticile descriptive reprezintă primul pas în analiza de date, calculând indicatori precum media, mediana, valorile maxime și minime. Acestea oferă un "rezumat executiv" al scării la care operează compania și ajută la înțelegerea volatilității pieței.

>[SCREENSHOT "Tabel Complet — Date Financiare CDPR"]
>[SCREENSHOT "📈 Evoluție Venituri" (graficul cu bare)]

**Interpretarea Datelor:** 
În perioada 2010-2025, compania a generat venituri totale de peste 10.3 miliarde PLN și un profit net cumulat de 4.4 miliarde PLN. Media anuală a profitului s-a situat în jurul valorii de 275,000 PLN, obținând o marjă globală excelentă de aproximativ 42.4%.
Totuși, așa cum arată graficele evolutive, analizăm o volatilitate extremă. Un singur exercițiu financiar, anul lansării *Cyberpunk 2077* (2020), a generat un profit record de 1.15 miliarde PLN, reprezentând aproximativ 26% din întregul profit istoric al companiei, demonstrând riscul inerent, dar și randamentul masiv al modelului "blockbuster" din industria de gaming.

---

## 2. Distribuția Geografică a Veniturilor

**Concept Teoretic:** Analiza geospațială presupune cartografierea datelor financiare (Revenue) pe coordonate geografice. Aceasta se realizează prin îmbinarea datelor contabile cu geometrii de tip GeoJSON, permițând evaluarea dependenței corporative de anumite piețe (Risc de Țară).

>[SCREENSHOT "Harta Distribuției Veniturilor" (Harta interactivă din Streamlit)]
>[SCREENSHOT "Structura Veniturilor pe regiuni"]

**Interpretarea Datelor:** 
Datele istorice indică o tranziție strategică radicală. Dacă la începutul deceniului precedent (2010) compania depindea puternic de piața europeană (40%) și cea locală (Polonia cumulând 20%), pe parcursul celor 16 ani expansiunea transatlantică a devenit principala sursă de venit. Până în 2025, piața din America de Nord a ajuns să reprezinte 75.5% din încasări. Această evoluție validează maturizarea brandului CD Projekt Red și o penetrare masivă pe cea mai dezvoltată și competitivă piață de divertisment digital la nivel mondial.

---

## 3. Analiza Valorilor Lipsă și Detectarea Anomaliilor (Outliers)

**Concept Teoretic:** Datele brute din lumea reală sunt adesea incomplete sau conțin valori aberante (Outliers) care pot strica algoritmul de Machine Learning. 
*Pentru anomalii*, s-a utilizat metoda statistică **IQR (Interquartile Range)**. IQR calculează distanța dintre mijlocul jumătății superioare ($Q3$) și mijlocul jumătății inferioare ($Q1$) a datelor. Orice punct situat dincolo de limitele $Q1 - 1.5 \times IQR$ sau $Q3 + 1.5 \times IQR$ este izolat matematic ca fiind o anomalie.

>[SCREENSHOT "Analiza Valorilor Lipsă"]
>[SCREENSHOT "Detectarea Valorilor Extreme (Outliers)"]

**Interpretarea Datelor:** 
După identificarea și tratarea lacunelor (valori NaN înainte de 2015 la indicatori precum RD_Expenditure sau EBITDA), algoritmul IQR a scanat automat istoricul de profitabilitate. Pragul superior de normalitate a fost stabilit matematic la 903,844 PLN. Conform acestui model, anul 2020, cu profitul său uluitor de 1,154,327 PLN, a fost catalogat automat drept **Outlier (Anomalie pozitivă)**. Această detecție validează faptul că șocul financiar produs de Cyberpunk 2077 a "spart" orice tipar de operare normală a studioului de până atunci.

---

## 4. Pregătirea Datelor pentru Algoritmi (Encoding)

**Concept Teoretic:** Deoarece modelele matematice nu pot citi cuvinte (cum ar fi numele "Era Cyberpunk"), a fost necesară codificarea acestora (Encoding). S-au utilizat două pachete din Sklearn:
*   **Label Encoding**: Atribuie pur și simplu un număr unei categorii (ex. Low Profit=1, High Profit=0). Se folosește când ordinea/ierarhia nu contează sau are doar două valori.
*   **One-Hot Encoding (OHE)**: Transformă fiecare categorie într-o coloană binară independentă. Dacă am fi lăsat erele istorice ca (1, 2, 3), algoritmul ar fi crezut fals că Era 3 este de 3 ori "mai mare" decât Era 1. OHE previne această iluzie statistică.

>[SCREENSHOT "Codificare 1: Era de Dezvoltare (Label Encoding)"]
>[SCREENSHOT "Codificare 3: One-Hot Encoding (Era)"]

**Interpretarea Datelor:** 
Așa cum reiese din tabelele generate, implementarea OHE a spart coloana "Era" în trei coloane separate: `Era_OHE_Cyberpunk`, `Era_OHE_Pre-Witcher`, `Era_OHE_Witcher`. De exemplu, anul 2015 a primit valoarea $1$ strict pe coloana "Witcher" și $0$ pe celelalte, permițând algoritmilor de machine learning să coreleze independent performanța financiară cu fiecare dintre aceste perioade istorice, fără a crea relații matematice false între ele.

---

## 5. Standardizarea și Scalarea Variabilelor

**Concept Teoretic:** Modelele de regresie sunt sensibile la diferența de magnitudine dintre coloane (un profit de 1.000.000 are o greutate "artificială" mai mare decât o marjă de 10%). Scalarea rezolvă problema:
*   **StandardScaler**: Centrează distribuția la media zero (scor Z). Un scor de +1 înseamnă "o deviație standard peste media istorică".
*   **MinMaxScaler**: Comprimă toate valorile într-un interval fix între 0 și 1.
*   **RobustScaler**: Asemănător cu Standardizarea, însă folosește Mediana și metoda IQR pentru a nu permite anomaliilor (cum e anul 2020) să strice complet calculul mediei globale.

>[SCREENSHOT "StandardScaler"]
>[SCREENSHOT "RobustScaler pentru TOATE variabilele"]

**Interpretarea Datelor:** 
Efectul scalării este vizibil clar asupra anului 2020. StandardScaler a transformat profitul masiv de peste un miliard PLN într-un scor Z de **+2.85**. Aceasta ne spune științific că rezultatul acelui an s-a situat cu aproape trei deviații standard deasupra mediei companiei, o performanță aproape imposibilă într-o distribuție statistică normală. Din cauza acestui șoc istoric, am optat pentru utilizarea exclusivă a *RobustScaler*-ului în antrenarea algoritmilor predictivi care au urmat.

---

## 6. Eficiența Marketingului (Grupări și Agregări Pandas)

**Concept Teoretic:** Analiza descriptivă avansată se bazează pe funcțiile pachetului Pandas: `groupby` (care grupează tabelul pe categorii comune), funcțiile de agregare (`mean`, `max`, `sum`) și `pivot_table` (care creează structuri multidimensionale pentru a analiza două sau mai multe variabile simultan).

>[SCREENSHOT "Grupare 1: Era Witcher vs. Era Cyberpunk"]
>[SCREENSHOT "Pivot: Eficiența Marketingului pe Eră"]

**Interpretarea Datelor:** 
Agregările `groupby` dovedesc maturizarea rapidă a studioului. Profitul net mediu anual a evoluat de la nivelul marginal de 13,633 PLN în perioada pre-Witcher, la 215,572 PLN în era "Witcher", și a explodat la o medie istorică de 542,669 PLN în era "Cyberpunk" (2020-2025). 
Tabelele Pivot adaugă un strat superior de informație: asocierea unui buget de marketing maxim ("High") în perioada modernă s-a tradus printr-un profit net mediu de 547,858 PLN, de peste două ori mai mare decât randamentul marketingului similar din epoca "Witcher". Astfel, Pandas demonstrează că brandul a învățat să convertească exponențial mai bine reclama în vânzări efective.

---

## 7. Predicția Performanței (Regresia Logistică)

**Concept Teoretic:** Regresia Logistică face parte din categoria *Machine Learning Supervizat* (învățare cu profesor). Algoritmul primește variabilele independente (Activele și Bugetul de Marketing) și rezultatele corecte din trecut (A fost anul profitabil sau nu? Da=1 / Nu=0). Modelul învață tiparele de succes pentru a oferi ulterior predicții și **probabilități procentuale** pentru fiecare an. 

>[SCREENSHOT "Rezultatele Modelului de regresie logistica" (Acuratețe, Matrice, Coeficienți)]
>[SCREENSHOT "Tabel Predicții vs. Realitate" sau graficul de probabilitate de pe ecran]

**Interpretarea Datelor:** 
Algoritmul a atins o acuratețe remarcabilă de **81.25%** în diferențierea anilor slabi de cei performanți. Analizând probabilitățile de pe grafic, modelul a calculat o certitudine de **96.4%** ca anul 2020 să fie un an de vârf. Deși noi știam deja istoria lansării Cyberpunk, este uluitor faptul că algoritmul de Inteligență Artificială a dedus inevitabilitatea succesului analizând *exclusiv* suma masivă de bani alocată costurilor de marketing și capitalul de active acumulat înainte de lansare.

---

## 8. Analiza Econometrică și Relații Cauzale (OLS)

**Concept Teoretic:** Ordinary Least Squares (OLS) este o metodă econometrică tradițională. Aceasta trasează o regresie liniară, calculând modul exact în care fluctuația unei variabile dependente (Profit Net) este dictată de schimbarea variabilelor independente (Venituri, Marketing). Conceptele cheie urmărite sunt:
*   **$R^2$ (R-squared)**: Coeficientul de determinare. Dacă este 1.0 (100%), modelul prezice profitul perfect.
*   **P-value (Probabilitatea)**: Arată dacă relația descoperită este o coincidență. Dacă $P < 0.05$, relația este "semnificativă statistic" și o putem lua ca adevăr științific.

>[SCREENSHOT "Sumar Model OLS COMPLET" (Tabelul din Statsmodels)]
>[SCREENSHOT "Profit Real vs. Predicție" & "Reziduuri vs. Valori Estimate" (Graficele cu linii/puncte)]

**Interpretarea Datelor:** 
Modelul OLS implementat via `statsmodels` a fost un real succes. A obținut un $R^2$ de **0.951**, indicând o potrivire absolută: 95.1% din toată variabilitatea profitului net CD Projekt este explicată direct, matematic, doar de venituri și cheltuielile cu marketingul. 
Testul de ipoteză a generat o valoare P-value de $0.000$ pentru `Revenue`, demonstrând o relație statistic semnificativă pozitivă. Graficul de "Predicție vs. Realitate" subliniază acuratețea modelului OLS: linia galbenă a predicției urmărește aproape perfect linia albastră a istoriei reale, distanțându-se vizibil (reziduuri mari) doar în anii șocurilor de piață, unde dinamica lansărilor AAA nu mai răspunde regulilor economiei liniare.

---

## 9. Segmentarea Strategică prin Inteligență Artificială (K-Means)

**Concept Teoretic:** K-Means face parte din categoria *Machine Learning Nesupervizat* (învățare fără profesor). Algoritmul primește doar tabelele financiare brute, fără ani și fără explicații istorice, fiind forțat să găsească singur "centroizi" (puncte de greutate) în jurul cărora se grupează date cu profile similare, formând clustere. S-a utilizat *Metoda Elbow* pentru a măsura momentul în care inerția (eroarea) se stabilizează, validând 3 ca număr optim de clustere.

>[SCREENSHOT "Metoda Elbow — Determinarea k Optim"]
>[SCREENSHOT "Rezultatele Clusterizării" (Tabele/Graficul cu Scatter Plot)]
>[SCREENSHOT "Detalii pe Clustere"]

**Interpretarea Datelor:** 
Fără absolut nicio intervenție umană, inteligența artificială a reconstruit perfect fazele istorice ale corporației poloneze:
*   **Clusterul 0 (2010–2019): "Construcția"**. A izolat deceniul inițial, recunoscând anii cu profituri și active mai modeste, dedicate finanțării și lansării francizei Witcher.
*   **Clusterul 2 (2021–2025): "Sustenabilitatea Post-Lansare"**. A grupat anii recenți pe un profil unic: active (Assets) imense și profituri susținute ("Long-tail sales"), confirmând reziliența afacerii după episodul Cyberpunk.
*   **Clusterul 1 (Anul 2020): "Anomalia Singulară"**. Așa cum s-a determinat și la curățarea datelor cu IQR, algoritmul K-Means a izolat anul 2020 într-un cluster din care face parte el singur, determinând matematic că investițiile de marketing și explozia de profit din acel an sunt irepetabile și imposibil de asociat cu oricare alt moment din trecutul sau viitorul apropiat al studioului.

Segmentarea nesupervizată reprezintă dovada absolută a valorii acestui proiect: algoritmii de date pot decripta și valida independent strategia și istoria reală a oricărei afaceri.
