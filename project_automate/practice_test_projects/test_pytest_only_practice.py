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
from page_functions.skiplagged_page import Skiplagged
from page_functions.delta_page import Delta
import time
import pytest
import sys 

### we're not using any unittest functions, we're simply using the pytest configuration to run our tests
class TestPytestOnlyPractice():

    @pytest.mark.run(order=1) 
    def test_arrive_to_skiplagged(self):
        self.driver = webdriver.Chrome()
        driver = self.driver
        skip = Skiplagged(driver)
        skip.navigate_to_skiplagged()
        self.driver.close()
        self.driver.quit()

    @pytest.mark.run(order=2)
    def test_arrive_to_delta_homepage(self):
        self.driver = webdriver.Chrome()
        driver = self.driver
        delta = Delta(driver)
        delta.navigate_to_delta()
        self.driver.close()
        self.driver.quit()
        