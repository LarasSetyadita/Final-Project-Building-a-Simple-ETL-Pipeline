import pandas as pd
import numpy as np
from datetime import datetime


def transform_to_Dataframe(data):
    '''Mengubah data menjadi dataframe'''
    products_df = pd.DataFrame(data)
    return products_df

def transform_price(data):
    '''Transformasi data harga'''
    data['price'] = data['price'].replace('Tidak tersedia', np.nan)
    data['price'] = data['price'].replace(r'\$', '', regex=True)
    data['price'] = pd.to_numeric(data['price'], errors='coerce')
    data['price'] = data['price'] * 16000
    return data

def transform_rating(data):
    """Transformasi data rating"""
    data['ratings'] = data['ratings'].replace(['Price Unavailable', 'Tidak tersedia'], np.nan)
    data['ratings'] = data['ratings'].replace('⭐', '', regex=True)
    data['ratings'] = pd.to_numeric(data['ratings'], errors='coerce')
    return data

def transform_title(data):
    """Transformasi data nama produk"""
    data['product_title'] = data['product_title'].astype('object')
    data['product_title'] = data['product_title'].str.replace(r'\s+\d+$', '', regex=True)
    return data

def transform_color(data):
    """Transformasi data jumlah warna"""
    data['colors'] = data['colors'].replace(r'Colors', '', regex=True)
    data['colors'] = pd.to_numeric(data['colors'], errors='coerce').astype('Int64') 
    return data

# fungsi untuk membersihkan data duplikat
def clean_duplicates(data, subset=None):
    """Membersihkan data duplikat"""
    data = data.drop_duplicates(subset=subset, keep='first')
    return data

# fungsi untuk menghilangkan missing value
def clean_missing_data(data):
    """Membersihkan baris dengan kolom yang hilang"""
    data = data.dropna()
    return data


def transform(data):
    """Menerapkan semua transformasi data"""
    data = transform_price(data)
    data = transform_rating(data)
    data = transform_title(data)
    data = transform_color(data)
    data = clean_missing_data(data)
    data = clean_duplicates(data)
    return data

