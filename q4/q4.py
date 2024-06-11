from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd

chrome_options = Options()

# 創建 Chrome WebDriver 實例
chrome_driver_path = "C:/Users/user/Desktop/大學二下作業/網路程式設計/chromedriver-win64/chromedriver.exe"
service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.implicitly_wait(15)
url = "https://www.google.com"
driver.get(url)
keyword = driver.find_element(By.CSS_SELECTOR, "#APjFqb")
keyword.send_keys("Steam 遊戲推薦")
keyword.send_keys(Keys.ENTER)

# 創建 WebDriverWait 對象
wait = WebDriverWait(driver, 10)

# 獲取搜索結果的項目
items = driver.find_elements(By.XPATH, '//div[@class="MjjYud"]')

# 初始化 last_number
last_number = len(items)

# 模擬向下滾動10次以加載更多結果
for _ in range(10):
    try:
        more = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "更多結果")]')))
        driver.execute_script("arguments[0].click();", more)
        time.sleep(1)
    except:
        break
    last_number = len(driver.find_elements(By.XPATH, '//div[@class="MjjYud"]'))

# 提取標題和鏈接
titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//h3[@class="LC20lb MBeuO DKV0Md"]')))
links = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@jsname="UWckNb"]')))

title_data, link_data = [], []
for i in range(len(titles)):
    title_data.append(f"Title: {titles[i].text}")
    link_data.append(f"Link: {links[i].get_attribute('href')}")
    print(f"Title: {titles[i].text}")
    print(f"Link: {links[i].get_attribute('href')}")
    print()

# 關閉瀏覽器
driver.quit()

# 指定保存路徑
save_path = r'C:\Users\user\Desktop\大學二下作業\網路程式設計\期末\Steam.csv'

# 將結果保存到 CSV 文件
df = pd.DataFrame({"Title": title_data, "Link": link_data})
df.to_csv(save_path, index=False, encoding='utf-8-sig')

print(f"數據已保存到 {save_path}")

