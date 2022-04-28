from asyncio import wait_for
from xml.dom import NotFoundErr
from functions.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By
from locators.skiplagged_locators import SkiplaggedLocators as sl
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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



    def search_flights(self):
        self.click_element(sl.SKIPLAGGED_SEARCH_FLIGHTS_BUTTON)
        time.sleep(2)

    def assert_cheapest_cities_and_flights(self):
        cards = self.find_elements_by_xpath(By.XPATH, sl.SKIPLAGGED_CHEAPEST_CITIES_CARD)
        for index, card in enumerate(cards):
            self.assert_element_is_displayed(sl.SKIPLAGGED_CHEAPEST_CITY % index)
            self.assert_element_is_displayed(sl.SKIPLAGGED_CHEAPEST_COUNTRY % index)
            if self.check_if_element_exists((sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX  % index) + sl.SKIPLAGGED_SKIPLAGGED_RATE):
                self.assert_element_is_displayed((sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX  % index) + sl.SKIPLAGGED_SKIPLAGGED_RATE)
            else:
                self.assert_element_is_displayed(sl.SKIPLAGGED_CHEAPEST_PRICE % index)
    
    # assert the two header lines
    def assert_header_preceding_deals_homepage(self):
        self.assert_element_is_displayed(sl.SKIPLAGGED_HOME_PAGE_DEALS_HEADER_1)
        self.assert_element_is_displayed(sl.SKIPLAGGED_HOME_PAGE_DEALS_HEADER_2)

    # assert there's 12 deals and they're all Skiplagged Rates
    def assert_deals_on_homepage(self):
        for x in range(1, 13):
            deal_card_xpath = '('+sl.SKIPLAGGED_DEALS_CARDS+')[%s]' % x
            self.assert_element_is_displayed(deal_card_xpath)
            self.assert_element_is_displayed(deal_card_xpath + '//div[@class="skip-rate-label"][text()="skiplagged rate"]')

    # search for deals from a location, assert that 12 cards are from that location, and are skiplagged rates
    def input_deals_location_and_assert(self, location):
        self.send_text_enter(sl.SKIPLAGGED_DEALS_LOCATION_INPUT, location)
        departure = self.get_attribute(sl.SKIPLAGGED_DEALS_LOCATION_TEXT, 'innerHTML')
        words = departure.split(', ')
        departure_city = words[1]
        self.click_element(sl.SKIPLAGGED_SEARCH_DEALS_BUTTON)
        time.sleep(1)
        deal_card_xpath = '('+sl.SKIPLAGGED_DEALS_CARDS+')[1]'
        location_xpath = deal_card_xpath + '//h4[@class="deal-city truncate"][contains(text(), "%s")]' % departure_city
        location_deal_xpath = deal_card_xpath + '//div[@class="skip-rate-label"][text()="skiplagged rate"]'
        self.wait_until_element_is_present(location_xpath)
        self.assert_element_is_displayed(location_xpath)        
        self.assert_element_is_displayed(location_deal_xpath)

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

    def navigate_into_filter_and_collect(self, index, directory, filter_price = None, filter_duration = None):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)))
        self.click_element(sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_DEPARTURE_AIRPORT_INPUT)))
        from_airline = self.get_attribute(sl.SKIPLAGGED_DEPARTURE_AIRPORT_INPUT, 'value')
        to_airline = self.get_attribute(sl.SKIPLAGGED_TO_AIRPORT, 'value')
        json_key = from_airline + ' to ' + to_airline
        self.add_new_dictionary(json_key, directory)       
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_FLIGHT_PRICE_ATTRIBUTE_INDEX % 1)))
        flights = self.find_elements_by_xpath(sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW)
        if filter_price != None:
            self.filter_list_by_price()
        if filter_duration != None:
            self.filter_list_by_duration()
        values = {}
        for index in range(1, 11, 1):
            price = self.get_text(sl.SKIPLAGGED_FLIGHT_PRICE_ATTRIBUTE_INDEX % index)
            duration = self.get_text(sl.SKIPLAGGED_FLIGHT_DURATION_INDEX % index)
            num_of_stops = self.get_text(sl.SKIPLAGGED_FLIGHT_NUMBER_OF_STOP_INDEX % index)
            json_key2 = "flight " + str(index) 
            values.update({json_key2 : {"price": str(price), "duration" : duration, "number of stops" : num_of_stops}})
        self.write_to_dictionary(json_key, values, directory)

    def navigate_into_filter_and_collect_all(self, index, directory, filter_price = None, filter_duration = None):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)))
        self.click_element(sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_DEPARTURE_AIRPORT_INPUT)))
        from_airline = self.get_attribute(sl.SKIPLAGGED_DEPARTURE_AIRPORT_INPUT, 'value')
        to_airline = self.get_attribute(sl.SKIPLAGGED_TO_AIRPORT, 'value')
        json_key = from_airline + ' to ' + to_airline
        self.add_new_dictionary(json_key, directory)       
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_FLIGHT_PRICE_ATTRIBUTE_INDEX % 1)))
        flights = self.find_elements_by_xpath(sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW)
        if filter_price != None:
            self.filter_list_by_price()
        if filter_duration != None:
            self.filter_list_by_duration()
        values = {}
        # the [:-1] is to stop the loop 1 before the end of the len of flights
        for index, flight in enumerate(flights[:-1], start=1):
            price = self.get_text(sl.SKIPLAGGED_FLIGHT_PRICE_ATTRIBUTE_INDEX % index)
            duration = self.get_text(sl.SKIPLAGGED_FLIGHT_DURATION_INDEX % index)
            num_of_stops = self.get_text(sl.SKIPLAGGED_FLIGHT_NUMBER_OF_STOP_INDEX % index)
            json_key2 = "flight " + str(index) 
            values.update({json_key2 : {"price": str(price), "duration" : duration, "number of stops" : num_of_stops}})
        self.write_to_dictionary(json_key, values, directory)

    def assert_tr_link_skiplagged(self):
        self.click_element(sl.SKIPLAGGED_TR_SKIPLAGGED_LINK)
        self.wait_until_element_is_present(sl.SKIPLAGGED_HOME_HEADER)
        self.assert_element_is_displayed(sl.SKIPLAGGED_HOME_HEADER)

    def assert_tr_link_flights(self):
        self.click_element(sl.SKIPLAGGED_TR_FLIGHTS_LINK)
        self.wait_until_element_is_present(sl.SKIPLAGGED_HOME_HEADER)
        self.assert_element_is_displayed(sl.SKIPLAGGED_HOME_HEADER)

    def assert_tr_link_hotels(self):
        self.click_element(sl.SKIPLAGGED_TR_HOTELS_LINK)
        self.wait_until_element_is_present(self.span_with_text('Check-in'))
        self.assert_element_is_displayed(self.span_with_text('Check-in'))

    def assert_tr_link_cars(self):
        self.click_element(sl.SKIPLAGGED_TR_CARS_LINK)
        self.wait_until_element_is_present(self.label_with_text('Pick-up Location'))
        self.assert_element_is_displayed(self.label_with_text('Pick-up Location'))

    def assert_tr_link_rewards(self):
        self.click_element(sl.SKIPLAGGED_TR_REWARDS_LINK)
        self.wait_until_element_is_present(self.div_with_text('Rewards Program'))
        self.assert_element_is_displayed(self.div_with_text('Rewards Program'))
    
    def assert_tr_link_login(self):
        self.click_element(sl.SKIPLAGGED_TR_LOGIN_LINK)
        self.wait_until_element_is_present(self.span_with_text('Sign In'))
        self.assert_element_is_displayed(self.span_with_text('Sign In'))

    def assert_sued_us_link(self):
        self.click_element(self.link_with_text('sued us'))
        time.sleep(1)
        self.switch_to_newest_tab()
        self.wait_until_element_is_present('//h1[@class="article-title speakable"]')
        self.assert_element_is_displayed('//h1[@class="article-title speakable"]')
        self.close_current_tab()