#!/usr/bin/env python3

import pandas as pd
import boto3
from datetime import datetime
import os

# ---------- Configuration ----------
bucket_name = "opencost-cur-bucket-demo"
cur_file_key = "AWS_CUR_Test/2025-11-11/test_cur.parquet"
region = "us-east-1"  # Replace with your bucket region

# ---------- Create sample CUR data ----------
data = {
    "line_item_usage_account_id": ["123456789012"],
    "product_product_name": ["Amazon EC2"],
    "line_item_usage_start_date": [datetime(2025, 11, 11)],
    "line_item_usage_end_date": [datetime(2025, 11, 11)],
    "line_item_unblended_cost": [5.25],
    "line_item_usage_amount": [1.0],
    "line_item_currency_code": ["USD"]
}

df = pd.DataFrame(data)

# Save as Parquet locally
parquet_file = "/tmp/test_cur.parquet"
df.to_parquet(parquet_file, engine='pyarrow', index=False)

# ---------- Upload to S3 ----------
boto3.client('pricing', 
                                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
                                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), 
                                region_name="us-east-1")

s3 = boto3.client("s3", region_name=region)
s3.upload_file(parquet_file, bucket_name, cur_file_key)

print(f"Test CUR Parquet uploaded to s3://{bucket_name}/{cur_file_key}")
