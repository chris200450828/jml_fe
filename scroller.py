import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


def scroll_to_lowest(driver, method, locate, start_count=0):
    wait = WebDriverWait(driver, 10)
    count_down = start_count

    if method == 'CSS':
        method = By.CSS_SELECTOR
    elif method == 'XPATH':
        method = By.XPATH
    elif method == By.XPATH or method == By.CSS_SELECTOR:
        pass
    else:
        raise ValueError('Method must be XPATH,CSS or selenium.By object')

    while True:
        try:
            elements = wait.until(EC.presence_of_all_elements_located((method, locate)))
            actions = ActionChains(driver)
            actions.move_to_element(elements[count_down]).perform()
            count_down += 1
            time.sleep(0.1)
            driver.execute_script("window.scrollBy(0, 1000);")
        except IndexError:
            print('WE ARRIVED')
            break
        except NameError as unknown_exception_unsolved_name:
            print('might end, or just bugged')
            print(unknown_exception_unsolved_name)
            break
