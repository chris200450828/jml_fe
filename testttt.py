import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 設定 Chrome 瀏覽器選項
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("detach", True)

# 啟動 Chrome 瀏覽器
driver = webdriver.Chrome(options=options)
driver.get(
    "https://www.momoshop.com.tw/main/Main.jsp?cid=memb&oid=back2hp&mdiv=1099800000-bt_0_150_01-bt_0_150_01_e1&ctype=B")
wait = WebDriverWait(driver, 10)

# 找到搜索框
search_box = driver.find_element(By.ID, "keyword")

# 在搜索框輸入 "nba"
search_box.send_keys("nba")

# 找到搜尋按鈕並點擊
search_button = driver.find_element(By.XPATH, "//button[contains(@class, 'inputbtn')]")
search_button.click()

# 等待網頁重定向和加載完全
WebDriverWait(driver, 10).until(EC.url_contains("https://www.momoshop.com.tw/search/searchShop.jsp"))

# 抓取網頁內容
html_content = driver.page_source

# 使用正則表達式查找並替換關鍵字
new_html_content = re.sub(
    r'location\.replace\(\'https:\/\/www\.momoshop\.com\.tw\/search\/searchShop\.jsp\?keyword=[^\']*\'\);',
    'location.replace(\'https://www.momoshop.com.tw/search/searchShop.jsp?keyword=nba\');',
    html_content
)

# 將 HTML 內容保存到文件中
with open("D:/NBA_test.html", "w", encoding="utf-8") as f:
    f.write(new_html_content)

# 關閉瀏覽器
driver.quit()
