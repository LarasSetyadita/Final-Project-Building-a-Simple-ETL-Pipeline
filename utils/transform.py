import pandas as pd
import numpy as np
from datetime import datetime


def transform_to_Dataframe(data):
    '''Mengubah data menjadi dataframe'''
    try:
        products_df = pd.DataFrame(data)
        return products_df
    except Exception as e:
        print(f'Error di transform_to_Dataframe: {e}')
        return None


def transform_price(data):
    '''Transformasi data harga'''
    try:
        data['price'] = data['price'].replace('Tidak tersedia', np.nan)
        data['price'] = data['price'].replace(r'\$', '', regex=True)
        data['price'] = pd.to_numeric(data['price'], errors='coerce')
        data['price'] = data['price'] * 16000
        return data
    except KeyError:
        print('Kolom "price" tidak ditemukan pada data.')
        return data
    except Exception as e:
        print(f'Error di transform_price: {e}')
        return data


def transform_rating(data):
    """Transformasi data rating"""
    try:
        data['ratings'] = data['ratings'].replace(['Price Unavailable', 'Tidak tersedia'], np.nan)
        data['ratings'] = data['ratings'].replace('⭐', '', regex=True)
        data['ratings'] = pd.to_numeric(data['ratings'], errors='coerce')
        return data
    except KeyError:
        print('Kolom "ratings" tidak ditemukan pada data.')
        return data
    except Exception as e:
        print(f'Error di transform_rating: {e}')
        return data


def transform_title(data):
    """Transformasi data nama produk"""
    try:
        data['product_title'] = data['product_title'].astype('object')
        data['product_title'] = data['product_title'].str.replace(r'\s+\d+$', '', regex=True)
        return data
    except KeyError:
        print('Kolom "product_title" tidak ditemukan pada data.')
        return data
    except Exception as e:
        print(f'Error di transform_title: {e}')
        return data


def transform_color(data):
    """Transformasi data jumlah warna"""
    try:
        data['colors'] = data['colors'].replace(r'Colors', '', regex=True)
        data['colors'] = pd.to_numeric(data['colors'], errors='coerce').astype('Int64')
        return data
    except KeyError:
        print('Kolom "colors" tidak ditemukan pada data.')
        return data
    except Exception as e:
        print(f'Error di transform_color: {e}')
        return data


def clean_duplicates(data, subset=None):
    """Membersihkan data duplikat"""
    try:
        data = data.drop_duplicates(subset=subset, keep='first')
        return data
    except Exception as e:
        print(f'Error di clean_duplicates: {e}')
        return data


def clean_missing_data(data):
    """Membersihkan baris dengan kolom yang hilang"""
    try:
        data = data.dropna()
        return data
    except Exception as e:
        print(f'Error di clean_missing_data: {e}')
        return data


def transform(data):
    """Menerapkan semua transformasi data"""
    try:
        data = transform_price(data)
        data = transform_rating(data)
        data = transform_title(data)
        data = transform_color(data)
        data = clean_missing_data(data)
        data = clean_duplicates(data)
        return data
    except Exception as e:
        print(f'Error di transform: {e}')
        return data
