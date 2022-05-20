from asyncio import wait_for
from xml.dom import NotFoundErr
from functions.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By
from locators.skiplagged_locators import SkiplaggedLocators as sl
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#### This page is filled with functions that are meant for Skiplagged.com
#### and use functions from BasePage

class Skiplagged(BasePage):

    def __init__(self, driver):
        self.driver = driver

    def navigate_to_skiplagged(self):
        self.navigate_to_webpage('https://skiplagged.com/')
        self.wait_until_element_is_present(sl.SKIPLAGGED_HOME_HEADER)
        self.assert_element_is_displayed(sl.SKIPLAGGED_HOME_HEADER)

#### click the dropdown for selecting Round Trip or One-Way then click the choice
    def select_round_one_way_trip(self, choice):
        self.click_element(sl.SKIPLAGGED_ROUND_TRIP_OR_ONE_WAY_DROP_DOWN)
        self.wait_until_element_is_present(sl.SKIPLAGGED_ROUND_TRIP_OR_ONE_WAY_DROP_DOWN_MENU_OPTIONS % choice)
        self.click_element(sl.SKIPLAGGED_ROUND_TRIP_OR_ONE_WAY_DROP_DOWN_MENU_OPTIONS % choice)
        self.assert_element_is_displayed(sl.SKIPLAGGED_ROUND_TRIP_OR_ONE_WAY_DROP_DOWN + '/span[text()="%s"]' % choice)

#### click the dropdown for selecting the number of travelers, click the + or - button
#### as many times as needed to get to the right number of adults and/or children
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
        # sometimes the departure date input box doesnt select and the calendars don't appear on the first click
        # so we check if its selected, if not, we try clicking again
        if self.check_if_element_exists(sl.SKIPLAGGED_DEPART_OR_RETURN_DATE_SELECTED) == True:
            pass
        else:
            self.click_element(sl.SKIPLAGGED_DEPART_DATE_INPUT)

        # two calendar months appear, so we create an array 
        # and fill it with the names of the two months
        listed_months = [(self.get_text(sl.SKIPLAGGED_CALENDAR_1_MONTH_NAME)).lower(), (self.get_text(sl.SKIPLAGGED_CALENDAR_2_MONTH_NAME)).lower()]
        month = month.lower()
        time.sleep(1)
        # if our desired month is in the array, we select the date on the correct month
        if month == listed_months[0]:
            self.click_element(sl.SKIPLAGGED_CALENDAR_1_DATES % date)
        elif month == listed_months[1]:
            self.click_element(sl.SKIPLAGGED_CALENDAR_2_DATES % date)

        # else navigate the to correct month if not on the correct one already
        else:
            while (month not in listed_months):
                self.click_element(sl.SKIPLAGGED_CALENDAR_NEXT_BUTTON)
                time.sleep(1)
                listed_months = [(self.get_text(sl.SKIPLAGGED_CALENDAR_1_MONTH_NAME)).lower(), (self.get_text(sl.SKIPLAGGED_CALENDAR_2_MONTH_NAME)).lower()]
        # click on the date
            time.sleep(1)
            self.click_element(sl.SKIPLAGGED_CALENDAR_2_DATES % date)

#### same idea as input_departure_date
#### make sure the date input box is selected and the calendars appear
#### if the desired month appears, the date will be selected
#### otherwise, click next, add months to the array and check until the desired month is there
#### and then select the correct date
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

    def click_search_flights(self):
        self.click_element(sl.SKIPLAGGED_SEARCH_FLIGHTS_BUTTON)
        time.sleep(2)

#### after searching for a flight to anywhere
#### assert that the flight cards that appear have city, country, and airline price or skiplagged price 
    def assert_cheapest_cities_and_flights(self):
        cards = self.find_elements_by_xpath(By.XPATH, sl.SKIPLAGGED_CHEAPEST_CITIES_CARD)
        for index, card in enumerate(cards):
            self.assert_element_is_displayed(sl.SKIPLAGGED_CHEAPEST_CITY % index)
            self.assert_element_is_displayed(sl.SKIPLAGGED_CHEAPEST_COUNTRY % index)
            if self.check_if_element_exists((sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX  % index) + sl.SKIPLAGGED_SKIPLAGGED_RATE):
                self.assert_element_is_displayed((sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX  % index) + sl.SKIPLAGGED_SKIPLAGGED_RATE)
            else:
                self.assert_element_is_displayed(sl.SKIPLAGGED_CHEAPEST_PRICE % index)
    
#### assert the three header lines that appear before the deals on the home page
    def assert_header_preceding_deals_homepage(self):
        self.assert_element_is_displayed(sl.SKIPLAGGED_HOME_PAGE_DEALS_HEADER_1)
        self.assert_element_is_displayed(sl.SKIPLAGGED_HOME_PAGE_DEALS_HEADER_2)
        self.assert_element_is_displayed(sl.SKIPLAGGED_HOME_PAGE_DEALS_HEADER_3)

#### assert there's 12 deals and they're all Skiplagged Rates on the home page
    def assert_deals_on_homepage(self):
        for x in range(1, 13):
            deal_card_xpath = '('+sl.SKIPLAGGED_DEALS_CARDS+')[%s]' % x
            self.assert_element_is_displayed(deal_card_xpath)
            self.assert_element_is_displayed(deal_card_xpath + '//div[@class="skip-rate-label"][text()="skiplagged rate"]')

#### on the home page, search for deals from a location, assert that the first card is from that location
#### because not all the cards will have deals from that location
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

#### after selecting departure airport, anywhere destination airport, departure and return date,
#### we arrive to a page filled with cities and prices, in ascending price order
#### here we select a city (with our index parameter), and collect the top 10 flight info to write to json
    def navigate_into_filter_and_collect(self, index, directory, filter_price = None, filter_duration = None):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)))
        # navigate into city n (which we'll declare with index)
        self.click_element(sl.SKIPLAGGED_INDEX_CHEAPEST_CITIES_CARD_INDEX % index)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_DEPARTURE_AIRPORT_INPUT)))
        # create a dictionary titled Departure Airport to Destination Airport
        from_airline = self.get_attribute(sl.SKIPLAGGED_DEPARTURE_AIRPORT_INPUT, 'value')
        to_airline = self.get_attribute(sl.SKIPLAGGED_TO_AIRPORT, 'value')
        json_key = from_airline + ' to ' + to_airline
        self.add_new_dictionary(json_key, directory)       
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_FLIGHT_PRICE_ATTRIBUTE_INDEX % 1)))
        flights = self.find_elements_by_xpath(sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW)
        # filter by price or duration
        if filter_price != None:
            self.filter_list_by_price()
        if filter_duration != None:
            self.filter_list_by_duration()
        # fill the dictionary with flight information; price, duration, and number of stops
        values = {}
        # only collecting the top 10 because when using 'find_elements_by_xpath'
        # a range of 12-17 elements are found
        for index in range(1, 11, 1):
            price = self.get_text(sl.SKIPLAGGED_FLIGHT_PRICE_ATTRIBUTE_INDEX % index)
            duration = self.get_text(sl.SKIPLAGGED_FLIGHT_DURATION_INDEX % index)
            num_of_stops = self.get_text(sl.SKIPLAGGED_FLIGHT_NUMBER_OF_STOP_INDEX % index)
            json_key2 = "flight " + str(index) 
            values.update({json_key2 : {"price": str(price), "duration" : duration, "number of stops" : num_of_stops}})
        # write flight information into the new dictionary
        self.write_to_dictionary(json_key, values, directory)

#### same as 'navigate_into_filter_and_collect' but we collect info from more flights
#### our 'find_elements_by_xpath' isn't always the same, usually between 12-17, so that's
#### how many flight information we're collecting and writing to json
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
        # the [:-1] is to stop the loop 1 before the end of the len of flights, otherwise we'd reach an Element Not Found error
        for index, flight in enumerate(flights[:-1], start=1):
            price = self.get_text(sl.SKIPLAGGED_FLIGHT_PRICE_ATTRIBUTE_INDEX % index)
            duration = self.get_text(sl.SKIPLAGGED_FLIGHT_DURATION_INDEX % index)
            num_of_stops = self.get_text(sl.SKIPLAGGED_FLIGHT_NUMBER_OF_STOP_INDEX % index)
            json_key2 = "flight " + str(index) 
            values.update({json_key2 : {"price": str(price), "duration" : duration, "number of stops" : num_of_stops}})
        self.write_to_dictionary(json_key, values, directory)

#### top row of home page has links that will be asserted, Skiplagged logo
    def assert_tr_link_skiplagged(self):
        self.click_element(sl.SKIPLAGGED_TR_SKIPLAGGED_LINK)
        self.wait_until_element_is_present(sl.SKIPLAGGED_HOME_HEADER)
        self.assert_element_is_displayed(sl.SKIPLAGGED_HOME_HEADER)

#### top row of home page has links that will be asserted, Flights
    def assert_tr_link_flights(self):
        self.click_element(sl.SKIPLAGGED_TR_FLIGHTS_LINK)
        self.wait_until_element_is_present(sl.SKIPLAGGED_HOME_HEADER)
        self.assert_element_is_displayed(sl.SKIPLAGGED_HOME_HEADER)

#### top row of home page has links that will be asserted, Hotels
    def assert_tr_link_hotels(self):
        self.click_element(sl.SKIPLAGGED_TR_HOTELS_LINK)
        self.wait_until_element_is_present(self.span_with_text('Check-in'))
        self.assert_element_is_displayed(self.span_with_text('Check-in'))

#### top row of home page has links that will be asserted, Cars
    def assert_tr_link_cars(self):
        self.click_element(sl.SKIPLAGGED_TR_CARS_LINK)
        self.wait_until_element_is_present(self.label_with_text('Pick-up Location'))
        self.assert_element_is_displayed(self.label_with_text('Pick-up Location'))

#### top row of home page has links that will be asserted, Rewards
    def assert_tr_link_rewards(self):
        self.click_element(sl.SKIPLAGGED_TR_REWARDS_LINK)
        self.wait_until_element_is_present(self.div_with_text('Rewards Program'))
        self.assert_element_is_displayed(self.div_with_text('Rewards Program'))

#### top row of home page has links that will be asserted, Login    
    def assert_tr_link_login(self):
        self.click_element(sl.SKIPLAGGED_TR_LOGIN_LINK)
        self.wait_until_element_is_present(self.span_with_text('Sign In'))
        self.assert_element_is_displayed(self.span_with_text('Sign In'))

#### asserts the 'sued us' hyperlink in the home page
    def assert_sued_us_link(self):
        self.click_element(self.link_with_text('sued us'))
        time.sleep(1)
        self.switch_to_newest_tab()
        self.wait_until_element_is_present('//h1[@class="article-title speakable"]')
        self.assert_element_is_displayed('//h1[@class="article-title speakable"]')
        self.close_current_tab()

#### asserts the image link works, image is a bar of different company logos that featured them
    def assert_featured_in_link(self):
        self.assert_element_is_displayed(sl.SKIPLAGGED_FEATURED_IN)
        self.assert_element_is_displayed(sl.SKIPLAGGED_FEATURED_IN + self.span_with_text('Featured in:'))
        self.click_element(sl.SKIPLAGGED_FEATURED_IN)
        self.wait_until_element_is_present(self.link_with_text('Download our Press Kit'))
        self.assert_element_is_displayed(self.link_with_text('Download our Press Kit'))

#### asserts a link that looks like an ad thats for their rewards program
    def assert_rewards_ad_link(self):
        self.click_element(sl.SKIPLAGGED_REWARDS_AD)
        time.sleep(1)
        self.switch_to_newest_tab()
        self.wait_until_element_is_present(self.div_with_text('Rewards Program'))
        self.assert_element_is_displayed(self.div_with_text('Rewards Program'))
        self.close_current_tab()

#### asserts a FAQ hyperlink that appears in a after a short explanation of "What is Skiplagged?"
    def assert_faq_link(self):
        self.click_element(self.link_with_text('Read the full FAQ'))
        self.wait_until_element_is_present(self.link_with_text('FAQ'))
        self.assert_element_is_displayed(self.link_with_text('FAQ'))

#### asserts a 'mobile app' hyperlink that appears in a after a short header and text "Access the best deals anywhere"
    def assert_mobile_app_link(self):
        self.click_element(self.link_with_text('mobile app'))
        self.wait_until_element_is_present(self.header_with_text('4', 'Download the app'))
        self.assert_element_is_displayed(self.header_with_text('4', 'Download the app'))
        self.click_element('//button[@data-dismiss="modal"]')

#### in the footer of the home page, asserts the 11 elements are there
#### skiplagged text, about faq press terms careers link, language and curreny selection
#### 3 social media links
    def assert_footer_elements(self):
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_LOGO)
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_ABOUT)
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_FAQ)
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_PRESS)
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_TERMS)
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_CAREERS)
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_LANGUAGE)
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_CURRENCY)
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_FACEBOOK)
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_TWITTER)
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_INSTAGRAM)

#### assert the language selector works
    def assert_footer_language_select(self):
        self.click_element(sl.SKIPLAGGED_FOOTER_LANGUAGE)
        self.wait_until_element_is_present(sl.SKIPLAGGED_FOOTER_LANGUAGE_DROPDOWN)
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_LANGUAGE_DROPDOWN)
        langauge = self.get_text(sl.SKIPLAGGED_FOOTER_LANGUAGE_DROPDOWN+'//li[3]//span')
        # select the 3rd language in the menu
        self.click_element(sl.SKIPLAGGED_FOOTER_LANGUAGE_DROPDOWN+'//li[3]//span')
        self.wait_until_element_is_present(sl.SKIPLAGGED_FOOTER_LANGUAGE+self.span_with_text(langauge))
        # assert the new language is the language selected
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_LANGUAGE+self.span_with_text(langauge))
        self.click_element(sl.SKIPLAGGED_FOOTER_LANGUAGE)
        self.wait_until_element_is_present(sl.SKIPLAGGED_FOOTER_LANGUAGE_DROPDOWN+self.span_with_text('English'))
        # switch back to english
        self.click_element(sl.SKIPLAGGED_FOOTER_LANGUAGE_DROPDOWN+self.span_with_text('English'))
        self.wait_until_element_is_present(sl.SKIPLAGGED_FOOTER_LANGUAGE+self.span_with_text('English'))
        # assert english is selected
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_LANGUAGE+self.span_with_text('English'))

#### assert the currency selector works
    def assert_footer_currency_select(self):
        self.click_element(sl.SKIPLAGGED_FOOTER_CURRENCY)
        self.wait_until_element_is_present(sl.SKIPLAGGED_FOOTER_CURRENCY_DROPDOWN)
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_CURRENCY_DROPDOWN)
        currency = self.get_text(sl.SKIPLAGGED_FOOTER_CURRENCY_DROPDOWN+'//li[3]//span')
        # select a different currency
        self.click_element(sl.SKIPLAGGED_FOOTER_CURRENCY_DROPDOWN+'//li[3]//span')
        self.wait_until_element_is_present(sl.SKIPLAGGED_FOOTER_CURRENCY+self.span_with_text(currency))
        # assert the new currency is selected
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_CURRENCY+self.span_with_text(currency))
        self.click_element(sl.SKIPLAGGED_FOOTER_CURRENCY)
        self.wait_until_element_is_present(sl.SKIPLAGGED_FOOTER_CURRENCY_DROPDOWN+self.span_with_text('USD'))
        # switch back to USD
        self.click_element(sl.SKIPLAGGED_FOOTER_CURRENCY_DROPDOWN+self.span_with_text('USD'))
        self.wait_until_element_is_present(sl.SKIPLAGGED_FOOTER_CURRENCY+self.span_with_text('USD'))
        # assert USD is selected
        self.assert_element_is_displayed(sl.SKIPLAGGED_FOOTER_CURRENCY+self.span_with_text('USD'))

    def assert_about_link(self):
        self.click_element(sl.SKIPLAGGED_FOOTER_ABOUT)
        self.wait_until_element_is_present(self.header_with_text('2', 'How are we doing this?'))
        self.assert_element_is_displayed(self.header_with_text('2', 'How are we doing this?'))

    def assert_faq_link(self):
        self.click_element(sl.SKIPLAGGED_FOOTER_FAQ)
        self.wait_until_element_is_present(self.link_with_text('FAQ'))
        self.assert_element_is_displayed(self.link_with_text('FAQ'))

    def assert_press_link(self):
        self.click_element(sl.SKIPLAGGED_FOOTER_PRESS)
        self.wait_until_element_is_present(self.link_with_text('Download our Press Kit'))
        self.assert_element_is_displayed(self.link_with_text('Download our Press Kit'))

    def assert_terms_link(self):
        self.click_element(sl.SKIPLAGGED_FOOTER_TERMS)
        self.wait_until_element_is_present(self.header_with_text('1', 'Terms and Conditions'))
        self.assert_element_is_displayed(self.header_with_text('1', 'Terms and Conditions'))

    def assert_careers_link(self):
        self.click_element(sl.SKIPLAGGED_FOOTER_CAREERS)
        self.wait_until_element_is_present(self.font_with_text('Careers at Skiplagged'))
        self.assert_element_is_displayed(self.font_with_text('Careers at Skiplagged'))

    def assert_facebook_link(self):
        self.click_element(sl.SKIPLAGGED_FOOTER_FACEBOOK)
        self.switch_to_newest_tab()
        self.wait_until_element_is_present(self.header_with_text('1', 'Skiplagged'))
        self.assert_element_is_displayed(self.header_with_text('1', 'Skiplagged'))
        self.close_current_tab()

    def assert_twitter_link(self):
        self.click_element(sl.SKIPLAGGED_FOOTER_TWITTER)
        self.switch_to_newest_tab()
        self.wait_until_element_is_present(self.span_with_text('Skiplagged'))
        self.assert_element_is_displayed(self.span_with_text('Skiplagged'))
        self.close_current_tab()

    def assert_instagram_link(self):
        self.click_element(sl.SKIPLAGGED_FOOTER_INSTAGRAM)
        self.switch_to_newest_tab()
        self.wait_until_element_is_present(self.header_with_text('2', 'skiplagged'))
        self.assert_element_is_displayed(self.header_with_text('2', 'skiplagged'))
        self.close_current_tab()

    def write_flight_info_to_json(self, directory, index, json_key1, json_key2):
        flight_box_xpath = sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW_INDEX % index
        from_airline = self.get_attribute(flight_box_xpath, 'value')
        to_airline = self.get_attribute(sl.SKIPLAGGED_TO_AIRPORT, 'value')
        json_key = from_airline + ' to ' + to_airline
        self.add_new_dictionary(json_key, directory)       
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, sl.SKIPLAGGED_FLIGHT_PRICE_ATTRIBUTE_INDEX % 1)))
        flights = self.find_elements_by_xpath(sl.SKIPLAGGED_LIST_OF_FLIGHT_ROW)
        values = {}
        # the [:-1] is to stop the loop 1 before the end of the len of flights, otherwise we'd reach an Element Not Found error
        price = self.get_text(sl.SKIPLAGGED_FLIGHT_PRICE_ATTRIBUTE_INDEX % index)
        duration = self.get_text(sl.SKIPLAGGED_FLIGHT_DURATION_INDEX % index)
        num_of_stops = self.get_text(sl.SKIPLAGGED_FLIGHT_NUMBER_OF_STOP_INDEX % index)
        json_key2 = "flight " + str(index) 
        values.update({json_key2 : {"price": str(price), "duration" : duration, "number of stops" : num_of_stops}})
        self.write_to_dictionary(json_key, values, directory)


#### select a flight by its position on the list
    def select_flight_index(self, index):
        self.click_element(self.button_with_text_index('Select', index))
        

    def collect_flight_info(self, index, directory):
        # collect departure flight info
        # collect layover flight info if any
        # collect destination flight
        # if destination is a skiplagged flight
        #   collect skipped layover flight info if any
        #   collect skipped destination flight info
        self.wait_until_element_is_present(sl.SKIPLAGGED_INDEX_FLIGHT_FIRST_AIRPORT % index)
        from_airline = self.get_text(sl.SKIPLAGGED_INDEX_FLIGHT_FIRST_AIRPORT % index)
        to_airline = self.get_text(sl.SKIPLAGGED_INDEX_FLIGHT_LAST_AIRPORT % index)
        json_key = from_airline + ' to ' + to_airline
        values = {}
        price = self.get_text(sl.SKIPLAGGED_FLIGHT_PRICE_ATTRIBUTE_INDEX % index)
        total_duration = self.get_text(sl.SKIPLAGGED_FLIGHT_DURATION_INDEX % index)
        num_of_stops = self.get_text(sl.SKIPLAGGED_FLIGHT_NUMBER_OF_STOP_INDEX % index)
        departure_airport = from_airline
        departure_city = self.get_attribute(sl.SKIPLAGGED_INDEX_FLIGHT_FIRST_CITY % index, "textContent")
        departure_takeoff_time = self.get_attribute(sl.SKIPLAGGED_INDEX_FLIGHT_FIRST_DEPART_TAKEOFF % index, "textContent")
        departure_flight_duration = self.get_attribute(sl.SKIPLAGGED_INDEX_FLIGHT_FIRST_DURATION % index, "textContent")
        # if layover info exists, collect

        values.update({ "price": str(price),
                        "duration" : total_duration, 
                        "number of stops" : num_of_stops,
                        "departure airport" : departure_airport,
                        "departure city": departure_city,
                        "departure takeoff time": departure_takeoff_time,
                        "departure flight duration": departure_flight_duration})
        if self.check_if_element_exists(sl.SKIPLAGGED_INDEX_FLIGHT_LAYOVER_AIRPORT % index):
            layovers = self.find_elements_by_xpath(sl.SKIPLAGGED_INDEX_FLIGHT_LAYOVER_AIRPORT % index)
            for layover_index, layover in enumerate(layovers, start=1):
                layover_arrival = self.get_attribute('('+sl.SKIPLAGGED_INDEX_FLIGHT_LAYOVER_ARRIVAL % index + ')[%s]' % layover_index, "textContent")
                layover_airport = self.get_attribute('('+sl.SKIPLAGGED_INDEX_FLIGHT_LAYOVER_AIRPORT % index + ')[%s]' % layover_index, "textContent")
                layover_city = self.get_attribute('('+sl.SKIPLAGGED_INDEX_FLIGHT_LAYOVER_CITY % index + ')[%s]' % layover_index, "textContent")
                layover_duration = self.get_attribute('('+sl.SKIPLAGGED_INDEX_FLIGHT_LAYOVER_DURATION % index + ')[%s]' % layover_index, "textContent")
                layover_departure_takeoff = self.get_attribute('('+sl.SKIPLAGGED_INDEX_FLIGHT_LAYOVER_DEPART_TAKEOFF % index + ')[%s]' % layover_index, "textContent")
                values.update({ "layover %s arrival" % index: layover_arrival,
                                "layover %s airport" % index: layover_airport,
                                "layover %s city" % index: layover_city,
                                "layover %s duration" % index: layover_duration,
                                "layover %s departure takeoff" % index: layover_departure_takeoff})
        destination_arrival = self.get_attribute(sl.SKIPLAGGED_INDEX_FLIGHT_LAST_ARRIVAL % index, "textContent")
        destination_airport = self.get_attribute(sl.SKIPLAGGED_INDEX_FLIGHT_LAST_AIRPORT % index, "textContent")
        destination_city = self.get_attribute(sl.SKIPLAGGED_INDEX_FLIGHT_LAST_CITY % index, "textContent")
        values.update({ "destination arrival": destination_arrival,
                        "destination airport": destination_airport,
                        "destination city": destination_city})
        if self.check_if_element_exists(sl.SKIPLAGGED_INDEX_FLIGHT_SKIP_LAYOVER_DURATION % index):
            skip_layover_duration = self.get_attribute(sl.SKIPLAGGED_INDEX_FLIGHT_SKIP_LAYOVER_DURATION % index, "textContent")
            skip_layover_takeoff = self.get_attribute(sl.SKIPLAGGED_INDEX_FLIGHT_SKIP_LAYOVER_DEPART_TAKEOFF % index, "textContent")
            skip_layover_flight_duration = self.get_attribute(sl.SKIPLAGGED_INDEX_FLIGHT_SKIP_LAYOVER_FLIGHT_DURATION % index, "textContent")
            skip_arrival = self.get_attribute(sl.SKIPLAGGED_INDEX_FLIGHT_SKIP_ARRIVAL % index, "textContent")
            skip_arrival_airport = self.get_attribute(sl.SKIPLAGGED_INDEX_FLIGHT_SKIP_ARRIVAL_AIRPORT % index, "textContent")
            skip_arrival_city = self.get_attribute(sl.SKIPLAGGED_INDEX_FLIGHT_SKIP_ARRIVAL_CITY % index, "textContent")
            values.update({ "skipped layover duration": skip_layover_duration,
                            "skipped layover takeoff": skip_layover_takeoff,
                            "skipped layover flight duration": skip_layover_flight_duration,
                            "skipped arrival": skip_arrival,
                            "skipped arrival airport": skip_arrival_airport,
                            "skipped arrival city": skip_arrival_city})
        self.write_to_dictionary(json_key, values, directory)

    def select_filter_type_of_flight(self, type, only=None):
        self.wait_until_element_is_present('//div[@class="trip-depart-header"][text()="Please select your departing flight"]')
        if self.check_if_element_exists(sl.SKIPLAGGED_FLIGHT_TYPE_HIDDEN_ONLY):
            if type == "Hidden":
                if only != None:
                    self.click_element(sl.SKIPLAGGED_FLIGHT_TYPE_HIDDEN_ONLY)
                else:
                    self.click_element(sl.SKIPLAGGED_FLIGHT_TYPE_HIDDEN)
            if type == "Standard":
                if only != None:
                    self.click_element(sl.SKIPLAGGED_FLIGHT_TYPE_STANDARD_ONLY)
                else:
                    self.click_element(sl.SKIPLAGGED_FLIGHT_TYPE_STANDARD)

# structure
{
    "from mco to hnl":{
        "price": "",
        "duration": "",
        "number of stops": "",
        "departure airport" : "",
        "departure city": "",
        "departure takeoff time": "",
        "departure flight duration": "",
        "layover 1 airport": "",
        "layover 1 city": "",
        "layover 1 duration": "",
        "layover 1 takeoff time": "",
        "layover 1 flight duration": "",
        "layover n airport": "",
        "layover n city": "",
        "layover n duration": "",
        "layover n takeoff time": "",
        "layover n flight duration": "",
        "destination airport": "",
        "destination city": "",
        "destination arrival time": "",
        "skip layover n airport": "",
        "skip layover n city": "",
        "skip layover n duration": "",
        "skip layover n takeoff time": "",
        "skip layover n flight duration": "",
        "skip destination airport": "",
        "skip destination city": "",
        "skip destination arrival time": ""
    }
}