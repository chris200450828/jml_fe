import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

def scroll_to_lowest(driver, method, locate, start_count=0, mouse_wait_time=0.1, return_number=None):
    """
    Scrolls through a webpage to the lowest point, interacting with elements along the way.

    Args:
        driver: Selenium WebDriver object.
        method: Method to locate elements ('CSS', 'XPATH', or selenium.By object).
        locate: The locator value to find elements.
        start_count: Initial count to start scrolling from.
        mouse_wait_time: Time to wait between mouse actions.
        return_number: If set, returns the number of elements scrolled through.

    Returns:
        If return_number is specified, returns the count of elements scrolled through.
    """
    
    # Initialize WebDriverWait with a timeout of 10 seconds
    wait = WebDriverWait(driver, 10)
    count_down = start_count

    # Map method string to selenium By object
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
            # Wait until elements are located
            elements = wait.until(EC.presence_of_all_elements_located((method, locate)))
            element = elements[count_down]

            # Check if the element is interactable
            if element.is_displayed() and element.size['height'] > 0 and element.size['width'] > 0:
                actions = ActionChains(driver)
                actions.move_to_element(element).perform()  # Move to the element
                count_down += 1
                time.sleep(mouse_wait_time)  # Wait for a short time
                driver.execute_script("window.scrollBy(0, 1000);")  # Scroll down by 1000 pixels
            else:
                print(f"Element {count_down} is not interactable. Skipping...")
                count_down += 1
        except IndexError:
            # Break the loop if there are no more elements to interact with
            break
        except Exception as e:
            # Print any other errors and break the loop
            print('An error occurred:', e)
            break

    # Return the count of elements scrolled through if return_number is specified
    if return_number:
        return count_down
