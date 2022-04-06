# go to skippedlagged
# input location, depart, and return date
# filter to "cheapest flights"
# store top 3 flights (all info) into json
# call the flight from json and go the the website of the airline
# theres a lot of airlines world wide, so we'll stick to comparing to domestic flights to big airports first
#     so i'll be switch-case'ing through a list of less than 10 airlines
# use flight info to find flight on the airline's site
# compare the flight information for accuracy
# class test_SkippedLagged_Comparison(unittest.TestCase):
import unittest
from selenium import webdriver
from functions.base_page import BasePage
from page_functions.skiplagged_page import Skiplagged
from page_functions.delta_page import Delta
import time
import pytest
import sys 

### we're using unittest so we can use the builtin functions setUp and tearDown
### honestly we dont need it, because there will be tests where just opening 1 browser per test
### isn't sufficient, but for practice's sake, we'll use it this time
class TestAirlineBasic(unittest.TestCase):
# class TestAirlineBasic():
    
    # since i plan on using one chrome browser per test
    # ill be opening one up and closing it at the end of each test
    def setUp(self):
        self.driver = webdriver.Chrome()

    @pytest.mark.run(order=3)
    def test_google(self):
        driver = self.driver
        base = BasePage(driver)
        base.navigate_to_webpage('https://www.google.com')
        
    @pytest.mark.run(order=1)
    def test_arrive_to_skiplagged(self):
        driver = self.driver
        skip = Skiplagged(driver)
        skip.navigate_to_skiplagged()

    @pytest.mark.run(order=2)
    def test_arrive_to_delta_homepage(self):
        driver = self.driver
        delta = Delta(driver)
        delta.navigate_to_delta()

    def tearDown(self):
        time.sleep(1)
        self.driver.close()
        self.driver.quit()

# if __name__ == "__main__":
#     sys.exit(pytest.main(["-qq"], plugins=[TestAirlineBasic()]))