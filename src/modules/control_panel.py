from parser_config import parser_config

class ControlPanel:

    def __init__(self):
        selected_region = None,
        selected_city = None,
        selected_category = None

    def get_user_prompt(self, user_str):
        user_prompt = input('выберите регион для поиска')
        avalible_regions = [f'{reg['name']} - {reg['key_number']}' for reg in parser_config['regions']]
    