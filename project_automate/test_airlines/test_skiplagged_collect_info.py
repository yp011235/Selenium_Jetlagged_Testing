from selenium import webdriver
from page_functions.skiplagged_page import Skiplagged
import pytest
from webdriver_manager.chrome import ChromeDriverManager
from functions.base_page import BasePage 
import unittest
# problems i encountered
# simple ones: changing xpaths
# more difficults ones:
#       creating classes so i could inherit functions and driver from other files in different folders
#       writing to json in an organized way, so it would just append onto the dictionary but replace the whole thing
#               or to change just one value in a dictionary
#       


### we're not using any unittest functions, we're simply using the pytest configuration to run our tests
### we're using unittest to set up our test class and emptying our json file
class TestSkiplagged(unittest.TestCase):

    def setUpClass():
        driver = webdriver.Chrome
        base = BasePage(driver)
        base.empty_json('//skiplagged_values')

    # @pytest.mark.run(order=1) 
    def test_collect_flight_info1(self):
        self.driver = webdriver.Chrome("/Users/yeti/Desktop/Selenium Testing/chromedriver")
        driver = self.driver
        skip = Skiplagged(driver)
        # go to skiplagged.com
        skip.navigate_to_skiplagged()
        # input departure airport
        skip.input_departure_airport('DTW')
        # input departure date and return date
        skip.input_departure_date('MAY', '22')
        skip.input_return_date('june', '1')
        skip.search_flights()
        # write a list of cheap cities and their price on a list, we'll use it for later price analytics
        # then we'll go into the top x cities or the cities within a price range, and collect their info
        skip.navigate_into_filter_and_collect('2', '//skiplagged_values')
        self.driver.close()
        self.driver.quit()

    def test_collect_flight_info2(self):
        self.driver = webdriver.Chrome("/Users/yeti/Desktop/Selenium Testing/chromedriver")
        driver = self.driver
        skip = Skiplagged(driver)
        skip.navigate_to_skiplagged()
        skip.input_departure_airport('DTW')
        skip.input_departure_date('MAY', '22')
        skip.input_return_date('june', '1')
        skip.search_flights()
        skip.navigate_into_filter_and_collect('2', '//skiplagged_values')
        self.driver.close()
        self.driver.quit()

    def test_collect_flight_info3(self):
        self.driver = webdriver.Chrome("/Users/yeti/Desktop/Selenium Testing/chromedriver")
        driver = self.driver
        skip = Skiplagged(driver)
        skip.navigate_to_skiplagged()
        skip.input_departure_airport('DTW')
        skip.input_departure_date('MAY', '22')
        skip.input_return_date('june', '11')
        skip.search_flights()
        skip.navigate_into_filter_and_collect_all('2', '//skiplagged_values')
        self.driver.close()
        self.driver.quit()

