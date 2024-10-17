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

s3_client = boto3.client('s3')

# Function to check if a file exists in the given S3 path
def file_exists(bucket_name, key):
    try:
        s3_client.head_object(Bucket=bucket_name, Key=key)
        return True
    except:
        return False

# Function to read parquet file and filter data
def read_and_filter_parquet(bucket_name, key, asset_id, tag_name):
    try:
        print(f"Fetching file from S3: {key}")
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        file_stream = BytesIO(response['Body'].read())
        table = pq.read_table(file_stream)
        df = table.to_pandas()

        print(f"Dataframe columns: {df.columns}")
        # Filter the data based on asset_id and tag_name
        filtered_df = df[(df['AssetID'] == asset_id) & (df['TagName'] == tag_name)]
        return filtered_df
    except Exception as e:
        print(f"Error processing {key}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# List to store filtered data
filtered_data = []

# Track missing days
missing_days = []

# Loop through the days and check for parquet files
for day in range(int(start_day), int(end_day) + 1):
    day_str = str(day)
    parquet_key = f"{year}/{month}/{day_str}/sample_data.parquet"
    
    print(f"Checking if file exists: {parquet_key}")
    if file_exists(bucket_name, parquet_key):
        try:
            filtered_df = read_and_filter_parquet(bucket_name, parquet_key, asset_id, tag_name)
            if not filtered_df.empty:
                print(f"Filtered data found for day {day_str}")
                filtered_data.append(filtered_df)
            else:
                print(f"No matching data for day {day_str}")
        except Exception as e:
            print(f"Error reading {parquet_key}: {e}")
    else:
        missing_days.append(day_str)

# Combine all the filtered data into one DataFrame
if filtered_data:
    combined_df = pd.concat(filtered_data)
    combined_df.to_csv('/home/ec2-user/output.csv', index=False)
    print("Data successfully written to /home/ec2-user/output.csv")
else:
    print("No data found for the given criteria.")

# Notify about missing days
if missing_days:
    print(f"No data available for the following days: {', '.join(missing_days)}")
