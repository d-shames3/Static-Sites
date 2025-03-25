from s3_push import empty_s3_bucket, upload_directory_to_s3_recursive
import os
from dotenv import load_dotenv
import boto3

def main():
    # set directory variables 
    path_to_repo = os.getcwd() 
    destination = os.path.join(path_to_repo, "public")

    # load env vars
    load_dotenv(dotenv_path='.envrc')
    aws_access_key_id=os.environ.get("aws_access_key_id"),
    aws_secret_access_key=os.environ.get("aws_secret_access_key")
    bucket=os.environ.get("bucket")

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    empty_s3_bucket(s3, bucket)
    upload_directory_to_s3_recursive(s3, bucket, destination)

if __name__ == "__main__":
    main()
