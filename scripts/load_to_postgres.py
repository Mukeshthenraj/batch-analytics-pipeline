import pandas as pd
from datetime import datetime
import os
from sqlalchemy import create_engine

def main():
    date_str = datetime.today().strftime("%Y%m%d")
    file_path = f"/opt/airflow/data/sales_{date_str}.csv"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing file: {file_path}")

    df = pd.read_csv(file_path)
    df["load_date"] = date_str

    engine = create_engine("postgresql+psycopg2://de_user:de_pass@postgres:5432/warehouse")
    df.to_sql("sales_raw", engine, if_exists="append", index=False)

    print(f"✅ Loaded {len(df)} rows into sales_raw")

if __name__ == "__main__":
    main()
