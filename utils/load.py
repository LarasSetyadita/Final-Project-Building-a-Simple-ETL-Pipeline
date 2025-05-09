from sqlalchemy import create_engine
import psycopg2
from psycopg2 import sql


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
