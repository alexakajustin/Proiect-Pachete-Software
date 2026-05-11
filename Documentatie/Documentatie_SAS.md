# Analiza Datelor Financiare CD Projekt Red folosind SAS

## 1. Importul datelor externe
**a) Definirea problemei**
Pentru a putea realiza analiza financiara, datele aflate intr-un format extern (CSV) trebuie aduse in mediul de lucru SAS pentru procesare.

**b) Informații necesare pentru rezolvare**
Fisierul sursa `cdpr_cleaned.csv` ce contine indicatori financiari ai companiei CD Projekt Red (Venituri, Profit Net, Costuri de Marketing, etc.).

**c) Metode de calcul, algoritmi, formule de calcul utilizate**
S-a utilizat procedura `PROC IMPORT` pentru a converti fisierul CSV intr-un set de date SAS numit `cdpr_data`. S-a specificat `dbms=csv` si optiunea `getnames=yes` pentru a pastra numele coloanelor.

**d) Prezentarea rezultatelor**
Un tabel SAS a fost creat in biblioteca temporara `work`, pregatit pentru manipularile ulterioare. 

**e) Interpretarea economica a rezultatelor**
Dispunem acum de o baza de date structurata ce cuprinde performantele economice anuale, esentiala pentru evaluarea evolutiei afacerii.

---

## 2. Definirea formatelor personalizate
**a) Definirea problemei**
Raportarea datelor numerice brute este greu de interpretat pentru decidentii de business. Este necesara o categorisire calitativa a profitului.

**b) Informații necesare pentru rezolvare**
Setul de date importat anterior. Variabila țintă pentru formatare este `NetProfit` si `Year`.

**c) Metode de calcul, algoritmi, formule de calcul utilizate**
S-a utilizat `PROC FORMAT` pentru a defini categoriile `profit_cat` (Pierdere, Profit Moderat, Profit Ridicat) si `deceniu_fmt` pentru gruparea anilor financiari in decenii.

**d) Prezentarea rezultatelor**
Aceste formate sunt stocate in catalogul de formate SAS si pot fi aplicate ulterior in procedurile de printare si statistica.

**e) Interpretarea economica a rezultatelor**
Asigura o vizualizare clara a rentabilitatii companiei (de exemplu, identificarea rapida a anilor pe minus) si faciliteaza analizele pe decenii de dezvoltare.

---

## 3. Procesare iterativa, conditionala si masive (arrays)
**a) Definirea problemei**
Datele brute necesita imbogatire cu indicatori derivati (Marja de profit) si o variabila de rating calitativ. De asemenea, trebuie validata distributia geografica a vanzarilor.

**b) Informații necesare pentru rezolvare**
Variabilele `NetProfit`, `Revenue`, precum si procentele regionale (`North_America_Pct`, `Europe_Pct`, etc.).

**c) Metode de calcul, algoritmi, formule de calcul utilizate**
In cadrul unui pas `DATA`, s-au folosit:
- Functia `ROUND` pentru calculul Marjei de Profit.
- Structura `IF-THEN-ELSE` pentru stabilirea performantei anuale.
- Un `ARRAY` parcurs printr-o bucla `DO` pentru calculul sumei ponderilor regionale (verificare a completitudinii ariei geografice).

**d) Prezentarea rezultatelor**
S-a generat un set de date rafinat `cdpr_refined` cu variabile suplimentare, din care au fost eliminate intrarile invalide prin declaratia `if not missing(Year);`.

**e) Interpretarea economica a rezultatelor**
Marja de profit procentuala si indicatorul calitativ ofera imediat o imagine a starii de sanatate a afacerii in anul respectiv. Validarea regionala asigura ca piata de desfacere analizata este reprezentata integral.

---

## 4. Fuziunea si interclasarea seturilor de date
**a) Definirea problemei**
Integrarea indicatorilor financiari cu evenimente de business majore (lansari de jocuri) pentru a oferi un context economic.

**b) Informații necesare pentru rezolvare**
Datasetul `cdpr_refined` si ani de lansare cheie (ex. 2015 - Witcher 3, 2020 - Cyberpunk).

**c) Metode de calcul, algoritmi, formule de calcul utilizate**
- `PROC SQL` pentru generarea unei tabele de metadate (`meta_evenimente`) cu o clauza `CASE WHEN`.
- Instructiunea `MERGE` pentru combinarea datelor dupa cheia `Year`, precedata de obligatoriul `PROC SORT`.

**d) Prezentarea rezultatelor**
Tabelul unificat `cdpr_final` ce include performanta financiara si contextul evenimentului de lansare.

**Extras din Raportul Financiar (PROC PRINT):**
* **Anul 2020:** Venituri 2.138.875 PLN, Profit Ridicat (Marja 53.97%), Performanta Excelenta. Eveniment: Lansare Cyberpunk 2077.
* **Anul 2023:** Venituri 1.230.199 PLN, Profit Ridicat (Marja 39.11%), Performanta Excelenta. Eveniment: An Intermediar.

**[INSEREAZA SCREENSHOT AICI: Tabelul "Raport Financiar CD Projekt Red (Selectie)"]**

**Distributia Performantei in raport cu Evenimentele Majore (PROC FREQ):**
* Dintre anii catalogati cu performanta "Excelenta" (8 in total), 1 a coincis cu Lansarea Cyberpunk 2077, iar restul de 7 au fost ani cu vanzari susținute post-lansare.

**[INSEREAZA SCREENSHOT AICI: Tabelul "Distributia Performantei in raport cu Evenimentele Majore"]**

**e) Interpretarea economica a rezultatelor**
Permite evidentierea dependentei absolute a veniturilor CD Projekt Red de lansarile majore (AAA releases), fenomen specific industriei de gaming.

---

## 5. Analiza si Raportare Statistica
**a) Definirea problemei**
Identificarea indicatorilor de performanta de baza si a asocierilor dintre principalii vectori financiari (Marketing vs. Profit).

**b) Informații necesare pentru rezolvare**
Setul unificat `cdpr_final` cu categoriile de profit si variabilele cantitative (Revenue, MarketingCosts, NetProfit).

**c) Metode de calcul, algoritmi, formule de calcul utilizate**
- `PROC MEANS` pentru determinarea mediei, minimului, maximului si abaterii standard. S-a utilizat declaratia `CLASS` pentru gruparea pe decenii.
- `PROC CORR` pentru calcularea coeficientului de corelatie liniara Pearson intre costurile de marketing si profit/venit.
- `PROC FREQ` pentru un tabel de contingenta intre Performanta si Eveniment_Major.

**d) Prezentarea rezultatelor**
Rapoarte agregate afisate in Output, prezentand relatiile si metricile cheie per categorie temporala si eveniment.

**Indicatori Statistici Generali (PROC MEANS):**
* **Media Veniturilor (Revenue):** 934.355 PLN
* **Media Profitului Net:** 407.455 PLN
* **Media Costurilor de Marketing:** 196.796 PLN

**[INSEREAZA SCREENSHOT AICI: Tabelul "Indicatori Statistici: Venituri, Profit si Cheltuieli Marketing"]**

**Corelatii Financiare (PROC CORR):**
* Corelatia intre Costuri Marketing si Venituri: **0.8659** (Foarte puternica si pozitiva)
* Corelatia intre Costuri Marketing si Profit Net: **0.7028** (Puternica si pozitiva)

**[INSEREAZA SCREENSHOT AICI: Tabelul "Corelatia dintre Venituri, Cheltuieli Marketing si Profit Net"]**

**e) Interpretarea economica a rezultatelor**
Se observa o corelatie foarte puternica intre sumele investite in marketing (MarketingCosts) si venitul brut generat in anul lansarii (0.86). Tabelul de frecvente arata o relatie clara de cauzalitate intre lansari si performanta "Excelenta".

---

## 6. Generare Grafice
**a) Definirea problemei**
Prezentarea vizuala a tendintelor de business de-a lungul istoriei companiei.

**b) Informații necesare pentru rezolvare**
Variabilele temporale (`Year`) si valorile absolute (`Revenue`, `OperatingProfit`).

**c) Metode de calcul, algoritmi, formule de calcul utilizate**
`PROC SGPLOT` cu functia `series` pentru a crea un grafic de tip linie pe doua axe (venit si profit operativ) pe acelasi grafic, folosind culori contrastante.

**d) Prezentarea rezultatelor**
O harta vizuala evolutiva (Time Series) generata in SAS.

**[INSEREAZA SCREENSHOT AICI: Graficul generat de SGPLOT (liniile verde si albastra)]**

**e) Interpretarea economica a rezultatelor**
Analiza vizuala permite actionarilor si analistilor sa distinga rapid varfurile de crestere (2015, 2020) fata de perioadele de stagnare intermediare.

---

## 7. Model de predictie (SAS Machine Learning si Regresie Liniara)
**a) Definirea problemei**
Construirea unui model capabil sa prezica succesul major (Performanta Excelenta) si sa ofere o estimare matematica exacta a venitului (Revenue) in functie de activele companiei si de resursele alocate in marketing.

**b) Informații necesare pentru rezolvare**
Variabile derivata binara `Este_Excelent` (1/0) formata pe baza calitativului calculat anterior. Predictorii cantitativi: `MarketingCosts`, `Assets` si tinta cantitativa `Revenue`.

**c) Metode de calcul, algoritmi, formule de calcul utilizate**
S-au aplicat concomitent doua modele:
1. `PROC REG` (Regresie Liniara) predat in Seminarul 4, pentru a estima matematic valoarea exacta a Venitului.
2. `PROC LOGISTIC` (Clasificare) predat in Seminarul de ML, pentru rezolvarea unei probleme de clasificare binara, folosind optiunea `descending` pentru a prezice probabilitatea riscului/succesului.

**d) Prezentarea rezultatelor**
Modelul genereaza atat o cifra exacta de afaceri estimata pentru un scenariu viitor (Anul 2026), cat si o probabilitate estimativa (P_1) ca anul respectiv sa fie considerat Excelent in portofoliu.

**Rezultate Predictie pentru Anul 2026:**
* **Date de Intrare (Scenariu propus):** Costuri Marketing = 250.000 PLN, Active (Assets) = 3.800.000 PLN.
* **Venit Estimat (PROC REG):** **1.489.530 PLN**
* **Probabilitate Succes (PROC LOGISTIC):** Sanse de **100% (P_1 = 1.0)** ca anul sa fie catalogat cu Performanta Excelenta.

**[INSEREAZA SCREENSHOT AICI: Tabelul "Analysis of Variance" (PROC REG)]**

**[INSEREAZA SCREENSHOT AICI: Tabelul "Parameter Estimates" (PROC REG)]**

**[INSEREAZA SCREENSHOT AICI: Tabelul cu Rezultatul Predictiei Venitului pentru 2026 (PROC REG)]**

**[INSEREAZA SCREENSHOT AICI: Tabelul "Model Fit Statistics" (PROC LOGISTIC)]**

**[INSEREAZA SCREENSHOT AICI: Tabelul "Analysis of Maximum Likelihood Estimates" (PROC LOGISTIC)]**

**[INSEREAZA SCREENSHOT AICI: Tabelul cu Probabilitatea de Succes pentru 2026 (PROC LOGISTIC)]**

**e) Interpretarea economica a rezultatelor**
Prin combinarea celor doua modele, analistii de risc au obtinut o previziune completa pentru anul 2026: oferind valori ipotetice pentru bugetul de marketing si active, algoritmul a returnat o suma concreta de incasari (1.48 milioane) impreuna cu sansele procentuale (100%) ca pragul de performanta maxima sa fie atins. Acest instrument hibrid asigura cel mai bun fundament pentru deciziile de finantare viitoare.
