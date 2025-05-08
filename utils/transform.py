import pandas as pd
import numpy as np
from datetime import datetime


def transform_to_Dataframe(data):
    '''Mengubah data menjadi dataframe'''
    products_df = pd.DataFrame(data)
    return products_df

# fungsi untuk transformasi data harga
def transform_price(data):
    data['price'] = data['price'].replace('Tidak tersedia', np.nan)
    data['price'] = data['price'].replace(r'\$', '', regex=True)
    data['price'] = pd.to_numeric(data['price'], errors='coerce')
    data['price_idr'] = data['price'] * 16000
    return data

# fungsi untuk transformasi data rating
def transform_rating(data):
    data['ratings'] = data['ratings'].replace(['Price Unavailable', 'Tidak tersedia'], np.nan)
    data['ratings'] = data['ratings'].replace('⭐', '', regex=True)
    data['ratings'] = pd.to_numeric(data['ratings'], errors='coerce')
    return data

# fungsi untuk transformasi data nama product
def transform_title(data):
    data['product_title'] = data['product_title'].astype('string')
    return data

# fungsi untuk transformasi data warna
def transform_color(data):
    data['colors'] = data['colors'].replace(r'Colors', '', regex=True)
    data['colors'] = pd.to_numeric(data['colors'], errors='coerce').astype('Int64') 
    return data

# fungsi untuk membersihkan data duplikat
def clean_duplicates(data, subset=None):
    data = data.drop_duplicates(subset=subset, keep='first')
    return data

# fungsi untuk menghilangkan missing value
def clean_missing_data(data):
    data=data.dropna()
    return data


# fungsi untuk menerapkan semua transformasi data
def transform(data):
    data = transform_price(data)
    data = transform_rating(data)
    data = transform_title(data)
    data = transform_color(data)
    data = clean_missing_data(data)
    data = clean_duplicates(data)
    return data

