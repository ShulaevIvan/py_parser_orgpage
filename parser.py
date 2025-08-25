from pprint import pprint
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


from utils.parse_company_items import parse_company_items

if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(chrome_options)
    driver.get('https://www.orgpage.ru/moskva/krasota-i-zdorove/')

    company_list = []
    main_container = driver.find_element(By.ID, 'rubricator-result')
    company_chanks = main_container.find_elements(By.CLASS_NAME, 'object-item')
    show_more_btn_wrap = driver.find_element(By.CLASS_NAME, 'catalog__show-more')

    company_chank = parse_company_items(company_chanks)
    company_list = company_list + company_chank

    show_more_btn = show_more_btn_wrap.find_element(By.CLASS_NAME, 'rubricator-next-button')
    last_company_name = company_chank[-1]['name']
    show_more_btn.click()
    time.sleep(1)
    company_chanks = main_container.find_elements(By.CLASS_NAME, 'object-item')
    company_chank = parse_company_items(company_chanks)
    company_list = company_list + company_chank
    pprint(company_list)



