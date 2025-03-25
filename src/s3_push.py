import boto3
import os
import pathlib

def empty_s3_bucket(s3_client: boto3.client, bucket: str) -> None:
    objects = s3_client.list_objects_v2(Bucket=bucket)
    if objects is None:
        raise Exception("No objects found")
    contents = objects.get("Contents")
    if contents is None:
        raise Exception("No contents found in objects payload")
    object_keys = [obj["Key"] for obj in contents]
    if object_keys is None:
        raise Exception("No objects keys found - check object contents response")
    for obj_key in object_keys:
        s3_client.delete_object(Bucket=bucket, Key=obj_key)

def upload_directory_to_s3_recursive(
    s3_client: boto3.client, 
    bucket: str,
    from_directory: os.path
) -> None:
    if not os.path.exists(from_directory):
        raise Exception("invalid from directory path")
    
    from_directory_objs = os.listdir(from_directory)
    for obj in from_directory_objs:
        obj_path = pathlib.Path(obj)
        file_path = os.path.join(from_directory, obj_path)
        if os.path.isfile(file_path):
            file_type = obj_path.suffix.strip(".")
            if file_type == 'txt':
                file_type = "plain"

            s3_client.upload_file(
                Bucket=bucket,
                Filename=file_path,
                Key=str(obj_path),
                ExtraArgs={"ContentType": f"text/{file_type}"}
            )
        else:
            upload_directory_to_s3_recursive(
                s3_client,
                bucket,
                file_path
            )
