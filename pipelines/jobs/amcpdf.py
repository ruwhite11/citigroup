import fitz
import pandas as pd
import os
from pipelines.common import *
from time import sleep

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PDF_FOLDER = os.path.join(PROJECT_ROOT, 'downloads/CertStatement/')

# distdate 2012 = December 2020
def download_pdf(distdate):
    url = "https://sf.citidirect.com/stfin/jsp/deallist.jsp"
    driver = getDriver()
    driver.get(url)
    amc_page = driver.find_element_by_link_text("2006-AMC1")
    amc_page.click()
    sleep(1)
    elements = driver.find_element_by_xpath(f'//a[contains(@href,"CertStmtCMLT06AMC1{distdate}")]')
    elements.click()
    sleep(10)
    driver.quit()


def getReconLocation(document):
    recon_page = 1
    for page_num in range(document.pageCount):
        doc_page = document.loadPage(page_num)
        if 'SOURCE OF FUNDS' in doc_page.getTextPage().extractText():
            recon_page += page_num

    return recon_page


def getPageData(document, pgNum):
    page = document.loadPage(pgNum)
    pageText = page.getTextPage().extractText()
    return pageText


def getReconData(document, inde):
    pg = getPageData(document, inde - 1)
    data_list = pg.splitlines()
    dic = {}
    for index, att in enumerate(data_list):
        if att.strip() == 'Scheduled Principal':
            dic['Scheduled_Principal'] = data_list[index + 1].strip()
        if att.strip() == 'Curtailments':
            dic['Curtailments'] = data_list[index + 1].strip()
        if att.strip() == 'Prepayments in Full':
            dic['Prepayments in Full'] = data_list[index + 1].strip()
        if att.strip() == 'Net Liquidation Proceeds':
            dic['Net Liquidation Proceeds'] = data_list[index + 1].strip()
        if att.strip() == 'Repurchased Principal':
            dic['Repurchased Principal'] = data_list[index + 1].strip()
        if att.strip() == 'Substitution Principal':
            dic['Substitution Principal'] = data_list[index + 1].strip()
        if att.strip() == 'Other Principal':
            dic['Other Principal'] = data_list[index + 1].strip()
        if att.strip() == 'Total Principal Funds Available:':
            dic['Total Principal Funds Available'] = data_list[index + 1].strip()
        if att.strip() == 'Cap Contract Amount':
            dic['Cap Contract Amount'] = data_list[index + 1].strip()
        if att.strip() == 'Prepayment Penalties':
            dic['Prepayment Penalties'] = data_list[index + 1].strip()
        if att.strip() == 'Other Charges':
            dic['Other Charges'] = data_list[index + 1].strip()
        if att.strip() == 'Total Other Funds Available:':
            dic['Total Other Funds Available'] = data_list[index + 1].strip()
        if att.strip() == 'Total Funds Available':
            dic['Total Funds Available'] = data_list[index + 1].strip()
        if att.strip() == 'Distribution Date:':
            dic['Distribution Date'] = data_list[index + 1].strip()

    return dic


def makeDataframe() -> pd.DataFrame:
    frames = []
    for pdf in os.listdir(PDF_FOLDER):
        if '.pdf' in pdf:
            doc = fitz.Document(PDF_FOLDER + pdf)
            ind = getReconLocation(doc)
            records = getReconData(doc, ind)
            frames.append(pd.DataFrame.from_records([records]))
    df = pd.concat(frames)
    return df


def uploadDataframe(distdate):
    df = makeDataframe()
    print(df)
    uploadToGCSBucket("rushtrexgroup", df, f"CertStatements/CertStmt{distdate}.csv")


def etl(distdate):
    download_pdf(distdate)
    bucketfile('.pdf')
    uploadDataframe(distdate)


