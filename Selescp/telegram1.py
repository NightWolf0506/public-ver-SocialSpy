import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

def capture_screenshot(driver, folder, filename):
    """Captures a screenshot and saves it to the specified folder."""
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, folder)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_save = os.path.join(file_path, filename)
    driver.save_screenshot(file_save)
    print(f"Screenshot saved as {filename}")

def login_to_telegram(driver, phone_number):
    """Logs into Telegram Web."""
    driver.get("https://web.telegram.org")
    try:
        # Wait for and click the 'Log in by phone Number' button
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "Button") and text()="Log in by phone Number"]'))
        )
        login_button.click()
        print("Clicked on 'Log in by phone Number' button.")

        # Wait for and enter the phone number
        phone_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="sign-in-phone-number" and @type="text"]'))  # Corrected selector
        )
        phone_input.send_keys(phone_number)
        print("Phone number entered.")

        # Click the 'Next' button
        next_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and contains(@class, "Button")]'))
        )
        next_button.click()
        print("Clicked on 'Next' button.")

        # Allow time for manual OTP entry
        print("Please enter the OTP manually.")
        time.sleep(15)  # Adjust the time if necessary

        # Wait until the chat list page loads
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'chat-list')))
        print("Logged into Telegram Web successfully.")
    except TimeoutException:
        print("An error occurred during login. Please check the selectors or wait time.")
        driver.quit()
        raise  # Exit the program if login fails

def main():
    phone_number = "+919631085870"  # Replace with your phone number
    folder = "TelegramSS"

    driver = uc.Chrome()
    driver.maximize_window()  # Ensure the browser is full screen

    try:
        # Log into Telegram
        login_to_telegram(driver, phone_number)

        # Wait for 5 seconds to ensure chats are fully loaded
        time.sleep(5)

        # Take a screenshot of the chat list page
        capture_screenshot(driver, folder, "Homepage.png")
    finally:
        # Quit the driver
        driver.quit()
        print("Driver quit.")

if __name__ == "__main__":
    main()
