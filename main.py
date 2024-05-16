import random
import time

import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://ui-stg-carrental.ratemetrics.com/")
driver.implicitly_wait(10)
driver.find_element(By.XPATH, "//input[@name='username']").send_keys("ezrental")
driver.find_element(By.XPATH, "//input[@name='password']").send_keys("ezrental")
driver.find_element(By.XPATH, "//button[@type='submit']").click()
driver.implicitly_wait(10)
rows = driver.find_elements(By.XPATH,"//table/tbody/tr")
driver.find_element(By.XPATH,f"//table/tbody/tr[{len(rows)-1}]/td[2]/a").click()
time.sleep(15)

market_element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div/div[1]/div/div/ul/li[4]/div/div[2]/span")))
market_element.click()
driver.find_element(By.XPATH, "//*[@placeholder='Search by alert name']/ancestor::div[1]/button").click()
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (By.XPATH, "//*[@class='stepper-one']/following-sibling::div/button[2]"))).click()

# Dropdown select
dropdown = Select(driver.find_element(By.NAME, "marketcategorieslabel"))
dropdown.select_by_visible_text("Test Category")
driver.find_element(By.XPATH, "//*[@class='stepper-two']/following-sibling::div/button[2]").click()
time.sleep(10)


# New experiment
dropdown_category = Select(driver.find_element(By.NAME, "alertme"))
dropdown_pricetype = Select(driver.find_element(By.NAME, "pricetype"))
dropdown_lor = Select(driver.find_element(By.NAME, "lor"))
dropdown_days = Select(driver.find_element(By.NAME, "horizon"))

for cat in dropdown_category.options:
    dropdown_category.select_by_visible_text(cat.text)
    time.sleep(5)
    for prc in dropdown_pricetype.options:
        dropdown_pricetype.select_by_visible_text(prc.text)
        time.sleep(5)
        driver.find_element(By.XPATH, "//*[@name='price']").send_keys("11")
        time.sleep(5)
        for lo in dropdown_lor.options[1:]:
            dropdown_lor.select_by_visible_text(lo.text)
            time.sleep(5)
            for da in dropdown_days.options:
                dropdown_days.select_by_visible_text(da.text)
                time.sleep(5)
                driver.find_element(By.XPATH, "//*[@class='stepper-three']/following-sibling::div/button[2]").click()

                driver.find_element(By.XPATH, "//*[@placeholder='Enter the alert name']").send_keys("test"+str(random.randint(0, 1000)))
                time.sleep(2)
                driver.find_element(By.XPATH, "//*[@name='emailone']").send_keys("xyz@yopmail.com")
                time.sleep(2)
                driver.find_element(By.XPATH, "//*[@class='stepper-four']/following-sibling::div/button[2]").click()
                time.sleep(2)
                driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/button").click()
                driver.find_element(By.XPATH, "//*[@placeholder='Search by alert name']/ancestor::div[1]/button").click()
                time.sleep(2)
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//*[@class='stepper-one']/following-sibling::div/button[2]"))).click()

                # Dropdown select
                dropdown = Select(driver.find_element(By.NAME, "marketcategorieslabel"))
                dropdown.select_by_visible_text("Test Category")
                driver.find_element(By.XPATH, "//*[@class='stepper-two']/following-sibling::div/button[2]").click()
                time.sleep(6)