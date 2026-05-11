import os

def append_results_to_docs():
    base_path = os.path.dirname(os.path.abspath(__file__))
    results_path = os.path.join(base_path, 'Toate_Rezultatele_Streamlit.txt')
    md_path = os.path.join(base_path, 'Documentatie_Python.md')
    
    with open(results_path, 'r', encoding='utf-8') as f:
        results_content = f.read()
        
    with open(md_path, 'a', encoding='utf-8') as f:
        f.write("\n\n---\n\n")
        f.write("## Anexa 1: Raport Complet de Rezultate Extrase din Streamlit\n")
        f.write("Secțiunea următoare prezintă datele brute, coeficienții statistici și output-urile modelelor de Machine Learning, extrase direct din aplicația de analiză.\n\n")
        f.write("```text\n")
        f.write(results_content)
        f.write("\n```\n")
        
if __name__ == '__main__':
    append_results_to_docs()
