============
Wprowadzenie
============

Autor: Michał Bystrzak

Repozytoria wykorzystane w projekcie
------------------------------------
Poniżej znajdują się odnośniki do repozytoriów zawierających kody źródłowe oraz dokumentację sprawozdania:

* **Sprawozdanie główne i dokumentacja:** https://github.com/bystrzakmichal/student04-dbms1
* **Badania literaturowe (Michał Bystrzak):** https://github.com/bystrzakmichal/Partycjonowanie-Danych

Opis tematyki projektu
----------------------
Przedmiotem niniejszego projektu jest zaprojektowanie, zdefiniowanie oraz obsługa relacyjnej bazy danych dla systemu zarządzania serwisem sprzętu IT. Aplikacja docelowa ma za zadanie obsługiwać pełen cykl życia zlecenia serwisowego – od momentu przyjęcia sprzętu od klienta, poprzez diagnozę i zużycie części magazynowych, aż po ostateczne rozliczenie i wydanie naprawionego urządzenia.

W ramach zajęć laboratoryjnych przygotowano schematy (koncepcyjny, logiczny i fizyczny), przeprowadzono normalizację bazy oraz przetestowano proces wprowadzania danych testowych i wykonywania zaawansowanych zapytań SQL w dwóch środowiskach: SQLite oraz PostgreSQL.

Wnioski końcowe z zajęć laboratoryjnych
---------------------------------------
Przeprowadzone ćwiczenia i eksperymenty pozwoliły na wyciągnięcie następujących wniosków:

* **Projektowanie struktury:** Normalizacja do 3. postaci normalnej (3NF) jest kluczowa w systemach takich jak zarządzanie zleceniami, aby uniknąć redundancji danych i anomalii przy aktualizacji statusów zleceń lub magazynu.
* **Proces importu danych:** Mechanizm COPY dostępny w PostgreSQL znacząco przewyższa wydajnością wielokrotne instrukcje INSERT w SQLite podczas wsadowego ładowania dużych zbiorów danych (np. tysięcy zużytych części).
* **Różnice w dialektach SQL:** Choć oba silniki wspierają standard SQL, widoczne są różnice w zaawansowanych funkcjach wierszowych oraz mechanizmach auto-inkrementacji (SERIAL w PostgreSQL vs zintegrowany mechanizm dla kluczy głównych w SQLite). PostgreSQL oferuje znacznie bogatszy system typów (np. precyzyjny typ NUMERIC dla kosztów robocizny).