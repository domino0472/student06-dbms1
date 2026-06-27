/Author: [Damian Dominiak, Michal Bystrzak] / Date: 2026-05-15 / Version: 1.0 /

===============================
Rozdział 1. Wprowadzenie
===============================

1.1. Repozytoria wykorzystane w projekcie
-----------------------------------------
Poniżej znajdują się odnośniki do repozytoriów zawierających kody źródłowe oraz dokumentację sprawozdania:

* **Sprawozdanie główne i dokumentacja (Sphinx):** `[Wklej link do repozytorium GitHub] <https://github.com/...>`_
* **Badania literaturowe (Michał Bystrzak):** `[Wklej link do podłączonego repozytorium] <https://github.com/...>`_
* **Eksperymenty i skrypty bazodanowe:** `[Wklej link do repozytorium ze skryptami .py] <https://github.com/...>`_

1.2. Opis tematyki projektu
---------------------------
Przedmiotem niniejszego projektu jest zaprojektowanie, zdefiniowanie oraz obsługa relacyjnej bazy danych dla systemu zarządzania serwisem sprzętu IT. Aplikacja docelowa ma za zadanie obsługiwać pełen cykl życia zlecenia serwisowego – od momentu przyjęcia sprzętu od klienta, poprzez diagnozę i zużycie części magazynowych, aż po ostateczne rozliczenie i wydanie naprawionego urządzenia. 

W ramach zajęć laboratoryjnych przygotowano schematy (koncepcyjny, logiczny i fizyczny), przeprowadzono normalizację bazy oraz przetestowano proces wprowadzania danych testowych i wykonywania zaawansowanych zapytań SQL w dwóch środowiskach: **SQLite** oraz **PostgreSQL**.

1.3. Wnioski końcowe z zajęć laboratoryjnych
--------------------------------------------
Przeprowadzone ćwiczenia i eksperymenty pozwoliły na wyciągnięcie następujących wniosków:

* **Projektowanie struktury:** Normalizacja do 3. postaci normalnej (3NF) jest kluczowa w systemach takich jak zarządzanie zleceniami, aby uniknąć redundancji danych i anomalii przy aktualizacji statusów zleceń lub magazynu.
* **Proces importu danych:** Mechanizm ``COPY`` dostępny w PostgreSQL znacząco przewyższa wydajnością wielokrotne instrukcje ``INSERT`` w SQLite podczas wsadowego ładowania dużych zbiorów danych (np. tysięcy zużytych części). 
* **Różnice w dialektach SQL:** Choć oba silniki wspierają standard SQL, widoczne są różnice w zaawansowanych funkcjach wierszowych oraz mechanizmach auto-inkrementacji (``SERIAL`` w PostgreSQL vs zintegrowany mechanizm dla kluczy głównych w SQLite). PostgreSQL oferuje znacznie bogatszy system typów (np. precyzyjny typ ``NUMERIC`` dla kosztów robocizny).


