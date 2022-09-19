################################################################################
# Script to search for the latest "LEIE Downloadable Databases" file in a given
# url and download the latest file content.
################################################################################

import re
import urllib3
from bs4 import BeautifulSoup


def url_scrapper_search_latest_file(base_url, fetch_url):
    """
    Function to scrape specific site with regex approach and returns the latest
    download_file_url on the website and the expected filename for it.
    :param base_url: base URL to scrape (string).
    :param fetch_url: last part of URL to scrape which is concat with base_url (string).
    :return: tuple(download_file_url, file_name_to_download) (both strings)
    """
    http = urllib3.PoolManager()
    response = http.request('GET', fetch_url)
    soup = BeautifulSoup(response.data, "html.parser")
    # print(soup)

    # Obtain specific tag based on client's regex requirements
    file_name_pretty = soup(text=re.compile("Last Update"))[0]
    print("Regex item found on website with ok criteria is: {}".format(file_name_pretty))

    # Get the "Last Update" value from the HTML content and tags
    complete_tag_1 = file_name_pretty.findPrevious()
    print("Tag 1 found is: {}".format(complete_tag_1))
    print("Value 1 found is: {}".format(complete_tag_1.string))
    complete_tag_2 = complete_tag_1.findPrevious()
    print("Tag 2 found is: {}".format(complete_tag_2))
    print("Value 2 found is: {}".format(complete_tag_2.string))
    last_updated_date = "{}.csv".format(complete_tag_2.string)

    # Obtain specific tag based on client's regex requirements
    file_name_pretty = soup(text=re.compile("Updated LEIE Database"))[0]
    print("Regex item found on website with ok criteria is: {}".format(file_name_pretty))

    # Get the "Updated LEIE Database" value from the HTML content and tags
    complete_tag_3 = file_name_pretty.findPrevious()
    print("Tag 3 found is: {}".format(complete_tag_3))

    # Only obtain filename (to intelligently create download_file_url)
    file_name_to_download = str(complete_tag_3).split("href=\"/")[1]
    file_name_to_download = file_name_to_download.split("\"")[0]

    print("The file_name_to_download is: {}".format(file_name_to_download))
    download_file_url = "{}{}".format(base_url, file_name_to_download)
    print("The obtained URL (download_url_file) is: {}".format(download_file_url))

    return download_file_url, last_updated_date


## ONLY FOR LOCAL TESTS! (OWN COMPUTER VALIDATIONS)
if __name__ == "__main__":
    # TESTS
    base_url = "https://oig.hhs.gov/"
    fetch_url = "{}/exclusions/exclusions_list.asp".format(base_url)
    print(url_scrapper_search_latest_file(base_url, fetch_url))
