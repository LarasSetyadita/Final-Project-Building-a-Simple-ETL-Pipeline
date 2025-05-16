import pandas as pd

from utils.extract import scrape_collection_data
from utils.transform import transform, transform_to_Dataframe
from utils.load import store_to_postgre, create_database, store_to_csv, store_to_spreadsheet


def main():
    """Fungsi utama untuk menjalankan proses scraping dan menyimpan data."""
    url = 'https://fashion-studio.dicoding.dev'
    collection_data = scrape_collection_data(url)

    if collection_data:
        # Jika data berhasil diambil, simpan dalam DataFrame dan tampilkan
        products_df = transform_to_Dataframe(collection_data)
        products_df = transform(products_df)
        print(products_df)
    else:
        print("Tidak ada data yang ditemukan.")

    products_df.info() # mengecek tipe data

    # menyimpan data ke dalam format csv
    store_to_csv(products_df)

    # menyimpan data ke dalam format excel
    spreadsheet_id = '1reol3Wu--fGOmqfC8N0vJMXUzW2rosA31YWvtRWsOTo'
    store_to_spreadsheet(products_df, spreadsheet_id)


    # menyimpan data ke dalam postgresql
    #db_name = 'productsdb'
    #create_database(db_name)
    #db_url = 'postgresql+psycopg2://developer:supersecretpassword@localhost:5432/productsdb'
    #store_to_postgre(products_df, db_url)

if __name__ == "__main__":
    main()

