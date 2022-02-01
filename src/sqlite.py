import sqlite3
from sqlite3 import Error
import traceback


class Sqlite:
    """Manages conection with sqlite database.

    Attributes:
        sqlite_db: the name od slqlite database
            Which is is located in main folder
        conn: sqlite connection object
        cursor: sqlite cursor object

    Methods:
        query_to_list: Execute query and return list

    """
    def __init__(self, sqlite3_db: str = None) -> None:
        if sqlite3_db is None:
            self.sqlite3_db = 'sqlite.db'
        else:
            self.sqlite3_db = sqlite3_db

    def __enter__(self):
        return self.__create_connection()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.__close_connection()

    def __create_connection(self):
        """Creates connection with database."""
        try:
            self.conn = sqlite3.connect(self.sqlite3_db)
            self.cursor = self.conn.cursor()
            return self
        except Error:
            traceback.print_exc()
            return None

    def __close_connection(self) -> None:
        """Close connection with database."""
        try:
            self.cursor.close()
            self.conn.close()
        except Error:
            traceback.print_exc()

    def __query(self, sql_str: str):
        """Executes sql query on connected database.

        Args:
            sql_str: sql query as a string
        """

        try:
            self.cursor.execute(sql_str)
        except Exception:
            traceback.print_exc()

    def __query_to_list(self):
        """Fetches everything from cursor and put it to list.

        Resturn:
            list: results from query inquary
        """
        try:
            return [item[0] for item in self.cursor]
        except Error:
            traceback.print_exc()

    def query_to_list(self, sql_str: str):
        """Connect '__query' and '__query_to_list' methods.

        1.Executes sql query on connected database.
        2.Fetches everything from cursor and put it to list.

        Resturn:
            list: results from query
                ONLY FIRST COLUMN!!!
        """

        self.__query(sql_str)
        return self.__query_to_list()

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
    #
    # def insert_record(self, an_DokId, an_DokNazwa, an_KhSym, an_Stany, an_Ceny, an_Czas):
    #     """Insert proceded dokument"""
    #
    #     query = ''' INSERT INTO
    #                     AnalizaDokomentow(an_DokId,an_DokNazwa,an_KhSym,an_Stany,an_Ceny,an_Czas)
    #                     VALUES(?,?,?,?,?,?) '''
    #
    #     values = [an_DokId, an_DokNazwa, an_KhSym, an_Stany, an_Ceny, an_Czas]
    #     try:
    #         self.cursor.execute(query, values)
    #         self.conn.commit()
    #     except Exception as e:
    #         traceback.print_exc()
    #
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
    #
    # def select_all_doc_ids(self) -> list:
    #     query = "SELECT an_DokId FROM AnalizaDokomentow"
    #     try:
    #         self.cursor.execute(query)
    #         an_DokId = [x[0] for x in self.cursor.fetchall()]
    #         return an_DokId
    #     except Error as e:
    #         traceback.print_exc()
    #
    # def _to_df(self, list_of_dict: list, columns: list=None) -> pd.DataFrame:
    #     try:
    #         df = pd.DataFrame(list_of_dict)
    #         if columns is not None and df.shape[1] == len(columns):
    #             df.columns = columns
    #         return df
    #     except Exception as e:
    #         traceback.print_exc()
    #
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
    #
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
    #
    # def delete(self, query, values):
    #     '''DELETE FROM tasks WHERE id=?'''
    #     try:
    #         self.cursor.execute(query, (values,))
    #         self.conn.commit()
    #     except Error as e:
    #         traceback.print_exc()
    #
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
