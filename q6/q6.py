# 名字、背號及薪資
from selenium.webdriver import Keys
from tqdm import trange
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get("https://hoopshype.com/salaries/players/")
wait = WebDriverWait(driver, 10)

all_play = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, '//table[@class="hh-salaries-ranking-table hh-salaries-table-sortable responsive"]')))
rows = all_play.find_elements(By.XPATH, ".//tr")

data = []
for row in rows:
    cells = row.find_elements(By.XPATH, ".//td")
    if cells:
        data.append([cell.text for cell in cells])

for i in trange(len(data)):
    while True:
        try:
            data[i].remove('')
        except ValueError as stop:
            break

player = []
player_object = all_play.find_elements(By.XPATH, '//tr/td/a')
for i in trange(len(player_object)):
    player.append(player_object[i].text)
del player[0:612]

player_df = pd.DataFrame(player, columns=['Player'])
data_df = pd.DataFrame(data[1:], columns=['2023/24', '2024/25', '2025/26', '2026/27'])
result = pd.concat([player_df, data_df], axis=1)

result.to_csv('all_play.csv', index=False, encoding='utf-8-sig')

first = player_object[1]
second = player_object[2]
third = player_object[3]

first_url = first.get_attribute('href')
second_url = second.get_attribute('href')
third_url = third.get_attribute('href')


def get_data(driver, element):  # prevent shadows name cases
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(element)

    name = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="player-fullname"]')))
    number = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="player-jersey"]')))
    salary = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="player-bio-text"]/span[5]/span')))

    return name.text, number.text, salary.text


first_name, first_number, first_salary = get_data(driver, first_url)
second_name, second_number, second_salary = get_data(driver, second_url)
third_name, third_number, third_salary = get_data(driver, third_url)

top_data = {
    'Name': [first_name, second_name, third_name],
    'Number': [first_number, second_number, third_number],
    'Salary': [first_salary, second_salary, third_salary]
}
df = pd.DataFrame(top_data)

df.to_csv('highest.csv', index=False, encoding='utf-8-sig')
