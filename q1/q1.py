import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service

# ChromeDriver 可執行文件的路徑
chrome_driver_path = "C:/Users/user/OneDrive/桌面/大學/112學期-大二下/網路程式設計/chromedriver-win64/chromedriver.exe"

# 滾動到頁面的最底部
def scroll_to_lowest(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# 指定主題的文章
def print_topic_articles(driver, topic_name, wait):
    topic_button = wait.until(EC.presence_of_element_located((By.XPATH, f'//a[@class="kNtDAe" and contains(text(), "{topic_name}")]')))
    driver.execute_script("arguments[0].click();", topic_button)

    time.sleep(2)
    scroll_to_lowest(driver)

    inside_topic_articles = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="gPFEn" or contains(@class, "JtKRv")]')))
    print(topic_name)
    for article in inside_topic_articles:
        print(article.text)

    driver.get("https://news.google.com/home?hl=zh-TW&gl=TW&ceid=TW:zh-Hant")

# 印出焦點新聞
def print_focus_news(driver, wait):
    print("焦點提要")
    focus = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="gPFEn" or contains(@class, "JtKRv iTin5e")]')))
    print("焦點新聞")
    for i in focus:
        print(i.text)

    print("-------------------")
    print("地方新聞")
    local = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="JtKRv"]')))
    for i in range(3):
        print(local[i].text)

    driver.get("https://news.google.com/home?hl=zh-TW&gl=TW&ceid=TW:zh-Hant")
#印出地方新聞
    print("-------------------")
    print("焦點新聞")
    focus_button = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="aqvwYd"]')))
    driver.execute_script("arguments[0].click();", focus_button)

    time.sleep(2)
    scroll_to_lowest(driver)

    inside_focus = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="gPFEn"]')))
    for i in inside_focus:
        print(i.text)

    driver.get("https://news.google.com/home?hl=zh-TW&gl=TW&ceid=TW:zh-Hant")

# 印出您所在位置的當地天氣
def print_weather(driver, wait):
    weather_button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@class="HDbYSe"]')))
    driver.execute_script("arguments[0].click();", weather_button)

    weather_div = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="PCFVm"]')))
    print("您所在位置的當地天氣")
    for weather in weather_div:
        print(weather.get_attribute('aria-label'))

# 設置 Chrome 選項
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 設置 ChromeDriver 服務
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)

# 打開目標網頁
driver.get("https://news.google.com/home?hl=zh-TW&gl=TW&ceid=TW:zh-Hant")

# 印出焦點新聞
print_focus_news(driver, wait)
print("-------------------")
print("您的主題")

#印出您的主題的全部標題
topics = ["台灣", "國際", "商業", "科學與科技", "娛樂", "體育"]
for topic in topics:
    print_topic_articles(driver, topic, wait)
    print("-------------------")

# 印出天氣資訊
print_weather(driver, wait)
