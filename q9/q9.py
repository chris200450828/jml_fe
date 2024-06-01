from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.get("https://github.com/")

wait = WebDriverWait(driver, 10)

username = 'forclassroom06@gmail.com'
password = 'chris0967201968'

login = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/header/div/div[1]/div[1]/a')))
driver.execute_script('arguments[0].click();', login)
account_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="login_field"]')))
account_input.send_keys(username)
password_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="password"]')))
password_input.send_keys(password)
submit = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="submit"]')))
submit.click()

title1 = wait.until(EC.presence_of_element_located(
    (By.XPATH, '/html/body/div[1]/div[6]/div/div/aside/div/div/loading-context/div/div[1]/div/h2')))
print(title1.text)
content1 = wait.until(EC.presence_of_element_located(
    (By.XPATH, '/html/body/div[1]/div[6]/div/div/aside/div/div/loading-context/div/div[1]/div/p')))
print(content1.text)
print('--------------------------------------------------------------------------------------------------------')

title2 = wait.until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="dashboard"]/div/feed-container/div[2]/div[1]/h3')))
print(title2.text)
content2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dashboard"]/div/feed-container/div[2]/p')))
print(content2.text)
