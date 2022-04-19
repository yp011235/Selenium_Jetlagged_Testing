from selenium import webdriver
from page_functions.skiplagged_page import Skiplagged
import pytest
from webdriver_manager.chrome import ChromeDriverManager
from functions.base_page import BasePage 

class TestSkiplagged():
    
#### TEST AIR.SKP.001, AIR.SKP.002, AIR.SKP.003, AIR.SKP.004, AIR.SKP.005, AIR.SKP.006, AIR.SKP.007
#### TEST SCENARIO: Assert you can navigate to skiplagged (001), Assert departure and destination airport
####    can be inputted (002, 003), Assert departure and return dates can be inputted (004, 005), Select Round Trip (006),
####    select more than 1 travelers (007)
    @pytest.mark.run(order=1) 
    def test_assert_departure_return_airports_dates(self):
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

    @pytest.mark.run(order=1) 
    def test_assert_departure_return_airports_dates_fail(self):
        self.driver = webdriver.Chrome("/Users/yeti/Desktop/Selenium Testing/chromedriver")
        driver = self.driver
        skip = Skiplagged(driver)
        skip.navigate_to_skiplagged()
        skip.select_round_one_way_trp('Round Trip')
        skip.select_number_of_travelers('2', '2')
        skip.input_departure_airport('DTW')
        skip.input_destination_airport('MIA')
        skip.input_departure_date('MAY', '44')
        skip.input_return_date('june', '1')
        skip.search_flights()