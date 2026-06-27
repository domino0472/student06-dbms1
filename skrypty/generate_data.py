import csv
import random
from datetime import datetime, timedelta

def generate_csv():
    # 1. Klienci
    with open('klienci.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in range(1, 51):
            writer.writerow([i, f"Imie{i}", f"Nazwisko{i}", f"500600{i:03d}", f"klient{i}@example.com"])

    # 2. Pracownicy
    stanowiska = ["Technik", "Serwisant", "Kierownik", "Stażysta"]
    with open('pracownicy.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in range(1, 11):
            writer.writerow([i, f"PracImie{i}", f"PracNazwisko{i}", random.choice(stanowiska)])

    # 3. Urządzenia
    marki = ["Dell", "HP", "Lenovo", "Apple", "Asus"]
    with open('urzadzenia.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in range(1, 101):
            id_klienta = random.randint(1, 50)
            writer.writerow([i, id_klienta, random.choice(marki), f"Model-{random.randint(100,999)}", f"SN{i*12345}"])

    # 4. Części
    czesci = ["Matryca", "Dysk SSD 512GB", "RAM 8GB", "Bateria", "Klawiatura", "Płyta główna", "Zasilacz"]
    with open('czesci.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i, nazwa in enumerate(czesci, start=1):
            writer.writerow([i, nazwa, "ProducentX", random.randint(5, 50), round(random.uniform(50.0, 500.0), 2)])

    # 5. Zlecenia
    statusy = ["Przyjęte", "Diagnoza", "Oczekuje na części", "Naprawione", "Wydane"]
    with open('zlecenia.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in range(1, 201):
            id_urzadzenia = random.randint(1, 100)
            id_pracownika = random.randint(1, 10)
            data = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
            koszt = round(random.uniform(50.0, 400.0), 2)
            writer.writerow([i, id_urzadzenia, id_pracownika, data.strftime("%Y-%m-%d %H:%M:%S"), "Opis usterki", random.choice(statusy), koszt])

    # 6. Zużyte części
    with open('zuzyte_czesci.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        zestaw_par = set()
        for _ in range(300):
            id_zlecenia = random.randint(1, 200)
            id_czesci = random.randint(1, len(czesci))
            if (id_zlecenia, id_czesci) not in zestaw_par:
                zestaw_par.add((id_zlecenia, id_czesci))
                writer.writerow([id_zlecenia, id_czesci, random.randint(1, 3)])

if __name__ == "__main__":
    generate_csv()
    print("Wygenerowano pliki CSV.")
