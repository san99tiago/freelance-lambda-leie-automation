# LEIE FILE AUTOMATIC SOLUTION

## General Explanation

The purpose of this project is to automatically validate when a file is updated from a given URL, and then, depending on the found file, upload it to an S3 bucket, or not. There is also a requirement to send an e-mail with the insights of the file after an automatic execution (Simple Email Service) based on a EventBridge CRON rule.
