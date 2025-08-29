from pprint import pprint
from src.modules.control_panel import ControlPanel
from src.modules.parser import Parser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


if __name__ == "__main__":
    control_panel = ControlPanel()
    # parser = Parser()
    # parser.parse_page()