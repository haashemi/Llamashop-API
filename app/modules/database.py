"""
Small and simple Library for Sqlite3
First Version Creator: omidnw
New Version Creator: MR-AliHaashemi

https://github.com/omidnw/Sqlite3-Management
"""
import sqlite3


class Database:
    """Class of database functions"""

    def __init__(self, db_name: str = "database.db"):
        """
        Connects to database and be ready to call functions
        You also can pass your main table name if you want to use one table
        for many times

        Parameters
        ----------
        - db_name : str :
            Name or FilePath of your sqlite database.
            It creates if that db not found
            Defaut is "database.db"
        """
        try:
            self.database = sqlite3.connect(db_name)
        except sqlite3.Error as sql_error:
            raise sql_error

    # >>> Functions to working with table >>>
    # _________________________________________

    def create_table(self, table_name: str, column_name: str) -> bool:
        """Creates a table inside connected database with some columns"""
        try:
            self.database.execute(f'CREATE TABLE {table_name}({column_name})')
            self.database.commit()
            return True
        except sqlite3.Error:
            return False

    def get_tables_name(self) -> list:
        """Return name of tables in your database"""
        try:
            self.database.row_factory = lambda cursor, row: row[0]
            cursor = self.database.cursor()
            return cursor.execute(
                "SELECT tbl_name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        except sqlite3.Error:
            return []

    def read_table(self, table_name: str = None, read_all: bool = False) -> list:
        """Read all/first column(s) of table"""
        if not read_all:  # Gets only first column of database
            self.database.row_factory = lambda cursor, row: row[0]

        try:
            return self.database.execute(f'SELECT * FROM {table_name}').fetchall()
        except sqlite3.Error:
            return []

    def delete_table(self, table_name: str) -> bool:
        """Delete table of database"""
        try:
            self.database.execute(f'DROP TABLE IF EXISTS {table_name}')
            self.database.commit()
            return True
        except sqlite3.Error:
            return False

    # >>> Functions to working with valus inside of table >>>
    # ________________________________________________________

    def insert_value(self, table_name, column_name, value) -> bool:
        """Insert value(s) in to table"""
        try:
            self.database.execute(
                f'INSERT OR REPLACE INTO {table_name}({column_name}) VALUES ({value})')
            self.database.commit()
            return True
        except sqlite3.Error:
            return False

    def update_value(self, table_name, update_string, where) -> bool:
        """Update a value of table"""
        try:
            self.database.execute(
                f"UPDATE {table_name} SET {update_string} WHERE {where}")
            self.database.commit()
            return True
        except sqlite3.Error:
            return False

    def read_one_value(self, table_name: str, column_name: str, where: str = None):
        """Read only one value of table"""
        cursor = self.database.cursor()
        base_string = f"""SELECT {column_name} FROM {table_name}"""

        try:
            if where is None:
                return cursor.execute(base_string).fetchone()
            return cursor.execute(f"{base_string} WHERE {where}").fetchone()
        except sqlite3.Error:
            return None

    def read_values(self, table_name: str, column_name: str, where: str = None) -> list:
        """Read only all values of table"""
        cursor = self.database.cursor()
        base_string = f"SELECT {column_name} FROM {table_name}"

        try:
            if where is None:
                return cursor.execute(base_string).fetchall()
            return cursor.execute(f"{base_string} WHERE {where}").fetchall()
        except sqlite3.Error:
            return []

    def delete_value(self, table_name, column_name, value_name) -> bool:
        """Delete value from table"""
        try:
            self.database.execute(
                f"DELETE FROM {table_name}WHERE {column_name}='{value_name}'")
            self.database.commit()
            return True
        except sqlite3.Error:
            return False
