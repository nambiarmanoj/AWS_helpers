# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.7
#   kernelspec:
#     display_name: conda_python3
#     language: python
#     name: conda_python3
# ---

# +
import boto3
import sagemaker
from sagemaker import get_execution_role

# Initialize the SageMaker role, session, and s3 client
role = sagemaker.get_execution_role() # specifies your permissions to use AWS tools
session = sagemaker.Session() 
s3 = boto3.client('s3')

# Print relevant details 
print(f"Execution Role: {role}")  # Displays the IAM role being used
bucket_names = [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]]
print(f"Available S3 Buckets: {bucket_names}")  # Shows the default S3 bucket assigned to SageMaker
print(f"AWS Region: {session.boto_region_name}")  # Prints the region where the SageMaker session is running

# +
import pandas as pd
# Define the S3 bucket and object key
bucket_name = 'me-uw-sagemaker-workshop'  # replace with your S3 bucket name

# Read the train data from S3
key = 'titanic_train.csv'  # replace with your object key
response = s3.get_object(Bucket=bucket_name, Key=key)
train_data = pd.read_csv(response['Body'])

# Read the test data from S3
key = 'titanic_test.csv'  # replace with your object key
response = s3.get_object(Bucket=bucket_name, Key=key)
test_data = pd.read_csv(response['Body'])

# check shape
print(train_data.shape)
print(test_data.shape)

# Inspect the first few rows of the DataFrame
train_data.head()

# +
# Initialize the total size counter (bytes)
total_size_bytes = 0

# Use a paginator to handle large bucket listings
# This ensures that even if the bucket contains many objects, we can retrieve all of them
paginator = s3.get_paginator("list_objects_v2")

# Iterate through all pages of object listings
for page in paginator.paginate(Bucket=bucket_name):
    # 'Contents' contains the list of objects in the current page, if available
    for obj in page.get("Contents", []):  
        total_size_bytes += obj["Size"]  # Add each object's size to the total

# Convert the total size to gigabytes for cost estimation
total_size_gb = total_size_bytes / (1024 ** 3)

# Convert the total size to megabytes for easier readability
total_size_mb = total_size_bytes / (1024 ** 2)

# Print the total size in MB
print(f"Total size of bucket '{bucket_name}': {total_size_mb:.2f} MB")

# Print the total size in GB
#print(f"Total size of bucket '{bucket_name}': {total_size_gb:.2f} GB")
# -

# %cd /home/ec2-user/SageMaker/
# !git clone https://github.com/nambiarmanoj/AWS_helpers.git # downloads AWS_helpers folder/repo (refresh file explorer to see)

import AWS_helpers.helpers as helpers
helpers.get_s3_bucket_size(bucket_name)

# +
# AWS S3 Standard Storage pricing for US East (N. Virginia) region
# Pricing tiers as of November 1, 2024
first_50_tb_price_per_gb = 0.023  # per GB for the first 50 TB
next_450_tb_price_per_gb = 0.022  # per GB for the next 450 TB
over_500_tb_price_per_gb = 0.021  # per GB for storage over 500 TB

# Calculate the cost based on the size
if total_size_gb <= 50 * 1024:
    # Total size is within the first 50 TB
    cost = total_size_gb * first_50_tb_price_per_gb
elif total_size_gb <= 500 * 1024:
    # Total size is within the next 450 TB
    cost = (50 * 1024 * first_50_tb_price_per_gb) + \
           ((total_size_gb - 50 * 1024) * next_450_tb_price_per_gb)
else:
    # Total size is over 500 TB
    cost = (50 * 1024 * first_50_tb_price_per_gb) + \
           (450 * 1024 * next_450_tb_price_per_gb) + \
           ((total_size_gb - 500 * 1024) * over_500_tb_price_per_gb)

print(f"Estimated monthly storage cost: ${cost:.5f}")
print(f"Estimated annual storage cost: ${cost*12:.5f}")
# -

monthly_cost, storage_size_gb = helpers.calculate_s3_storage_cost(bucket_name)
print(f"Estimated monthly cost ({storage_size_gb:.4f} GB): ${monthly_cost:.5f}")
print(f"Estimated annual cost ({storage_size_gb:.4f} GB): ${monthly_cost*12:.5f}")

# +
# Define the S3 bucket name and the file paths
notes_file_path = "Notes.txt" # assuming your file is in root directory of jupyter notebook (check file explorer tab)

# Upload the training file to a new folder called "docs". You can also just place it in the bucket's root directory if you prefer (remove docs/ in code below).
s3.upload_file(notes_file_path, bucket_name, "docs/Notes.txt")

print("Files uploaded successfully.")

# +
# List and print all objects in the bucket
response = s3.list_objects_v2(Bucket=bucket_name)

# Check if there are objects in the bucket
if 'Contents' in response:
    for obj in response['Contents']:
        print(obj['Key'])  # Print the object's key (its path in the bucket)
else:
    print("The bucket is empty or does not exist.")
# -

file_list = helpers.list_S3_objects(bucket_name)
file_list


