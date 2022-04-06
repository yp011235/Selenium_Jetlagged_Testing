from selenium.webdriver.common.by import By

class AmazonLocators():

    # single quotes only, "" doesnt work
    AMAZON_SEARCH_INPUT_BOX = '//input[@id="twotabsearchtextbox"]' # AMAZON_SEARCH_INPUT_BOX = (By.ID, "twotabsearchtextbox")
    AMAZON_SEARCH_BUTTON = '//input[@id="nav-search-submit-button"]'
    AMAZON_HOME_UPPER_NAV_BAR = '//div[@id="nav-xshop"]'
    SELECT_FROM_AMAZON_HOME_UPPER_NAV_BAR = '//div[@id="nav-xshop"]//a[@class="nav-a  "][contains(text(), "%s")]'

    # Books page
    AMAZON_BOOK_PAGE_HEADER = '//img[@alt="Books%20at%20Amazon"]' # add another % to make it a string, %%
