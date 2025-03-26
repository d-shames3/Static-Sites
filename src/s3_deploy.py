from s3_push import empty_s3_bucket, upload_directory_to_s3_recursive
import os
import boto3

def main():
    # set directory variables 
    path_to_repo = os.getcwd() 
    destination = os.path.join(path_to_repo, "public")

    # load env vars
    bucket=os.environ.get("AWS_STATIC_SITE_BUCKET")

    s3 = boto3.client('s3')
    empty_s3_bucket(s3, bucket)
    upload_directory_to_s3_recursive(s3, bucket, destination)

if __name__ == "__main__":
    main()
