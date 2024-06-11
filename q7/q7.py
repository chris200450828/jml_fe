import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import trange
import old_sr as sr
import pandas as pd

options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com")
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(20)
search = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@class="gLFyf"]')))
search.send_keys('Xpath')
search.send_keys(Keys.ENTER)

last_number = 0
last_number = sr.scroll_to_lowest(driver, 'XPATH', '//h3[@class="LC20lb MBeuO DKV0Md"]', start_count=last_number,
                                  mouse_wait_time=0.1, return_number=True)
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
title = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//h3[@class="LC20lb MBeuO DKV0Md"]')))
link = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@jsname="UWckNb"]')))
title_data, link_data = [], []
print(len(title), '  ', len(link))
for i in trange(len(title)):
    title_data.append(title[i].text)
    link_data.append(link[i].get_attribute('href'))
    print(title[i].text, '   ', link[i].get_attribute('href'))

data = zip(title_data, link_data)
df = pd.DataFrame(data, columns=['title', 'link'])
df.to_csv('Xpath.csv', index=False, encoding='utf-8-sig')
