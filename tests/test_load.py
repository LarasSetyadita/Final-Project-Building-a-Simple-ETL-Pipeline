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

        self.spreadsheet_id = 'dummy_spreadsheet_id'
        self.worksheet_name = 'Sheet1'

    def test_store_to_csv(self):
        store_to_csv(self.df)
        read_back = pd.read_csv('products.csv')
        read_back["timestamp"] = pd.to_datetime(read_back["timestamp"])
        pd.testing.assert_frame_equal(self.df, read_back)

    @patch('utils.load.set_with_dataframe')
    @patch('utils.load.gspread.authorize')
    @patch('utils.load.ServiceAccountCredentials.from_json_keyfile_name')
    def test_store_to_spreadsheet(self, mock_creds, mock_authorize, mock_set_with_dataframe):
        # Setup mock objects
        mock_client = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()

        # Chain mocks
        mock_creds.return_value = 'mocked_creds'
        mock_authorize.return_value = mock_client
        mock_client.open_by_key.return_value = mock_spreadsheet
        mock_spreadsheet.worksheet.return_value = mock_worksheet

        # Call function
        store_to_spreadsheet(
            data=self.df,
            spreadsheet_id=self.spreadsheet_id,
            worksheet_name=self.worksheet_name,
            credentials_json='sentiment-analysis-456613-7a6e0a6a71ad.json'
        )

        # Assertions
        mock_creds.assert_called_once()
        mock_authorize.assert_called_once_with('mocked_creds')
        mock_client.open_by_key.assert_called_once_with(self.spreadsheet_id)
        mock_spreadsheet.worksheet.assert_called_once_with(self.worksheet_name)
        mock_worksheet.clear.assert_called_once()
        mock_set_with_dataframe.assert_called_once_with(mock_worksheet, self.df)

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
