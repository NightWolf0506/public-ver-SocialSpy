import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

def capture_screenshot(driver, folder, filename):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, folder)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_save = os.path.join(file_path, filename)
    driver.save_screenshot(file_save)
    print(f"Screenshot saved as {filename}")

def login_to_chrome(driver, email, password):
    driver.get("https://accounts.google.com/signin")
    try:
        # Enter the email
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]'))
        )
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)

        # Wait for the transition to the password page
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "password")))

        # Enter the password
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        # Wait until the login is complete
        WebDriverWait(driver, 20).until(EC.url_contains("myaccount.google.com"))
        print("Logged into Google account successfully.")
    except TimeoutException:
        print("An error occurred during login.")

def main():
    email = "adarshayush1128@gmail.com"
    password = "sih24@01"
    folder = "ChromeSS"

    # Using undetected-chromedriver
    driver = uc.Chrome()
    try:
        login_to_chrome(driver, email, password)
        time.sleep(5)
        capture_screenshot(driver, folder, "homepage.png")
        print("Screenshot of the home page taken.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
