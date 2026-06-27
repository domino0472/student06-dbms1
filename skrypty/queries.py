"""
Moduł realizujący zaawansowane zapytania SQL do baz danych SQLite oraz PostgreSQL.
Wykorzystywany w Rozdziale 5 sprawozdania laboratoryjnego.
"""

import sqlite3
import psycopg2

# ==========================================
# ZAPYTANIA DLA BAZY SQLITE
# ==========================================

def get_top_clients_by_spend_sqlite(db_path):
    """
    Oblicza całkowity koszt zleceń dla poszczególnych klientów i zwraca tych z największymi wydatkami.
    Wykorzystuje **JOIN** oraz **GROUP BY** z funkcją agregującą **SUM()**.

    :param db_path: Ścieżka do pliku bazy danych SQLite.
    :type db_path: str
    :return: Lista krotek zawierająca dane klienta oraz sumę kosztów robocizny.
    :rtype: list
    """
    query = """
        SELECT K.Imie, K.Nazwisko, SUM(Z.Koszt_robocizny) as Laczny_Koszt
        FROM KLIENT K
        JOIN URZADZENIE U ON K.ID_Klienta = U.ID_Klienta
        JOIN ZLECENIE Z ON U.ID_Urzadzenia = Z.ID_Urzadzenia
        GROUP BY K.ID_Klienta
        ORDER BY Laczny_Koszt DESC
        LIMIT 5;
    """
    with sqlite3.connect(db_path) as conn:
        return conn.execute(query).fetchall()

def get_devices_without_orders_sqlite(db_path):
    """
    Zwraca listę urządzeń, dla których nie zarejestrowano jeszcze żadnego zlecenia serwisowego.
    Wykorzystuje operator zbiorowy **EXCEPT**.

    :param db_path: Ścieżka do pliku bazy danych SQLite.
    :type db_path: str
    :return: Lista numerów seryjnych urządzeń bez zleceń.
    :rtype: list
    """
    query = """
        SELECT ID_Urzadzenia FROM URZADZENIE
        EXCEPT
        SELECT ID_Urzadzenia FROM ZLECENIE;
    """
    with sqlite3.connect(db_path) as conn:
        return conn.execute(query).fetchall()

def get_average_cost_per_status_sqlite(db_path):
    """
    Oblicza średni koszt robocizny dla poszczególnych statusów zleceń.
    Wykorzystuje agregację **AVG()** i grupowanie.

    :param db_path: Ścieżka do pliku bazy SQLite.
    :type db_path: str
    :return: Lista krotek ze statusem i średnim kosztem.
    :rtype: list
    """
    query = "SELECT Status, AVG(Koszt_robocizny) FROM ZLECENIE GROUP BY Status;"
    with sqlite3.connect(db_path) as conn:
        return conn.execute(query).fetchall()

def get_parts_used_in_multiple_orders_sqlite(db_path):
    """
    Wyszukuje części, które zostały zużyte w więcej niż 5 różnych zleceniach.
    Wykorzystuje **JOIN**, **GROUP BY** oraz klauzulę **HAVING**.

    :param db_path: Ścieżka do pliku bazy SQLite.
    :type db_path: str
    :return: Lista nazw części oraz liczby zleceń.
    :rtype: list
    """
    query = """
        SELECT C.Nazwa, COUNT(ZC.ID_Zlecenia) as Liczba_Zlecen
        FROM CZESC C
        JOIN ZUZYTE_CZESCI ZC ON C.ID_Czesci = ZC.ID_Czesci
        GROUP BY C.ID_Czesci
        HAVING Liczba_Zlecen > 5;
    """
    with sqlite3.connect(db_path) as conn:
        return conn.execute(query).fetchall()

def get_employees_above_avg_orders_sqlite(db_path):
    """
    Znajduje pracowników, którzy obsłużyli więcej zleceń niż wynosi średnia dla wszystkich pracowników.
    Wykorzystuje zaawansowane **podzapytanie (Subquery)** w klauzuli HAVING.

    :param db_path: Ścieżka do pliku bazy SQLite.
    :type db_path: str
    :return: Lista krotek z danymi pracownika i liczbą obsłużonych zleceń.
    :rtype: list
    """
    query = """
        SELECT P.Imie, P.Nazwisko, COUNT(Z.ID_Zlecenia) as Liczba
        FROM PRACOWNIK P
        JOIN ZLECENIE Z ON P.ID_Pracownika = Z.ID_Pracownika
        GROUP BY P.ID_Pracownika
        HAVING Liczba > (
            SELECT CAST(COUNT(ID_Zlecenia) AS REAL) / COUNT(DISTINCT ID_Pracownika) FROM ZLECENIE
        );
    """
    with sqlite3.connect(db_path) as conn:
        return conn.execute(query).fetchall()


# ==========================================
# ZAPYTANIA DLA BAZY POSTGRESQL
# ==========================================

def get_monthly_revenue_pg(db_params):
    """
    Analizuje miesięczne przychody z robocizny w serwisie.
    Wykorzystuje funkcję wyciągającą datę **EXTRACT()** oraz agregację **SUM()**.

    :param db_params: Słownik z parametrami logowania do PostgreSQL (dbname, user, password, host, port).
    :type db_params: dict
    :return: Lista krotek (rok, miesiąc, suma przychodów).
    :rtype: list
    """
    query = """
        SELECT EXTRACT(YEAR FROM Data_przyjecia) as Rok, 
               EXTRACT(MONTH FROM Data_przyjecia) as Miesiac, 
               SUM(Koszt_robocizny) as Przychody
        FROM ZLECENIE
        GROUP BY Rok, Miesiac
        ORDER BY Rok DESC, Miesiac DESC;
    """
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def get_expensive_orders_pg(db_params):
    """
    Zwraca szczegóły zleceń, w których koszt robocizny jest większy niż średnia cena części z magazynu.
    Wykorzystuje **skalarne podzapytanie w klauzuli WHERE**.

    :param db_params: Parametry połączenia do bazy.
    :type db_params: dict
    :return: ID zlecenia i koszt robocizny.
    :rtype: list
    """
    query = """
        SELECT ID_Zlecenia, Koszt_robocizny
        FROM ZLECENIE
        WHERE Koszt_robocizny > (SELECT AVG(Cena) FROM CZESC);
    """
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def get_total_cost_per_order_pg(db_params):
    """
    Oblicza całkowity koszt zlecenia (robocizna + suma cen zużytych części).
    Wykorzystuje **wielokrotne JOIN** oraz zaawansowaną arytmetykę w wierszach.

    :param db_params: Parametry połączenia do bazy.
    :type db_params: dict
    :return: Lista krotek (ID_Zlecenia, Całkowity Koszt).
    :rtype: list
    """
    query = """
        SELECT Z.ID_Zlecenia, 
               Z.Koszt_robocizny + COALESCE(SUM(C.Cena * ZC.Ilosc), 0) as Calkowity_Koszt
        FROM ZLECENIE Z
        LEFT JOIN ZUZYTE_CZESCI ZC ON Z.ID_Zlecenia = ZC.ID_Zlecenia
        LEFT JOIN CZESC C ON ZC.ID_Czesci = C.ID_Czesci
        GROUP BY Z.ID_Zlecenia, Z.Koszt_robocizny;
    """
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def get_brands_needing_parts_pg(db_params):
    """
    Zwraca marki urządzeń, dla których kiedykolwiek wydano z magazynu część o nazwie 'Matryca'.
    Wykorzystuje podzapytanie z operatorem **IN**.

    :param db_params: Parametry połączenia do bazy.
    :type db_params: dict
    :return: Unikalne nazwy marek urządzeń.
    :rtype: list
    """
    query = """
        SELECT DISTINCT Marka FROM URZADZENIE
        WHERE ID_Urzadzenia IN (
            SELECT Z.ID_Urzadzenia 
            FROM ZLECENIE Z
            JOIN ZUZYTE_CZESCI ZC ON Z.ID_Zlecenia = ZC.ID_Zlecenia
            JOIN CZESC C ON ZC.ID_Czesci = C.ID_Czesci
            WHERE C.Nazwa = 'Matryca'
        );
    """
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def get_clients_with_unresolved_orders_pg(db_params):
    """
    Wyszukuje klientów, którzy mają w systemie zlecenia o statusie 'Oczekuje na części' korzystając z operatora **EXISTS**.

    :param db_params: Parametry połączenia do bazy.
    :type db_params: dict
    :return: Dane klientów.
    :rtype: list
    """
    query = """
        SELECT Imie, Nazwisko FROM KLIENT K
        WHERE EXISTS (
            SELECT 1 FROM URZADZENIE U
            JOIN ZLECENIE Z ON U.ID_Urzadzenia = Z.ID_Urzadzenia
            WHERE U.ID_Klienta = K.ID_Klienta AND Z.Status = 'Oczekuje na części'
        );
    """
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
