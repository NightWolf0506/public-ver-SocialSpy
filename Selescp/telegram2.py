import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from fpdf import FPDF
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
    return file_save


def click_element(driver, by, identifier, description):
    """Waits for and clicks an element."""
    try:
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((by, identifier))
        )
        element.click()
        print(f"Clicked on {description}.")
    except TimeoutException:
        print(f"Failed to find or click {description}. Check the selector.")


def login_to_telegram(driver, phone_number):
    """Logs into Telegram Web."""
    driver.get("https://web.telegram.org")
    try:
        # Wait for and click the 'Log in by phone Number' button
        click_element(driver, By.XPATH, '//button[contains(@class, "Button") and text()="Log in by phone Number"]', "Log in by phone Number button")

        # Wait for and enter the phone number
        phone_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="sign-in-phone-number" and @type="text"]'))
        )
        phone_input.send_keys(phone_number)
        print("Phone number entered.")

        # Click the 'Next' button
        click_element(driver, By.XPATH, '//button[@type="submit" and contains(@class, "Button")]', "Next button")

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


def capture_settings(driver, folder):
    """Captures the settings page and returns the file path."""
    # Click the menu icon
    click_element(driver, By.XPATH, '//button[@title="Open menu" and @aria-label="Open menu"]', "Menu icon")

    # Click the settings button
    click_element(driver, By.XPATH, '//i[@class="icon icon-settings"]', "Settings button")

    # Wait for the settings page to load and take a screenshot
    time.sleep(12)
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
    """Generates a PDF with the given information."""
    from datetime import datetime
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title Page
    pdf.add_page()
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, txt="Case Report", ln=True, align="C")
    pdf.ln(10)  # Space after the title

    # Date
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.set_font("Arial", size=12, style="I")
    pdf.cell(0, 10, txt=f"Report Date: {report_date}", ln=True)

    # Horizontal Line
    pdf.set_draw_color(0, 0, 0)  # Black line
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y() + 5, 200, pdf.get_y() + 5)
    pdf.ln(10)  # Space after the line

    # Accused Information
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(0, 10, txt="Accused Information", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Case Number: {case_number}", ln=True)
    pdf.cell(0, 10, txt=f"Accused Name: {accused_name}", ln=True)
    pdf.ln(10)  # Add space after text

    # Horizontal Line
    pdf.set_draw_color(0, 0, 0)  # Black line
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y() + 5, 200, pdf.get_y() + 5)
    pdf.ln(5)  # Space after the line

    # Profile Information
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(0, 10, txt="Profile and Chat Information", ln=True)
    pdf.ln(1)  # Gap between heading and image
    pdf.image(settings_screenshot, x=10, y=pdf.get_y(), w=190)
    pdf.ln(10)  # Small space after the image


    for chat in chat_screenshots:
        if pdf.get_y() > 250:  # Adjust based on the page height
            pdf.add_page()  # Add a new page if nearing the end
        pdf.image(chat, x=10, y=pdf.get_y(), w=190)
        pdf.ln(100)  # Add space between screenshots

    # Save PDF
    pdf.output(output_file)
    print(f"PDF generated and saved as {output_file}")


def main():
    case_number = input("Enter Case Number: ")
    accused_name = input("Enter Accused Name: ")
    phone_number = input("Enter Accused phone number with (+ISD code): ")
    folder = "TelegramData"
    pdf_output = "TelegramCaseReport.pdf"

    driver = uc.Chrome()
    driver.maximize_window()

    try:
        login_to_telegram(driver, phone_number)

        time.sleep(5)  # Allow chats to load

        settings_screenshot = capture_settings(driver, folder)
        chat_screenshots = capture_chats(driver, folder)

        generate_pdf(case_number, accused_name, settings_screenshot, chat_screenshots, pdf_output)
    finally:
        driver.quit()
        print("Driver quit.")


if __name__ == "__main__":
    main()

# def generate_pdf(case_number, accused_name, settings_screenshot, chat_screenshots, output_file):
#     """Generates a PDF with the given information."""
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)

#     # Title Page
#     pdf.add_page()
#     pdf.set_font("Arial", size=14, style="B")
#     pdf.cell(200, 10, txt="Case Report", ln=True, align="C")

#     # Accused Information
#     pdf.set_font("Arial", size=12, style="B")
#     pdf.cell(0, 10, txt="Accused Information", ln=True)
#     pdf.set_font("Arial", size=12)
#     pdf.cell(0, 10, txt=f"Case Number: {case_number}", ln=True)
#     pdf.cell(0, 10, txt=f"Accused Name: {accused_name}", ln=True)
#     pdf.ln(10)  # Add space after text

#     # Profile Information
#     pdf.set_font("Arial", size=12, style="B")
#     pdf.cell(0, 10, txt="Profile Information", ln=True)
#     pdf.ln(5)  # Gap between heading and image
#     pdf.image(settings_screenshot, x=10, y=pdf.get_y(), w=190)
#     pdf.ln(80)  # Ensure there's enough space after the image

#     # Chat Information
#     pdf.set_font("Arial", size=12, style="B")
#     pdf.cell(0, 10, txt="Chat Information", ln=True)
#     pdf.ln(5)  # Gap between heading and images
#     for chat in chat_screenshots:
#         if pdf.get_y() > 250:  # Adjust based on the page height
#             pdf.add_page()  # Add a new page if nearing the end
#         pdf.image(chat, x=10, y=pdf.get_y(), w=190)
#         pdf.ln(80)  # Space after each image

#     # Save PDF
#     pdf.output(output_file)
#     print(f"PDF generated and saved as {output_file}")




# def main():
#     case_number = input("Enter Case Number: ")
#     accused_name = input("Enter Accused Name: ")
#     phone_number = input("Enter Accused phone number with (+ISD code): ")
#     folder = "TelegramData"
#     pdf_output = "TelegramCaseReport.pdf"

#     driver = uc.Chrome()
#     driver.maximize_window()

#     try:
#         login_to_telegram(driver, phone_number)

#         time.sleep(5)  # Allow chats to load

#         settings_screenshot = capture_settings(driver, folder)
#         chat_screenshots = capture_chats(driver, folder)

#         generate_pdf(case_number, accused_name, settings_screenshot, chat_screenshots, pdf_output)
#     finally:
#         driver.quit()
#         print("Driver quit.")


# if __name__ == "__main__":
#     main()
