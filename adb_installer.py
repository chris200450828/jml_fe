import time
from selenium import webdriver
import os
import getpass
from selenium.webdriver.chrome.options import Options

def find_extension():
    """
    查找 Chrome 瀏覽器中 AdBlock 擴展的路徑。
    
    返回:
        adb_path: AdBlock 擴展的路徑
    """
    username = getpass.getuser()  # 獲取當前用戶名
    chrome_profile = os.path.expanduser(
        fr'C:\Users\{username}\AppData\Local\Google\Chrome\User Data\Default\Extensions')  # 擴展的默認路徑
    extension_key = 'gighmmpiobklfepjocnamgkkbiglidom'  # AdBlock 擴展的唯一標識符
    full_path = fr'C:\Users\{username}\AppData\Local\Google\Chrome\User Data\Default\Extensions\{extension_key}'
    for root, dirs, files in os.walk(chrome_profile):
        if extension_key in dirs:  # 檢查目錄中是否包含 AdBlock 擴展
            version_dirs = os.listdir(full_path)  # 列出擴展的版本目錄
            print(version_dirs)
            if version_dirs:
                latest_version = sorted(version_dirs, reverse=True)[0]  # 找到最新版本
                adb_path = os.path.join(root, extension_key, latest_version)  # 組合擴展路徑
                return adb_path

def adb(site, opt=None):
    """
    啟動 Chrome 瀏覽器並打開指定的網站，如果 opt 為 True，則加載 AdBlock 擴展。
    
    參數:
        site: 要打開的網站 URL
        opt: 是否加載 AdBlock 擴展
        
    返回:
        driver: Selenium WebDriver 對象
    """
    manual = False
    adb_path = find_extension()  # 查找 AdBlock 擴展的路徑
    manual_adb_path = r'YOUR ADB PATH HERE'  # 手動指定的 AdBlock 路徑

    if not adb_path and opt:
        print("couldn't find extension path, may need to add path manually")
        manual = True

    options = webdriver.ChromeOptions()  # 創建 Chrome 瀏覽器選項

    if opt:
        if manual is False:
            options.add_argument('load-extension=' + adb_path)  # 加載自動找到的 AdBlock 擴展
        else:
            options.add_argument('load-extension=' + manual_adb_path)  # 加載手動指定的 AdBlock 擴展

    options.add_argument('--disable-dev-shm-usage')  # 禁用 /dev/shm 共享內存
    options.add_experimental_option("detach", True)  # 使瀏覽器在腳本結束後不關閉

    driver = webdriver.Chrome(options=options)  # 啟動 Chrome 瀏覽器
    driver.get(site)  # 打開指定的網站

    if opt:
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])  # 切換到新打開的窗口
        adb_site = 'https://getadblock.com/zh_TW/installed/'
        while adb_site not in driver.current_url:  # 檢查 AdBlock 是否已安裝
            print("waiting ad_blocker install...")
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[-1])  # 繼續切換到新打開的窗口
        driver.close()  # 關閉 AdBlock 安裝頁面
        driver.switch_to.window(driver.window_handles[0])  # 返回主窗口

    return driver
