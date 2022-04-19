import time
import unittest
from selenium import webdriver
from page_functions.practice_amazon_search_page import AmazonPage

# when configuring the testing, we start by searching '>Python: Configure Tests'
# afterwards we select unittest as our framework/tool (explain why we dont pick pytest)
# and then we select the directory where we are keeping the tests
# i usually select the parent folder of my test folder, in case i 
# want to reuse certain methods, tests, or workflows differently after
# a few adjustments
# it really does pay to make your code reuseable, when possible of course
# finally we decide how our tests are discovered
# because i like to name methods and tests using '_',
# i chose the option with the python files beginning with 'test_'
# the options included: 
# python files ending with 'test' or '_test'
# or beginning with 'test' or 'test_'
# or files containing the word 'test'
# so my file name and the names of my tests will have to begin with '_test'

# inheriting unittest into our class so we can use its functions
class PraticeTest(unittest.TestCase):
    
    # this will run once before the class
    # added @classmethod becuase it is used on the entire class
    # if we wanted to do something before every test, then we would use
    # def setUp(self):
    #     self.driver = webdriver.Chrome()
    @classmethod
    def setUpClass(cls):
        # i need to put in cls.driver or self.driver = webdriver.Chrome() everytime i want to open a new instance of Chrome
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(4)
        cls.driver.maximize_window()
        print("chrome is ready")
### depending on test, i wouldn't use one brower to complete all the tests
### most likely to open up a browser for each test and close it at the end of each test

    # in order for the test to show up on the testing extension
    # the name must begin with 'test_', i set it up like that in the test configuration (>Python: Test Configuration)
    def test_search_google(self):
        self.driver.get("https://www.google.com")
        print("arrived to google")
        time.sleep(2)

    def test_amazon_book_page(self):
        driver = self.driver # this is so we dont have to write self.driver all the time, we just type driver now
        # in our AmazonPage, our constructor __init__ is accepting a driver input
        # so we call the page as an object and input the driver instance as the arguement
        amazon_page = AmazonPage(driver)
        amazon_page.navigate_to_amazon()
        amazon_page.click_a_link_from_upper_nav('Books')
        amazon_page.assert_books_page()
    


    # this will run at the end of every class
    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()
        print("test completed")