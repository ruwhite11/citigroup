from selenium import webdriver
from time import sleep
import os

abs_path = os.path.dirname(os.path.abspath(__file__))
folder = os.path.join(abs_path,'pdfs')
chromedriver = '/Users/rushellwhite/Projects/trex/chromedriver'

preferences = {
                "profile.default_content_settings.popups": 0,
                "download.default_directory": folder,
                "directory_upgrade": True
            }

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', preferences)
driver = webdriver.Chrome(chromedriver,options=options)

url = "https://sf.citidirect.com/stfin/jsp/deallist.jsp"

driver.get(url)

amc_page = driver.find_element_by_link_text("2006-AMC1")

amc_page.click()

sleep(1)

os.chdir(folder)
elements = driver.find_elements_by_xpath('//a[contains(@href,"Cert")]')

for pdf in elements:
    pdf.click()

driver.quit()