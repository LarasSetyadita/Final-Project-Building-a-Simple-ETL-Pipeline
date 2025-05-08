import pandas as pd

class DataLoad:
    '''Kelas untuk menyimpan data ke file.'''
    
    def __init__(self, data):
        self.data = data

    def to_csv(self, filename="data_produk.csv"):
        '''Menyimpan data ke file CSV'''
        try:
            df = pd.DataFrame(self.data)
            df.to_csv(filename, index=False)
            print(f"Data berhasil disimpan ke '{filename}'")
        except Exception as e:
            print(f"Gagal menyimpan data ke CSV: {e}")
