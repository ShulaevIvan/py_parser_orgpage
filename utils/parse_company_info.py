from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def parse_company_info(company_url):
    chrome_options = Options()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--headless=new') 
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    company_page = driver.get(company_url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.problem-modal-for-company')))
    company_information_wrap = driver.find_element(By.CSS_SELECTOR, '.company-information__row')
    # company_address_main = driver.find_element(By.CSS_SELECTOR, '.main-address.company-information__address-title').find_element(By.TAG_NAME, 'span')
    # company_address_region = driver.find_element(By.CSS_SELECTOR, '.company-information__address-text').find_elements(By.TAG_NAME, 'span')
    company_information_site = driver.find_element(By.CSS_SELECTOR, '.company-information__site-text')

    phone_tag = company_information_wrap.find_element(By.CSS_SELECTOR, '.company-information__phone')
    # site_tag = company_information_site.find_element(By.TAG_NAME, 'p')
    # email_tag = company_information_site.find_element(By.CSS_SELECTOR, '.email')
    phone = ''
    site = ''
    address = ''
    email = ''


    if phone_tag:
        phone = phone_tag.text
    # if site_tag:
    #     site: site_tag.find_element(By.TAG_NAME, 'a').get_attribute('href')
    # if email_tag:
    #     email = email_tag.find_element(By.TAG_NAME, 'a')
    # if site_tag:
    #     site = site_tag.get_attribute('href')
    # if email_tag:
    #     email = email_tag.text
    # if company_address_main:
    #     address = company_address_main.text
    # if len(company_address_region) > 0 and address:
    #     address = f'{company_address_main} ' + ' '.join([str(i.text) for i in company_address_region])


    company_data = {
        'phone': phone,
        'site': site,
        'email': email,
        'address': address
    }
    driver.close()
    return company_data