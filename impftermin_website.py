import datetime
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class ImpfterminWebsite:
    url = ""

    def __init__(self, url, headless=False):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")  # for sudo linux usage
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1600, 768)
        self.url = url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        time.sleep(5)
        self.driver.close()

    def open_website(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/app-root/div/app-page-ets-search/div/app-ets-corona-search-overlay/div/div/div[2]/div/div[2]/form/div/button')))
        assert "116117" in self.driver.title

    def has_available_slot(self):
        return not "Derzeit stehen leider keine Termine zur Verfügung." in self.driver.page_source
