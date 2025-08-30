from pprint import pprint
from parser_config import parser_config

class ControlPanel:


    def __init__(self):
        selected_region = None,
        selected_city = None,
        selected_category = None
        
        self.get_parametrs()

    def get_parametrs(self):
        regions_str = ''.join([f"\n{reg['name']} - {reg['key_number']}" for reg in parser_config['regions']])
        categories_str = ''.join([f"\n{cat['name']} - {cat['key_number']}" for cat in parser_config['categories']])
        region_welcome_message = f'Выберите регион для поиска: {regions_str}'
        category_welcome_message = f'Выберите категорию для поиска:\n {categories_str}'
        region_number = ''
        category_number = ''

        while True:
            if (region_number and int(region_number)) and category_number and int(category_number):
                self.start_parsing()
                break
            try:
                print(region_welcome_message)
                region_number = int(input('\nВведите номер региона:'))
                check_region_is_avalible = list(filter(lambda region: (region['key_number'] == region_number) , parser_config['regions']))
                if region_number and int(region_number) and len(check_region_is_avalible) > 0:
                    self.selected_region = int(region_number)
                    print(category_welcome_message)
                    category_number = int(input('\nВведите номер категории:'))
                    check_category_is_avalible = list(filter(lambda category: (category['key_number'] == category_number) , parser_config['categories']))
                    if category_number and int(category_number) and len(check_category_is_avalible) > 0:
                        self.selected_category = int(category_number)
                else:
                    continue
            except ValueError:
                self.get_parametrs()
                break

    def start_parsing(self):
        print(self.selected_category)
        print(self.selected_region)

    