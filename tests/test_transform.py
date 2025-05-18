import unittest
import pandas as pd
import numpy as np
from utils.transform import transform_to_Dataframe, transform_price, transform_rating,transform_title, transform_color, clean_duplicates,clean_missing_data, transform


class TestTransformFunctions(unittest.TestCase):

    def setUp(self):
        self.raw_data = [
            {
                'product_title': 'Produk A',
                'price': '$10',
                'ratings': '⭐4.5',
                'colors': '3 Colors'
            },
            {
                'product_title': 'Produk B',
                'price': 'Tidak tersedia',
                'ratings': 'Price Unavailable',
                'colors': '2 Colors'
            },
            {
                'product_title': 'Produk A',  # duplicate
                'price': '$10',
                'ratings': '⭐4.5',
                'colors': '3 Colors'
            }
        ]
        self.df = pd.DataFrame(self.raw_data)

    def test_transform_to_dataframe(self):
        df = transform_to_Dataframe(self.raw_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)

    def test_transform_price(self):
        df = transform_price(self.df.copy())
        self.assertEqual(df['price'].dtype, 'float64')
        self.assertAlmostEqual(df['price'][0], 160000.0)
        self.assertTrue(np.isnan(df['price'][1]))

    def test_transform_rating(self):
        df = transform_rating(self.df.copy())
        self.assertEqual(df['ratings'].dtype, 'float64')
        self.assertAlmostEqual(df['ratings'][0], 4.5)
        self.assertTrue(np.isnan(df['ratings'][1]))

    def test_transform_title(self):
        df = transform_title(self.df.copy())
        self.assertEqual(df['product_title'].dtype, 'object')

    def test_transform_color(self):
        df = transform_color(self.df.copy())
        self.assertEqual(df['colors'].dtype.name, 'Int64')
        self.assertEqual(df['colors'][0], 3)

    def test_clean_duplicates(self):
        df = clean_duplicates(self.df.copy(), subset=['product_title'])
        self.assertEqual(len(df), 2)

    def test_clean_missing_data(self):
        df = self.df.copy()
        df.loc[1, 'ratings'] = np.nan
        df_clean = clean_missing_data(df)
        self.assertEqual(len(df_clean), 2)

    def test_full_transform(self):
        df_transformed = transform(self.df.copy())
        self.assertEqual(len(df_transformed), 1)
        self.assertEqual(df_transformed.iloc[0]['price'], 160000.0)
        self.assertEqual(df_transformed.iloc[0]['ratings'], 4.5)
        self.assertEqual(df_transformed.iloc[0]['colors'], 3)

if __name__ == '__main__':
    unittest.main()
