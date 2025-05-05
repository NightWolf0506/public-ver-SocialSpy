from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

num_chats = int(input("Enter the number of chats you want to interact with: "))

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")
time.sleep(5)  # Allow page to load

try:
    # Wait for QR code scan or login via phone
    print("Please scan the QR code or complete the login process on your phone.")
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Chats']"))
    )
    print("Logged in successfully.")

    # Create a folder for screenshots
    os.makedirs("chat_screenshots", exist_ok=True)

    # Find the scrollable chat panel
    try:
        scrollable_panel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='pane-side']"))
        )
        scrollable = True
    except Exception:
        print("Scrollable panel not found. Proceeding without scrolling.")
        scrollable = False

    # Scroll and interact with chats
    interacted_chats = 0
    scroll_attempts = 0
    max_scroll_attempts = 10

    while interacted_chats < num_chats and scroll_attempts < max_scroll_attempts:
        # Get the list of visible chats
        chat_boxes = driver.find_elements(By.XPATH, "//div[contains(@class, '_8nE1Y')]//span[@title]")

        for chat in chat_boxes:
            if interacted_chats >= num_chats:
                break

            try:
                # Click on the chat
                chat_title = chat.get_attribute("title")
                print(f"Interacting with chat: {chat_title}")
                ActionChains(driver).move_to_element(chat).click().perform()

                # Wait for the chat to open
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Message list']"))
                )

                # Take a screenshot of the chat
                screenshot_path = os.path.join("chat_screenshots", f"{chat_title}.png")
                driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved for chat: {chat_title} at {screenshot_path}")

                interacted_chats += 1
                time.sleep(2)  # Pause between interactions
            except Exception as e:
                print(f"Error interacting with chat {chat_title}: {e}")

        # Scroll down the chat list if more interactions are needed
        if interacted_chats < num_chats and scrollable:
            try:
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_panel)
                time.sleep(2)
                scroll_attempts += 1
            except Exception as e:
                print(f"Error while scrolling: {e}")
                break

    print("Interaction completed.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
    