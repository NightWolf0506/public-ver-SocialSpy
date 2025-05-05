import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from fpdf import FPDF
import time
import os
from datetime import datetime

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

def capture_settings(driver, folder):
    """Captures the settings page and returns the file path."""
    click_element(driver, By.XPATH, '//button[@title="Open menu" and @aria-label="Open menu"]', "Menu icon")

    click_element(driver, By.XPATH, '//i[@class="icon icon-settings"]', "Settings button")

    time.sleep(4)
    settings_screenshot = capture_screenshot(driver, folder, "settings.png")
    print("Captured settings page screenshot.")

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

            # Scroll up in chat before taking screenshot
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)

            screenshot_path = capture_screenshot(driver, folder, f"Chat_{index + 1}.png")
            chat_screenshots.append(screenshot_path)

            click_element(driver, By.XPATH, '//button[@title="Go back" and @aria-label="Go back"]', "Go back to chat list")
    except TimeoutException:
        print("No chats found or an error occurred while capturing chats.")
    return chat_screenshots

def generate_pdf(report_title, accused_info, profile_info, screenshots, output_path):
    """
    Generates a PDF report with accused and profile information along with screenshots.

    Args:
        report_title (str): The title of the PDF report.
        accused_info (dict): Information about the accused (e.g., name, contact details).
        profile_info (dict): Profile details of the Telegram account (e.g., username, bio).
        screenshots (list): List of file paths to the screenshots.
        output_path (str): Path where the generated PDF should be saved.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title page
    pdf.add_page()
    pdf.set_font("Arial", "B", size=16)
    pdf.cell(0, 10, txt=report_title, ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(10)

    # Accused Information
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(0, 10, txt="Accused Information", ln=True)
    pdf.set_font("Arial", size=12)
    for key, value in accused_info.items():
        pdf.cell(0, 10, txt=f"{key}: {value}", ln=True)
    pdf.ln(10)

    # Profile Information
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(0, 10, txt="Profile Information", ln=True)
    pdf.set_font("Arial", size=12)
    for key, value in profile_info.items():
        pdf.cell(0, 10, txt=f"{key}: {value}", ln=True)
    pdf.ln(20)

    # Screenshots
    for idx, screenshot in enumerate(screenshots):
        pdf.add_page()
        pdf.set_font("Arial", "B", size=14)
        pdf.cell(0, 10, txt=f"Screenshot {idx + 1}", ln=True, align="C")
        pdf.ln(5)
        try:
            pdf.image(screenshot, x=10, y=30, w=190)
        except RuntimeError as e:
            pdf.cell(0, 10, txt=f"Error loading screenshot: {e}", ln=True, align="C")

    # Save the PDF
    try:
        pdf.output(output_path)
        print(f"PDF report successfully generated at {output_path}")
    except Exception as e:
        print(f"Failed to generate PDF: {e}")


# def generate_pdf(report_title, screenshots, output_path):
#     """
#     Generates a PDF report with the provided screenshots.
    
#     Args:
#         report_title (str): The title of the PDF report.
#         screenshots (list): List of file paths to the screenshots.
#         output_path (str): Path where the generated PDF should be saved.
#     """
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)

#     # Title page
#     pdf.add_page()
#     pdf.set_font("Arial", "B", size=16)
#     pdf.cell(0, 10, txt=report_title, ln=True, align="C")
#     pdf.set_font("Arial", size=12)
#     pdf.ln(10)  # Line break
#     pdf.multi_cell(0, 10, txt=f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#     pdf.ln(10)
#     pdf.multi_cell(0, 10, txt="This report contains captured screenshots of Telegram chats and settings for documentation purposes.")
#     pdf.ln(20)

#     # Add each screenshot to the PDF
#     for idx, screenshot in enumerate(screenshots):
#         pdf.add_page()
#         pdf.set_font("Arial", "B", size=14)
#         pdf.cell(0, 10, txt=f"Screenshot {idx + 1}: {os.path.basename(screenshot)}", ln=True, align="C")
#         pdf.ln(5)  # Line break before image

#         # Attempt to add the screenshot, with error handling
#         try:
#             pdf.image(screenshot, x=10, y=30, w=190)  # Dynamically position the image
#             pdf.ln(120)  # Ensure space for next content (if any)
#         except RuntimeError as e:
#             pdf.set_font("Arial", size=12)
#             pdf.cell(0, 10, txt=f"Error adding screenshot {os.path.basename(screenshot)}: {e}", ln=True, align="C")

#     # Save the PDF
#     try:
#         pdf.output(output_path)
#         print(f"PDF report successfully generated at {output_path}")
#     except Exception as e:
#         print(f"Failed to generate PDF report: {e}")

# def generate_pdf(report_title, screenshots, output_path):
#     """Generates a PDF report with the provided screenshots."""
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.set_font("Arial", size=16)
#     pdf.cell(200, 10, txt=report_title, ln=True, align="C")

#     for screenshot in screenshots:
#         pdf.add_page()
#         pdf.set_font("Arial", size=12)
#         pdf.cell(200, 10, txt=os.path.basename(screenshot), ln=True, align="C")
#         pdf.image(screenshot, x=10, y=30, w=190)

#     pdf.output(output_path)
#     print(f"PDF report generated at {output_path}")

def main():
    folder_name = "Telegram_Case_Reportt"
    phone_number = "+919631085870"
    report_title = "Telegram Case Report"
    output_pdf = "Telegram_Case_Report.pdf"

    driver = uc.Chrome()
    try:
        login_to_telegram(driver, phone_number)

        # Capture settings page screenshot
        settings_screenshot = capture_settings(driver, folder_name)

        # Capture chat screenshots
        chat_screenshots = capture_chats(driver, folder_name)

        # Generate PDF report
        screenshots = [settings_screenshot] + chat_screenshots
        generate_pdf(report_title, screenshots, output_pdf)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
