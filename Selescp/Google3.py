from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

def undetectable_driver():
    # Configure Chrome options for undetectable behavior
    options = Options()
    options.add_argument("--start-maximized")  # Maximize browser window
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Create and return the undetectable driver
    service = Service()  # Use default webdriver.chrome() behavior
    driver = webdriver.Chrome(service=service, options=options)

    # Bypass detection scripts
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        """
    })
    return driver

def login_google():
    # Get user input for email and password
    email = input("Enter your Google email: ")
    password = input("Enter your Google password: ")

    # Initialize undetectable Chrome driver
    driver = undetectable_driver()

    try:
        # Open Google login page
        driver.get("https://accounts.google.com/signin")

        # Wait for the email input field and enter the email
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        ).send_keys(email)

        # Click "Next"
        driver.find_element(By.ID, "identifierNext").click()

        # Wait for the password field to appear and enter the password
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        ).send_keys(password)

        # Click "Next"
        driver.find_element(By.ID, "passwordNext").click()

        # Wait for a while to verify login success
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Welcome')]"))
        )
        print("Login successful!")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(5)  # Keep the browser open for 5 seconds for inspection
        driver.quit()

if __name__ == "__main__":
    login_google()
