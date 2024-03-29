################################################################################
# Script with helpers for S3 management (upload, read_files, ...)
################################################################################

import sys
import os
import time
import threading
from boto3.s3.transfer import TransferConfig

class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()


def get_all_files_from_s3(s3_resource, s3_bucket_name, output_folder):
    """
    Function to retrieve all files from S3 bucket (to validate need to download or not)
    """
    list_of_existing_files = []
    for my_bucket_object in s3_resource.Bucket(s3_bucket_name).objects.all():
        list_of_existing_files.append(my_bucket_object.key)
        # print(my_bucket_object.key)

    return list_of_existing_files


def upload_file_to_s3(s3_client, s3_bucket_name, file_path, s3_path):
    """
    Function to export a file to a S3 bucket.
    :note: creates object in bucket at path -->  s3://<bucket_name>/<s3_path>
    """
    print("upload_file_to_s3: uploading file {} to S3 bucket at path {}".format(file_path, s3_path))

    start = time.time()

    # # DEFAULT METHOD (without multi-threading configuration)
    # s3_client.upload_file(
    #     file_path,
    #     s3_bucket_name,
    #     s3_path
    # )

    config = TransferConfig(max_concurrency=10, use_threads=True)
    file = file_path
    key = s3_path
    s3_client.upload_file(file, s3_bucket_name, key,
    Config = config,
    Callback=ProgressPercentage(file)
    )

    print("Total time to upload file was: {} seconds".format(time.time() - start))


## ONLY FOR LOCAL TESTS! (OWN COMPUTER VALIDATIONS)
if __name__ == "__main__":
    # TESTS
    import boto3
    s3_resource = boto3.resource("s3")
    s3_bucket_name = "leie-monthly-data"
    output_folder = "./tmp"
    print(get_all_files_from_s3(s3_resource, s3_bucket_name, output_folder))

    s3_client = boto3.client("s3")
    file_path = "./tmp/favicon.ico"
    s3_path = "favicon.ico"
    upload_file_to_s3(s3_client, file_path, s3_path)
