################################################################################
# Script to download a given file from endpoint to specific local path. It also
# handles the logging for "status" of the download in the meantime.
################################################################################

from urllib import request
import time

def download_file_from_url(download_file_url, output_folder, desired_filename):
    """
    Function to download a file from a given URL and saves it to desired folder.
    :return: output_file_path (string of the output path of the file)
    """
    output_file_path = "{}/{}".format(output_folder, desired_filename)

    start = time.time()
    print("Starting file download from URL: {} ...".format(download_file_url))
    response = request.urlretrieve(download_file_url, output_file_path)
    print("Total time to download file was: {} seconds".format(time.time() - start))
    print("Output path of the downloaded file is: {}".format(output_file_path))

    return output_file_path


## ONLY FOR LOCAL TESTS! (OWN COMPUTER VALIDATIONS)
if __name__ == "__main__":
    # TESTS
    # download_file_url = "https://instagram.com/favicon.ico"
    download_file_url = "https://oig.hhs.gov/exclusions/downloadables/UPDATED.csv"
    output_folder = "./tmp"
    print(download_file_from_url(download_file_url, output_folder, "09-08-2022.csv"))
