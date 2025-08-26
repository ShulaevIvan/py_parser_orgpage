from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import re
from pprint import pprint

def parse_next_page(company_elements, index_num):
    if not company_elements:
        return []
    
    company_list = []

    for company_item in company_elements:
        index_num = index_num + 1
        company_data = {
            'company_id': '',
            'name': '',
            'description': '',
            'page_url': '',
            'index_num': ''
        }
        company_link_obj = company_item.find_element(By.CSS_SELECTOR,'.similar-item__title')
        company_description = company_item.find_element(By.CSS_SELECTOR, '.similar-item__description')
        company_link = company_link_obj.find_element(By.TAG_NAME, 'a')
        company_data['company_id'] = int(company_item.get_attribute('data-companyid'))
        company_data['name'] = re.sub(r'\d+.', '', company_link_obj.find_element(By.TAG_NAME, 'a').text)
        company_data['index_num'] = index_num
        company_data['description'] = company_description.text
        company_data['page_url'] = company_link.get_attribute('href')
        company_list.append(company_data)

    return company_list