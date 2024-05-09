import time

from selenium import webdriver
import pytest
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class TestCarRentals():

    @pytest.fixture()
    def setup(self):
        self.driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("https://ui-stg-carrental.ratemetrics.com/")
        self.driver.implicitly_wait(6)
        yield
        self.driver.close()

    @pytest.mark.parametrize("username,password,should_pass", [("ezrental","ezrental",True),("ez","ezrental",False),("ezrental","ez",False)])
    def test_Login(self,setup,username,password,should_pass):
        self.driver.find_element(By.XPATH, "//input[@name='username']").send_keys(username)
        self.driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='logged-user']/button/div/img")))
            if not should_pass:
                pytest.fail("Test should fail because user should not be able to login, but they did.")
        except TimeoutException:
            if should_pass:
                pytest.fail("Test should pass with correct login, but it failed to find the user image.")

    def test_markets_count(self,setup):
        self.driver.find_element(By.XPATH, "//input[@name='username']").send_keys("ezrental")
        self.driver.find_element(By.XPATH, "//input[@name='password']").send_keys("ezrental")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        self.driver.implicitly_wait(10)
        first_row_element =  self.driver.find_element(By.XPATH,"//table/tbody/tr[1]/td[1]")
        assert first_row_element.text != "No Records Found" , pytest.fail("No markets here")

    def test_markets_edit(self,setup):
        # Login
        self.driver.find_element(By.XPATH, "//input[@name='username']").send_keys("ezrental")
        self.driver.find_element(By.XPATH, "//input[@name='password']").send_keys("ezrental")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        self.driver.implicitly_wait(10)

        # Row count
        rows = self.driver.find_elements(By.XPATH,"//table/tbody/tr")
        self.driver.find_element(By.XPATH,f"//table/tbody/tr[{len(rows)-1}]/td[5]/span").click()

        # Wait for table to display
        market_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='marketName']")))
        self.driver.implicitly_wait(4)

        # Getting exising value
        existing_market_text = self.driver.find_element(By.XPATH, "//input[@name='marketName']").get_attribute("value")

        # Adding new data
        added_market_name = " test"
        market_element.send_keys(added_market_name)

        # Save data
        self.driver.find_element(By.XPATH, "//*[@class='text-center']/button").click()
        self.driver.implicitly_wait(4)

        # Click on alert
        self.driver.find_element(By.XPATH, "//*[@class='textleft']/button").click()
        self.driver.implicitly_wait(3)

        # Reopen table
        self.driver.find_element(By.XPATH, f"//table/tbody/tr[{len(rows) - 1}]/td[5]/span").click()
        self.driver.implicitly_wait(3)

        # Wait for table to display
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='marketName']")))

        # Checking editing
        new_market_text = self.driver.find_element(By.XPATH, "//input[@name='marketName']").get_attribute("value")
        assert new_market_text == existing_market_text + added_market_name, pytest.fail("Market edit is not working properly")
        self.driver.implicitly_wait(5)

        # Restore original data
        market_element = self.driver.find_element(By.XPATH,"//input[@name='marketName']")
        market_element.clear()
        market_element.send_keys(existing_market_text)

        # Trigger vendor
        vendor_name = self.driver.find_element(By.XPATH, "//*[(text())='VENDOR']/ancestor::table/tbody/tr[1]/td[3]/span/input")

        # Getting exising vendor value
        existing_vendor_text = self.driver.find_element(By.XPATH, "//*[(text())='VENDOR']/ancestor::table/tbody/tr[1]/td[3]/span/input").get_attribute("value")

        # Adding new data to vendor
        added_vendor_name = " xyz"
        vendor_name.send_keys(added_vendor_name)

        # Save data again for vendor name
        self.driver.find_element(By.XPATH, "//*[@class='text-center']/button").click()
        self.driver.implicitly_wait(4)

        # Click on alert again
        self.driver.find_element(By.XPATH, "//*[@class='textleft']/button").click()
        self.driver.implicitly_wait(3)

        # Reopen table again
        self.driver.find_element(By.XPATH, f"//table/tbody/tr[{len(rows) - 1}]/td[5]/span").click()
        self.driver.implicitly_wait(3)

        # Wait for table to display
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[(text())='VENDOR']/ancestor::table/tbody/tr[1]/td[3]/span/input")))

        # Checking editing for vendor
        new_vendor_text = self.driver.find_element(By.XPATH, "//*[(text())='VENDOR']/ancestor::table/tbody/tr[1]/td[3]/span/input").get_attribute("value")
        assert new_vendor_text == existing_vendor_text + added_vendor_name, pytest.fail("Vendor edit is not working properly")

        # Restore original data for vendor name
        vendor_element = self.driver.find_element(By.XPATH,"//*[(text())='VENDOR']/ancestor::table/tbody/tr[1]/td[3]/span/input")
        vendor_element.clear()
        vendor_element.send_keys(existing_vendor_text)

        # Save data
        self.driver.find_element(By.XPATH, "//*[@class='text-center']/button").click()
        self.driver.implicitly_wait(4)

        # Click on alert
        self.driver.find_element(By.XPATH, "//*[@class='textleft']/button").click()
        self.driver.implicitly_wait(3)