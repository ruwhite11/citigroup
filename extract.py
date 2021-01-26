import fitz
import pandas as pd
import os


# doc = fitz.Document('/Users/rushellwhite/Projects/trex/pdfs/CertStmtCMLT06AMC10712.pdf')
#
# for x in range(doc.pageCount):
#     print(f'Page {x}')
#     page = doc.loadPage(x)
#     if 'SOURCE OF FUNDS' in page.getTextPage().extractText():
#         print('True')


def tableOfContents(document):
    recon_page = 1
    for page_num in range(document.pageCount):
        doc_page = doc.loadPage(page_num)
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


frames = []
for pdf in os.listdir('pdfs/'):
    if '.pdf' in pdf:
        doc = fitz.Document(os.getcwd() + '/pdfs/' + pdf)
        ind = tableOfContents(doc)
        records = getReconData(doc, ind)
        frames.append(pd.DataFrame.from_records([records]))

final = pd.concat(frames)
final.to_csv('data.csv',index=False)

