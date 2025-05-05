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
        email_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]')))
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)

        # Wait for the password input to be present
        password_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@name="Passwd"]')))
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        # Wait until we're logged in and the home page loads
        WebDriverWait(driver, 20).until(EC.url_contains("myaccount.google.com"))
        print("Logged into Google account successfully.")
    except TimeoutException:
        print("An error occurred during login.")

def zoom_out_browser(driver, percentage):
    """Zooms out the browser by the specified percentage."""
    zoom_steps = int((100 - percentage) / 10)  # Each CTRL + '-' reduces 10% zoom approximately
    for _ in range(zoom_steps):
        driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.CONTROL, Keys.SUBTRACT)
    print(f"Zoomed out to approximately {percentage}%.")

def take_multiple_screenshots(driver, folder, count=10):
    """Takes multiple screenshots by scrolling the page."""
    for i in range(count):
        capture_screenshot(driver, folder, f"Screenshot_{i + 1}.png")
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        print(f"Screenshot {i + 1} taken and scrolled one screen size.")
        time.sleep(1)

def navigate_to_personal_info_and_take_screenshot(driver):
    """Navigates to 'Personal Info' section, scrolls down 11%, and takes a screenshot."""
    driver.get("https://myaccount.google.com/personal-info")
    time.sleep(3)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight * 0.11);")
    print("Scrolled down 11% of the page in 'Personal Info' section.")
    capture_screenshot(driver, "ChromeSS", "Personalinfo.png")

def handle_chrome_activity(driver):
    """Handles Chrome activity screenshots."""
    driver.get("https://myactivity.google.com/myactivity")
    time.sleep(3)
    zoom_out_browser(driver, 67)  # Zoom out to 67%
    take_multiple_screenshots(driver, "ChromeHistory")

def handle_youtube_activity(driver):
    """Handles YouTube activity screenshots."""
    driver.get("https://myactivity.google.com/product/youtube")
    time.sleep(3)
    take_multiple_screenshots(driver, "YouTubeHistory")

def handle_google_maps_timeline(driver):
    """Handles Google Maps timeline screenshots."""
    driver.get("https://www.google.com/maps/timeline")
    time.sleep(3)
    capture_screenshot(driver, "GoogleMapsTimeline", "Timeline.png")
    print("Screenshot of Google Maps timeline taken.")

def main():
    email = "adarshayush1128@gmail.com"
    password = "sih24@01"

    driver = uc.Chrome()
    driver.maximize_window()
    login_to_chrome(driver, email, password)

    navigate_to_personal_info_and_take_screenshot(driver)

    handle_chrome_activity(driver)

    handle_youtube_activity(driver)

    handle_google_maps_timeline(driver)

    # Quit the driver
    driver.quit()
    print("Driver quit.")

if __name__ == "__main__":
    main()
