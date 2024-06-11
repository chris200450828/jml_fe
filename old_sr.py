import time
from selenium.webdriver.common.by import By  # 引入 By 模組，定位元素
from selenium.webdriver.support import expected_conditions as EC  # 引入 expected_conditions，用於等待特定條件
from selenium.webdriver.common.action_chains import ActionChains  # 引入 ActionChains，執行高級互動
from selenium.webdriver.support.ui import WebDriverWait  # 引入 WebDriverWait，用於顯式等待

def scroll_to_lowest(driver, method, locate, start_count=0, mouse_wait_time=0.1, return_number=None):
    """
    滾動頁面到最底部，同時與指定的元素互動。

    參數:
        driver: Selenium WebDriver 對象
        method: 定位元素的方法 ('CSS', 'XPATH' 或 selenium.By 對象)
        locate: 定位符值
        start_count: 開始計數
        mouse_wait_time: 每次鼠標動作後的等待時間
        return_number: 是否返回滾動過的元素數量

    返回:
        如果 return_number 設置為 True，返回滾動過的元素數量
    """
    wait = WebDriverWait(driver, 10)  # 設置顯式等待，超時時間為 10 秒
    count_down = start_count  # 初始化計數器

    # 轉換方法字符串為 selenium 的 By 對象
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
            # 等待所有元素出現
            elements = wait.until(EC.presence_of_all_elements_located((method, locate)))
            actions = ActionChains(driver)
            actions.move_to_element(elements[count_down]).perform()  # 移動到當前元素
            count_down += 1  # 增加計數器
            time.sleep(mouse_wait_time)  # 等待一段時間
            driver.execute_script("window.scrollBy(0, 1000);")  # 滾動頁面
        except IndexError:
            break  # 如果沒有更多元素，跳出循環
        except NameError as unknown_exception_unsolved_name:
            print('might end, or just bugged')
            print(unknown_exception_unsolved_name)  # 打印異常信息
            break

    # 如果 return_number 為 True，返回滾動過的元素數量
    if return_number is True:
        return count_down
