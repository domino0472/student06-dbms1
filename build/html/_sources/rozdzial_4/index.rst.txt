/Author: [Damian Dominiak, Michał Bystrzak] / Date: 2026-05-15 / Version: 1.0 /

=======================================================
Rozdział 4. Definiowanie bazy i wprowadzanie danych
=======================================================

W tym rozdziale opisano mechanizmy wykorzystane do wsadowego wprowadzania danych testowych do baz SQLite oraz PostgreSQL dla systemu serwisu IT.

4.1. Generowanie danych testowych
---------------------------------
W celu symulacji rzeczywistego środowiska pracy serwisu sprzętu IT, przygotowano skrypt w języku Python, który automatycznie generuje losowe dane testowe (m.in. dane klientów, urządzeń, pracowników oraz zleceń i zużytych części) i eksportuje je do plików w formacie CSV.

4.2. Import danych do PostgreSQL
--------------------------------
Dla silnika PostgreSQL zdecydowano się na wykorzystanie natywnego mechanizmu ``COPY``. Pozwala on na najszybszy bulk-insert danych z plików CSV.

4.3. Import danych do SQLite
----------------------------
W przypadku bazy SQLite zaimplementowano skrypt w języku Python z wykorzystaniem wbudowanej biblioteki ``sqlite3``, który wczytuje dane z plików CSV i wykonuje instrukcje ``INSERT`` wewnątrz transakcji, co znacząco optymalizuje czas wstawiania setek rekordów.


