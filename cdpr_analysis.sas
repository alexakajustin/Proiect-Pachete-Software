/* 
   CD Projekt Red Financial Analysis 
   Project: Pachete Software Seminar
   Requirements: 11 Mandatory facilities
*/

/* 1. PROC IMPORT: Create SAS dataset from external CSV */
proc import datafile="c:\Users\Justin\Desktop\Pachete Software\cdpr_cleaned.csv"
    out=work.cdpr_data
    dbms=csv
    replace;
    getnames=yes;
run;

/* 2. PROC FORMAT: User-defined formats */
proc format;
    value profit_cat
        low - 0 = "Loss"
        0 - 200000 = "Moderate Profit"
        200000 - high = "High Profit";
run;

/* 3 & 4. DATA STEP: Iterative processing, conditionals, and subsets */
data work.cdpr_refined;
    set work.cdpr_data;
    
    /* 5. SAS Functions: Calculate Profit Margin and Year Age */
    Profit_Margin = (NetProfit / Revenue) * 100;
    Years_Since_Launch = 2025 - Year;
    
    /* 3. Conditional processing */
    if Profit_Margin > 30 then Performance = "Excellent";
    else if Profit_Margin > 0 then Performance = "Stable   ";
    else Performance = "Critical ";

    /* 7. ARRAY: Calculate average of percentage distributions */
    array regions[*] North_America_Pct Europe_Pct Asia_Pct Poland_Pct;
    total_check = 0;
    do i = 1 to dim(regions);
        total_check + regions[i];
    end;
    
    /* 4. Creating subsets: High performance years only */
    if Profit_Margin > 20 then output work.cdpr_refined;
run;

/* 6. SQL & Dataset Combining: Create a metadata table and merge */
proc sql;
    create table work.meta as
    select Year, 
           case when Year = 2020 then "Cyberpunk Launch"
                when Year = 2015 then "Witcher 3 Launch"
                else "Inter-release"
           end as Event
    from work.cdpr_data;
quit;

data work.cdpr_final;
    merge work.cdpr_refined(in=a) work.meta(in=b);
    by Year;
    if a;
run;

/* 8. Reporting Procedures: PROC MEANS & PROC FREQ */
title "Financial Summary by Performance Category";
proc means data=work.cdpr_final mean std min max;
    var Revenue NetProfit Profit_Margin;
    class Performance;
run;

proc freq data=work.cdpr_final;
    tables Performance * Event / nocol norow;
    format NetProfit profit_cat.;
run;

/* 9. Statistical Procedures: PROC CORR */
title "Correlation between Revenue, Marketing, and Profit";
proc corr data=work.cdpr_data;
    var Revenue MarketingCosts NetProfit;
run;

/* 10. Graphics: PROC SGPLOT */
title "Revenue Trend vs Operating Profit";
proc sgplot data=work.cdpr_data;
    series x=Year y=Revenue / lineattrs=(color=gold thickness=2) name="Revenue";
    series x=Year y=OperatingProfit / lineattrs=(color=cyan thickness=2) name="OpProfit";
    yaxis label="kPLN";
    xaxis label="Year";
    keylegend "Revenue" "OpProfit";
run;

/* 11. SAS ML: Logistic Regression (PROC LOGISTIC) */
/* Predict if a year is 'Excellent' performance (Margin > 30%) */
data work.ml_prep;
    set work.cdpr_refined;
    is_excellent = (Performance = "Excellent");
run;

proc logistic data=work.ml_prep descending;
    model is_excellent = Revenue MarketingCosts Assets;
run;
