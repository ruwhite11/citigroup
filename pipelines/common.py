import pandas as pd
from google.cloud import storage
from selenium import webdriver
import os
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
CHROME_DRIVER = os.path.join(PROJECT_ROOT, 'chromedriver')
DOWNLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'downloads')

PREFERENCES = {
    "profile.default_content_settings.popups": 0,
    "download.default_directory": DOWNLOAD_FOLDER,
    "directory_upgrade": True
}


def uploadToGCSBucket(bucket, df, filename):
    df.to_csv(f"gs://{bucket}/{filename}",index=False)


def getDriver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', PREFERENCES)
    driver = webdriver.Chrome(CHROME_DRIVER, options=options)
    return driver

def bucketfile(filetype:str):
    for file in os.listdir(DOWNLOAD_FOLDER):
        if filetype.lower() == '.csv' and file.endswith('csv'):
            shutil.move(DOWNLOAD_FOLDER + '/' + file,DOWNLOAD_FOLDER + '/loandetail/' + file)
        if filetype.lower() == '.pdf' and (file.endswith('.pdf') or file.endswith('.PDF')):
            shutil.move(DOWNLOAD_FOLDER + '/' + file,DOWNLOAD_FOLDER + '/CertStatement/' + file)
