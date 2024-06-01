import time
from selenium import webdriver
import os
import getpass
from selenium.webdriver.chrome.options import Options


def find_extension():
    username = getpass.getuser()
    chrome_profile = os.path.expanduser(
        fr'C:\Users\{username}\AppData\Local\Google\Chrome\User Data\Default\Extensions')
    extension_key = 'gighmmpiobklfepjocnamgkkbiglidom'
    full_path = fr'C:\Users\{username}\AppData\Local\Google\Chrome\User Data\Default\Extensions\gighmmpiobklfepjocnamgkkbiglidom'
    for root, dirs, files in os.walk(chrome_profile):
        if extension_key in dirs:
            version_dirs = os.listdir(full_path)
            print(version_dirs)
            if version_dirs:
                latest_version = sorted(version_dirs, reverse=True)[0]
                adb_path = os.path.join(root, extension_key, latest_version)
                return adb_path


def adb(site, opt=None):
    manual = False
    adb_path = find_extension()
    manual_adb_path = r'YOUR ADB PATH HERE'
    if not adb_path and opt:
        print("couldn't find extension path,may need to add path manually")
        manual = True

    if opt:
        options = webdriver.ChromeOptions()
        if manual is False:
            options.add_argument('load-extension=' + adb_path)
        else:
            options.add_argument('load-extension=' + manual_adb_path)
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.get(site)
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        adb_site = 'https://getadblock.com/zh_TW/installed/'
        while adb_site not in driver.current_url:  # check if the adb is loaded or not
            print("waiting ad_blocker install...")
            time.sleep(1)  # wait for adb installed
            driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.get(site)

    return driver
