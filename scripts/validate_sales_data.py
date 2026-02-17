import pandas as pd
from datetime import datetime
import os

def main():
    date_str = datetime.today().strftime("%Y%m%d")
    file_path = f"/opt/airflow/data/sales_{date_str}.csv"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing file: {file_path}")

    df = pd.read_csv(file_path)

    required = {"order_id", "order_date", "product", "quantity", "price", "country"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    if df.empty:
        raise ValueError("CSV is empty")

    if (df["quantity"] <= 0).any():
        raise ValueError("Found quantity <= 0")

    if (df["price"] <= 0).any():
        raise ValueError("Found price <= 0")

    if df["country"].isna().any() or (df["country"].astype(str).str.strip() == "").any():
        raise ValueError("Empty country values found")

    if df["product"].isna().any() or (df["product"].astype(str).str.strip() == "").any():
        raise ValueError("Empty product values found")

    print(f"✅ Validation passed. Rows={len(df)} File={file_path}")

if __name__ == "__main__":
    main()
