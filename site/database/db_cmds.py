import sqlite3
from sqlite3 import Cursor
from typing import Any, Generator
import logging

from contextlib import contextmanager

DATABASE = "database/sqlite.db"


class Database:
    def __init__(self, path: str = DATABASE):
        self.__path = path

    def __create_connection(self) -> sqlite3.Connection | None:
        try:
            connection = sqlite3.connect(
                self.__path,
                check_same_thread=False,
            )
        except sqlite3.Error as err:
            connection = None
            print(err)
        return connection

    @contextmanager
    def cursor(self) -> Generator[Cursor, Any, None]:
        """
        Provides a database connection as a context manager.

        Yields:
            sqlite3.Cursor: A cursor for interacting with the database.
        """
        conn = self.__create_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except sqlite3.Error as err:
            logging.error(f"Database error: {err}")
            if conn:
                conn.rollback()
            raise  # Re-raise the exception after logging and rollback
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def setup(self) -> None:
        return

    def reset(self) -> None:
        return
