import pandas as pd
import os
from pipelines.common import *
from time import sleep

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CSV_FOLDER = os.path.join(PROJECT_ROOT, 'downloads/loandetail/')

def download(distdate):
    url = "https://sf.citidirect.com/stfin/jsp/deallist.jsp"
    driver = getDriver()
    driver.get(url)
    amc_page = driver.find_element_by_link_text("2006-AMC1")
    amc_page.click()
    sleep(1)
    elements = driver.find_element_by_xpath(f'//a[contains(@href,"LoanDetailCMLT06AMC1{distdate}")]')
    elements.click()
    sleep(10)
    driver.quit()

def uploadDataframe(distdate):
    filename = f"LoanDetailCMLT06AMC1{distdate}.csv"
    df = pd.read_csv(CSV_FOLDER + filename)
    if len(df.columns) > 67:
        df.drop(['Ending Deferred Balance','Beginning Deferred Balance'],axis=1,inplace=True)
    df.columns = df.columns.str.replace("#","").str.strip().str.replace(" ","_").str.replace("/","_").str.replace("&","")
    df.Distribution_Date = pd.to_datetime(df.Distribution_Date,format='%Y%m%d')
    print(df)    
    uploadToGCSBucket("rushtrexgroup",df,f"loandetails/loandetails{distdate}.csv")

def etl(distdate):
     download(distdate)
     bucketfile('.csv')
     uploadDataframe(distdate)



