import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


def scroll_to_lowest(driver, method, locate, start_count=0, mouse_wait_time=0.1, return_number=None):
    wait = WebDriverWait(driver, 10)
    count_down = start_count

    if method == 'CSS':
        method = By.CSS_SELECTOR
    elif method == 'XPATH':
        method = By.XPATH
    elif method == By.XPATH or method == By.CSS_SELECTOR:
        pass
    else:
        raise ValueError('Method must be XPATH, CSS, or selenium.By object')

    while True:
        try:
            elements = wait.until(EC.presence_of_all_elements_located((method, locate)))
            element = elements[count_down]

            # Check if the element is interactable
            if element.is_displayed() and element.size['height'] > 0 and element.size['width'] > 0:
                actions = ActionChains(driver)
                actions.move_to_element(element).perform()
                count_down += 1
                time.sleep(mouse_wait_time)
                driver.execute_script("window.scrollBy(0, 1000);")
            else:
                print(f"Element {count_down} is not interactable. Skipping...")
                count_down += 1
        except IndexError:
            break
        except Exception as e:
            print('An error occurred:', e)
            break

    if return_number:
        return count_down
