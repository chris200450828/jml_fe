from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 設置 ChromeDriver 的路徑
driver_path = 'C:/Users/user/OneDrive/桌面/大學/112學期-大二下/網路程式設計/chromedriver-win64/chromedriver.exe'  # 更新為正確的 ChromeDriver 路徑
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# 打開目標網站
driver.get("https://www.ptt.cc/bbs/Gossiping/index.html")

try:
    # 等待並點擊 '我已滿18歲' 按鈕
    print("等待年齡驗證按鈕...")
    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/form/div[1]/button'))
    )
    print("點擊 '我已滿18歲'!")
    button.click()

    # 確保頁面完全加載
    time.sleep(2)

    # 獲取網站標題
    website_title = driver.title
    print("Website Title:", website_title)

    # 獲取文章列表
    posts = driver.find_elements(By.CSS_SELECTOR, 'div.r-ent')

    # 準備存儲文章詳情的列表
    post_details = []

    # 提取每篇文章的詳情
    for post in posts:
        try:
            title = post.find_element(By.CSS_SELECTOR, 'div.title a').text
            url = post.find_element(By.CSS_SELECTOR, 'div.title a').get_attribute('href')
            author = post.find_element(By.CSS_SELECTOR, 'div.meta .author').text
            post_details.append({
                'title': title,
                'url': url,
                'author': author
            })
        except:
            continue

    # 列出文章詳情
    print("List of Posts:")
    for detail in post_details:
        print(f"Title: {detail['title']}")
        print(f"URL: {detail['url']}")
        print(f"Author: {detail['author']}")
        print()

except Exception as e:
    print(f"發生錯誤: {e}")

finally:
    # 關閉瀏覽器
    driver.quit()
