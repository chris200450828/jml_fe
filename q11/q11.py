import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from adb_installer import adb

# 詢問使用者是否安裝廣告阻擋器
install_adblocker = input("Do you want to install the adblocker? (yes/no): ").strip().lower()
site_url = "http://www.atmovies.com.tw/movie/new/"

# 根據使用者選擇，決定是否安裝廣告阻擋器
if install_adblocker == "yes" or install_adblocker == 'y' or install_adblocker == 'Y':
    driver = adb(site_url, opt=True)
else:
    driver = adb(site_url, opt=False)

wait = WebDriverWait(driver, 10)

# 跳轉到票房排行榜
rank = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#dropdownMenu > li:nth-child(1) > ul > li:nth-child(7) > a')))
driver.execute_script("arguments[0].click();", rank)

# 獲取排行榜、片名和票房數據
rank = wait.until(EC.presence_of_all_elements_located(
    (By.XPATH, '//*[@id="main"]/div/div[1]/div/table[1]/tbody/tr/td[1]')))
title = wait.until(EC.presence_of_all_elements_located(
    (By.XPATH, '//*[@id="main"]/div/div[1]/div/table[1]/tbody/tr/td[2]')))
box = wait.until(EC.presence_of_all_elements_located(
    (By.XPATH, '//*[@id="main"]/div/div[1]/div/table[1]/tbody/tr/td[3]')))
url = driver.current_url

# 打印前幾名電影的票房資訊
for i in range(0, len(title)):
    print("{:<5} {:<70} {:<15}".format(rank[i].text, title[i].text, box[i].text))
print("==========================================================================")

# 跳轉到更多票房資訊
tp_more = wait.until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[1]/div/table[1]/tbody/tr[7]/td/a')))
driver.execute_script("arguments[0].click();", tp_more)

# 獲取更詳細的票房資訊
tp_rank = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[1]/div/table[2]/tbody//tr/td[1]/b')))
current = driver.current_url
print(current)

# 獲取表格頭部資訊
tb = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[1]/div/table[2]')))
headers = [header.text for header in tb.find_elements(By.XPATH, ".//th")]

# 獲取所有行的數據
rows = tb.find_elements(By.XPATH, ".//tr")

# 提取每行的數據
data = []
for row in rows:
    cells = row.find_elements(By.XPATH, ".//td")
    if cells:
        data.append([cell.text for cell in cells])

# 創建一個 DataFrame
df = pd.DataFrame(data, columns=headers)

cleaned_data = []

# 清洗數據
for i in range(0, len(df), 2):
    # 提取電影標題行和對應的數據行
    title_row = df.iloc[i]
    data_row = df.iloc[i + 1]

    # 將數據合併成一行
    combined_row = {
        '排行': title_row['排行'],
        '片名': title_row['片名'],
        '本週票房': data_row['本週票房'],
        '累計票房': data_row['累計票房']
    }
    cleaned_data.append(combined_row)

# 創建一個包含清洗數據的新 DataFrame
cleaned_df = pd.DataFrame(cleaned_data)

# 將 DataFrame 保存為 CSV 文件
cleaned_df.to_csv("tablee.csv", index=False, encoding='utf-8-sig')
