import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import scroller as sr

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get("https://www.agoda.com/zh-tw/")
wait = WebDriverWait(driver, 10)

search_city = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="textInput"]')))
search_city.send_keys('台中')
time.sleep(1)
search_city.send_keys(Keys.ESCAPE)

search_button = wait.until(EC.presence_of_element_located(
    (By.XPATH, '//button[@class="Buttonstyled__ButtonStyled-sc-5gjk6l-0 iCZpGI Box-sc-kv6pi1-0 fDMIuA"]')))
search_button.click()
driver.switch_to.window(driver.window_handles[-1])

hotel_item = wait.until(EC.presence_of_all_elements_located(
    (By.CSS_SELECTOR, '[data-selenium="hotel-item"]')))
count_down = 0

sr.scroll_to_lowest(driver, 'CSS', '[data-selenium="hotel-item"]')

hotel_name_list, hotel_price_list = [], []

for hotel in hotel_item:
    hotel_name = hotel.find_element(By.XPATH, './/h3[@data-selenium="hotel-name"]').text
    try:
        hotel_price = hotel.find_element(By.XPATH,
                                         './/div[@data-element-name="final-price"]/span[@data-selenium="display-price"]').text
    except NoSuchElementException as slow:
        try:
            hotel_price = hotel.find_element(By.XPATH, './/div[@data-element-name="final-price"]').text
            hotel_price = '慢了一步 ' + hotel_price
        except Exception as ex:
            hotel_price = '甚麼都沒有'
    print(hotel_name, '   ', hotel_price)
    hotel_name_list.append(hotel_name)
    hotel_price_list.append(hotel_price)

data = zip(hotel_name_list, hotel_price_list)
df = pd.DataFrame(data, columns=['Name', 'Price'])
df.to_csv('agoda_result.csv', index=False, encoding='utf-8-sig')
