from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# 初始化 Chrome 選項
chrome_options = Options()

# 設定 ChromeDriver 路徑
chrome_driver_path = "C:/Users/user/Desktop/大學二下作業/網路程式設計/chromedriver-win64/chromedriver.exe"

# 創建 Chrome WebDriver 實例
service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# 隱式等待，等待元素加載的最長時間為10秒
driver.implicitly_wait(10)

# 前往指定網址
url = "https://data.gov.tw/"
driver.get(url)

# 找到搜索框並輸入關鍵字
search_box = driver.find_element(By.ID, "searchbar-input")
search_box.send_keys("腸病毒")

# 找到搜尋按鈕並點擊
search_button = driver.find_element(By.XPATH, "//button[contains(@class, 'searchbar-submit-btn')]")
search_button.click()

# 等待搜尋結果頁面加載完全
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '健保門診及住院就診人次統計-腸病毒')]")))

# 點擊目標鏈接
link = driver.find_element(By.XPATH, "//a[contains(text(), '健保門診及住院就診人次統計-腸病毒')]")
link.click()

driver.switch_to.window(driver.window_handles[-1])
# 等待新頁面 URL 變化並加載完全
WebDriverWait(driver, 20).until(EC.url_contains("/dataset/14590"))

# 找到 CSV 下載鏈接
csv_link = driver.find_element(By.XPATH, "//*[@id='__nuxt']/div/div[1]/main/div[3]/div[2]/div[2]/div[2]/ul[1]/li/a")
csv_link.click()

# 獲取 CSV 下載鏈接的 URL
csv_url = csv_link.get_attribute("href")

# 使用 requests 下載 CSV 文件，忽略 SSL 驗證
response = requests.get(csv_url, verify=False)

# 確認請求成功
if response.status_code == 200:
    # 假設文件編碼為 Big5，解碼並重新保存為 UTF-8-sig 編碼
    decoded_content = response.content.decode('utf-8-sig', errors='ignore')
    
    csv_path = "C:/Users/user/Desktop/大學二下作業/網路程式設計/期末/NHI_EnteroviralInfection.csv"
    with open(csv_path, "w", encoding="utf-8-sig") as f:
        f.write(decoded_content)
    
    print("CSV 文件已成功下載並保存到", csv_path)
else:
    print("下載 CSV 文件失敗，狀態碼:", response.status_code)

# 關閉瀏覽器
driver.quit()
