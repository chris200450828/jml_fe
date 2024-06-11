import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import old_sr as sr  # 假設 old_sr 是一個自定義的模組，包含 scroll_to_lowest 函數

# 設定 Chrome 瀏覽器選項
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("detach", True)

# 啟動 Chrome 瀏覽器並打開 Agoda 網站
driver = webdriver.Chrome(options=options)
driver.get("https://www.agoda.com/zh-tw/")
wait = WebDriverWait(driver, 10)

# 定位並操作搜尋框，輸入城市名稱
search_city = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="textInput"]')))
search_city.send_keys('台中')
time.sleep(1)
search_city.send_keys(Keys.ESCAPE)

# 定位並點擊搜尋按鈕
search_button = wait.until(EC.presence_of_element_located(
    (By.XPATH, '//button[@class="Buttonstyled__ButtonStyled-sc-5gjk6l-0 iCZpGI Box-sc-kv6pi1-0 fDMIuA"]')))
search_button.click()
driver.switch_to.window(driver.window_handles[-1])

# 滾動頁面以加載所有酒店
sr.scroll_to_lowest(driver, 'CSS', '[data-selenium="hotel-item"]')

# 定位所有酒店項目
hotel_item = wait.until(EC.presence_of_all_elements_located(
    (By.CSS_SELECTOR, '[data-selenium="hotel-item"]')))
hotel_name_list, hotel_price_list = [], []

# 提取每個酒店的名稱和價格
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

# 將數據轉換為 DataFrame 並保存到 CSV 文件
data = zip(hotel_name_list, hotel_price_list)
df = pd.DataFrame(data, columns=['Name', 'Price'])
df.to_csv('agoda_result.csv', index=False, encoding='utf-8-sig')
