# import mysql.connector
import dask.dataframe as dd
import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, text, select, column
from sqlalchemy.orm import Session

load_dotenv()

# While dask dataframes are for larger databases, the overhead is worth it at this size, thus making the operation overall faster.
time_to_use_dask = 100


class EmptyDatabase:
    pass

class Database:
    """A class that holds information about the database."""

    DATABASE = os.environ.get("DATABASE")
    HOST = os.environ.get("HOST")
    USER = os.environ.get("USER")
    PASSWORD = os.environ.get("PASSWORD")

    def __init__(self, port: int = 3306):
        """
        Instantiates the 'Database' object with a connection to the database.
        ---
        Parameters:
            port, int: The port used to connect to the MySQL server. Defaults to the default of 3306.
        """

        self.port = port
        self.connection_str = f"mysql+pymysql://{__class__.USER}:{__class__.PASSWORD}@{__class__.HOST}:{self.port}/{__class__.DATABASE}"
        self.engine = create_engine(self.connection_str)

        self.size = self._get_size

    @property
    def _get_size(self):
        """Returns the size of the database."""

        query = f"""
            SELECT
                table_schema AS "database name",
                SUM(data_length + index_length) / 1024 / 1024 AS "database size in MB"
            FROM
                information_schema.TABLES
            WHERE
                table_schema = '{__class__.DATABASE}'
            GROUP BY
                table_schema;
        """

        with Session(self.engine) as session:
            result = session.execute(text(query)).fetchone()
            if result:
                _, size = result
                return size
            else:
                raise EmptyDatabase

    def get_data(self):
        """Returns the data of the database."""

        if self.size > time_to_use_dask:
            print("Using Dask to collect the data from the MySQL database.")
            df = dd.read_sql_table(
                __class__.DATABASE,
                con=self.connection_str,
                index_col='id',
            )
            df = df.compute()
        else:
            print("Using Pandas to collect the data from the MySQL database.")
            df = pd.read_sql_table(
                __class__.DATABASE,
                con=self.connection_str,
                index_col='id',)

        return df
