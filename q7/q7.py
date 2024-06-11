import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import trange
import old_sr as sr  # 假設 old_sr 是一個自定義的模組，包含 scroll_to_lowest 函數
import pandas as pd

# 設定 Chrome 瀏覽器選項
options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox')  # 註解掉這一行以適應不同環境
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("detach", True)

# 啟動 Chrome 瀏覽器並打開 Google
driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com")

# 設置顯式等待和隱式等待
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(20)

# 定位並操作 Google 搜索框
search = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@class="gLFyf"]')))
search.send_keys('Xpath')
search.send_keys(Keys.ENTER)

# 初始化滾動數量
last_number = 0
last_number = sr.scroll_to_lowest(driver, 'XPATH', '//h3[@class="LC20lb MBeuO DKV0Md"]', start_count=last_number,
                                  mouse_wait_time=0.1, return_number=True)

# 連續點擊“更多結果”按鈕並滾動頁面，直到沒有更多新結果
while True:
    last_count = last_number
    more = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "更多結果")]')))
    driver.execute_script("arguments[0].click();", more)
    time.sleep(1)
    last_number = sr.scroll_to_lowest(driver, 'XPATH', '//h3[@class="LC20lb MBeuO DKV0Md"]',
                                      start_count=last_number,
                                      mouse_wait_time=0.1, return_number=True)
    if last_number == last_count:
        break

# 提取搜索結果的標題和鏈接
title = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//h3[@class="LC20lb MBeuO DKV0Md"]')))
link = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@jsname="UWckNb"]')))

# 初始化數據列表
title_data, link_data = [], []
print(len(title), '  ', len(link))

# 將標題和鏈接存入數據列表
for i in trange(len(title)):
    title_data.append(title[i].text)
    link_data.append(link[i].get_attribute('href'))
    print(title[i].text, '   ', link[i].get_attribute('href'))

# 將數據轉換為 DataFrame 並保存到 CSV 文件
data = zip(title_data, link_data)
df = pd.DataFrame(data, columns=['title', 'link'])
df.to_csv('Xpath.csv', index=False, encoding='utf-8-sig')
