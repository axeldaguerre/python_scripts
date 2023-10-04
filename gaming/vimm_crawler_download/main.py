import sys 
import time
import os
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

script_name = sys.argv[0]
web_driver_exe_path = sys.argv[1]
urls_file_path = sys.argv[2]
data_count_target = sys.argv[3]
executable_path = os.getcwd()
total_byte_count = 0

def is_download_complete(folder_path):
    files = os.listdir(folder_path)
    for file in files:
        if file.endswith('.crdownload'):
            return False
    return True 


if len(sys.argv) == 1:
    print(f"{script_name} [web driver path] [urls file path] [max data byte count]")
driver = webdriver.Chrome()

with open(urls_file_path, 'r') as file:
    content = file.read()
    for platform in content.split('_'):
        platform = platform.replace("\n", "")
        urls = content.split('\n')

        for url in urls:
            if (url.find("http") == -1): continue  
            folder_path = f"{executable_path}/{platform}"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--auto-open-devtools-for-tabs") 
            chrome_options.add_experimental_option("prefs", {
                "download.default_directory": "C:/Users/axeld/Downloads",
                "download.prompt_for_download": False,
            })
            
            driver = webdriver.Chrome(options=chrome_options)
            
            driver.get(url)
            form = driver.find_element(By.ID, "download_form")
            download = form.submit()
            
            while not is_download_complete(folder_path):
                print(f"downloading : ")
                time.sleep(1)






