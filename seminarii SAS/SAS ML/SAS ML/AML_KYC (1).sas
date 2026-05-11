
/* Incarcare set de date */
proc import datafile='/home/u61140151/Seminar ML/aml_demo.csv'
   out=work.aml
   dbms=csv
   replace;
run;

/* Salvare variabile categoriale si numerice in liste separate */
proc sql noprint;
   select name into :var_categ separated by ' ' from dictionary.columns
   where libname='WORK' and memname='AML' and type='char';
   select name into :var_num separated by ' ' from dictionary.columns
   where libname='WORK' and memname='AML' and type='num';
quit;

/* Proportia valorilor lipsa din cele doua liste de variabile */
proc freq data=work.aml;
   tables &var_categ / missing;
run;

proc means data=work.aml n nmiss;
   var &var_num;
run;

/* BEGIN IMPUTARE SIMPLA */
/*
 ===============================================================================
 SE DECOMENTEAZA DACA FOLOSIM METODA ACEASTA DE IMPUTARE - PRIN MEDIE SI MEDIANA
 ===============================================================================
*/

/* proc stdize data=work.aml out=work.aml */
/*             method=mean reponly; */
/*     var totalPaymentAmt90d; */
/*  */
/* proc stdize data=work.aml out=work.aml */
/*             method=median reponly; */
/*     var income; */

/* Verificam daca, prin imputarea simpla, s-au completat corect valorile lipsa tratate mai sus */
/* proc means data=work.aml n nmiss; */
/*    var &var_num; */
/* run; */

/* END IMPUTARE SIMPLA */

/* BEGIN ETAPA ENCODING*/
/*
 =============================================
 ETAPA DE PREPROCESARI DE TIP DROP SI ENCODING
 =============================================
*/

data work.aml;
   set work.aml;
   drop csrNotes; 
run;

proc freq data=work.aml;
   tables state / nocum;
run;

proc freq data=work.aml noprint;
   tables state / out=work.state_freq (drop=count);
run;

proc sort data=work.aml;
   by state;
run;

data work.aml;
   merge work.aml(in=a) work.state_freq(in=b rename=(percent=state_freq));
   by state;
   if a;

   if b then state = state_freq;
run;

data work.aml;
   set work.aml;
   drop state; 
run;

data work.aml;
   set work.aml;
   
   ALERT_numeric = (ALERT = 'Y');
   indOwnsHome_numeric = (indOwnsHome = 'Y');
   SAR_numeric = (SAR = 'Y');

   drop ALERT indOwnsHome SAR;
   rename ALERT_numeric=ALERT indOwnsHome_numeric=indOwnsHome SAR_numeric=SAR;
run;

/* END ETAPA ENCODING */ 


/* BEGIN CORELATII */
/*
 =========================================================================
 CORELATIILE DINTRE VARIABILA DEPENDENTA SI SUBMULTIMEA DE VARIABILE ALESE
 =========================================================================
*/
proc corr data=work.aml;
   var income tenureMonths creditScore kycRiskScore nbrPurchases90d avgTxnSize90d totalSpend90d maxRevolveLine;
   with SAR;
run;
/* END CORELATII */



/* BEGIN ETAPA ANTRENARE-TESTARE REGRESIE LOGISTICA*/
/*
 ============================================================
 ANTRENARE TESTARE PENTRU MODELUL DE REGRESIE LOGISTICA
 IMPUTARE SIMPLA
 ============================================================
*/

/* Definim proportia de impartire in antrenament-test */
/* %let train_prop = 0.7; */
/*  */
/* Impartim setul de date */
/* proc surveyselect data=MIdata out=work.train outall */
/*    method=srs  */
/*    rate=&train_prop */
/*    seed=12345; */
/* run; */
/*  */
/* data work.train work.test; */
/*    set work.train; */
/*    if selected then output work.train; */
/*    else output work.test; */
/* run; */
/*  */
/* Selectam variabilele independente in lista separata */
/* proc sql noprint; */
/*    select name into :indepVars separated by ' ' */
/*    from dictionary.columns */
/*    where libname='WORK' and memname='AML' and name ne 'SAR'; */
/* quit; */
/*  */
/* Construirea modelului de regresie logistica */
/* proc logistic data=work.train descending outmodel=work.logitmodel; */
/*    model SAR(event='1') = &indepVars; */
/*    score data=work.test out = test_pred outroc=vroc; */
/* run; */
/*  */
/* Cream predictii pe baza unor praguri */
/* data work.test_pred; */
/*    set work.test_pred; */
/*    pred_class = (P_1 > 0.5); */
/*    pred_class_2 = (P_1 > 0.115); */
/* run; */
/*  */
/* title1 'Matrice de confuzie pentru modelul de regresie logistica'; */
/* proc freq data=work.test_pred; */
/* 	tables SAR * pred_class / nocol; */
/* run; */
/* title2 'Matrice de confuzie pentru modelul de regresie logistica prag 2'; */
/* proc freq data=work.test_pred; */
/* 	tables SAR * pred_class_2 / nocol; */
run;
/* END CONSTRUIRE RL */


/* BEGIN ARBORE DE DECIZIE PRIN HPSPLIT */
/*
 ================================================================================
 HPSLIT ESTE O PROCEDURA MAI AVANSATA DE A CREA UN ARBORE DE DECIZIE. ALTERNATIVA
 ESTE DTREE, PE CARE O VOM UTILIZA IN PROCESUL DIN IMPUTAREA MULTIPLA, DEOARECE 
 HPSPLIT NU ARE SUPORT PENTRU UTILIZAREA IMPUTARII MULTIPLE.
 ================================================================================
*/

/* Construire si antrenare arbore */
/* proc hpsplit data=work.train seed=123; */
/*     class SAR; */
/* 	model SAR(event='1') = &indepVars; */
/* 	grow entropy; */
/* 	prune costcomplexity; */
/* 	code file = '/home/u61140151/Seminar ML/tree.sas'; */
/* run; */
/*  */
/* Construire predictii si analize pe baza pragurilor stabilite empiric */
/* data predictii_arbore; */
/* 	set work.test; */
/* 	%include '/home/u61140151/Seminar ML/tree.sas'; */
/* 	pred_tree_05 = (P_SAR1 > 0.5); */
/* 	pred_tree_0115 = (p_SAR1 > 0.1); */
/* run; */
/*  */
/* title3 'Matrice de confuzie pentru modelul arbore de decizie, threshold 0.5'; */
/* proc freq data=work.predictii_arbore; */
/* 	tables SAR * pred_tree_05 / nocol; */
/* run; */
/*  */
/* title4 'Matrice de confuzie pentru modelul arbore de decizie, threshold 0.115'; */
/* proc freq data=work.predictii_arbore; */
/* 	tables SAR * pred_tree_0115 / nocol; */
/* run; */

/* END ARBORE DE DECIZIE PRIN HPSPLIT */


/* Multiple Imputation */

/*
 ==============================================================================
 VOM FACE IMPUTARE MULTIPLA ATAT PENTRU REGRESIA LOGISTICA (PROC LOGISTIC), CAT
 SI PENTRU ARBORELE DE DECIZIE
 ***NOTA: RULAM DIN NOU CODUL DE LA INCARCAREA SETULUI DE DATE PANA LA ETAPA
 DE REALIZARE CORELATII.
 ==============================================================================
*/

proc MI data = work.aml seed=1234 out=MIdata nimpute=1; 
	var totalPaymentAmt90d income; 
run;

/* Selectam variabilele independente in lista separata */
proc sql noprint;
   select name into :indepVars separated by ' '
   from dictionary.columns
   where libname='WORK' and memname='AML' and name ne 'SAR';
quit;

/* Definim proportia de impartire in antrenament-test */
%let train_prop = 0.7;

/* Impartim setul de date */
proc surveyselect data=MIdata out=work.train outall
   method=srs 
   rate=&train_prop
   seed=12345;
run;

data work.train work.test;
   set work.train;
   if selected then output work.train;
   else output work.test;
run;

/* 
 ============================
   REGRESIA LOGISTICA
 ============================
*/
/* Construirea modelului de regresie logistica */
proc logistic data=work.train descending outmodel=work.logitmodel;
   model SAR(event='1') = &indepVars;
   score data=work.test out = test_pred outroc=vroc;
run;

/* Cream predictii pe baza unor praguri */
data work.test_pred;
   set work.test_pred;
   pred_class = (P_1 > 0.5);
   pred_class_2 = (P_1 > 0.115);
run;

title5 'Matrice de confuzie pentru modelul de regresie logistica MI';
proc freq data=work.test_pred;
	tables SAR * pred_class / nocol;
run;
title6 'Matrice de confuzie pentru modelul de regresie logistica prag 2 MI';
proc freq data=work.test_pred;
	tables SAR * pred_class_2 / nocol;
	
	
/* 
 ============================
   ARBORE - HPSPLIT
 ============================
*/
	
/* Construire si antrenare arbore */
proc hpsplit data=work.train seed=123;
    class SAR;
	model SAR(event='1') = &indepVars;
	grow entropy;
	prune costcomplexity;
	code file = '/home/u61140151/Seminar ML/tree.sas';
run;

/* Construire predictii si analize pe baza pragurilor stabilite empiric */
data predictii_arbore;
	set work.test;
	%include '/home/u61140151/Seminar ML/tree.sas';
	pred_tree_05 = (P_SAR1 > 0.5);
	pred_tree_0115 = (p_SAR1 > 0.1);
run;

title3 'Matrice de confuzie pentru modelul arbore de decizie, threshold 0.5 MI';
proc freq data=work.predictii_arbore;
	tables SAR * pred_tree_05 / nocol;
run;

title4 'Matrice de confuzie pentru modelul arbore de decizie, threshold 0.115 MI';
proc freq data=work.predictii_arbore;
	tables SAR * pred_tree_0115 / nocol;
run;

/* END ARBORE DE DECIZIE PRIN HPSPLIT */




