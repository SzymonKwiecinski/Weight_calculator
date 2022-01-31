import os
from pytest import mark


@mark.sqlite
def test_db_file_exist_in_main_dir():
    files = os.listdir()
    assert 'sqlite.db' in files

@mark.sqlite
def test_table_waga_exist_in_db(sql):
    assert sql.query_to_list("SELECT name FROM sqlite_master") == ['waga']

@mark.sqlite
@mark.parametrize('column_name',[
    'waga_Id',
    'waga_Norma',
    'waga_Rozmiar1',
    'waga_rozmiar2',
    'waga_Waga1000szt'])
def test_query(sql, column_name):
    result = sql.query_to_list(f"SELECT {column_name} FROM waga LIMIT 1")
    assert 1 == len(result)






