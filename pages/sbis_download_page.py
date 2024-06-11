import os
import requests
import tempfile
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

from pages.locators.sbis_download_page_locators import *
from utilites.constants import *

logger = logging.getLogger(__name__)

class SBISDownloadPage:

    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        logger.info(f"Opening URL: {url}")
        self.driver.get(url)

    def click_download_link(self):
        logger.info("Clicking on download link")
        download_link = self.driver.find_element(*SbisDownloadPageLocators.DOWNLOAD_LINK)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", download_link)
        download_link.click()

    def click_plugin_element(self):
        logger.info("Clicking on plugin element")
        plugin_element = self.driver.find_element(*SbisDownloadPageLocators.PLUGIN_ELEMENT)
        self.mouse_click(plugin_element)

    def download_file(self):
        logger.info("Downloading file from URL")
        response = requests.get(FILE_URL)
        assert response.status_code == 200, "Failed to download the file"

        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, FILE_NAME)

        with open(file_path, 'wb') as f:
            f.write(response.content)

        assert os.path.exists(file_path), "Downloaded file does not exist"
        return file_path

    def validate_file_size(self, file_path, expected_size):
        actual_size = os.path.getsize(file_path)
        assert actual_size == expected_size, f"File size mismatch: expected {expected_size}, got {actual_size}"

    def mouse_click(self, element):
        logger.info("Performing mouse click on element")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

    def wait_for_plugin_element(self):
        logger.info("Waiting for plugin element to be visible")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(SbisDownloadPageLocators.PLUGIN_ELEMENT)
        )
