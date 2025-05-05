import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from fpdf import FPDF
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
    return file_save

def click_element(driver, by, identifier, description):
    try:
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((by, identifier))
        )
        element.click()
        print(f"Clicked on {description}.")
    except TimeoutException:
        print(f"Failed to find or click {description}. Check the selector.")

def login_to_telegram(driver, phone_number):
    driver.get("https://web.telegram.org")
    try:
        click_element(driver, By.XPATH, '//button[contains(@class, "Button") and text()="Log in by phone Number"]', "Log in by phone Number button")
        phone_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="sign-in-phone-number" and @type="text"]'))
        )
        phone_input.send_keys(phone_number)
        print("Phone number entered.")
        click_element(driver, By.XPATH, '//button[@type="submit" and contains(@class, "Button")]', "Next button")
        print("Please enter the OTP manually.")
        time.sleep(15)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'chat-list')))
        print("Logged into Telegram Web successfully.")
    except TimeoutException:
        print("An error occurred during login. Please check the selectors or wait time.")
        driver.quit()
        raise

def select_date(driver, date):
    print("Opening date selector...")
    click_element(driver, By.XPATH, '//span[text()="Today"]', "Today button")
    time.sleep(2)

    desired_month, desired_day = date.split("-")[1], date.split("-")[2]
    current_month = driver.find_element(By.XPATH, '//div[@class="month-selector"]/h4').text.split()[0]

    while current_month != desired_month:
        click_element(driver, By.XPATH, '//button[@class="Button smaller translucent round" and .//i[contains(@class, "icon-next")]]', "Next month button")
        current_month = driver.find_element(By.XPATH, '//div[@class="month-selector"]/h4').text.split()[0]

    day_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//div[contains(@class, "day-button") and text()="{desired_day}"]'))
    )
    day_button.click()
    click_element(driver, By.XPATH, '//button[text()="Jump to Date"]', "Jump to Date button")
    print(f"Date {date} selected.")

def capture_chats_from_date(driver, folder, start_date):
    select_date(driver, start_date)
    time.sleep(3)

    chat_screenshots = []
    while True:
        screenshot_path = capture_screenshot(driver, folder, f"Chat_{len(chat_screenshots) + 1}.png")
        chat_screenshots.append(screenshot_path)

        try:
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(2)
            more_chats = driver.find_element(By.XPATH, '//div[contains(@class, "chat-list") and contains(@class, "loading")]')
            if not more_chats.is_displayed():
                break
        except:
            break

    return chat_screenshots

def capture_settings(driver, folder):
    """Captures the settings page and returns the file path."""
    # Click the menu icon
    click_element(driver, By.XPATH, '//button[@title="Open menu" and @aria-label="Open menu"]', "Menu icon")

    # Click the settings button
    click_element(driver, By.XPATH, '//i[@class="icon icon-settings"]', "Settings button")

    # Wait for the settings page to load and take a screenshot
    time.sleep(4)
    settings_screenshot = capture_screenshot(driver, folder, "settings.png")
    print("Captured settings page screenshot.")

    # Click the go back button
    click_element(driver, By.XPATH, '//button[@title="Go back" and @aria-label="Go back"]', "Go back button")
    return settings_screenshot


def capture_chats(driver, folder):
    """Captures screenshots of all chats and returns a list of file paths."""
    chat_screenshots = []
    try:
        chats = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "chat-list")]//div[contains(@class, "chat")]'))
        )
        print(f"Found {len(chats)} chats. Taking screenshots...")

        for index, chat in enumerate(chats):
            driver.execute_script("arguments[0].scrollIntoView();", chat)
            time.sleep(1)
            chat.click()
            print(f"Opened chat {index + 1}.")

            time.sleep(3)
            screenshot_path = capture_screenshot(driver, folder, f"Chat_{index + 1}.png")
            chat_screenshots.append(screenshot_path)

            # Go back to the chat list
            click_element(driver, By.XPATH, '//button[@title="Go back" and @aria-label="Go back"]', "Go back to chat list")
    except TimeoutException:
        print("No chats found or an error occurred while capturing chats.")
    return chat_screenshots

def generate_pdf(case_number, accused_name, settings_screenshot, chat_screenshots, output_file):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    pdf.set_font("Arial", size=14, style="B")
    pdf.cell(200, 10, txt="Case Report", ln=True, align="C")

    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(0, 10, txt="Accused Information", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Case Number: {case_number}", ln=True)
    pdf.cell(0, 10, txt=f"Accused Name: {accused_name}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(0, 10, txt="Profile Information", ln=True)
    pdf.ln(5)
    pdf.image(settings_screenshot, x=10, y=pdf.get_y(), w=190)
    pdf.ln(80)

    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(0, 10, txt="Chat Information", ln=True)
    pdf.ln(5)
    for chat in chat_screenshots:
        if pdf.get_y() > 250:
            pdf.add_page()
        pdf.image(chat, x=10, y=pdf.get_y(), w=190)
        pdf.ln(80)

    pdf.output(output_file)
    print(f"PDF generated and saved as {output_file}")

def main():
    case_number = input("Enter Case Number: ")
    accused_name = input("Enter Accused Name: ")
    phone_number = input("Enter Accused phone number with (+ISD code): ")
    start_date = input("Enter start date for chats (YYYY-MM-DD): ")
    folder = "TelegramData"
    pdf_output = "TelegramCaseReport.pdf"

    driver = uc.Chrome()
    driver.maximize_window()

    try:
        login_to_telegram(driver, phone_number)
        time.sleep(5)
        settings_screenshot = capture_screenshot(driver, folder, "settings.png")
        chat_screenshots = capture_chats_from_date(driver, folder, start_date)
        generate_pdf(case_number, accused_name, settings_screenshot, chat_screenshots, pdf_output)
    finally:
        driver.quit()
        print("Driver quit.")

if __name__ == "__main__":
    main()
