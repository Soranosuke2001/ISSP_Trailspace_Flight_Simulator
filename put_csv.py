import boto3
from datetime import datetime

FILE_PATH = './results.csv'
BUCKET_NAME = 'trailspace-sim-output'

s3 = boto3.client('s3')

def upload():
    try:
        current_timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        object_name = f"results-{current_timestamp}.csv"
        s3.upload_file(FILE_PATH, BUCKET_NAME, object_name)
        print(f"Successuflly uploaded '{FILE_PATH} to {BUCKET_NAME}/{object_name}'")
    except Exception as e:
        print(f"Error uploading file '{FILE_PATH}' to '{BUCKET_NAME}/{object_name}': {e}")

if __name__ == '__main__':
    upload()