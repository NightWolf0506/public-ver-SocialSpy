from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")
time.sleep(5)  # Allow page to load

try:
    # Click on "Log in with phone number" button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Log in with phone number')]"))
    )
    login_button.click()

    # Input phone number
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Type your phone number.']"))
    )

    # Clear the default value (+1) and enter the desired phone number
    phone_input.click()  # Focus on the input field
    for _ in range(len(phone_input.get_attribute('value'))):
        phone_input.send_keys(Keys.BACKSPACE)  # Remove the default value

    phone_number = "+9631085870"  # Replace with the phone number
    phone_input.send_keys(phone_number)

    # Click on "Next" button
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[div/div[text()='Next']]"))
    )
    next_button.click()

    # Wait for OTP and manual login
    print("Please complete OTP verification on your phone.")
    time.sleep(99)

    # Click on Profile button
    profile_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Profile']"))
    )
    profile_button.click()
    time.sleep(8)

    # Take screenshot of profile
    driver.save_screenshot("profile_screenshot.png")
    print("Profile screenshot saved as 'profile_screenshot.png'")

    # Click on Status button
    status_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Status']"))
    )
    status_button.click()

    # Click on "My Status"
    my_status_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='My status']"))
    )
    my_status_button.click()

    # Click on Chats button
    chats_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Chats']"))
    )
    chats_button.click()
    time.sleep(3)

    print("Automation completed successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the WebDriver
    driver.quit()
