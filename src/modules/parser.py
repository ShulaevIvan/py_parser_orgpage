from pprint import pprint
import re
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Parser:
    def __init__(self):
        self.options = Options()
        self.driver = ''
        self.options.add_argument('--headless=new') 
        self.options.add_argument('--incognito')
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.options)
        self.company_list = []
        self.start_index = 0
        


    def parse_page(self):
        self.driver.get('https://www.orgpage.ru/moskva/krasota-i-zdorove/')
        main_container = self.driver.find_element(By.ID, 'rubricator-result')
        next_btn_wrap = self.driver.find_element(By.CSS_SELECTOR, '.rubricator-paging')
        wait = WebDriverWait(self.driver, 3)

        for i in range(1):
            company_items = self.driver.find_elements(By.CSS_SELECTOR, '.object-item.similar-item')
            company_data = self.parse_next_page(company_items, self.start_index)
            self.company_list = self.company_list + company_data
            self.start_index = int(self.company_list[-1]['index_num'])
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.gradient.next')))
            next_page_btn = self.driver.find_element(By.CSS_SELECTOR, '.gradient.next')
            next_page_btn.click()

        for company_data in self.company_list:
            company_data['contact_data'] = self.parse_company_info(company_data['page_url'])
    
    def parse_next_page(self, company_elements, index_num):
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

    def parse_company_info(self, company_url):
        self.driver.get(company_url)
        wait = WebDriverWait(self.driver, 3)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.problem-modal-for-company')))
        company_information_wrap = self.driver.find_element(By.CSS_SELECTOR, '.company-information__row')
        company_information_site = self.driver.find_element(By.CSS_SELECTOR, '.company-information__site-text')
        company_address_main = self.driver.find_element(By.CSS_SELECTOR, '.main-address.company-information__address-title')
        company_address_region = self.driver.find_element(By.CSS_SELECTOR, '.company-information__address-text')

        phone_tag = company_information_wrap.find_element(By.CSS_SELECTOR, '.company-information__phone')
        phone = ''
        site = ''
        address = ''
        email = ''

        if company_information_site:
            web_contacts = company_information_site.find_elements(By.TAG_NAME, 'p')

            for i in range(len(web_contacts)):
                if i == 0:
                    site = web_contacts[i].text
                else:
                    email = web_contacts[i].text

        if phone_tag:
            phone = phone_tag.text
        if company_information_site and company_information_site.find_element(By.TAG_NAME, 'p'):
            site = company_information_site.find_element(By.TAG_NAME, 'p').find_element(By.TAG_NAME, 'a').get_attribute('href')
        if company_address_region and company_address_main:
            company_address_span = company_address_region.find_elements(By.TAG_NAME, 'span')
            company_street = company_address_main.find_element(By.TAG_NAME, 'span').text
            address = f'{company_street} ' + ' '.join([str(i.text) for i in company_address_span])

        company_data = {
            'phone': phone,
            'site': site,
            'email': email,
            'address': address
        }
        self.save_to_json(company_data)
        return company_data
    
    def save_to_json(self, company_info):
        
        target_folder = f'{os.getcwd()}/output'
        file_name = f'{target_folder}/companies.json'
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)
        if not os.path.exists(file_name):
            with open(file_name, 'w+', encoding='utf-8') as json_file:
                json.dump({'company_list': []}, json_file, ensure_ascii=False, indent=4)

        with open(file_name, 'r+', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            json_data['company_list'].append(company_info)
            json_file.seek(0)
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        

