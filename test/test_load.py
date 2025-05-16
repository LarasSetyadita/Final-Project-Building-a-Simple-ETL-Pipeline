import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import store_to_postgre, create_database, store_to_csv, store_to_spreadsheet


class TestETLFunctions(unittest.TestCase):
    def setUp(self):
        # DataFrame dummy
        self.df = pd.DataFrame({
            'product_title': ['Product A'],
            'price': [29.99],
            'ratings': [4.5],
            'colors': [2],
            'size': ['M'],
            'gender': ['Unisex'],
            'timestamp': [pd.Timestamp('2023-01-01 00:00:00')]
        })

    def test_store_to_csv(self):
        store_to_csv(self.df)
        read_back = pd.read_csv('products.csv')
        read_back["timestamp"] = pd.to_datetime(read_back["timestamp"])
        pd.testing.assert_frame_equal(self.df, read_back)

    def test_store_to_spreadsheet(self):
        store_to_spreadsheet(self.df)
        read_back = pd.read_excel('products.xlsx', engine='openpyxl')
        pd.testing.assert_frame_equal(self.df, read_back)

    @patch('utils.load.psycopg2.connect')
    def test_create_database(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # database belum ada

        create_database("testdb")
        mock_cursor.execute.assert_any_call(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", ("testdb",)
        )

    @patch('utils.load.create_engine')
    @patch('utils.load.psycopg2.connect')
    def test_store_to_postgre_success(self, mock_pg_connect, mock_create_engine):
        # Setup mock psycopg2 connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_pg_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # Setup mock SQLAlchemy engine
        mock_engine = MagicMock()
        mock_connection = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__.return_value = mock_connection

        # Simulate to_sql method on mock connection
        self.df.to_sql = MagicMock()

        store_to_postgre(self.df, "postgresql://developer:supersecretpassword@localhost:5432/productsdb")
        self.df.to_sql.assert_called_once()

    def test_store_to_postgre_missing_column(self):
        df_missing = self.df.drop(columns=["ratings"])
        with self.assertRaises(ValueError):
            store_to_postgre(df_missing, "postgresql://developer:supersecretpassword@localhost:5432/productsdb")


if __name__ == '__main__':
    unittest.main()
