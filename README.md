# s3-parquet-query-prototype
Read the parquet files using SSM

## Project details
# S3 Parquet Query Pipeline

This Jenkins pipeline automates the process of querying Parquet files stored in S3, processing the data, and retrieving the results.

## Pipeline Overview

1. Uploads a Python script to S3
2. Prepares an EC2 instance with necessary dependencies
3. Executes the script to process Parquet files
4. Retrieves and stores the results

## Key Components

- `Jenkinsfile`: Defines the pipeline stages and steps
- `script.py`: Python script for processing Parquet files

## Usage

To run the pipeline, provide the following parameters:
- BUCKET_NAME: S3 bucket containing Parquet files
- ASSET_ID: Asset identifier for filtering data
- YEAR: Year of data to process
- MONTH: Month of data to process
- START_DAY: Start day of the date range
- END_DAY: End day of the date range
- TAG_NAME: Tag name for filtering data

## Output

The pipeline produces a CSV file containing the filtered and processed data, which is saved as a Jenkins artifact.

## Notes

- Ensure proper AWS credentials are configured in Jenkins
- The EC2 instance must have necessary permissions to access S3
