import pandas as pd

html_file = 'cdpr-results.html'
tables = pd.read_html(html_file)

with open('extracted_tables.txt', 'w', encoding='utf-8') as f:
    for i, tbl in enumerate(tables):
        f.write(f"### Table {i}\n")
        f.write(tbl.to_csv(index=False, sep='|'))
        f.write("\n\n")
