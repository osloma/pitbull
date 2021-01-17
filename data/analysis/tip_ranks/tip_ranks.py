from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TipRanksAnalysis():

    def __init__(self, web_driver):
        self.web_driver = web_driver        
        self.web_driver.get(self.url)
        self.web_driver.set_window_size(3000,1500)
        self.web_driver.execute_script("window.scrollTo(0,0)")
        self.web_driver.execute_script("window.scrollTo(0,0)")

    def __to_stock(self, stock):
        self.web_driver.get(f"https://www.tipranks.com/stocks/{stock}/forecast")        

    def __five_stars(self):
        combo = self.web_driver.find_element(By.CSS_SELECTOR, ".bgpurple-dark > span")
        actions = ActionChains(self.web_driver)
        actions.move_to_element(combo).perform()
        five_starts = self.web_driver.find_element(By.LINK_TEXT, "Go Ultimate")
        actions = ActionChains(self.web_driver)
        actions.move_to_element(five_starts).perform()
        self.web_driver.find_element(By.CSS_SELECTOR, ".css-1szy77t-control .tipranks-icon").click()
        self.web_driver.find_element(By.CSS_SELECTOR, "#react-select-6-option-4 .tipranks-icon").click()
        self.web_driver.find_element(By.CSS_SELECTOR, ".client-components-stock-research-analysts-style__analysts").click()

    def run(self):
        pass
