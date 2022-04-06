
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import os, glob, shutil
import json
import urllib.request
from PIL import Image


# This will the the parent class for all the pages in our application
# the most common elements and functions will be stored here
class BasePage():
    
# this function is called every time a new object in this class is created
# the self variable is used to represent the instance of the class
    def __init__(self, driver):
        self.driver = driver

    def open_chrome(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def navigate_to_webpage(self, link):
        self.driver.get(link)

    def highlight_element(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        def apply_style(s):
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)
        original_style = element.get_attribute('style')
        apply_style("border: 4px solid green")
        time.sleep(.2)
        apply_style(original_style)

    def assert_element_is_displayed(self, xpath):
        WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.XPATH, xpath)))
        self.highlight_element(xpath)

    def click_element(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        self.highlight_element(xpath)
        element.click()
        time.sleep(1)

    def send_text(self, xpath, text):
        element = self.driver.find_element(By.XPATH, xpath)
        self.highlight_element(xpath)
        element.clear()
        element.send_keys(text)
        time.sleep(0.5)

    def enter_text(self, by_locator, text):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).send_keys(text)

    def send_text_enter(self, xpath, text):
        element = self.driver.find_element(By.XPATH, xpath)
        self.highlight_element(xpath)
        element.clear()
        element.send_keys(text)
        time.sleep(0.5)
        element.send_keys(Keys.RETURN)
        time.sleep(1)

    def check_if_element_exists(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            self.highlight_element(xpath)
            return True
        except Exception:
            return False

    def get_text(self, xpath):
        WebDriverWait(self, 4).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = self.driver.find_element(By.XPATH, xpath)
        element_text = element.text
        self.highlight_element(xpath)
        return element_text






################################################################
################################################################
################    JSON CODE   ################################
################                ################################

    def write_to_json(products):
        try:
            with open(os.getcwd() + '//values3.json', 'w') as json_file:
                # assume products are json objects
                json_file.write(json.dumps(products, indent=2))
        except FileNotFoundError as e:
            pass

    def get_from_json(directory):
        with open(os.getcwd() + '//%s.json' % directory) as json_file:
            data = json.load(json_file)
        return data

    def empty_json(directory):
        open(os.getcwd() + '//%s.json' % directory, 'w').close()


    def write_to_json_directory(json_values, directory=None):
        if directory == None:
            try:
                with open(os.getcwd() + '//values.json', 'w') as json_file:
                    # assume products are json objects
                    json_file.write(json.dumps(json_values, indent=2))
            except FileNotFoundError as e:
                pass
        else:
            try:
                with open(os.getcwd() + '//%s.json' % directory, 'w') as json_file:
                    # assume products are json objects
                    json_file.write(json.dumps(json_values, indent=2))
            except FileNotFoundError as e:
                pass

    def append_to_json_directory(json_values, directory=None):
        if directory == None:
            try:
                with open(os.getcwd() + '//values.json', 'a') as json_file:
                    # assume products are json objects
                    json_file.write(json.dumps(json_values, indent=2))
            except FileNotFoundError as e:
                pass
        else:
            try:
                with open(os.getcwd() + '//%s.json' % directory, 'a') as json_file:
                    # assume products are json objects
                    json_file.write(json.dumps(json_values, indent=2))
            except FileNotFoundError as e:
                pass

    def write_to_ebay_folder(json_values, directory=None):
        if directory == None:
            try:
                with open(os.getcwd() + '//ebay_values//values.json', 'w') as json_file:
                    # assume products are json objects
                    json_file.write(json.dumps(json_values, indent=2))
            except FileNotFoundError as e:
                pass
        else:
            try:
                with open(os.getcwd() + '//ebay_values//%s.json' % directory, 'w') as json_file:
                    # assume products are json objects
                    json_file.write(json.dumps(json_values, indent=2))
            except FileNotFoundError as e:
                with open(os.getcwd() + '//ebay_values//ebay_backup.json', 'w') as json_file:
                    # assume products are json objects
                    json_file.write(json.dumps(json_values, indent=2))

    def empty_folder(folder_name):
        dir = os.getcwd() + '/%s' % folder_name
        for file in os.scandir(dir):
            os.remove(file.path)

    # def empty_desktop_folder(folder_name):
    #     dir = '/%s' % folder_name
    #     for file in os.scandir(dir):
    #         os.remove(file.path)1

    def empty_desktop_folder(path):
        nested_paths = glob.glob(path)
        for nested_path in nested_paths:
            if os.path.isdir(nested_path):
                shutil.rmtree(nested_path)
            else:
                os.remove(nested_path)
        # dirs = glob.glob(path)
        # for dir in dirs:
        #     for file in glob.glob(dir):
        #         os.remove(file)
        #     os.rmdir(dir)

    def get_image(self, xpath, save_path):
        self.highlight_element(xpath)
        img_url = self.driver.find_element(By.XPATH, xpath).get_attribute('src')
        urllib.request.urlretrieve(img_url, save_path) # to save to folder in vscode, os.getcwd() + //nameOfFolder
        
        return save_path

    def get_image_to_desktop_folder(self, xpath, path, file_name):
        self.highlight_element(xpath)
        # path = os.path.join('/Users/yeti/Desktop/', folder_name)

        img_url = self.driver.find_element(By.XPATH, xpath).get_attribute('src')
        urllib.request.urlretrieve(img_url, "//%s//%s.jpg" % (path, file_name))
