import json
import boto3
import botocore.exceptions

BUCKET_NAME = 'trailspace-json-input'
CONFIG_FILE_PATH = './config/config.json'

s3 = boto3.client('s3')

# Will find and retrieve the most recently uploaded file in the bucket
def get_most_recent():
    try:
        response_list = s3.list_objects_v2(Bucket=BUCKET_NAME)

        most_recent_object = None
        most_recent_timestamp = None

        # Loop through the entire bucket, comparing each object's timestamp
        for obj in response_list.get('Contents', []):
            if most_recent_timestamp is None or obj['LastModified'] > most_recent_timestamp:
                most_recent_object = obj
                most_recent_timestamp = obj['LastModified']

        if most_recent_object is None:
            raise RuntimeError('No objects were found in the bucket')
        
        response_object = s3.get_object(Bucket=BUCKET_NAME, Key=most_recent_object['Key'])
        object_contents = response_object['Body'].read().decode('utf-8')
        return object_contents

    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchBucket':
            raise ValueError(f"Bucket '{BUCKET_NAME}' does not exist.")
        else:
            raise RuntimeError(f"An error occurred: {e}")
        
def write_to_file(json_string):
    json_body = json.loads(json_string)
    with open(CONFIG_FILE_PATH, 'w') as file:
        json.dump(json_body, file, indent=4)

if __name__ == '__main__':
    json_body = get_most_recent()
    write_to_file(json_body)