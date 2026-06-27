import sqlite3
import csv
import psycopg2 

def import_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Przykładowy import jednej tabeli (powtórz dla reszty)
    with open('klienci.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        cur.executemany("INSERT OR IGNORE INTO KLIENT (ID_Klienta, Imie, Nazwisko, Telefon, Email) VALUES (?, ?, ?, ?, ?)", reader)
    
    conn.commit()
    conn.close()
    print("Dane zaimportowane do SQLite.")

def import_postgresql(db_params):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    
    # Import za pomocą COPY (najszybsza metoda)
    tabele_pliki = {
        'klient': 'klienci.csv',
        'pracownik': 'pracownicy.csv',
        'urzadzenie': 'urzadzenia.csv',
        'czesc': 'czesci.csv',
        'zlecenie': 'zlecenia.csv',
        'zuzyte_czesci': 'zuzyte_czesci.csv'
    }
    
    for tabela, plik in tabele_pliki.items():
        with open(plik, 'r', encoding='utf-8') as f:
            cur.copy_expert(f"COPY {tabela} FROM STDIN WITH CSV", f)
            
    conn.commit()
    conn.close()
    print("Dane zaimportowane do PostgreSQL za pomocą COPY.")

if __name__ == "__main__":
    # import_sqlite('serwis.db')
    # import_postgresql({'dbname': 'student06db', 'user': 'student06', 'password': 'fwbmfh7xqdZNP', 'host': '127.0.0.1'})
    pass
