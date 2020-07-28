import random
import time
import traceback

from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage(object):
    def __init__(self, browser):
        self.browser = browser

    def find_element(self, loc):
        return self.browser.find_element(By.XPATH, loc)

    def find_element_if_exists(self, loc):
        try:
            if self.exists(loc):
                return self.find_element(loc)
        except (TimeoutException, StaleElementReferenceException):
            return None

    def find_elements(self, loc):
        return self.browser.find_elements(By.XPATH, loc)

    def visit(self, url):
        self.browser.get(url)

    def hover(self, element):
        ActionChains(self.browser).move_to_element(element).perform()
        time.sleep(5)

    def exists(self, loc):
        try:
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, loc))
            )
            return True
        except (TimeoutException, StaleElementReferenceException):
            return False

    def wait_element_to_be_visible(self, loc, timeout=30):
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((By.XPATH, loc))
            )
        except (TimeoutException, StaleElementReferenceException):
            pass

    def scroll_x_times(self, x):
        y = 0
        while x > y:
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            x -= 1
            time.sleep(random.uniform(1, 3))

    @staticmethod
    def humanized_send_keys(element, keys):
        for character in keys:
            element.send_keys(character)
            time.sleep(random.uniform(0, 0.3))

    @staticmethod
    def humanized_clear_input(input):
        input.send_keys(Keys.CONTROL + "a")
        time.sleep(random.uniform(0, 0.2))
        input.send_keys(Keys.BACK_SPACE)

    @staticmethod
    def humanized_enter_input(input):
        input.send_keys(Keys.ENTER)

    def __getattr__(self, what, timeout=30):
        try:
            time.sleep(1)
            if what in self._locator_dictionary.keys():
                try:
                    WebDriverWait(self.browser, timeout).until(
                        EC.presence_of_element_located(
                            (By.XPATH, self._locator_dictionary[what])
                        )
                    )
                except (TimeoutException, StaleElementReferenceException):
                    traceback.print_exc()

                try:
                    WebDriverWait(self.browser, timeout).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, self._locator_dictionary[what])
                        )
                    )
                except (TimeoutException, StaleElementReferenceException):
                    traceback.print_exc()
                return self.find_element(self._locator_dictionary[what])
        except AttributeError:
            super(BasePage, self).__getattribute__("method_missing")(what)

    @staticmethod
    def method_missing(what):
        print("No %s here!" % what)
