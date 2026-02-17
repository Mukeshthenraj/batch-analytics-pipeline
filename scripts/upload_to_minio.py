import boto3
import os
from datetime import datetime

MINIO_ENDPOINT = "http://minio:9000"
ACCESS_KEY = "minio"
SECRET_KEY = "minio12345"
BUCKET = "raw"

def main():
    date_str = datetime.today().strftime("%Y%m%d")
    file_path = f"/opt/airflow/data/sales_{date_str}.csv"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    object_name = f"sales/date={date_str}/sales_{date_str}.csv"
    s3.upload_file(file_path, BUCKET, object_name)

    print(f"✅ Uploaded to MinIO bucket '{BUCKET}': {object_name}")

if __name__ == "__main__":
    main()
