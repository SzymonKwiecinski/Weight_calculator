import secrets
import sys
import os
sys.path.append(f'{os.path.abspath("")}\\venv')
sys.path.append(f'{os.path.abspath("")}\\venv\\Scripts')
sys.path.append(f'{os.path.abspath("")}\\venv\\Lib\\site-packages')
import sqlite3
from sqlite3 import Error
import pandas as pd
import traceback


class Sqlite:

    def __init__(self, sqlite3_db=None) -> None:
        if sqlite3_db is None:
            self.sqlite3_db = 'sqlite.db'
        else:
            self.sqlite3_db = sqlite3_db
    
    def __enter__(self):
        return self.create_connection()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close_connection()

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.sqlite3_db)
            self.cursor = self.conn.cursor()
            print(f'{self.sqlite3_db} - connect')
            return self
        except Error as e:
            traceback.print_exc()
            return None
    
    def close_connection(self):
        try:
            self.cursor.close()
            print(f'{self.sqlite3_db} cursor close')
        except Error as e:
            traceback.print_exc()
        try:
            self.conn.close()
            print(f'{self.sqlite3_db} connection close')
        except Error as e:
            traceback.print_exc()

    def query(self, sql_str: str):
        try:
            self.cursor.execute(sql_str)
        except Exception:
            traceback.print_exc()
    
    def _query_to_list(self):
        try:
            return [item[0] for item in self.cursor]
        except Exception:
            traceback.print_exc()
    
    
    
    
    #############
    # def create_table(self, query):
    #     """ create a table from the create_table_sql statement
    #     :param conn: Connection object
    #     :param create_table_sql: a CREATE TABLE statement
    #     :return:
    #     """
    #     try:
    #         self.cursor.execute(query)
    #     except Error as e:
    #         traceback.print_exc()

    # def insert_record(self, an_DokId, an_DokNazwa, an_KhSym, an_Stany, an_Ceny, an_Czas):
    #     """Insert proceded dokument"""

    #     query = ''' INSERT INTO
    #                     AnalizaDokomentow(an_DokId,an_DokNazwa,an_KhSym,an_Stany,an_Ceny,an_Czas)
    #                     VALUES(?,?,?,?,?,?) '''
        
    #     values = [an_DokId, an_DokNazwa, an_KhSym, an_Stany, an_Ceny, an_Czas]
    #     try:
    #         self.cursor.execute(query, values)
    #         self.conn.commit()
    #     except Exception as e:
    #         traceback.print_exc()

    # def select_all(self):
    #     query = "SELECT * FROM AnalizaDokomentow"
    #     columns = ['an_Id','an_DokId','an_DokNazwa','an_KhSym','an_Stany','an_Ceny','an_Czas']
    #     try:
    #         self.cursor.execute(query)
    #         df = self._to_df(self.cursor.fetchall(), columns)
    #         df['an_Czas'] = pd.to_datetime(df['an_Czas'])
    #         return df
    #     except Error as e:
    #         traceback.print_exc()

    # def select_all_doc_ids(self) -> list:
    #     query = "SELECT an_DokId FROM AnalizaDokomentow"
    #     try:
    #         self.cursor.execute(query)
    #         an_DokId = [x[0] for x in self.cursor.fetchall()]
    #         return an_DokId
    #     except Error as e:
    #         traceback.print_exc()

    # def _to_df(self, list_of_dict: list, columns: list=None) -> pd.DataFrame:
    #     try:
    #         df = pd.DataFrame(list_of_dict)
    #         if columns is not None and df.shape[1] == len(columns):
    #             df.columns = columns
    #         return df
    #     except Exception as e:
    #         traceback.print_exc()      


####################
    # def insert(self, query, values):
    #     ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
    #           VALUES(?,?,?,?,?,?) '''
    #     try:
    #         self.cursor.execute(query, values)
    #         self.conn.commit()
    #         return self.cursor.lastrowid
    #     except Error as e:
    #         traceback.print_exc()
    
    # def update(self, query, values):
    #     ''' UPDATE tasks
    #           SET priority = ? ,
    #               begin_date = ? ,
    #               end_date = ?
    #           WHERE id = ?'''
    #     try:
    #         self.cursor.execute(query, values)
    #         self.conn.commit()
    #     except Error as e:
    #         traceback.print_exc()
    
    # def delete(self, query, values):
    #     '''DELETE FROM tasks WHERE id=?'''
    #     try:
    #         self.cursor.execute(query, (values,))
    #         self.conn.commit()
    #     except Error as e:
    #         traceback.print_exc()
    
    # def select(self, query, values):
    #     "SELECT * FROM tasks WHERE priority=?"
    #     try:
    #         self.cursor.execute(query, (values,))
    #         return self._fetchall_to_list_of_dict()
    #     except Error as e:
    #         traceback.print_exc()

    # def _to_list_of_dict(self):
    #     try:
    #         list_of_dict = []
    #         for row in self.cursor.fetchall():
    #             d_poz = { i_x:row_x  for i_x, row_x in enumerate(row)}
    #             list_of_dict.append(d_poz)
    #             print(list_of_dict) 
    #         return list_of_dict
    #     except Error as e:
    #         traceback.print_exc()
