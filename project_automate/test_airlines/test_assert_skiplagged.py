from selenium import webdriver
from page_functions.skiplagged_page import Skiplagged
import pytest
import unittest
from functions.base_page import BasePage

class TestSkiplagged(unittest.TestCase):
    
#### TEST AIR.SKP.001, AIR.SKP.002, AIR.SKP.003, AIR.SKP.004, AIR.SKP.005, AIR.SKP.006, AIR.SKP.007, AIR.SKP.008
#### TEST SCENARIO: Assert you can navigate to skiplagged (001), Assert departure and destination airport
####    can be inputted (002, 003), Assert departure and return dates can be inputted (004, 005), Select Round Trip (006),
####    select more than 1 adult and more than 1 child travelers (007, 008)

    def tearDown(self):
        driver = webdriver.Chrome
        self.driver.quit()

    @pytest.mark.run(order=1) 
    def test_assert_return_trip_input(self):
        self.driver = webdriver.Chrome("/Users/yeti/Desktop/Selenium Testing/chromedriver")
        driver = self.driver
        skip = Skiplagged(driver)
        skip.navigate_to_skiplagged()
        skip.select_round_one_way_trip('Round Trip')
        skip.select_number_of_travelers('2', '2')
        skip.input_departure_airport('DTW')
        skip.input_destination_airport('MIA')
        skip.input_departure_date('MAY', '22')
        skip.input_return_date('june', '1')
        skip.search_flights()


#### TEST AIR.SKP.009, AIR.SKP.010
#### TEST SCENARIO: Select One Way trip (009), Search for a flight (010)    
    def test_assert_one_way_trip_input(self):
        self.driver = webdriver.Chrome("/Users/yeti/Desktop/Selenium Testing/chromedriver")
        driver = self.driver
        skip = Skiplagged(driver)
        skip.navigate_to_skiplagged()
        skip.select_round_one_way_trip('One Way')
        skip.input_departure_airport('MCO')
        skip.input_destination_airport('DTW')
        skip.input_departure_date('MAY', '22')
        skip.search_flights()

#### TEST AIR.SKP.011, AIR.SKP.012, AIR.SKP.013
#### TEST SCENARIO: Assert header titles that precede the deals (011), Assert all the 12 deals on the home page are skiplagged rates (012),
####        Input location to search deal (013), Assert searched location appears on one of the Deals (014)
    def test_assert_home_page_deals(self):
        self.driver = webdriver.Chrome("/Users/yeti/Desktop/Selenium Testing/chromedriver")
        driver = self.driver
        skip = Skiplagged(driver)
        skip.navigate_to_skiplagged()
        skip.assert_header_preceding_deals_homepage()
        skip.assert_deals_on_homepage()
        skip.input_deals_location_and_assert('MIA')
        skip.input_deals_location_and_assert('Los Angeles')

#### TEST AIR.SKP.014-0.19
#### TEST SCENARIO: Assert top row of links work (skiplagged, flights, hotels, cars, rewards, login)
    def test_assert_top_page_links(self):
        self.driver = webdriver.Chrome("/Users/yeti/Desktop/Selenium Testing/chromedriver")
        driver = self.driver
        skip = Skiplagged(driver)
        skip.navigate_to_skiplagged()
        skip.assert_tr_link_skiplagged()
        skip.navigate_to_skiplagged()
        skip.assert_tr_link_flights()
        skip.navigate_to_skiplagged()
        skip.assert_tr_link_hotels()
        skip.navigate_to_skiplagged()
        # cars link believes im a robot
        # skip.assert_tr_link_cars()
        # skip.navigate_to_skiplagged()
        skip.assert_tr_link_rewards()
        skip.navigate_to_skiplagged()
        skip.assert_tr_link_login()
        skip.navigate_to_skiplagged()
        skip.assert_sued_us_link()
