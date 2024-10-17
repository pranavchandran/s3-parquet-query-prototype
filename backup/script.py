# __Author__ = "Pranav Chandran"
# __Date__ = 14-10-2024
# __Time__ = 20:17
# __FileName__ = script.py
import boto3
import pandas as pd
import pyarrow.parquet as pq
from io import BytesIO
import sys

# Collecting command-line arguments
bucket_name = sys.argv[1]
asset_id = sys.argv[2]
year = sys.argv[3]
month = sys.argv[4]
start_day = sys.argv[5]
end_day = sys.argv[6]
tag_name = sys.argv[7]

print(f"Bucket Name: {bucket_name}")
print(f"Asset ID: {asset_id}")
print(f"Year: {year}")
print(f"Month: {month}")
print(f"Start Day: {start_day}")
print(f"End Day: {end_day}")
print(f"Tag Name: {tag_name}")

