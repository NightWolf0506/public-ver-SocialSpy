import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
from PyPDF2 import PdfMerger

# Function to capture screenshots
def capture_screenshot(driver, folder, filename):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, folder)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_save = os.path.join(file_path, filename)
    driver.save_screenshot(file_save)
    print(f"Screenshot saved as {filename}")

# Function to combine PDFs into a single file
def combine_pdfs(pdf_folder, output_filename):
    merger = PdfMerger()
    for root, dirs, files in os.walk(pdf_folder):
        for file in sorted(files):
            if file.endswith(".pdf"):
                merger.append(os.path.join(root, file))
    merger.write(output_filename)
    merger.close()
    print(f"All PDFs combined into {output_filename}")

# Function to log in to Google account
def login_to_chrome(driver, email, password):
    driver.get("https://accounts.google.com/signin")
    try:
        email_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]')))
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)

        password_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@name="Passwd"]')))
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        WebDriverWait(driver, 20).until(EC.url_contains("myaccount.google.com"))
        print("Logged into Google account successfully.")
    except TimeoutException:
        print("An error occurred during login.")

# Function to take multiple screenshots by scrolling the page
def take_multiple_screenshots(driver, folder, count=10):
    for i in range(count):
        capture_screenshot(driver, folder, f"Screenshot_{i + 1}.png")
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        print(f"Screenshot {i + 1} taken and scrolled one screen size.")
        time.sleep(1)

# Function to handle Chrome activity screenshots
def handle_chrome_activity(driver):
    driver.get("https://myactivity.google.com/myactivity")
    time.sleep(3)
    take_multiple_screenshots(driver, "ChromeHistory")

# Function to handle YouTube activity screenshots
def handle_youtube_activity(driver):
    driver.get("https://myactivity.google.com/product/youtube")
    time.sleep(3)
    take_multiple_screenshots(driver, "YouTubeHistory")

# Function to handle Google Maps timeline screenshots
def handle_google_maps_timeline(driver):
    driver.get("https://www.google.com/maps/timeline")
    time.sleep(3)
    capture_screenshot(driver, "GoogleMapsTimeline", "Timeline.png")
    print("Screenshot of Google Maps timeline taken.")

# Function to print and save PDF for each email
def print_gmail_emails(driver, count):
    driver.get("https://mail.google.com/")
    time.sleep(5)

    pdf_folder = "GmailPrints"
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    emails = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='main'] .zA")))
    
    for index, email in enumerate(emails[:count]):
        try:
            email.click()
            time.sleep(3)
            
            # Click on the "More options" button
            more_options = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='More message options']")))
            more_options.click()
            
            # Click on "Print"
            print_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Print']")))
            print_option.click()
            
            time.sleep(5)  # Wait for the print dialog to appear

            # Handle the print pop-up
            print_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "cr-button.action-button")))
            print_button.click()
            
            time.sleep(5)  # Wait for the print to process
            
            print(f"Email {index + 1} printed.")
            driver.back()  # Go back to the inbox
            time.sleep(3)
        except Exception as e:
            print(f"Error printing email {index + 1}: {e}")
            driver.back()

    # Combine the PDFs
    combine_pdfs(pdf_folder, "CombinedGmailPrints.pdf")

# Main function
def main():
    email = "adarshayush1128@gmail.com"
    password = "sih24@01"

    driver = uc.Chrome()
    driver.maximize_window()

    # Login to Chrome
    login_to_chrome(driver, email, password)

    # Navigate and take screenshots
    handle_chrome_activity(driver)
    handle_youtube_activity(driver)
    handle_google_maps_timeline(driver)

    # Handle Gmail activity
    print_gmail_emails(driver, 10)

    # Quit the driver
    driver.quit()
    print("Driver quit.")

if __name__ == "__main__":
    main()
