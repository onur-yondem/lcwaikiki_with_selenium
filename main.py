from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains


class LCWaikiki:
    # Locators
    HEADER_LOGO = (By.CLASS_NAME, "main-header-logo")
    CATEGORY_PAGE_LINK = (By.CLASS_NAME, "zone-header__anchor")
    MAIN_CATEGORY_BTN = (By.CLASS_NAME, "menu-header-item")
    PRODUCT_PAGE_LINK = (By.CLASS_NAME, "product-image")  # 4
    PRODUCT_SIZE_ELEMENTS = (By.CSS_SELECTOR, "#option-size a")
    ADD_TO_CART_BTN = (By.ID, "pd_add_to_cart")
    BASKET_BTN = (By.CLASS_NAME, "cart-action__btn--bg-green")  # 1

    # Assert Locators
    IS_ON_CATEGORY_PAGE = (By.CLASS_NAME, "product-list-heading__product-count")
    IS_ADDED_PRODUCT = (By.CLASS_NAME, "badge-circle")
    IS_ON_BASKET_PAGE = (By.CLASS_NAME, "main-button")
    IS_ON_MAIN_PAGE = (By.CLASS_NAME, "header__top")
    website = "https://www.lcwaikiki.com/tr-TR/TR"

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(ChromeDriverManager(chrome_options=chrome_options).install())
        self.driver.maximize_window()
        self.driver.get(self.website)
        self.wait = WebDriverWait(self.driver, 10)
        self.actions = ActionChains(self.driver)

    def test_navigate(self):
        assert self.wait.until(
            ec.presence_of_element_located(self.IS_ON_MAIN_PAGE)).is_displayed(), "We are not on the home page"

        self.actions.move_to_element(self.wait.until(ec.presence_of_element_located(self.MAIN_CATEGORY_BTN))).click(
            self.wait.until(ec.presence_of_element_located(self.CATEGORY_PAGE_LINK))).perform()

        assert "ürün listelendi." in self.wait.until(
            ec.presence_of_element_located(self.IS_ON_CATEGORY_PAGE)).text, "We are not on the category page"

        self.wait.until(ec.presence_of_all_elements_located(self.PRODUCT_PAGE_LINK))[4].click()
        assert self.wait.until(
            ec.presence_of_element_located(self.ADD_TO_CART_BTN)).is_displayed(), "We are not on the product page"

        for size in self.wait.until(ec.presence_of_all_elements_located(self.PRODUCT_SIZE_ELEMENTS)):
            if int(size.get_attribute("data-stock")) > 0:
                size.click()
                break

        self.wait.until(ec.presence_of_element_located(self.ADD_TO_CART_BTN)).click()
        assert int(
            self.wait.until(ec.presence_of_element_located(
                self.IS_ADDED_PRODUCT)).text) > 0, "The product has not been added to the cart"

        self.wait.until(ec.presence_of_all_elements_located(self.BASKET_BTN))[1].click()
        assert self.wait.until(
            ec.presence_of_element_located(self.IS_ON_BASKET_PAGE)).is_displayed(), "We are not on the cart page"

        self.wait.until(ec.presence_of_element_located(self.HEADER_LOGO)).click()
        assert self.wait.until(
            ec.presence_of_element_located(self.IS_ON_MAIN_PAGE)).is_displayed(), "We are not on the home page"

    def tear_down(self):
        self.driver.quit()


waikiki_test = LCWaikiki()

waikiki_test.test_navigate()
waikiki_test.tear_down()
