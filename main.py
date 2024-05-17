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
    EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div/div[1]/div/div/ul/li[5]/div/div[2]/span")))
market_element.click()
time.sleep(5)

driver.find_element(By.XPATH, "//*[@placeholder='Search by Report name']/ancestor::div[1]/button").click()
time.sleep(3)


reportfreq_options = Select(driver.find_element(By.NAME, "reportFrequency")).options
for i in reportfreq_options[1:]:
    print(i.get_attribute("value"))