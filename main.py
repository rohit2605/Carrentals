from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
driver.find_element(By.XPATH, f"//table/tbody/tr[{len(rows) - 1}]/td[5]/span").click()
market_element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//input[@name='marketName']")))
existing_market_name = driver.find_element(By.XPATH, "//input[@name='marketName']").get_attribute("value")
print(existing_market_name)