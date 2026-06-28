========================
Zapytania do bazy danych
========================

Autorzy: Michał Bystrzak, Damian Dominiak

Poniższa dokumentacja zawiera zaawansowane zapytania SQL zaimplementowane w projekcie, wykorzystujące mechanizmy takie jak podzapytania, złączenia (JOIN), agregacje oraz operatory zbiorowe w dialektach SQLite oraz PostgreSQL.

Średni koszt robocizny dla poszczególnych statusów
--------------------------------------------------
Zapytanie oblicza średni koszt robocizny dla poszczególnych statusów zleceń, wykorzystując agregację ``AVG()`` i grupowanie.

.. code-block:: sql

    SELECT Status, ROUND(AVG(Koszt_robocizny), 2) AS Sredni_koszt
    FROM ZLECENIE
    GROUP BY Status;

Marki urządzeń wymagające wymiany matrycy
-----------------------------------------
Zapytanie zwraca unikalne marki urządzeń, dla których kiedykolwiek wydano z magazynu część o nazwie "Matryca". Wykorzystuje podzapytanie z operatorem ``IN``.

.. code-block:: sql

    SELECT DISTINCT Marka 
    FROM URZADZENIE 
    WHERE ID_Urzadzenia IN (
        SELECT u.ID_Urzadzenia 
        FROM URZADZENIE u
        JOIN ZLECENIE z ON u.ID_Urzadzenia = z.ID_Urzadzenia
        JOIN ZUZYTE_CZESCI zc ON z.ID_Zlecenia = zc.ID_Zlecenia
        JOIN CZESC c ON zc.ID_Czesci = c.ID_Czesci
        WHERE c.Nazwa = 'Matryca'
    );

Klienci z oczekującymi zleceniami
---------------------------------
Wyszukuje klientów, którzy mają w systemie zlecenia o statusie "Oczekuje na części", korzystając z operatora ``EXISTS``.

.. code-block:: sql

    SELECT Imie, Nazwisko, Email 
    FROM KLIENT k 
    WHERE EXISTS (
        SELECT 1 
        FROM URZADZENIE u 
        JOIN ZLECENIE z ON u.ID_Urzadzenia = z.ID_Urzadzenia 
        WHERE u.ID_Klienta = k.ID_Klienta 
        AND z.Status = 'Oczekuje na części'
    );

Urządzenia bez historii zleceń (SQLite)
---------------------------------------
Zwraca listę urządzeń, dla których nie zarejestrowano jeszcze żadnego zlecenia serwisowego, wykorzystując operator zbiorowy ``EXCEPT``.

.. code-block:: sql

    SELECT Numer_seryjny FROM URZADZENIE
    EXCEPT
    SELECT u.Numer_seryjny 
    FROM URZADZENIE u 
    JOIN ZLECENIE z ON u.ID_Urzadzenia = z.ID_Urzadzenia;

Pracownicy powyżej średniej wydajności
--------------------------------------
Znajduje pracowników, którzy obsłużyli więcej zleceń niż wynosi średnia dla wszystkich pracowników. Wykorzystuje zaawansowane podzapytanie w klauzuli ``HAVING``.

.. code-block:: sql

    SELECT p.Imie, p.Nazwisko, COUNT(z.ID_Zlecenia) AS Liczba_Zlecen
    FROM PRACOWNIK p
    JOIN ZLECENIE z ON p.ID_Pracownika = z.ID_Pracownika
    GROUP BY p.ID_Pracownika
    HAVING COUNT(z.ID_Zlecenia) > (
        SELECT CAST(COUNT(ID_Zlecenia) AS FLOAT) / COUNT(DISTINCT ID_Pracownika) 
        FROM ZLECENIE
    );

Zlecenia droższe niż średnia cena części
----------------------------------------
Zwraca szczegóły zleceń, w których koszt robocizny jest większy niż średnia cena części z magazynu, wykorzystując skalarne podzapytanie w klauzuli ``WHERE``.

.. code-block:: sql

    SELECT ID_Zlecenia, Koszt_robocizny 
    FROM ZLECENIE 
    WHERE Koszt_robocizny > (SELECT AVG(Cena) FROM CZESC);

Miesięczne przychody z robocizny (PostgreSQL)
---------------------------------------------
Analizuje miesięczne przychody z robocizny w serwisie, wykorzystując funkcję wyciągającą datę ``EXTRACT()`` oraz agregację ``SUM()``.

.. code-block:: sql

    SELECT 
        EXTRACT(YEAR FROM Data_przyjecia) AS Rok, 
        EXTRACT(MONTH FROM Data_przyjecia) AS Miesiac, 
        SUM(Koszt_robocizny) AS Przychody 
    FROM ZLECENIE 
    GROUP BY Rok, Miesiac
    ORDER BY Rok DESC, Miesiac DESC;

Najczęściej zużywane części
---------------------------
Wyszukuje części, które zostały zużyte w więcej niż 5 różnych zleceniach, wykorzystując ``JOIN``, ``GROUP BY`` oraz klauzulę ``HAVING``.

.. code-block:: sql

    SELECT c.Nazwa, COUNT(zc.ID_Zlecenia) AS Liczba_Zlecen 
    FROM CZESC c 
    JOIN ZUZYTE_CZESCI zc ON c.ID_Czesci = zc.ID_Czesci 
    GROUP BY c.ID_Czesci, c.Nazwa 
    HAVING COUNT(zc.ID_Zlecenia) > 5;

Klienci o największych wydatkach
--------------------------------
Oblicza całkowity koszt zleceń dla poszczególnych klientów i zwraca tych z największymi wydatkami, wykorzystując złączenia wielu tabel.

.. code-block:: sql

    SELECT k.Imie, k.Nazwisko, SUM(z.Koszt_robocizny) AS Wydatki_Robocizna 
    FROM KLIENT k 
    JOIN URZADZENIE u ON k.ID_Klienta = u.ID_Klienta 
    JOIN ZLECENIE z ON u.ID_Urzadzenia = z.ID_Urzadzenia 
    GROUP BY k.ID_Klienta, k.Imie, k.Nazwisko 
    ORDER BY Wydatki_Robocizna DESC;

Całkowity koszt zlecenia (Robocizna + Części)
---------------------------------------------
Oblicza całkowity koszt zlecenia (robocizna + suma cen zużytych części przemnożona przez ich ilość). Wykorzystuje wielokrotne ``JOIN`` oraz funkcję ``COALESCE()``.

.. code-block:: sql

    SELECT 
        z.ID_Zlecenia, 
        (z.Koszt_robocizny + COALESCE(SUM(c.Cena * zc.Ilosc), 0)) AS Calkowity_Koszt 
    FROM ZLECENIE z 
    LEFT JOIN ZUZYTE_CZESCI zc ON z.ID_Zlecenia = zc.ID_Zlecenia 
    LEFT JOIN CZESC c ON zc.ID_Czesci = c.ID_Czesci 
    GROUP BY z.ID_Zlecenia, z.Koszt_robocizny;