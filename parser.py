from pprint import pprint
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.parse_next_page import parse_next_page
from utils.parse_company_info import parse_company_info

if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument('--headless=new') 
    chrome_options.add_argument('--incognito')
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.orgpage.ru/moskva/krasota-i-zdorove/')
    wait = WebDriverWait(driver, 10)

    company_list = []
    start_index = 0
    main_container = driver.find_element(By.ID, 'rubricator-result')
    next_btn_wrap = driver.find_element(By.CSS_SELECTOR, '.rubricator-paging')

    for i in range(1):
        company_items = driver.find_elements(By.CSS_SELECTOR, '.object-item.similar-item')
        company_data = parse_next_page(company_items, start_index)
        company_list = company_list + company_data
        start_index = int(company_list[-1]['index_num'])
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.gradient.next')))
        next_page_btn = driver.find_element(By.CSS_SELECTOR, '.gradient.next')
        next_page_btn.click()
    # print(company_list)
    # first_c = parse_company_info(company_list[0]['page_url'])
    for company_data in company_list:
        company_data['contact_data'] = parse_company_info(company_data['page_url'])

    pprint(company_list)



