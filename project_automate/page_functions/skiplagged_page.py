from functions.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By
from locaters.skiplagged_locators import SkiplaggedLocators as sl

class Skiplagged(BasePage):

    def __init__(self, driver):
        self.driver = driver

    def navigate_to_skiplagged(self):
        self.navigate_to_webpage('https://skiplagged.com/')
        self.assert_element_is_displayed(sl.SKIPLAGGED_HOME_HEADER)