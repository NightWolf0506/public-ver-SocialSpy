from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image
from fpdf import FPDF
import time
import os


def capture_screenshot(driver,folder ,filename):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, folder)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_save = os.path.join(file_path, filename)
    driver.save_screenshot(file_save)
    print(f"Screenshot saved as {filename}")

def get_posts(driver, username):
    folder = "IPostSS"
    driver.get(f"https://www.instagram.com/{username}/")
    time.sleep(3)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    post_links = []
    posts = driver.find_elements(By.XPATH, '//div//a[contains(@href, "/p/") or contains(@href, "/reel/")]')

    for post in posts[:10]:
        try:
            post_link = post.get_attribute('href')
            if post_link:
                post_links.append(post_link)
        except Exception as e:
            print(f"An error occurred while retrieving post link: {e}")

    for i, post_link in enumerate(post_links):
        try:
            driver.get(post_link)
            time.sleep(3)
            capture_screenshot(driver,folder,f'post_{i}.png')
            print(f"Screenshot for post {i} taken.")
        except Exception as e:
            print(f"An error occurred for post {i}: {e}")

def get_followers_following(driver, username):
    folder_followers = "IFwerSS"
    folder_following = "IFwingSS"
    
    driver.get(f"https://www.instagram.com/{username}/")
    time.sleep(3)
    
    try:
        followers_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/followers/")]'))
        )
        followers_button.click()
        time.sleep(3)

        scrollable_panel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3")]'))
        )
        
        last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_panel)
        screenshot_count = 1
        
        while True:
            # Scroll a little
            driver.execute_script("arguments[0].scrollTop += 200", scrollable_panel)
            time.sleep(2)
            
            capture_screenshot(driver, folder_followers, f'followers_{screenshot_count}.png')
            screenshot_count += 1
            
            try:
                driver.find_element(By.XPATH, '//span[contains(text(), "Suggested for you")]')
                print("Suggested for you section found. Stopping the followers process.")
                break
            except:
                pass
            
            new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_panel)
            if new_height == last_height:
                break
            last_height = new_height
    except Exception as e:
        print(f"An error occurred while handling followers: {e}")
    

    try:
        driver.get(f"https://www.instagram.com/{username}/")
        following_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/following/")]'))
        )
        following_button.click()
        time.sleep(3)

        scrollable_panel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3")]'))
        )
        
        last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_panel)
        screenshot_count = 1
        
        while True:
            driver.execute_script("arguments[0].scrollTop += 200", scrollable_panel)
            time.sleep(2)
            
            capture_screenshot(driver, folder_following, f'following_{screenshot_count}.png')
            screenshot_count += 1
            
            try:
                driver.find_element(By.XPATH, '//span[contains(text(), "Suggested for you")]')
                print("Suggested for you section found. Stopping the following process.")
                break
            except:
                pass
            
            new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_panel)
            if new_height == last_height:
                break
            last_height = new_height
    except Exception as e:
        print(f"An error occurred while handling following: {e}")

def get_messages(driver):
    folder = "IMessSS"
    message_url = 'https://www.instagram.com/direct/inbox/'
    driver.get(message_url)
    

    try:
        not_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))
        )
        not_now_button.click()
    except Exception as e:
        print(f"No 'Turn on Notifications' popup found: {e}")

    message_links = set()
    time.sleep(3)

    try:
        scrollable_panel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="region" and contains(@class, "scrollable")]'))
        )
        scrollable = True
    except TimeoutException:
        print("Scrollable panel not found. Proceeding without scrolling.")
        scrollable = False

    if scrollable:
        last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_panel)

        while True:
            try:
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_panel)
                time.sleep(5)

            except Exception as e:
                print(f"An error occurred while scrolling or finding messages: {e}")
                break

    for i, message in enumerate(driver.find_elements(By.XPATH, '//div[@role="listitem"]')):
        try:
            message.click()
            time.sleep(5)
            capture_screenshot(driver, folder, f'message_{i}.png')
            message_url = 'https://www.instagram.com/direct/inbox/'
            time.sleep(3) 
        except Exception as e:
            print(f"An error occurred for message {i}: {e}")


def create_pdf_from_screenshots(name, pdf_title, folder_titles):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 10, pdf_title, 0, 1, 'C')

    def add_images_to_pdf(images, pdf, subheading):
        x_margin = 10
        y_margin = 10
        image_size = (pdf.w - 2 * x_margin)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, subheading, 0, 1, 'L')
        pdf.ln(10)

        num_images = len(images)
        for i, image_file in enumerate(images):
            image_path = os.path.join(folder_path, image_file)
            img = Image.open(image_path)
            width = min(image_size, img.width * 0.75)  
            height = (img.height / img.width) * width

            if pdf.get_y() + height + y_margin > pdf.h - y_margin:
                pdf.add_page()

            x = (pdf.w - width) / 2
            pdf.image(image_path, x, pdf.get_y(), width, height)
            pdf.ln(height + y_margin)

    for folder, subheading in folder_titles.items():
        current_directory = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(current_directory, folder)
        images = [img for img in os.listdir(folder_path) if img.endswith('.png')]

        if images:
            add_images_to_pdf(images, pdf, subheading)
        else:
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, subheading, 0, 1, 'L')
            pdf.ln(10)
            pdf.set_font("Arial", 'I', 12)
            pdf.cell(0, 10, "No data found", 0, 1, 'C')

    output_dir = os.path.join(current_directory, "Output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    pdf_output = f'{name}.pdf'
    file_save = os.path.join(output_dir, pdf_output)
    pdf.output(file_save)
    print(f"PDF created: {file_save}")


def img_remover(folder_titles):
    current_directory = os.path.dirname(os.path.abspath(__file__))

    for folder in folder_titles.keys():
        folder_path = os.path.join(current_directory, folder)
        
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            image_extensions = ('.png')

            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                
                if os.path.isfile(file_path) and file_path.lower().endswith(image_extensions):
                    os.remove(file_path)
                    print(f"Removed: {file_path}")

def spy(u, p):
    folder = "IProfileSS"
    global username
    username = u
    password = p

    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)

    username_input = driver.find_element(By.NAME, "username")
    username_input.send_keys(username)

    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)

    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

    try:
        driver.get(f"https://www.instagram.com/{username}/")
        time.sleep(3)
        capture_screenshot(driver, folder,'profile.png')
        get_followers_following(driver,username)
    except Exception as e:
        print(f"An error occurred while handling profile, followers, or following: {e}")

    time.sleep(3)

    get_posts(driver, username)
    time.sleep(3)

    get_messages(driver)

    driver.quit()

    name = username
    title = username
    folder_titles = {
    'IProfileSS': 'Profile Information :',
    'IFwingSS': 'Followings List : ',
    'IFwerSS': 'Followers List : ',
    'IPostSS': 'Posts : ',
    'IMessSS': 'Messages : '
    }
    create_pdf_from_screenshots(name,title,folder_titles)
    img_remover(folder_titles)

def main():
    spy("ABC", "123")

if __name__ == "__main__":
    main()