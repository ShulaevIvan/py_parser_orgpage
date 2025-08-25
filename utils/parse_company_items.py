from selenium.webdriver.common.by import By
import re

def parse_company_items(company_chanks):
    company_list = []

    for company_item in company_chanks:
        company_data = {
            'company_id': '',
            'name': '',
            'description': '',
            'page_url': '',
            'index_num': ''
        }
        company_link_obj = company_item.find_element(By.CLASS_NAME,'similar-item__title')
        company_description = company_item.find_element(By.CLASS_NAME, 'similar-item__description')
        company_link = company_link_obj.find_element(By.TAG_NAME, 'a')
        company_data['company_id'] = int(company_item.get_attribute('data-companyid'))
        company_data['name'] = company_link_obj.find_element(By.TAG_NAME, 'a').text
        company_data['index_num'] = int(re.match(r"^\d+", company_data['name']).group(0))
        company_data['description'] = company_description.text
        company_data['page_url'] = company_link.get_attribute('href')
        company_list.append(company_data)
    
    return company_list