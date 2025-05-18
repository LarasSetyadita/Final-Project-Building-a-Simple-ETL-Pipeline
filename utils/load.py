from sqlalchemy import create_engine
import psycopg2
from psycopg2 import sql
import csv
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials


def store_to_csv(data):
    """Load data ke dalam format csv"""
    try:
        data.to_csv('products.csv', index=False)
        print('Data berhasil disimpan dalam format csv')
    except Exception as e:
        print(f'Gagal menyimpan data ke CSV: {e}')


def store_to_spreadsheet(data, spreadsheet_id, worksheet_name='Sheet1', credentials_json='sentiment-analysis-456613-7a6e0a6a71ad.json'):
    """Load data ke dalam format spreadsheet"""
    try:
        # Autentikasi Google API
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scope)
        client = gspread.authorize(creds)

        # Buka spreadsheet yang sudah ada dengan ID
        spreadsheet = client.open_by_key(spreadsheet_id)

        # Pilih worksheet (sheet) sesuai nama (default 'Sheet1')
        worksheet = spreadsheet.worksheet(worksheet_name)

        # Hapus isi worksheet dulu (opsional, supaya update bersih)
        worksheet.clear()

        # Masukkan dataframe ke worksheet
        set_with_dataframe(worksheet, data)
        print(f'Data berhasil diupload ke Google Sheets dengan ID: {spreadsheet_id} pada worksheet: {worksheet_name}')
    except FileNotFoundError:
        print(f'File credential JSON tidak ditemukan: {credentials_json}')
    except gspread.exceptions.APIError as api_err:
        print(f'Error API Google Sheets: {api_err}')
    except Exception as e:
        print(f'Gagal mengupload data ke Google Sheets: {e}')


def create_database(db_name):
    """Membuat database baru untuk menyimpan data"""
    try:
        # Connect ke postgres dengan user developer
        conn = psycopg2.connect(
            dbname="postgres",
            user="developer",
            password="supersecretpassword",
            host="localhost",
            port=5432
        )
        conn.set_session(autocommit=True)
        cur = conn.cursor()

        # Mengecek apakah database dengan nama yang sama sudah ada
        cur.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
            (db_name,)
        )
        exists = cur.fetchone()

        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Database '{db_name}' berhasil dibuat.") # pesan jika database berhasil dibuat
        else:
            print(f"Database '{db_name}' sudah ada.") # pesan yang ditampilkan jika database yang sama sudah ada

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Pembuatan database gagal : {e}") # pesan error jika pembuatan database gagal



def store_to_postgre(data, db_url, table_name='producttoscrape'):
    '''Menyimpan DataFrame ke PostgreSQL'''

    required_columns = ['product_title', 'price', 'ratings', 'colors', 'size', 'gender', 'timestamp']

    if not all(col in data.columns for col in required_columns):
        missing = [col for col in required_columns if col not in data.columns]
        raise ValueError(f"Kolom {missing} tidak ditemukan di DataFrame.")

    try:
        # Koneksi SQLAlchemy untuk to_sql()
        engine = create_engine(db_url)

        # Koneksi psycopg2 untuk eksekusi SQL manual
        with psycopg2.connect(
                dbname='productsdb',
                user='developer',
                password='supersecretpassword',
                host='localhost',
                port='5432'
        ) as conn:
            with conn.cursor() as cur:
                create_sql = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id SERIAL PRIMARY KEY,
                    product_title TEXT NOT NULL,
                    price NUMERIC(10,2) NOT NULL,
                    ratings NUMERIC(3,2) NOT NULL,
                    colors INTEGER NOT NULL,
                    size TEXT NOT NULL,
                    gender TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL  
                );
                """
                cur.execute(create_sql)

        # Menyimpan data ke dalam tabel
        with engine.connect() as con:
            data.to_sql(table_name, con=con, if_exists='append', index=False)
            print("Data berhasil ditambahkan ke tabel PostgreSQL!")

    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")
        raise
