import pytest
import sqlite3
from src.moduls.Sqlite import Sqlite


try:
    with Sqlite() as sql:
        sql.query("""
                SELECT DISTINCT waga_Norma
                FROM waga""")

        print(sql._query_to_list())

except Exception as e:
    print(e)













