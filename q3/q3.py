from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# 指定 ChromeDriver 的絕對路徑
chrome_driver_path = "C:/Users/user/OneDrive/桌面/大學/112學期-大二下/網路程式設計/chromedriver-win64/chromedriver.exe"
service = Service(chrome_driver_path)

# 初始化 WebDriver
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(10)
driver.get("https://fchart.github.io/ML/nba_items.html")

# 商品編號範圍
start_product_number = 1
end_product_number = 165

page_num = start_product_number

while page_num <= end_product_number:
    time.sleep(3)
    print("當前頁面:", page_num)
    
    # 等待表格出現
    try:
        table = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "table"))
        )
    except:
        print("未找到表格或加載超時")
        break
    
    # 如果表格存在
    if table:
        df = pd.read_html(driver.page_source)[0]
        print("儲存頁面:", page_num)
        df.to_csv(f"NBA_Products{page_num}.csv", index=False, encoding="utf-8-sig")
    else:
        print("未找到表格")
    
    # 檢查是否達到指定的頁面
    if page_num == 17:
        print("儲存完畢")
        break
    
    try:
        # 找到下一頁的按鈕並點擊
        next_page_num = page_num + 1
        page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="pagination-wrapper"]/button[text()="{next_page_num}"]'))
        )
        page_button.click()
        time.sleep(5)
        page_num += 1
    except Exception as e:
        print("結束:", e)
        break

driver.quit()
