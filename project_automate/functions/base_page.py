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


#### This page contains all the basic, builder functions that are resuable throughout
#### more than one webpage

class BasePage():
    
    def __init__(self, driver):
        self.driver = driver

    def open_chrome(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def navigate_to_webpage(self, link):
        self.driver.get(link)

    def wait_until_element_is_present(self, element_xpath):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, element_xpath)))

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

    def hover_over_element(self, xpath):
        hover_element = self.driver.find_element(By.XPATH, xpath)
        hover = ActionChains(self.driver)
        hover.move_to_element(hover_element)
        hover.perform()

    def hover_and_click_element(self, hover_xpath, click_xpath):
        hover_element = self.driver.find_element(By.XPATH, hover_xpath)
        hover = ActionChains(self.driver)
        hover.move_to_element(hover_element)
        hover.perform()
        self.find_element_by_xpath(click_xpath).click()

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
        # WebDriverWait(self, 4).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = self.driver.find_element(By.XPATH, xpath)
        element_text = element.text
        self.highlight_element(xpath)
        return element_text

    # def get_flight_data(self, )

    def get_table_col_values(self, table_xpath, col_number, array_name, element_tag = None):
        array_name = []
        self.driver.find_element_by_xpath(By.XPATH, table_xpath)
        rows_xpath = table_xpath + '//tr'
        rows = self.driver.find_elements_by_xpath(By.XPATH, rows_xpath)
        for index, row in enumerate(rows, start = 1):
            col_xpath = rows_xpath + '//td[%d]//span' % col_number
            col_data = self.driver.find_elements_by_xpath(By.XPATH, col_xpath)
            for index2, cell_data in enumerate(col_data, start = 2): #start at 2 because the first row is the header
                array_name.append(cell_data.text)

    def table_match_value_and_assert_element(self, table_xpath, match_index, match_value, element_tag = None):
        self.driver.find_element_by_xpath(By.XPATH, table_xpath)
        rows_xpath = table_xpath + '//tr'
        rows = self.driver.find_elements_by_xpath(By.XPATH, rows_xpath)
        for index, row in enumerate(rows, start = 1):
            col_xpath = rows_xpath + '//td[%d]//span' % match_index
            col_data = self.driver.find_elements_by_xpath(By.XPATH, col_xpath)
            for index2, cell_data in enumerate(col_data, start = 2): #start at 2 because the first row is the header
                rows_xpath = table_xpath + '//tr[%d]' % index2
                if cell_data.text == match_value:
                    if element_tag != None:
                        element = rows_xpath + '//%s[text()="%s"]' %  (element_tag, match_value)
                    else:
                        element = rows_xpath + '//span[text()="%s"]' % match_value
                    self.assert_element_is_displayed(element)
                    break
    
    def span_with_text(self, text):
        xpath = '//span[text()="%s"]' % text
        return xpath

    def span_containing_text(self, text):
        xpath = '//span[contains(text(), "%s")]' % text
        return xpath

    def div_with_text(self, text):
        xpath = '//div[text()="%s"]' % text
        return xpath

    def label_with_text(self, text):
        xpath = '//label[text()="%s"]' % text
        return xpath

    def link_with_text(self, text):
        xpath = '//a[text()="%s"]' % text
        return xpath

    def font_with_text(self, text):
        xpath = '//font[text()="%s"]' % text
        return xpath

    def button_with_text(self, text):
        xpath = '//button[text()="%s"]' % text
        return xpath

    def button_with_text_index(self, text, index):
        xpath = '(//button[text()="%s"])[%s]' % (text, index)
        return xpath

    def header_with_text(self, header_number, text):
        xpath = '//h%s[text()="%s"]' % (header_number, text)
        return xpath

    def find_element_by_xpath(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        return element

    def find_elements_by_xpath(self, xpath):
        elements = self.driver.find_elements(By.XPATH, xpath)
        return elements

    def empty_folder(folder_name):
        dir = os.getcwd() + '/%s' % folder_name
        for file in os.scandir(dir):
            os.remove(file.path)

    def empty_desktop_folder(path):
        nested_paths = glob.glob(path)
        for nested_path in nested_paths:
            if os.path.isdir(nested_path):
                shutil.rmtree(nested_path)
            else:
                os.remove(nested_path)

    def get_image(self, xpath, save_path):
        self.highlight_element(xpath)
        img_url = self.driver.find_element(By.XPATH, xpath).get_attribute('src')
        urllib.request.urlretrieve(img_url, save_path) # to save to folder in vscode, os.getcwd() + //nameOfFolder
        
        return save_path

    def get_image_to_desktop_folder(self, xpath, path, file_name):
        self.highlight_element(xpath)

        img_url = self.driver.find_element(By.XPATH, xpath).get_attribute('src')
        urllib.request.urlretrieve(img_url, "//%s//%s.jpg" % (path, file_name))

    def get_attribute(self, xpath, attribute):
        element_attribute = self.driver.find_element(By.XPATH, xpath).get_attribute(attribute)
        return element_attribute

    def add_new_dictionary(self, dictionary, directory):
        with open(os.getcwd() + '//project_automate//values%s.json' % directory) as json_file:
            data = json_file.read()
        d = json.loads(data)
        new_dictionary = {
            "%s" % dictionary: []
        }
        d.update(new_dictionary)
        with open(os.getcwd() + '//project_automate//values%s.json' % directory, 'w') as json_file:
            json_file.seek(0)
            json_file.write(json.dumps(d, indent=2))
            json_file.truncate()

    def write_to_dictionary(self, json_key, json_value, directory): ### add to the bottom of a json dictionary
        file_location = os.getcwd() + '//project_automate//values%s.json' % directory
        with open(os.getcwd() + '//project_automate//values%s.json' % directory) as json_file:
            data = json_file.read()
        d = json.loads(data)
        d["%s" % json_key] = json_value
        with open(os.getcwd() + '//project_automate//values%s.json' % directory, 'w') as json_file:
            json_file.seek(0)
            json_file.write(json.dumps(d, indent=2))
            json_file.truncate()

    def empty_json(self, directory):
        file_location = os.getcwd() + '//project_automate//values%s.json' % directory
        with open(os.getcwd() + '//project_automate//values%s.json' % directory, "w") as json_file:
            json.dump({}, json_file, indent=4, sort_keys=True)

    def get_from_json(self, json_key, directory):
        file_location = os.getcwd() + '//project_automate//values%s.json' % directory
        with open(os.getcwd() + '//project_automate//values%s.json' % directory, 'r') as json_file:
            data = json_file.read()
        d = json.loads(data)
        json_value = d["%s" % json_key]
        print(json_value)
        return json_value

    def get_from_json_all(self, directory):
        file_location = os.getcwd() + '//project_automate//values%s.json' % directory
        with open(os.getcwd() + '//project_automate//values%s.json' % directory, 'r') as json_file:
            data = json_file.read()
        json_value = json.loads(data)
        print(json_value)
        return json_value

    def get_from_json2(self, json_key1, json_key2, directory):
        file_location = os.getcwd() + '//project_automate//values%s.json' % directory
        with open(os.getcwd() + '//project_automate//values%s.json' % directory, 'r') as json_file:
            data = json_file.read()
        d = json.loads(data)
        json_value = d["%s" % json_key1]["%s" % json_key2]
        print(json_value)
        return json_value

    def get_from_json3(self, json_key1, json_key2, json_key3, directory):
        file_location = os.getcwd() + '//project_automate//values%s.json' % directory
        with open(os.getcwd() + '//project_automate//values%s.json' % directory, 'r') as json_file:
            data = json_file.read()
        d = json.loads(data)
        json_value = d["%s" % json_key1]["%s" % json_key2]["%s" % json_key3]
        print(json_value)
        return json_value

    def switch_to_newest_tab(self):
        time.sleep(0.5)
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def close_current_tab(self):
        self.driver.close()
        time.sleep(0.5)
        try:
            self.switch_to_newest_tab()
        except Exception:
            pass