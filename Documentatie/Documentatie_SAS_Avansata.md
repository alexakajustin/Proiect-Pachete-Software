# Raport de Analiză a Performanței Financiare: CD Projekt Red 

Acest raport detaliază implementarea și rezultatele analizei cantitative a datelor financiare aparținând companiei CD Projekt Red, realizată prin intermediul pachetului software SAS (Statistical Analysis System). Analiza combină tehnici de procesare a datelor, statistică descriptivă, analiză de corelație și modele econometrice predictive (regresie liniară multiplă și regresie logistică).

---

## 1. Integrarea și Structurarea Datelor Externe
**a) Definirea problemei**
Primul pas în orice demers analitic îl reprezintă preluarea datelor brute dintr-o sursă externă și transpunerea acestora într-un format nativ, optimizat pentru procesare statistică. Lipsa unei integrări corecte poate duce la pierderea integrității datelor financiare.

**b) Informații necesare pentru rezolvare**
S-a utilizat setul de date `cdpr_cleaned.csv`, care conține serii de timp anuale (2010-2025) cu indicatori fundamentali: Venituri (Revenue), Profit Net (NetProfit), Costuri de Marketing (MarketingCosts), Active (Assets) și procente ale vânzărilor regionale.

**c) Metode de calcul, algoritmi, formule de calcul utilizate**
Importul a fost realizat utilizând procedura `PROC IMPORT`, cu specificarea DBMS-ului aferent formatului CSV. Argumentul `getnames=yes` a asigurat maparea automată a primului rând din fișier ca denumiri de variabile SAS, evitând asocierile manuale.

**d) Prezentarea rezultatelor**
Sistemul a generat setul de date `work.cdpr_data`, conținând 16 variabile cantitative și calitative, cu tipurile de date alocate automat de motorul SAS pe baza inspectării primelor înregistrări.

**e) Interpretarea economică a rezultatelor**
Baza de date obținută oferă o perspectivă istorică completă, esențială pentru a înțelege ciclicitatea și volatilitatea unui model de afaceri bazat pe lansarea de produse de divertisment digital de calibru AAA.

---

## 2. Definirea Formantelor Personalizate (Data Labeling)
**a) Definirea problemei**
Datele financiare continue (ex. Profit Net) sunt dificil de analizat la nivel macroscopic fără o discretizare în categorii calitative (ex. "Profit Ridicat", "Pierdere").

**b) Informații necesare pentru rezolvare**
Setul de date `cdpr_data`, cu focus pe variabilele `NetProfit` și `Year`.

**c) Metode de calcul, algoritmi, formule de calcul utilizate**
S-a implementat `PROC FORMAT` pentru a crea formatul `profit_cat` (discretizarea valorilor negative ca "Pierdere", a valorilor [0, 200.000] ca "Profit Moderat", și peste 200.000 ca "Profit Ridicat"). Similar, formatul `deceniu_fmt` grupează anii calendaristici în decenii.

**d) Prezentarea rezultatelor**
Aceste dicționare de mapare au fost salvate în catalogul intern SAS și sunt disponibile pentru a fi aplicate dinamic în fazele de raportare, fără a altera datele brute subiacente.

**e) Interpretarea economică a rezultatelor**
Clasificarea calitativă ajută managementul superior să evalueze rapid starea de sănătate financiară a companiei și facilitează agregarea rapoartelor pe perioade extinse de raportare (decenii).

---

## 3. Procesare Iterativă, Condițională și Utilizarea Masivelor (Arrays)
**a) Definirea problemei**
A fost necesară derivarea unor noi indicatori de performanță (KPIs) și validarea datelor structurale (verificarea faptului că piețele regionale cumulează 100% din vânzări).

**b) Informații necesare pentru rezolvare**
Variabilele `Revenue`, `NetProfit` și indicatorii regionali (`North_America_Pct`, `Europe_Pct`, `Asia_Pct`, `Poland_Pct`).

**c) Metode de calcul, algoritmi, formule de calcul utilizate**
Într-un pas `DATA` iterativ:
- S-a calculat marja de profit (`Profit_Margin = ROUND((NetProfit / Revenue) * 100, 0.01)`).
- S-a aplicat logica condițională (`IF-THEN-ELSE`) pentru a crea variabila `Performanta` ("Excelenta" > 30%, "Stabila" > 0%, "Critica" altfel).
- S-a definit un vector de tip `ARRAY` pentru iterarea (`DO loop`) peste coloanele regionale în vederea calculului unei sume de verificare.

**d) Prezentarea rezultatelor**
S-a obținut setul de date `cdpr_refined`, curățat de anomaliile în variabila `Year` (via `IF not missing(Year);`), îmbogățit cu marja de profit net și etichete de performanță.

**e) Interpretarea economică a rezultatelor**
Marja de profit procentuală este un indicator fundamental de rentabilitate. Faptul că SAS permite crearea și clasificarea automată a acestor praguri reduce timpul necesar analizelor de due-diligence financiar.

---

## 4. Fuziunea și Interclasarea Datelor
**a) Definirea problemei**
Contextualizarea datelor financiare este imposibilă fără raportarea la calendarul evenimentelor majore operaționale (lansări de produse).

**b) Informații necesare pentru rezolvare**
Setul de date `cdpr_refined` și date metadate reprezentând anii lansărilor AAA.

**c) Metode de calcul, algoritmi, formule de calcul utilizate**
- S-a utilizat interogarea `PROC SQL` (`CASE WHEN`) pentru a construi un tabel adițional cu evenimente.
- Interclasarea relațională s-a realizat prin `MERGE` condiționat pe cheia primară `Year`, urmat de un mecanism logic de tip `Left Join` (`if a;`). Aceasta a fost precedată în mod obligatoriu de `PROC SORT`.

**d) Prezentarea rezultatelor**
Setul de date complet `cdpr_final`.

**Extras din Raportul Financiar Integrat (PROC PRINT):**
* **Anul 2020:** Venituri 2.138.875 PLN, Profit Ridicat (Marjă 53.97%), Performanță Excelentă. Eveniment: *Lansare Cyberpunk 2077*.
* **Anul 2023:** Venituri 1.230.199 PLN, Profit Ridicat (Marjă 39.11%), Performanță Excelentă. Eveniment: *An Intermediar*.

**[INSEREAZA SCREENSHOT AICI: Tabelul "Raport Financiar CD Projekt Red (Selectie)"]**

**Distribuția Performanței în raport cu Evenimentele Majore (PROC FREQ):**
Dintre cei 8 ani înregistrați cu performanță „Excelentă”, 1 a coincis direct cu o lansare majoră, în timp ce restul reprezintă fluxuri de venituri susținute (long-tail sales) din anii ulteriori lansării.

**[INSEREAZA SCREENSHOT AICI: Tabelul "Distributia Performantei in raport cu Evenimentele Majore"]**

**e) Interpretarea economică a rezultatelor**
Asocierea bazelor de date demonstrează modelul de afaceri asimetric al studiourilor de jocuri: efort capital masiv pe termen lung, recompensat prin explozii exponențiale de capital ("spikes") în anii lansărilor.

---

## 5. Analiză Statistică Multivariată
**a) Definirea problemei**
Extragerea tendinței centrale, a dispersiei și a intensității legăturilor de asociere liniară dintre investițiile în marketing și rezultatele nete (Profit/Revenue).

**b) Informații necesare pentru rezolvare**
Setul integrat `cdpr_final` cuprinzând variabilele cantitative pe tot parcursul istoric.

**c) Metode de calcul, algoritmi, formule de calcul utilizate**
- `PROC MEANS` a generat indicatorii statistici de ordin I și II (Media, Abaterea Standard, Min, Max).
- `PROC CORR` a evaluat coeficientul de corelație Pearson ($r$) și nivelul de semnificație ($p-value$) aferent.

**d) Prezentarea rezultatelor**

**Statistici Descriptive Absolute (PROC MEANS):**
Din analiza output-ului obținem următoarele medii multianuale:
* **Media Veniturilor:** 648.761 PLN (cu o abatere standard foarte mare de 544.385 PLN, dovedind o volatilitate extremă a încasărilor).
* **Media Profitului Net:** 275.128 PLN (abatere standard 300.646 PLN).
* **Media Costurilor de Marketing:** 131.172 PLN.

**[INSEREAZA SCREENSHOT AICI: Tabelul "Indicatori Statistici: Venituri, Profit si Cheltuieli Marketing"]**

**Asocieri Liniere Liniar-Pearson (PROC CORR):**
* Corelația între Costuri Marketing și Venituri: **$r = 0.9041$**, cu $p < 0.0001$.
* Corelația între Costuri Marketing și Profit Net: **$r = 0.7898$**, cu $p = 0.0003$.

**[INSEREAZA SCREENSHOT AICI: Tabelul "Corelatia dintre Venituri, Cheltuieli Marketing si Profit Net"]**

**e) Interpretarea economică a rezultatelor**
Volatilitatea uriașă (evaluată prin abaterile standard) confirmă riscul inerent al domeniului. Corelația masivă și extrem de semnificativă statistic ($p < 0.0001$) de 0.90 între Marketing și Venituri fundamentează decizia economică de a aloca bugete masive campaniilor de conștientizare, acestea dictând direct proporțional rata de adopție a produsului (Revenue).

---

## 6. Reprezentări Vizuale Avansate
**a) Definirea problemei**
Graficele evolutive sunt esențiale pentru detectarea vizuală a anomaliilor, ciclurilor economice și stagiilor de expansiune ale companiei.

**b) Informații necesare pentru rezolvare**
Axa timpului (`Year`) corelată cu axa valorilor pentru `Revenue` și `OperatingProfit`.

**c) Metode de calcul, algoritmi, formule de calcul utilizate**
S-a utilizat modernul `PROC SGPLOT` combinând două grafice de tip `series` (serii de timp) suprapuse pe aceeași proiecție spațială.

**d) Prezentarea rezultatelor**
Graficul ilustrează două maxime globale vizibile în 2015 și 2020.

**[INSEREAZA SCREENSHOT AICI: Graficul generat de SGPLOT (liniile verde si albastra)]**

**e) Interpretarea economică a rezultatelor**
Așa cum evidențiază seriile de timp, profitul operațional urmărește fidel veniturile brute, demonstrând că, deși costurile cresc în anii de lansare, ele sunt absorbite extrem de eficient de volumul vânzărilor, marja menținându-se excepțională.

---

## 7. Modelare Econometrică: Regresie Liniară și Logistică (Machine Learning)
**a) Definirea problemei**
Depășirea sferei descriptiv-statistice și intrarea în zona de modelare prescriptivă. Se dorește prognoza exactă a veniturilor pentru anul fiscal 2026 și estimarea riscului (șansei) ca 2026 să fie un an de performanță absolută.

**b) Informații necesare pentru rezolvare**
Setul de antrenament istoric. S-a construit un set de date *holdout* (scenariu viitor) pentru 2026: Costuri de Marketing de 250.000 PLN și Active de 3.800.000 PLN.

**c) Metode de calcul, algoritmi, formule de calcul utilizate**
Pentru o analiză robustă, problema a fost tratată bidimensional:
1. **Regresie Liniară Multiplă (`PROC REG`)**: Estimarea indicatorului continuu (Revenue) folosind metoda celor mai mici pătrate (OLS). Variabile independente: `MarketingCosts`, `Assets`.
2. **Regresie Logistică (`PROC LOGISTIC`)**: Model de Machine Learning supervizat, estimând variabila dependentă binară `Este_Excelent` folosind optimizarea verosimilității maxime (Maximum Likelihood).

**d) Prezentarea rezultatelor**

**A. Regresie Liniară (PROC REG):**
Modelul liniar este extrem de puternic (F-Value = 40.25, $p < 0.0001$). Modelul explică $86.10\%$ din varianța veniturilor ($R^2 = 0.8610$).
Conform estimărilor parametrilor, coeficientul pentru costurile de marketing este de **3.30** ($p = 0.0006$). Adică, fiecare PLN investit în marketing generează în medie 3.30 PLN ca venit suplimentar.
Pentru 2026, aplicând parametrii OLS pe bugetul simulat, **Venitul prognozat este de 1.382.458 PLN.**

**[INSEREAZA SCREENSHOT AICI: Tabelul "Analysis of Variance" (PROC REG)]**
**[INSEREAZA SCREENSHOT AICI: Tabelul "Parameter Estimates" (PROC REG)]**
**[INSEREAZA SCREENSHOT AICI: Tabelul cu Rezultatul Predictiei Venitului pentru 2026 (PROC REG)]**

**B. Regresie Logistică (PROC LOGISTIC):**
Funcția de probabilitate logistică evaluează modelul ca fiind foarte viabil statistic (Likelihood Ratio $p = 0.0065$). Evaluând intrările viitoare (2026), probabilitatea estimată ($P\_1$) ca anul 2026 să obțină flag-ul de Performanță Excelentă este asimilată certitudinii logistice: **1.0 (100%)**.

**[INSEREAZA SCREENSHOT AICI: Tabelul "Model Fit Statistics" (PROC LOGISTIC)]**
**[INSEREAZA SCREENSHOT AICI: Tabelul "Analysis of Maximum Likelihood Estimates" (PROC LOGISTIC)]**
**[INSEREAZA SCREENSHOT AICI: Tabelul cu Probabilitatea de Succes pentru 2026 (PROC LOGISTIC)]**

**e) Interpretarea economică a rezultatelor**
Modelarea avansată SAS dovedește empiric fezabilitatea planului de afaceri pentru 2026. Dacă managementul se va angaja la bugetul propus de 250k PLN pentru publicitate și expansiunea activelor continuă la 3.8M PLN, randamentul marginal excelent al campaniilor de piață (multiplicator de x3.30) va garanta încasări sigure de aproximativ 1.38 milioane PLN. Din punct de vedere al clasificării de risc (Machine Learning), acest scenariu blochează riscul de "underperformance", garantând menținerea standardului excelent cu probabilitate maximă.
