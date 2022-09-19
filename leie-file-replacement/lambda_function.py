# Built-in dependencies
import boto3

# Own dependencies
import url_scrapper_search_latest_file
import download_file_from_url
import s3_helpers
import send_emails_ses

################################################################################
# GLOBAL VARIABLES TO CONFIGURE SOLUTION
# URL SITE CONFIGURATIONS
BASE_URL = "https://oig.hhs.gov/"
FETCH_URL = "{}/exclusions/exclusions_list.asp".format(BASE_URL)

# AWS CONFIGURATIONS
S3_BUCKET_NAME = "leie-monthly-data"
OUTPUT_FOLDER = "/tmp"

# EMAIL CONFIGURATIONS
FROM_EMAIL = "san99tiagodevsecops@gmail.com"
TO_EMAILS_LIST = ["san99tiagodevsecops@gmail.com"]
SES_CONFIG_SET_NAME = "leie-downloads-set"
################################################################################


# AWS resources and clients (best practice is to keep outside handler for efficiency)
s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")
ses_client = boto3.client('ses')


def lambda_handler(event, context):
    """
    Main lambda handler function.
    """
    print("Event is:")
    print(event)

    # Get latest file from the website
    print("Retrieving latest file name and URL from the official website...")
    download_info = url_scrapper_search_latest_file.url_scrapper_search_latest_file(BASE_URL, FETCH_URL)
    download_file_url = download_info[0]
    file_name = download_info[1]

    # Get existing files names (the ones already downloaded)
    existing_files_in_s3 = s3_helpers.get_all_files_from_s3(s3_resource, S3_BUCKET_NAME, OUTPUT_FOLDER)
    print("Existing files in s3 are: {}".format(existing_files_in_s3))

    if file_name in existing_files_in_s3:
        # If file already exists (inform duplicate)...
        message_title_to_send = "LEIE file found is already downloaded"
        message_body_to_send = "The LEIE-FILE found is already downloaded ({})".format(file_name)
    else:
        # If file is new (download from site, upload to s3 and inform action)...
        output_file_path = download_file_from_url.download_file_from_url(download_file_url, OUTPUT_FOLDER, file_name)
        print("The download was successful and the temp path is: {}".format(output_file_path))
        s3_helpers.upload_file_to_s3(s3_client, S3_BUCKET_NAME, output_file_path, file_name)
        message_title_to_send = "New LEIE file found and downloaded successfully!"
        message_body_to_send = "The LEIE-FILE solution found a new file ({}), and you can find it at the s3 bucket ({}).".format(file_name, S3_BUCKET_NAME)

    # Send e-mail based on process workflow and messages
    print("Starting e-mail process with SES...")
    print("Message title: {}".format(message_title_to_send))
    print("Message body: {}".format(message_body_to_send))
    print(send_emails_ses.email_handler(FROM_EMAIL, TO_EMAILS_LIST, ses_client, SES_CONFIG_SET_NAME, message_title_to_send, message_body_to_send))

    return {
        'statusCode': 200,
        'body': message_body_to_send
    }


## ONLY FOR LOCAL TESTS! (OWN COMPUTER VALIDATIONS)
if __name__ == "__main__":
    # TESTS
    print(lambda_handler({"info": "fake event for local validations"}, None))
