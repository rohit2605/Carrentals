import pytest
from selenium import webdriver
from selenium.common import TimeoutException
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
rows = driver.find_elements(By.XPATH,"//table/tbody/tr")
driver.find_element(By.XPATH,f"//table/tbody/tr[{len(rows)-1}]/td[2]/a").click()

        # Setup Category
setup_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'Setup')]")))
setup_element.click()

        # Add New Category
driver.find_element(By.XPATH,"//button[contains(text(),'Add New')]").click()
category_name = "Test Category"
categoryName_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Category Name')]/ancestor::label/following-sibling::div/input")))
categoryName_element.send_keys(category_name)
driver.find_element(By.XPATH, "//*[contains(text(),'Category Name')]/ancestor::div[1]/following-sibling::div/button[@type='submit']").click()

        # Category Created
modal_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(),'Category Info')]/ancestor::div[1]/following-sibling::div/button")))
modal_element.click()

        # All competitors selected
competitors = driver.find_elements(By.XPATH, "//div[@class='grid-my-cate']/div[2]/div/div[2]/div")
for i in range(1,len(competitors)):
    driver.find_element(By.XPATH, f"//div[@class='grid-my-cate']/div[2]/div/div[2]/div[{i}]/button").click()
driver.find_element(By.XPATH, " //div[@class='grid-my-cate']/ancestor::div[2]/following-sibling::div/button").click()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div/button"))).click()
driver.find_element(By.XPATH,"//div[@class='grid-my-cate']/ancestor::div[2]/div[1]/h2/button").click()

        # Validate Category is created or not
try:
    assert WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(),'{category_name}')]")))
except TimeoutException:
    pytest.fail(f"Category '{category_name}' is not created")

        # Click on view details of new category
driver.find_element(By.XPATH, f"//*[contains(text(),'{category_name}')]//ancestor::div[3]/following-sibling::div/center/button").click()
# try:
#     WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='apexcharts-legend-series']")))
# except TimeoutException:
#     pytest.fail("No data displays on chart")