import pandas as pd
import random
from datetime import datetime
import os

def generate_data():
    products = ["Shoes", "Laptop", "Phone", "T-shirt", "Watch"]
    countries = ["Germany", "France", "Netherlands", "Italy"]

    data = []
    for i in range(100):
        data.append({
            "order_id": i + 1,
            "order_date": datetime.today().strftime("%Y-%m-%d"),
            "product": random.choice(products),
            "quantity": random.randint(1, 5),
            "price": random.randint(10, 1000),
            "country": random.choice(countries)
        })

    df = pd.DataFrame(data)

    # ✅ write to shared folder mounted from Windows: ./data
    os.makedirs("/opt/airflow/data", exist_ok=True)
    date_str = datetime.today().strftime("%Y%m%d")
    file_path = f"/opt/airflow/data/sales_{date_str}.csv"
    df.to_csv(file_path, index=False)

    print(f"Generated file at {file_path}")

if __name__ == "__main__":
    generate_data()
