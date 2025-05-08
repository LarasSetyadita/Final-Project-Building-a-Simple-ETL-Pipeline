import pandas as pd

from utils.extract import scrape_collection_data
from utils.transform import transform, transform_to_Dataframe

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

if __name__ == "__main__":
    main()

