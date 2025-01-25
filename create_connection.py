import logging
import sqlite3
from contextlib import contextmanager
import os

database = "./database/college_data.sqlite"
logging.basicConfig(level=logging.INFO)


@contextmanager
def get_connection(db=database):
    connection = None
    if not os.path.exists(os.path.dirname(db)):
        os.mkdir(os.path.dirname(db))
    try:
        connection = sqlite3.connect(db)
        yield connection
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
    finally:
        if connection:
            connection.close()
