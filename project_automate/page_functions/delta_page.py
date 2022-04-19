from functions.base_page import BasePage
from locators.delta_locators import DeltaLocators as dl

class Delta(BasePage):

    def __init__(self, driver):
        self.driver = driver

    def navigate_to_delta(self):
        self.navigate_to_webpage('https://www.delta.com/')
        self.assert_element_is_displayed(dl.DELTA_HOME_NAV_BAR)