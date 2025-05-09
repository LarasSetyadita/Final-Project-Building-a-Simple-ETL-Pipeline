from sqlalchemy import create_engine
import pandas as pd

db_url = "postgresql://developer:supersecretpassword@localhost:5432/productsdb"
engine = create_engine(db_url)

df = pd.read_sql("SELECT * FROM producttoscrape LIMIT 10;", con=engine)
print(df)