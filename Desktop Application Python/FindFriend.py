from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import os


def find_friend():
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)

    username_input = driver.find_element(By.NAME, "username")
    username_input.send_keys(username)

    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)

    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

    try:
        user = ["itachi.strike","adar5hthakur","shagun__yadav"]
        found = []
        not_found = []
        n = 4
        for u in user:
            driver.get(f"https://www.instagram.com/{u}/")
            try:
                WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Following')]")))
                print("Found")
                found.append(u)
            except:
                not_found.append(u)
                print('Not Found')
            time.sleep(5)
        print("Found : ",found)
        print("Not Found : ",not_found)
    except Exception as e:
        print(f"An error occurred while handling Friend search: {e}")

find_friend()