from asyncio import wait_for
from xml.dom import NotFoundErr
from functions.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By
from locators.skiplagged_locators import SkiplaggedLocators as sl
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)))

class Skiplagged(BasePage):

    def __init__(self, driver):
        self.driver = driver

    def navigate_to_skiplagged(self):
        self.navigate_to_webpage('https://skiplagged.com/')
        self.wait_until_element_is_present(sl.SKIPLAGGED_HOME_HEADER)
        self.assert_element_is_displayed(sl.SKIPLAGGED_HOME_HEADER)

    def select_round_one_way_trip(self, choice):
        self.click_element(sl.SKIPLAGGED_ROUND_TRIP_OR_ONE_WAY_DROP_DOWN)
        self.wait_until_element_is_present(sl.SKIPLAGGED_ROUND_TRIP_OR_ONE_WAY_DROP_DOWN_MENU_OPTIONS % choice)
        self.click_element(sl.SKIPLAGGED_ROUND_TRIP_OR_ONE_WAY_DROP_DOWN_MENU_OPTIONS % choice)
        self.assert_element_is_displayed(sl.SKIPLAGGED_ROUND_TRIP_OR_ONE_WAY_DROP_DOWN + '/span[text()="%s"]' % choice)

    def select_number_of_travelers(self, adults, children=None):
        self.assert_element_is_displayed(sl.SKIPLAGGED_TRAVELERS_OPTION)
        self.click_element(sl.SKIPLAGGED_TRAVELERS_OPTION)
        self.wait_until_element_is_present(sl.SKIPLAGGED_ADULTS_TRAVELLERS)
        self.assert_element_is_displayed(sl.SKIPLAGGED_ADULTS_TRAVELLERS)
        self.assert_element_is_displayed(sl.SKIPLAGGED_CHILDREN_TRAVELLERS)
        num_of_adults = self.get_text(sl.SKIPLAGGED_ADULTS_COUNT)
        while int(adults) != int(num_of_adults):
            if int(adults) > int(num_of_adults):
                self.click_element(sl.SKIPLAGGED_ADULTS_PLUS)
                time.sleep(0.5)
            if int(adults) < int(num_of_adults):
                self.click_element(sl.SKIPLAGGED_ADULTS_MINUS)
                time.sleep(0.5)
            num_of_adults = self.get_text(sl.SKIPLAGGED_ADULTS_COUNT)

        if children != None:
            num_of_children = self.get_text(sl.SKIPLAGGED_CHILDREN_COUNT)
            while int(children) != int(num_of_children):
                if int(children) > int(num_of_children):
                    self.click_element(sl.SKIPLAGGED_CHILDREN_PLUS)
                    time.sleep(0.5)
                if int(children) < int(num_of_children):
                    self.click_element(sl.SKIPLAGGED_CHILDREN_MINUS)
                    time.sleep(0.5)
                num_of_children = self.get_text(sl.SKIPLAGGED_CHILDREN_COUNT)

        if children == None:
            children = 0

        self.click_element(sl.SKIPLAGGED_TRAVELERS_OPTION)
        total_travelers = int(adults) + int(children)
        self.assert_element_is_displayed(sl.SKIPLAGGED_TOTAL_NUMBER_OF_TRAVLERS % total_travelers)

    def input_departure_airport(self, airport):
        self.send_text_enter(sl.SKIPLAGGED_DEPARTURE_AIRPORT_INPUT, airport)
        time.sleep(1)
        self.assert_element_is_displayed(sl.SKIPLAGGED_DEPARTURE_AIRPORT_INPUT + '[@value="%s"]' % airport)

    def input_destination_airport(self, airport):
        self.send_text_enter(sl.SKIPLAGGED_DESTINATION_AIRPORT_INPUT, airport)
        time.sleep(1)
        self.assert_element_is_displayed(sl.SKIPLAGGED_DESTINATION_AIRPORT_INPUT + '[@value="%s"]' % airport)
    
    def input_departure_date(self, month, date):
        self.click_element(sl.SKIPLAGGED_DEPART_DATE_INPUT)
        time.sleep(1)
        if self.check_if_element_exists(sl.SKIPLAGGED_DEPART_OR_RETURN_DATE_SELECTED) == True:
            pass
        else:
            self.click_element(sl.SKIPLAGGED_DEPART_DATE_INPUT)

        listed_months = [(self.get_text(sl.SKIPLAGGED_CALENDAR_1_MONTH_NAME)).lower(), (self.get_text(sl.SKIPLAGGED_CALENDAR_2_MONTH_NAME)).lower()]
        month = month.lower()
        time.sleep(1)
        if month == listed_months[0]:
            self.click_element(sl.SKIPLAGGED_CALENDAR_1_DATES % date)
        elif month == listed_months[1]:
            self.click_element(sl.SKIPLAGGED_CALENDAR_2_DATES % date)
        # navigate the to correct month if not on the correct one already
        else:
            while (month not in listed_months):
                self.click_element(sl.SKIPLAGGED_CALENDAR_NEXT_BUTTON)
                time.sleep(1)
                listed_months = [(self.get_text(sl.SKIPLAGGED_CALENDAR_1_MONTH_NAME)).lower(), (self.get_text(sl.SKIPLAGGED_CALENDAR_2_MONTH_NAME)).lower()]
        # click on the date
            time.sleep(1)
            self.click_element(sl.SKIPLAGGED_CALENDAR_2_DATES % date)

    def input_return_date(self, month, date):
        self.click_element(sl.SKIPLAGGED_RETURN_DATE_INPUT)
        time.sleep(1)
        if self.check_if_element_exists(sl.SKIPLAGGED_DEPART_OR_RETURN_DATE_SELECTED) == False:
            self.click_element(sl.SKIPLAGGED_RETURN_DATE_INPUT)
        else:
            pass

        listed_months = [(self.get_text(sl.SKIPLAGGED_CALENDAR_1_MONTH_NAME)).lower(), (self.get_text(sl.SKIPLAGGED_CALENDAR_2_MONTH_NAME)).lower()]
        month = (month).lower()
        time.sleep(1)
        if month == listed_months[0]:
            self.click_element(sl.SKIPLAGGED_CALENDAR_1_DATES % date)
        elif month == listed_months[1]:
            self.click_element(sl.SKIPLAGGED_CALENDAR_2_DATES % date)
        else:
            while (month not in listed_months):
                self.click_element(sl.SKIPLAGGED_CALENDAR_NEXT_BUTTON)
                time.sleep(1)
                listed_months = [(self.get_text(sl.SKIPLAGGED_CALENDAR_1_MONTH_NAME)).lower(), (self.get_text(sl.SKIPLAGGED_CALENDAR_2_MONTH_NAME)).lower()]
            self.click_element(sl.SKIPLAGGED_CALENDAR_2_DATES % date)

    # def input_departure_date2(self, month, date):
    #     self.click_element(sl.SKIPLAGGED_DEPART_DATE_INPUT)
    #     if self.check_if_element_exists(sl.SKIPLAGGED_DEPART_DATE_SELECTED) == False:
    #         self.click_element(sl.SKIPLAGGED_DEPART_DATE_INPUT)
    #     else:
    #         pass
            
    #     month = month.capitalize()

    #     while self.check_if_element_exists(sl.SKIPLAGGED_CALENDAR_1_MONTH_NAME + '[text()="%s"]' % month) == False:
    #         self.click_element(sl.SKIPLAGGED_CALENDAR_NEXT_BUTTON)
    #         time.sleep(0.5)

    #     self.click_element(sl.SKIPLAGGED_CALENDAR_1_DATES % date)

    # def input_return_date2(self, month, date):
    #     self.click_element(sl.SKIPLAGGED_RETURN_DATE_INPUT)
    #     if self.check_if_element_exists(sl.SKIPLAGGED_RETURN_DATE_SELECTED) == False:
    #         self.click_element(sl.SKIPLAGGED_RETURN_DATE_INPUT)
    #     else:
    #         pass
    #     month = month.capitalize()

    #     if self.check_if_element_exists(sl.SKIPLAGGED_CALENDAR_1_MONTH_NAME + '[text()="%s"]' % month):
    #         self.click_element(sl.SKIPLAGGED_CALENDAR_1_DATES % date)
    #     else:
    #         while self.check_if_element_exists(sl.SKIPLAGGED_CALENDAR_2_MONTH_NAME + '[text()="%s"]' % month) == False:
    #             self.click_element(sl.SKIPLAGGED_CALENDAR_NEXT_BUTTON)
    #             time.sleep(0.5)
    #         self.click_element(sl.SKIPLAGGED_CALENDAR_2_DATES % date)

    def search_flights(self):
        self.click_element(sl.SKIPLAGGED_SEARCH_FLIGHTS_BUTTON)
        time.sleep(2)

    def collect_cheapest_cities_and_flights(self):
        cities = []
        countries = []
        prices = []

        cards = self.find_elements_by_xpath(By.XPATH, sl.SKIPLAGGED_CHEAPEST_CITIES_CARD)
        for index, card in enumerate(cards):
            city = self.get_text(sl.SKIPLAGGED_CHEAPEST_CITY % index)
            country = self.get_text(sl.SKIPLAGGED_CHEAPEST_COUNTRY % index)
            if self.check_if_element_exists((sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX  % index) + sl.SKIPLAGGED_SKIPLAGGED_RATE):
                price = self.get_text((sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX  % index) + sl.SKIPLAGGED_SKIPLAGGED_RATE)
            else:
                price = self.get_text(sl.SKIPLAGGED_CHEAPEST_PRICE % index)
            
            cities.append(city)
            countries.append(country)
            prices.append(price)
        
    def navigate_into_cheapest_city_index_write_to_json(self, index, directory):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)))
        city_name = self.get_text('('+sl.SKIPLAGGED_CHEAPEST_CITY+')[%s]' % index)
        country_name = self.get_text('('+sl.SKIPLAGGED_CHEAPEST_COUNTRY+')[%s]' % index)
        json_values = {"Destination" : city_name + ", " + country_name}
        self.append_to_json_directory(json_values, directory) 
        self.write_to_json("Destination", city_name + ", " + country_name, directory=directory)       
        self.click_element(sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)
        time.sleep(1)

    def navigate_into_cheapest_city_index_write_to_json2(self, index, directory):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)))
        city_name = self.get_text('('+sl.SKIPLAGGED_CHEAPEST_CITY+')[%s]' % index)
        country_name = self.get_text('('+sl.SKIPLAGGED_CHEAPEST_COUNTRY+')[%s]' % index)
        json_value = city_name + ", " + country_name
        self.write_to_json2("Destination", json_value, directory=directory)       
        self.click_element(sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)
        time.sleep(1)

    def navigate_into_cheapest_city_index_write_to_json3(self, index, directory):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)))
        city_name = self.get_text('('+sl.SKIPLAGGED_CHEAPEST_CITY+')[%s]' % index)
        country_name = self.get_text('('+sl.SKIPLAGGED_CHEAPEST_COUNTRY+')[%s]' % index)
        json_key = city_name + ", " + country_name
        self.add_new_dictionary(json_key, directory)       
        self.click_element(sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)
        time.sleep(1)

    def navigate_into_cheapest_city_index_write_to_json4(self, index, directory):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)))
        self.click_element(sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)
        from_airline = self.get_text(sl.SKIPLAGGED_DEPARTURE_AIRPORT_INPUT + '[@value]')
        to_airline = self.get_text(sl.SKIPLAGGED_DESTINATION_AIRPORT_INPUT + '[@value]')
        json_key = from_airline + ' to ' + to_airline
        self.add_new_dictionary(json_key, directory)       
        time.sleep(1)

    def filter_list_by_price(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_PRICE_FILTER)))
        if self.check_if_element_exists(sl.SKIPLAGGED_PRICE_FILTER + '[@class="active"]'):
            pass
        else:
            self.click_element(sl.SKIPLAGGED_PRICE_FILTER)

    def filter_list_by_duration(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_DURATION_FILTER)))
        if self.check_if_element_exists(sl.SKIPLAGGED_DURATION_FILTER + '[@class="active"]'):
            pass
        else:
            self.click_element(sl.SKIPLAGGED_DURATION_FILTER)


    def  collect_top_10_flight_info(self, directory):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_LIST_OF_FLIGHTS)))
        flights = self.find_elements_by_xpath(sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW)
        # flights = driver.find_elements(by=By.XPATH, value=sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW)
        flight_time = []
        number_of_stops = []
        prices = []
        values = {}
        for index in range(1, 11, 1):
            row_xpath = '(' + sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW + ')[%s]' % index
            # row = self.find_element_by_xpath(row_xpath)
            attribute_value = self.get_attribute(row_xpath, "id")
            # flight_info = "flight %s: %s" % (index, attribute_value)
            key = "flight " + str(index) 
            values.update({key : str(attribute_value)})
            # values.append(attribute_value)
            # self.write_to_json_directory(json_values=attribute_value, directory=directory)
            # attribute_values = {
            #     index: values
            # }
        self.append_to_json_directory2(values, directory)

    def  collect_top_10_flight_info2(self, json_key, directory):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_LIST_OF_FLIGHTS)))
        flights = self.find_elements_by_xpath(sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW)
        # flights = driver.find_elements(by=By.XPATH, value=sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW)
        flight_time = []
        number_of_stops = []
        prices = []
        values = {}
        for index in range(1, 11, 1):
            row_xpath = '(' + sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW + ')[%s]' % index
            # row = self.find_element_by_xpath(row_xpath)
            attribute_value = self.get_attribute(row_xpath, "id")
            # flight_info = "flight %s: %s" % (index, attribute_value)
            key = "flight " + str(index) 
            values.update({key : str(attribute_value)})
            # values.append(attribute_value)
            # self.write_to_json_directory(json_values=attribute_value, directory=directory)
            # attribute_values = {
            #     index: values
            # }
        self.append_to_json(values, json_key, directory)

    def  collect_top_10_flight_info2(self, json_key, directory):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_LIST_OF_FLIGHTS)))
        flights = self.find_elements_by_xpath(sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW)
        # flights = driver.find_elements(by=By.XPATH, value=sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW)
        flight_time = []
        number_of_stops = []
        prices = []
        values = {}
        for index in range(1, 11, 1):
            row_xpath = '(' + sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW + ')[%s]' % index
            attribute_value = self.get_attribute(row_xpath, "id")
            key = "flight " + str(index) 
            values.update({key : str(attribute_value)})
        self.write_to_dictionary(json_key, values, directory)

    def navigate_into_and_collect(self, index, directory):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)))
        self.click_element(sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_DEPARTURE_AIRPORT_INPUT)))
        from_airline = self.get_attribute(sl.SKIPLAGGED_DEPARTURE_AIRPORT_INPUT, 'value')
        to_airline = self.get_attribute(sl.SKIPLAGGED_TO_AIRPORT, 'value')
        json_key = from_airline + ' to ' + to_airline
        self.add_new_dictionary(json_key, directory)       
        time.sleep(1)
        flights = self.find_elements_by_xpath(sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW)
        values = {}
        for index in range(1, 11, 1):
            row_xpath = '(' + sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW + ')[%s]' % index
            attribute_value = self.get_attribute(row_xpath, "id")
            key = "flight " + str(index) 
            values.update({key : str(attribute_value)})
        self.write_to_dictionary(json_key, values, directory)

    def navigate_into_and_collect2(self, index, directory, filter_price = None, filter_duration = None):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)))
        self.click_element(sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_DEPARTURE_AIRPORT_INPUT)))
        from_airline = self.get_attribute(sl.SKIPLAGGED_DEPARTURE_AIRPORT_INPUT, 'value')
        to_airline = self.get_attribute(sl.SKIPLAGGED_TO_AIRPORT, 'value')
        json_key = from_airline + ' to ' + to_airline
        self.add_new_dictionary(json_key, directory)       
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_FLIGHT_PRICE_ATTRIBUTE_INDEX % 1)))
        # while self.check_if_element_exists(sl.SKIPLAGGED_FLIGHT_PRICE_ATTRIBUTE_INDEX % 1 != True):
        #     time.sleep(1)
        flights = self.find_elements_by_xpath(sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW)
        if filter_price != None:
            self.filter_list_by_price()
        if filter_duration != None:
            self.filter_list_by_duration()
        values = {}
        for index in range(1, 11, 1):
            # time.sleep(2)
            row_xpath = '(' + sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW + ')[%s]' % index
            # attribute_value = self.get_attribute(row_xpath, "id")
            price = self.get_text(sl.SKIPLAGGED_FLIGHT_PRICE_ATTRIBUTE_INDEX % index)
            duration = self.get_text(sl.SKIPLAGGED_FLIGHT_DURATION_INDEX % index)
            num_of_stops = self.get_text(sl.SKIPLAGGED_FLIGHT_NUMBER_OF_STOP_INDEX % index)

### the below code was for debugging purposes
### a break point was added to each exception
### because if an exception was reached, the element was not found
### and i can inspect the page during debugging
            # try:
            #     attribute_value = self.get_attribute(row_xpath, "id")
            # except Exception:
            #     attribute_value = ""
            # try:
            #     price = self.get_text(sl.SKIPLAGGED_FLIGHT_PRICE_ATTRIBUTE_INDEX % index)
            # except Exception:
            #     price = ""
            # try:
            #     duration = self.get_text(sl.SKIPLAGGED_FLIGHT_DURATION_INDEX % index)
            # except Exception:
            #     duration = ""
            # try:
            #     num_of_stops = self.get_text(sl.SKIPLAGGED_FLIGHT_NUMBER_OF_STOP_INDEX % index)
            # except Exception:
            #     num_of_stops = ""
            #     pass            
            json_key2 = "flight " + str(index) 
            values.update({json_key2 : {"price": str(price), "duration" : duration, "number of stops" : num_of_stops}})
        self.write_to_dictionary(json_key, values, directory)
        ### create a nested json dictionary, first key is the departure airport to destination airport
        ### append a dictionary of flight information into that dictionary
        # {
        #     "dtw to mia" : [
        #         {                                             append
        #             "flight 1 price": "",                     append
        #             "flight 1 number of stops": "",           append
        #             "flight 1 layover cities": [],            append
        #             "flight 1 total time": ""                 append
        #         },                                            append
        #         {
        #             "flight 2 price": "",
        #             "flight 2 number of stops": "",
        #             "flight 2 layover cities": "none",  # if no layovers, there wont be an array but just "none"
        #             "flight 2 total time": ""                }
        #     ]
        # }
        #   "dtw to mia": [                                     create
        #      ]                                                create