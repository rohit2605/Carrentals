import time
import random

from selenium import webdriver
import pytest
from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
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

    @pytest.mark.sanity
    def test_categories(self,setup):
        # Login
        self.driver.find_element(By.XPATH, "//input[@name='username']").send_keys("ezrental")
        self.driver.find_element(By.XPATH, "//input[@name='password']").send_keys("ezrental")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        self.driver.implicitly_wait(10)
        rows = self.driver.find_elements(By.XPATH,"//table/tbody/tr")
        self.driver.find_element(By.XPATH,f"//table/tbody/tr[{len(rows)-1}]/td[2]/a").click()

        # Setup Category
        setup_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'Setup')]")))
        setup_element.click()

        # Add New Category
        self.driver.find_element(By.XPATH,"//button[contains(text(),'Add New')]").click()
        category_name = "Test Category"
        categoryName_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Category Name')]/ancestor::label/following-sibling::div/input")))
        categoryName_element.send_keys(category_name)
        self.driver.find_element(By.XPATH, "//*[contains(text(),'Category Name')]/ancestor::div[1]/following-sibling::div/button[@type='submit']").click()

        # Category Created
        modal_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(),'Category Info')]/ancestor::div[1]/following-sibling::div/button")))
        modal_element.click()

        # All competitors selected
        competitors = self.driver.find_elements(By.XPATH, "//div[@class='grid-my-cate']/div[2]/div/div[2]/div")
        for i in range(len(competitors)):
            self.driver.find_element(By.XPATH,
                                     f"//div[@class='grid-my-cate']/div[2]/div/div[2]/div[{i+1}]/button").click()
        self.driver.find_element(By.XPATH,
                                 " //div[@class='grid-my-cate']/ancestor::div[2]/following-sibling::div/button").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div/button"))).click()
        self.driver.find_element(By.XPATH, "//div[@class='grid-my-cate']/ancestor::div[2]/div[1]/h2/button").click()

        # Validate Category is created or not
        try:
            assert WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(),'{category_name}')]")))
        except TimeoutException:
            pytest.fail(f"Category '{category_name}' is not created")

        # Click on view details of new category
        self.driver.find_element(By.XPATH, f"//*[contains(text(),'{category_name}')]//ancestor::div[3]/following-sibling::div/center/button").click()
        competitor_list = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@class='lor-filter']/following-sibling::div/button")))
        competitor_list.click()
        # self.driver.find_element(By.XPATH, "//*[@class='lor-filter']/following-sibling::div/button").click()
        try:
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='cars-list-box']")))
            total_competitors = self.driver.find_elements(By.XPATH, "//*[@class='cars-list-box']/div")

            # Check the length of the competitor elements and assert
            assert len(total_competitors) > 0, "No competitors found"

        except TimeoutException:
            pytest.fail("No competitors found")

        # Click on cross button
        self.driver.find_element(By.XPATH, "//*[@class='cars-list-box']/preceding-sibling::div[2]/h3").click()

        # Back to list page using breadcrumbs
        self.driver.find_element(By.XPATH, "//div[@class= 'desk-breadcrumbs']/div/nav/ol/li[5]").click()

        # # Click on Setup Category again
        # setup_element_1 = WebDriverWait(self.driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'Setup')]")))
        # setup_element_1.click()

        # #Delete the category
        # WebDriverWait(self.driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Test Category')]/ancestor::div[1]/*[local-name()='svg'][2]"))).click()
        # time.sleep(8)


    def test_market_alert(self,setup):
        # Login
        self.driver.find_element(By.XPATH, "//input[@name='username']").send_keys("ezrental")
        self.driver.find_element(By.XPATH, "//input[@name='password']").send_keys("ezrental")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        self.driver.implicitly_wait(10)
        rows = self.driver.find_elements(By.XPATH,"//table/tbody/tr")
        self.driver.find_element(By.XPATH,f"//table/tbody/tr[{len(rows)-1}]/td[2]/a").click()
        time.sleep(15)

         # Select Market Alerts
        market_element = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div/div[1]/div/div/ul/li[4]/div/div[2]/span")))
        market_element.click()

        # Click on Create Alert Button
        self.driver.find_element(By.XPATH, "//*[@placeholder='Search by alert name']/ancestor::div[1]/button").click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@class='stepper-one']/following-sibling::div/button[2]"))).click()

        # Dropdown select
        dropdown = Select(self.driver.find_element(By.NAME, "marketcategorieslabel"))
        dropdown.select_by_visible_text("Test Category")
        self.driver.find_element(By.XPATH, "//*[@class='stepper-two']/following-sibling::div/button[2]").click()
        self.driver.implicitly_wait(6)

        initial_options = [option.text for option in Select(self.driver.find_element(By.NAME, "alertme")).options]
        for option_text in initial_options:
            dropdown_category = Select(self.driver.find_element(By.NAME, "alertme"))
            dropdown_category.select_by_visible_text(option_text)
            time.sleep(3)
            dropdown_pricetype = Select(self.driver.find_element(By.NAME, "pricetype"))
            dropdown_pricetype.select_by_visible_text("is less than")
            time.sleep(3)
            self.driver.find_element(By.XPATH, "//*[@name='price']").send_keys("11")
            time.sleep(3)
            dropdown_lor = Select(self.driver.find_element(By.NAME, "lor"))
            dropdown_lor.select_by_visible_text("1 day")
            time.sleep(3)
            dropdown_days = Select(self.driver.find_element(By.NAME, "horizon"))
            dropdown_days.select_by_value("30")

            # Click on Next button for 3rd step
            self.driver.find_element(By.XPATH, "//*[@class='stepper-three']/following-sibling::div/button[2]").click()
            time.sleep(3)
            new_name = "test" + str(random.randint(0, 1000))
            self.driver.find_element(By.XPATH, "//*[@placeholder='Enter the alert name']").send_keys(new_name)
            time.sleep(2)
            self.driver.find_element(By.XPATH, "//*[@name='emailone']").send_keys("xyz@yopmail.com")
            time.sleep(2)
            self.driver.find_element(By.XPATH, "//*[@class='stepper-four']/following-sibling::div/button[2]").click()
            time.sleep(2)

            # Alert handle
            self.driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/button").click()
            time.sleep(3)

            # Assert
            total_rows = self.driver.find_elements(By.XPATH, "//*[contains(text(),'Alert Type')]/ancestor::div[1]/table/tbody/tr")
            alertnames = []
            for i in range(len(total_rows)):
                    single_alertname = self.driver.find_element(By.XPATH, f"//*[contains(text(),'Alert Type')]/ancestor::div[1]/table/tbody/tr[{i+1}]/td[2]").text
                    alertnames.append(single_alertname)
            assert new_name in alertnames, f"Required value {new_name} is not created"

            # Click on create alert again
            self.driver.find_element(By.XPATH, "//*[@placeholder='Search by alert name']/ancestor::div[1]/button").click()
            time.sleep(2)
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[@class='stepper-one']/following-sibling::div/button[2]"))).click()

            # Dropdown select
            dropdown = Select(self.driver.find_element(By.NAME, "marketcategorieslabel"))
            dropdown.select_by_visible_text("Test Category")
            self.driver.find_element(By.XPATH, "//*[@class='stepper-two']/following-sibling::div/button[2]").click()
            time.sleep(3)


    def test_market_activity(self, setup):
        # Login
        self.driver.find_element(By.XPATH, "//input[@name='username']").send_keys("ezrental")
        self.driver.find_element(By.XPATH, "//input[@name='password']").send_keys("ezrental")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        self.driver.implicitly_wait(10)
        rows = self.driver.find_elements(By.XPATH,"//table/tbody/tr")
        self.driver.find_element(By.XPATH,f"//table/tbody/tr[{len(rows)-1}]/td[2]/a").click()
        time.sleep(15)

         # Select Activity Report
        market_element = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div/div[1]/div/div/ul/li[5]/div/div[2]/span")))
        market_element.click()
        time.sleep(5)

        # Click on Add New Report Button
        self.driver.find_element(By.XPATH, "//*[@placeholder='Search by Report name']/ancestor::div[1]/button").click()

        reportfreq_options = [option.get_attribute("value") for option in Select(self.driver.find_element(By.NAME, "reportFrequency")).options]
        for option_value in reportfreq_options[1:]:
            dropdown_reportfreq = Select(self.driver.find_element(By.NAME, "reportFrequency"))
            dropdown_reportfreq.select_by_value(option_value)
            time.sleep(3)

            report_name = "report" + str(random.randint(0, 1000))
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@name='reportName']"))).send_keys(report_name)
            time.sleep(2)
            dropdown_lorental = Select(self.driver.find_element(By.NAME, "lengthOfRental"))
            dropdown_lorental.select_by_value("1")
            time.sleep(2)
            dropdown_horizon = Select(self.driver.find_element(By.NAME, "horizon"))
            dropdown_horizon.select_by_value("30")
            time.sleep(2)
            total_categories = self.driver.find_elements(By.XPATH, "//*[@class='category-options']/li")
            for i in range(len(total_categories)):
                self.driver.find_element(By.XPATH, f"//*[@class='category-options']/li[{i+1}]").click()
            self.driver.find_element(By.XPATH, "//*[@name='emailone']").send_keys("abc@yopmail.com")
            time.sleep(2)
            self.driver.find_element(By.XPATH, "//*[@name='emailone']/ancestor::div[4]/following-sibling::div/button[2]").click()
            time.sleep(3)

            # Alert handle
            self.driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/button").click()
            time.sleep(3)

            # Assert
            total_activity_rows = self.driver.find_elements(By.XPATH, "//*[contains(text(),'Activity Reports')]/ancestor::div[1]/following-sibling::div/div/div/table/tbody/tr")
            reportnames = []
            for i in range(len(total_activity_rows)):
                    single_activityname = self.driver.find_element(By.XPATH, f"//*[contains(text(),'Activity Reports')]/ancestor::div[1]/following-sibling::div/div/div/table/tbody/tr[{i+1}]/td[1]").text
                    reportnames.append(single_activityname)
            assert report_name in reportnames, f"Required value {report_name} is not created"

            # Click on Add New Report Button
            self.driver.find_element(By.XPATH, "//*[@placeholder='Search by Report name']/ancestor::div[1]/button").click()
            time.sleep(2)
