from selenium import webdriver
from page_functions.skiplagged_page import Skiplagged
import pytest
import unittest
from functions.base_page import BasePage 

#### The tests below are to assert the different elements on the website Skiplagged.com
#### Currently there is no full end to end test
#### Each test has comments above it with test scenario ID and an explanation of what 
####     the script aims to test

# class TestSkiplagged(unittest.TestCase):
class TestSkiplagged():
    
    def tearDown(self):
        driver = webdriver.Chrome
        self.driver.quit()

#### TEST ID: AIR.SKP.001, AIR.SKP.002, AIR.SKP.003, AIR.SKP.004, AIR.SKP.005, AIR.SKP.006, AIR.SKP.007, AIR.SKP.008
#### TEST DESCRIPTION: Assert you can navigate to skiplagged (001), Assert departure and destination airport
####    can be inputted (002, 003), Assert departure and return dates can be inputted (004, 005), Select Round Trip (006),
####    select more than 1 adult and more than 1 child travelers (007, 008)
    @pytest.mark.run(order=1) 
    def test_round_trip_adult_children(self):
        self.driver = webdriver.Chrome("/Users/yeti/Desktop/Selenium Testing/chromedriver")
        driver = self.driver
        skip = Skiplagged(driver)
        base = BasePage(driver)
        direct = '//skiplagged_input_values'
        skip.navigate_to_skiplagged()
        skip.select_round_one_way_trip('Round Trip')
        skip.select_number_of_travelers(base.get_from_json("number of adults", direct), '//skiplagged_values', base.get_from_json("number of children", direct))
        skip.input_departure_airport('DTW')
        skip.input_destination_airport('MIA')
        skip.input_departure_date(base.get_from_json("departure month", direct), base.get_from_json("departure date", direct))
        skip.input_return_date(base.get_from_json("return month", direct), base.get_from_json("return date", direct))
        skip.click_search_flights

#### TEST ID: AIR.SKP.009, AIR.SKP.010
#### TEST DESCRIPTION: Select One Way trip (009), Search for a flight (010)    
    def test_one_way_trip_adult_children(self):
        self.driver = webdriver.Chrome("/Users/yeti/Desktop/Selenium Testing/chromedriver")
        driver = self.driver
        skip = Skiplagged(driver)
        base = BasePage(driver)
        direct = '//skiplagged_input_values'
        skip.navigate_to_skiplagged()
        skip.select_round_one_way_trip('One Way')
        skip.select_number_of_travelers(base.get_from_json("number of adults", direct), '//skiplagged_values', base.get_from_json("number of children", direct))
        skip.input_departure_airport('MCO')
        skip.input_destination_airport('DTW')
        skip.input_departure_date(base.get_from_json("departure month", direct), base.get_from_json("departure date", direct))
        skip.click_search_flights

#### TEST ID: AIR.SKP.011, AIR.SKP.012, AIR.SKP.013
#### TEST DESCRIPTION: Assert header titles that precede the deals (011), Assert all the 12 deals on the home page are skiplagged rates (012),
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

#### TEST ID: AIR.SKP.014, AIR.SKP.015, AIR.SKP.016, AIR.SKP.017, AIR.SKP.018, AIR.SKP.019
#### TEST DESCRIPTION: Assert top row of links work (skiplagged, flights, hotels, cars, rewards, login)
    def test_assert_top_home_page_links(self):
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

#### TEST ID: AIR.SKP.020, AIR.SKP.021, AIR.SKP.022, AIR.SKP.023
#### TEST DESCRIPTION: Assert links below the Airpot Input box on the home page (20), Assert rewards ad link (21), Assert Read Full FAQ link (22),
#### Assert mobile app link (23)
    def test_assert_rest_of_home_page_links(self):
        self.driver = webdriver.Chrome("/Users/yeti/Desktop/Selenium Testing/chromedriver")
        driver = self.driver
        skip = Skiplagged(driver)
        skip.navigate_to_skiplagged()
        skip.assert_featured_in_link()
        skip.navigate_to_skiplagged()
        skip.assert_rewards_ad_link()
        skip.assert_faq_link()
        skip.navigate_to_skiplagged()
        skip.assert_mobile_app_link()

#### TEST ID: AIR.SKP.024
#### TEST DESCRIPTION: Assert Links on the footer of home page,
    def test_assert_home_page_footer(self):
        self.driver = webdriver.Chrome("/Users/yeti/Desktop/Selenium Testing/chromedriver")
        driver = self.driver
        skip = Skiplagged(driver)
        skip.navigate_to_skiplagged()
        skip.assert_footer_elements()
        skip.assert_about_link()
        skip.navigate_to_skiplagged()
        skip.assert_faq_link()
        skip.navigate_to_skiplagged()
        skip.assert_press_link()
        skip.navigate_to_skiplagged()
        skip.assert_terms_link()
        skip.navigate_to_skiplagged()
        skip.assert_careers_link()
        skip.navigate_to_skiplagged()
        skip.assert_footer_language_select()
        skip.navigate_to_skiplagged()
        skip.assert_footer_currency_select()
        skip.navigate_to_skiplagged()
        skip.assert_facebook_link()
        skip.navigate_to_skiplagged()
        skip.assert_twitter_link()
        skip.navigate_to_skiplagged()
        skip.assert_instagram_link()
        skip.navigate_to_skiplagged()

#### assert page of departure flights, check if a departure flight can be selected
#### assert page of return flights, check if return flight can be selected
#### confrim information on Book Now module; date, duration, number of spots, number of traveleres, price
#### switch tabs
#### confirm
    def test_end_to_end_round_trip(self):
        self.driver = webdriver.Chrome("/Users/yeti/Desktop/Selenium Testing/chromedriver")
        driver = self.driver
        skip = Skiplagged(driver)
        base = BasePage(driver)
        our_input_values_directory = '//skiplagged_input_values'
        write_to_directory = '//skiplagged_values'
        base.empty_json(write_to_directory)
        skip.navigate_to_skiplagged()
        skip.select_round_one_way_trip('Round Trip')
        # select_number_of_travelers is buggy
        skip.select_number_of_travelers(base.get_from_json("number of adults", our_input_values_directory), directory = write_to_directory, children = base.get_from_json("number of children", our_input_values_directory))
        skip.input_departure_airport(base.get_from_json("departure airport", our_input_values_directory))
        skip.input_destination_airport(base.get_from_json("destination airport", our_input_values_directory))
        skip.input_departure_date(base.get_from_json("departure month", our_input_values_directory), base.get_from_json("departure date", our_input_values_directory))
        skip.input_return_date(base.get_from_json("return month", our_input_values_directory), base.get_from_json("return date", our_input_values_directory))
        skip.click_search_flights()
        # assert departure flights page
        # select departure flight
        skip.select_filter_type_of_flight(type="Standard", only="Yes")
        skip.collect_flight_info('5', write_to_directory)
        skip.select_flight_index('5')
        # assert information is correct after selection
        skip.assert_selected_departure_flight(base.get_from_json("flight", our_input_values_directory), write_to_directory)
        # select return flight
        skip.collect_flight_info('5', write_to_directory)
        skip.select_flight_index('5')
        # assert information is correct on module
        # skip.assert_departure_module(base.get_from_json("flight", our_input_values_directory), write_to_directory, our_input_values_directory)
        # book now, switch tabs, wait
        # confirm flight information again
        # assert/input traveler infomration and contact details
        # assert payment box information

    def test_test(self):
        self.driver = webdriver.Chrome("/Users/yeti/Desktop/Selenium Testing/chromedriver")
        driver = self.driver
        skip = Skiplagged(driver)
        base = BasePage(driver)
        our_input_values_directory = '//skiplagged_input_values'
        write_to_directory = '//skiplagged_values'
        driver.get('https://skiplagged.com/flights/LAX/DTW/2022-06-18/2022-07-28?adults=2&children=2#trip=NK1720-NK1188,NK417-NK339')
        # skip.assert_departure_module(base.get_from_json("flight", our_input_values_directory), write_to_directory, our_input_values_directory)
