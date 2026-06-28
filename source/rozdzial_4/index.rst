=======================================
Definiowanie bazy i wprowadzanie danych
=======================================

Autorzy: Michał Bystrzak, Damian Dominiak

W tym rozdziale opisano mechanizmy wykorzystane do wsadowego wprowadzania danych testowych do baz SQLite oraz PostgreSQL dla systemu serwisu IT.

Generowanie danych testowych
----------------------------
W celu symulacji rzeczywistego środowiska pracy serwisu sprzętu IT, przygotowano skrypt w języku Python. Wykorzystuje on bibliotekę ``csv`` do automatycznego generowania losowych danych (m.in. części magazynowych, zleceń) i eksportowania ich do płaskich plików.

.. code-block:: python

   import csv
   import random

   # Generator danych dla tabeli CZESC
   czesci = []
   dostawcy = ["Intel", "AMD", "Samsung", "Asus", "Nvidia"]
   for i in range(1, 101):
       czesci.append([i, f"Podzespol_Serwisowy_{i}", random.choice(dostawcy), random.randint(0, 50), round(random.uniform(20.0, 1500.0), 2)])

   with open('czesci.csv', 'w', newline='', encoding='utf-8') as file:
       writer = csv.writer(file)
       writer.writerow(["ID_Czesci", "Nazwa", "Producent", "Stan_magazynowy", "Cena"])
       writer.writerows(czesci)

Import danych do PostgreSQL
---------------------------
Dla silnika PostgreSQL zdecydowano się na wykorzystanie natywnego mechanizmu ``COPY``. Pozwala on na błyskawiczny bulk-insert danych bezpośrednio z plików CSV do tabeli ``CZESC``, omijając ogromny narzut wydajnościowy tradycyjnych instrukcji ``INSERT``.

.. code-block:: sql

   -- Skrypt ładujący części magazynowe zgodnie ze strukturą zdefiniowaną w modelu fizycznym
   COPY CZESC(ID_Czesci, Nazwa, Producent, Stan_magazynowy, Cena)
   FROM '/tmp/dane_testowe/czesci.csv'
   DELIMITER ','
   CSV HEADER;

Import danych do SQLite
-----------------------
W przypadku bazy SQLite zaimplementowano skrypt w języku Python z wykorzystaniem wbudowanej biblioteki ``sqlite3``. Skrypt wczytuje dane i ładuje je np. do tabeli ``PRACOWNIK`` wewnątrz jednej spójnej transakcji, co drastycznie optymalizuje czas wstawiania rekordów.

.. code-block:: python

   import sqlite3
   import csv

   conn = sqlite3.connect('serwis_it.db')
   cursor = conn.cursor()

   with open('pracownicy.csv', 'r', encoding='utf-8') as file:
       dr = csv.DictReader(file)
       to_db = [(i['Imie'], i['Nazwisko'], i['Stanowisko']) for i in dr]

   # Wykorzystanie executemany() dla optymalizacji transakcji
   cursor.executemany(
       "INSERT INTO PRACOWNIK (Imie, Nazwisko, Stanowisko) VALUES (?, ?, ?);", to_db
   )
   
   conn.commit()
   conn.close()