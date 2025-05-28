import mysql.connector
import os
import pandas as pd

from dotenv import load_dotenv

load_dotenv()


class Database:
    """
    A class that holds information about the database.
    """

    HOST = os.environ.get("HOST")
    USER = os.environ.get("DATABASE_USER")
    PASSWORD = os.environ.get("PASSWORD")

    def __init__(self):
        """Instantiates the 'Database' object with a connection to the database."""

        self.database = os.environ.get("DATABASE")

        self.connection = mysql.connector.connect(
            host=__class__.HOST,
            user=__class__.USER,
            password=__class__.PASSWORD,
            database=self.database,
        )

    def get_columns(self):
        """Returns the columns of the database."""

        if self.database and self.connection.is_connected():
            with self.connection.cursor() as cursor:
                _ = cursor.execute(f"SHOW COLUMNS FROM {self.database}")

                return [_[0] for _ in cursor.fetchall()]

    def get_data(self):
        """Returns the data of the database."""

        if self.database and self.connection.is_connected():
            df = pd.read_sql(f"SELECT * FROM {self.database}", con=self.connection)
            df.drop(columns=["id"], inplace=True)

            return df
