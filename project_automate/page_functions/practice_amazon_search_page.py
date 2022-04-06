from locaters.practice_amazon_locators import AmazonLocators as al
from functions.base_page import BasePage as base
# we would use the above if we 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from functions.base_page import BasePage

# inheriting methods from BasePage class
class AmazonPage(BasePage):
# class AmazonPage():
    def __init__(self, driver):
        self.driver = driver

    def navigate_to_amazon(self):
        self.navigate_to_webpage("https://www.amazon.com/")
        
    def enter_search(self, search_query):
        self.send_text(al.AMAZON_SEARCH_INPUT_BOX, search_query)
        self.click_element(al.AMAZON_SEARCH_BUTTON)

    def click_a_link_from_upper_nav(self, link):
        self.click_element(al.SELECT_FROM_AMAZON_HOME_UPPER_NAV_BAR % str(link))

    def assert_books_page(self):
        self.assert_element_is_displayed(al.AMAZON_BOOK_PAGE_HEADER)
