from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()

# 創建 Chrome WebDriver 實例
chrome_driver_path = "C:/Users/user/Desktop/網路程式設計/chromedriver-win64/chromedriver.exe"
service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.implicitly_wait(10)

# 前往指定網址
url = "https://www.momoshop.com.tw/main/Main.jsp?cid=memb&oid=back2hp&mdiv=1099800000-bt_0_150_01-bt_0_150_01_e1&ctype=B"
driver.get(url)

# 找到搜索框
search_box = driver.find_element(By.ID, "keyword")

# 在搜索框輸入 "nba"，你可以自行更改關鍵字
search_box.send_keys("nba")

# 找到搜尋按鈕並點擊
search_button = driver.find_element(By.XPATH, "//button[contains(@class, 'inputbtn')]")
search_button.click()

# 等待網頁重定向和加載完全
WebDriverWait(driver, 10).until(EC.url_contains("https://www.momoshop.com.tw/search/searchShop.jsp"))

# 抓取網頁內容
html_content = driver.page_source

# 將 HTML 內容保存到文件中
with open("C:/Users/user/Desktop/網路程式設計/期末/NBA_test.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# 關閉瀏覽器
driver.quit()
