# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from PIL import Image
# from fpdf import FPDF
# import time
# from time import sleep
# import os
# import pytesseract
# import cv2
# import google.generativeai as genai
# from selenium.webdriver.chrome.options import Options


# def extract_text(image_path):
#     try:
#         image = cv2.imread(image_path)
#         TEXT_THRESHOLD = 5
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         ret, thresh = cv2.threshold(gray, TEXT_THRESHOLD, 255, cv2.THRESH_BINARY_INV)
        
#         mask = cv2.bitwise_not(thresh)
#         occlusion_mask = cv2.dilate(mask, None, iterations=2)
#         occluded_image = cv2.bitwise_and(gray, gray, mask=occlusion_mask)
#         text = pytesseract.image_to_string(Image.fromarray(occluded_image))
#         return text
#     except Exception as e:
#         print(f"Error extracting text: {e}")
#         return ""

# def clean_text(text, words_to_remove):
#     words_to_remove = [word.lower() for word in words_to_remove]
#     cleaned_words = [word for word in text.split() if word.lower() not in words_to_remove]
#     return ' '.join(cleaned_words)

# def summery(ch):
#     full_text = ""
#     words_to_remove = ['Comments', 'Start' ,'conversation', 'Home','Search','Explore','Reels','Messages','Notifications','Create','Profile','More',]
#     if(ch==1):
#         folder_titles = [
#                 'IPostSS',
#                 'IMessSS'
#                 ]
#     if(ch==2):
#         folder_titles = [
#                 'FbPosts',
#                 'FbMessages'
#                 ]
#     if(ch==3):
#         folder_titles = [
#                 'XPosts',
#                 'XMessages'
#                 ]
#     if(ch==4):
#         folder_titles = [
#                 'Mails',
#                 ]

#     for folder in folder_titles:
#         current_directory = os.path.dirname(os.path.abspath(__file__))
#         folder_path = os.path.join(current_directory, folder)
#         images = [img for img in os.listdir(folder_path) if img.endswith('.png')]

#         def add_images_to_pdf(images):
#             nonlocal full_text
#             for i,image_file in enumerate(images):
#                 image_path = os.path.join(folder_path, image_file)
#                 t = extract_text(image_path).lower()
#                 full_text += t + "\n"

#         if images:
#             add_images_to_pdf(images)

#     current_directory = os.path.dirname(os.path.abspath(__file__))
#     parse_file_path = os.path.join(current_directory, 'parse.txt')

#     with open(parse_file_path, 'w') as f:
#         f.write(full_text)

#     with open(parse_file_path, 'r') as f:
#         file_content = f.read()

#     cleaned_text = clean_text(file_content, words_to_remove)
    
#     return cleaned_text

# def generate_sum(text):

#     GOOGLE_API_KEY='env'
#     genai.configure(api_key=GOOGLE_API_KEY)
#     pass_text = text
#     if(text!=""):
#         model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

#         try:
#             response = model.generate_content([pass_text, 
#                                                 '''Generate overall summary for the person based on these texts in its posts and messages.''' 
#                                             ])
            
#             info = response.text 

#             return info

#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return None
#     else:
#         return ""

# def capture_screenshot(driver,folder ,filename):
#     current_directory = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(current_directory, folder)
#     if not os.path.exists(file_path):
#         os.makedirs(file_path)
#     file_save = os.path.join(file_path, filename)
#     driver.save_screenshot(file_save)
#     print(f"Screenshot saved as {filename}")
#     yield f"Screenshot saved as {filename}"

    
# def get_posts(driver, username):
#     folder = "IPostSS"
#     driver.get(f"https://www.instagram.com/{username}/")
#     time.sleep(3)

#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(3)

#     post_links = []
#     reel_links = []
#     posts = driver.find_elements(By.XPATH, '//div//a[contains(@href, "/p/") or contains(@href, "/reel/")]')

#     for post in posts[:100]:
#         try:
#             post_link = post.get_attribute('href')
#             if "/p/" in post_link:
#                 post_links.append(post_link)
#             else:
#                 reel_links.append(post_link)
#         except Exception as e:
#             print(f"An error occurred while retrieving post link: {e}")

#     for i, post_link in enumerate(post_links):
#         try:
#             driver.get(post_link)
#             time.sleep(3)
#             capture_screenshot(driver,folder,f'post_{i}.png')
#             print(f"Screenshot for post {i} taken.")
#             yield f"Screenshot for post {i} taken."
#         except Exception as e:
#             print(f"An error occurred for post {i}: {e}")
#     return reel_links

# def get_followers_following(driver, username):
#     li = []
#     li2 = []
#     sug = []
#     count = []
    
#     driver.get(f"https://www.instagram.com/{username}/")
#     time.sleep(3)

#     ele = driver.find_elements(By.XPATH, "//span[contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'xexx8yu') and contains(@class, 'x4uap5') and contains(@class, 'x18d9i69') and contains(@class, 'xkhd6sd') and contains(@class, 'x1hl2dhg') and contains(@class, 'x16tdsg8') and contains(@class, 'x1vvkbs')]")
#     time.sleep(3)
    
#     try:
#         followers_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/followers/")]'))
#         )
#         followers_button.click()
#         time.sleep(3)
#         elements = driver.find_elements(By.XPATH, "//span[contains(@class, '_ap3a') and contains(@class, '_aaco') and contains(@class, '_aacw') and contains(@class, '_aacx') and contains(@class, '_aad7') and contains(@class, '_aade')]")

#         for element in elements:
#             t = element.text
#             li.append(t)
#         for e in ele:
#             t = int(e.text)
#             count.append(t)
#         sug = li[count[1]::]
#         li = li[0:count[1]]
        
#     except Exception as e:
#         print(f"An error occurred while handling followers: {e}")
    

#     try:
#         driver.get(f"https://www.instagram.com/{username}/")
#         following_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/following/")]'))
#         )
#         following_button.click()
#         time.sleep(3)

#         elements = driver.find_elements(By.XPATH, "//span[contains(@class, '_ap3a') and contains(@class, '_aaco') and contains(@class, '_aacw') and contains(@class, '_aacx') and contains(@class, '_aad7') and contains(@class, '_aade')]")

#         for element in elements:
#             t = element.text
#             li2.append(t)
#         li2 = li2[0:count[2]]

#     except Exception as e:
#         print(f"An error occurred while handling following: {e}")

#     return li,li2,sug

# def get_messages(driver):
#     folder = "IMessSS"
#     message_url = 'https://www.instagram.com/direct/inbox/'
#     driver.get(message_url)
    

#     try:
#         not_now_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))
#         )
#         not_now_button.click()
#     except Exception as e:
#         print(f"No 'Turn on Notifications' popup found: {e}")

#     message_links = set()
#     time.sleep(3)

#     try:
#         scrollable_panel = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//div[@role="region" and contains(@class, "scrollable")]'))
#         )
#         scrollable = True
#     except TimeoutException:
#         print("Scrollable panel not found. Proceeding without scrolling.")
#         yield "Scrollable panel not found. Proceeding without scrolling."
#         scrollable = False

#     if scrollable:
#         last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_panel)

#         while True:
#             try:
#                 driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_panel)
#                 time.sleep(5)

#             except Exception as e:
#                 print(f"An error occurred while scrolling or finding messages: {e}")
#                 break

#     for i, message in enumerate(driver.find_elements(By.XPATH, '//div[@role="listitem"]')):
#         try:
#             message.click()
#             time.sleep(5)
#             capture_screenshot(driver, folder, f'message_{i}.png')
#             message_url = 'https://www.instagram.com/direct/inbox/'
#             time.sleep(3) 
#         except Exception as e:
#             print(f"An error occurred for message {i}: {e}")


# def create_pdf_from_screenshots(name, pdf_title, folder_titles,fn_list,fr_list,fr_sug,summ,links):
#     check = 0
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", 'B', 18)
#     pdf.cell(0, 10, pdf_title, 0, 1, 'C')

#     def add_images_to_pdf(images, pdf, subheading):
#         x_margin = 10
#         y_margin = 10
#         image_size = (pdf.w - 2 * x_margin)
        
#         pdf.ln(10)
#         pdf.set_font("Arial", 'B', 14)
#         pdf.cell(0, 10, subheading, 0, 1, 'L')
#         pdf.ln(10)

#         for i, image_file in enumerate(images):
#             image_path = os.path.join(folder_path, image_file)
#             img = Image.open(image_path)
#             width = min(image_size, img.width * 0.75)  
#             height = (img.height / img.width) * width

#             if pdf.get_y() + height + y_margin > pdf.h - y_margin:
#                 pdf.add_page()

#             x = (pdf.w - width) / 2
#             pdf.image(image_path, x, pdf.get_y(), width, height)
#             pdf.ln(height + y_margin)
#         pdf.ln(10)

#     for folder, subheading in folder_titles.items():
#         current_directory = os.path.dirname(os.path.abspath(__file__))
#         folder_path = os.path.join(current_directory, folder)
#         images = [img for img in os.listdir(folder_path) if img.endswith('.png')]
        
#         if images:
#             add_images_to_pdf(images, pdf, subheading)
#             if(len(links)!=0) and subheading == "Posts : ":
#                 pdf.set_font("Arial", size=12)
#                 data2 = links
#                 pdf.ln(5)
#                 sno_width = 20
#                 data_width = 150
#                 for i in range(0, 1):
#                     pdf.cell(sno_width, 10, "S no.", border=1, align='C')
#                     pdf.cell(data_width, 10, "Reels Link", border=1, align='C')
#                 pdf.ln()
#                 for i in range(0, len(data2), 1):
#                     pdf.cell(sno_width, 10, f"{i+1}.", border=1, align='C')  
#                     pdf.cell(data_width, 10, data2[i], border=1, align='C')  
#                     pdf.ln()

#         elif subheading == "Followings List : " and len(fn_list) !=0 :
#             # pdf.add_page()
#             pdf.set_font("Arial", 'B', 14)
#             pdf.cell(0, 10, subheading, 0, 1, 'L')
#             pdf.ln(5)
#             pdf.set_font("Arial", size=12)
#             data = fn_list
#             data2 = fr_sug

#             sno_width = 20
#             data_width = 75
#             if(len(fn_list)>1):
#                 for i in range(0, 2):
#                     pdf.cell(sno_width, 10, "S no.", border=1, align='C')
#                     pdf.cell(data_width, 10, "Username", border=1, align='C')
#                 pdf.ln()
#             else:
#                 for i in range(0, 1):
#                     pdf.cell(sno_width, 10, "S no.", border=1, align='C')
#                     pdf.cell(data_width, 10, "Username", border=1, align='C')
#                 pdf.ln()

#             for i in range(0, len(data), 2):
#                 pdf.cell(sno_width, 10, f"{i+1}.", border=1, align='C')  
#                 pdf.cell(data_width, 10, data[i], border=1, align='C')  
                
#                 if i+1 < len(data):
#                     pdf.cell(sno_width, 10, f"{i+2}.", border=1, align='C') 
#                     pdf.cell(data_width, 10, data[i+1], border=1, align='C') 

#                 pdf.ln()
#             if(len(fr_sug)!=0):
#                 pdf.ln(5)
#                 check = 1
#                 sno_width = 20
#                 data_width = 75
#                 for i in range(0, 2):
#                     pdf.cell(sno_width, 10, "S no.", border=1, align='C')
#                     pdf.cell(data_width, 10, "Suggested Connection", border=1, align='C')
#                 pdf.ln()
#                 for i in range(0, len(data2), 2):
#                     pdf.cell(sno_width, 10, f"{i+1}.", border=1, align='C')  
#                     pdf.cell(data_width, 10, data2[i], border=1, align='C')  
                    
#                     if i+1 < len(data2):
#                         pdf.cell(sno_width, 10, f"{i+2}.", border=1, align='C') 
#                         pdf.cell(data_width, 10, data2[i+1], border=1, align='C') 

#                     pdf.ln()

#         elif subheading == "Followers List : " and len(fr_list) != 0:
#             # pdf.add_page()
#             pdf.ln(10)
#             pdf.set_font("Arial", 'B', 14)
#             pdf.cell(0, 10, subheading, 0, 1, 'L')
#             pdf.ln(5)
#             pdf.set_font("Arial", size=12)
#             data = fr_list
#             data2 = fr_sug

#             sno_width = 20
#             data_width = 75
#             if(len(fr_list)>1):
#                 for i in range(0, 2):
#                     pdf.cell(sno_width, 10, "S no.", border=1, align='C')
#                     pdf.cell(data_width, 10, "Username", border=1, align='C')
#                 pdf.ln()
#             else:
#                 for i in range(0, 1):
#                     pdf.cell(sno_width, 10, "S no.", border=1, align='C')
#                     pdf.cell(data_width, 10, "Username", border=1, align='C')
#                 pdf.ln()

#             for i in range(0, len(data), 2):
#                 pdf.cell(sno_width, 10, f"{i+1}.", border=1, align='C')  
#                 pdf.cell(data_width, 10, data[i], border=1, align='C')  
                
#                 if i+1 < len(data):
#                     pdf.cell(sno_width, 10, f"{i+2}.", border=1, align='C') 
#                     pdf.cell(data_width, 10, data[i+1], border=1, align='C') 

#                 pdf.ln()
            
#             if(len(fr_sug)!=0) and check == 0:
#                 pdf.ln(5)
#                 sno_width = 20
#                 data_width = 75
#                 for i in range(0, 2):
#                     pdf.cell(sno_width, 10, "S no.", border=1, align='C')
#                     pdf.cell(data_width, 10, "Suggested Connection", border=1, align='C')
#                 pdf.ln()
#                 for i in range(0, len(data2), 2):
#                     pdf.cell(sno_width, 10, f"{i+1}.", border=1, align='C')  
#                     pdf.cell(data_width, 10, data2[i], border=1, align='C')  
                    
#                     if i+1 < len(data2):
#                         pdf.cell(sno_width, 10, f"{i+2}.", border=1, align='C') 
#                         pdf.cell(data_width, 10, data2[i+1], border=1, align='C') 

#                     pdf.ln()

#         elif subheading == "Summery : " and summ != "":
#             pdf.set_font("Arial", 'B', 14)
#             pdf.cell(0, 10, subheading, 0, 1, 'L')
#             pdf.ln(5)
#             pdf.set_font("Arial", size=12)
#             pdf.multi_cell(0, 10, summ)

#         else:
#             # pdf.add_page()
#             pdf.ln(10)
#             pdf.set_font("Arial", 'B', 14)
#             pdf.cell(0, 10, subheading, 0, 1, 'L')
#             pdf.ln(5)
#             pdf.set_font("Arial", 'I', 12)
#             pdf.cell(0, 10, "No data found", 0, 1, 'C')
#             pdf.ln(10)

#     output_dir = os.path.join(current_directory, "Output")
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
    
#     pdf_output = f'{name}.pdf'
#     file_save = os.path.join(output_dir, pdf_output)
#     pdf.output(file_save)
#     print(f"PDF created: {file_save}")
#     yield f"PDF created: {file_save}"
 
# def img_remover(folder_titles):
#     current_directory = os.path.dirname(os.path.abspath(__file__))

#     for folder in folder_titles.keys():
#         folder_path = os.path.join(current_directory, folder)
        
#         if os.path.exists(folder_path) and os.path.isdir(folder_path):
#             image_extensions = ('.png')

#             for filename in os.listdir(folder_path):
#                 file_path = os.path.join(folder_path, filename)
                
#                 if os.path.isfile(file_path) and file_path.lower().endswith(image_extensions):
#                     os.remove(file_path)
#                     print(f"Removed: {file_path}")
#                     yield f"Removed: {file_path}"

# def extract_text(image_path):
#     try:
#         image = cv2.imread(image_path)
#         TEXT_THRESHOLD = 5
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         ret, thresh = cv2.threshold(gray, TEXT_THRESHOLD, 255, cv2.THRESH_BINARY_INV)
        
#         mask = cv2.bitwise_not(thresh)
#         occlusion_mask = cv2.dilate(mask, None, iterations=2)
#         occluded_image = cv2.bitwise_and(gray, gray, mask=occlusion_mask)
#         text = pytesseract.image_to_string(Image.fromarray(occluded_image))
#         return text
#     except Exception as e:
#         print(f"Error extracting text: {e}")
#         return ""


# def parse(ch):
#     a  = input("Enter words , seprated value : ")
#     a = [b.strip() for b in a.split(",")]
#     if(ch==1):
#         folder_titles = [
#                 'IPostSS',
#                 'IMessSS'
#                 ]
#     if(ch==2):
#         folder_titles = [
#                 'FbPosts',
#                 'FbMessages'
#                 ]

#     for folder in folder_titles:
#         current_directory = os.path.dirname(os.path.abspath(__file__))
#         folder_path = os.path.join(current_directory, folder)
#         images = [img for img in os.listdir(folder_path) if img.endswith('.png')]

#         def add_images_to_pdf(images):
#             for image_file in images:
#                 check = 0
#                 image_path = os.path.join(folder_path, image_file)
#                 t = extract_text(image_path).lower()
#                 for b in a:
#                     if b in t:
#                         print("Found")
#                         check += 1
#             if check == 0:
#                 print("Not Found")
#                 os.remove(image_path)


#         if images:
#             add_images_to_pdf(images)
#         else:
#             print("Empty Folder")


# def perform_scraping(username, password):
#     try:
#         folder = "IProfileSS"

#         # Set Chrome options to run in headless mode
#         options = Options()
#         options.add_argument("--headless")  # Run in headless mode (without opening the window)
#         options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration (optional but recommended for headless)
#         options.add_argument("--window-size=1920x1080")  # Set window size (optional)

#         # driver = webdriver.Chrome()
#         # driver.maximize_window()

#         # Initialize Selenium WebDriver with headless mode
#         driver = webdriver.Chrome(options=options)

#         # Login to Instagram
#         yield "Logging in..."
#         driver.get("https://www.instagram.com/accounts/login/")
#         sleep(3)

#         username_input = driver.find_element(By.NAME, "username")
#         username_input.send_keys(username)

#         password_input = driver.find_element(By.NAME, "password")
#         password_input.send_keys(password)

#         password_input.send_keys(Keys.RETURN)
#         sleep(5)

#         # Start scraping
#         try:
#             yield "Navigating to profile page..."
#             driver.get(f"https://www.instagram.com/{username}/")
#             sleep(3)
#             capture_screenshot(driver, folder, 'profile.png')

#             yield "Fetching followers, following, and suggested followers..."
#             followers, following, sug_followers = get_followers_following(driver, username)
#             yield f"Followers: {followers}"
#             yield f"Following: {following}"
#             yield f"Suggested Followers: {sug_followers}"

#         except Exception as e:
#             yield f"Error during profile, followers, or following scraping: {e}"
#             return {"error": f"Error during profile, followers, or following scraping: {e}"}

#         sleep(3)

#         # Scrape posts and messages
#         try:
#             yield "Scraping posts..."
#             links = get_posts(driver, username)
#             yield f"Post Links: {links}"

#             sleep(3)

#             yield "Scraping messages..."
#             get_messages(driver)
#         except Exception as e:
#             yield f"Error during posts or messages scraping: {e}"
#             return {"error": f"Error during posts or messages scraping: {e}"}

#         # Generate summary
#         try:
#             yield "Generating summary..."
#             su = summery(1)
#             summ = generate_sum(su)
#             yield f"Summary: {summ}"
#         except Exception as e:
#             yield f"Error during summary generation: {e}"
#             return {"error": f"Error during summary generation: {e}"}

#         # Quit the WebDriver
#         yield "Scraping complete, quitting WebDriver..."
#         driver.quit()

#         # Generate the final PDF
#         try:
#             yield "Generating final PDF..."
#             name = f"{username}_Instagram_Report"
#             title = f"{username}'s Instagram Activity Report"
#             folder_titles = {
#                 'IProfileSS': 'Profile Information :',
#                 'IFwingSS': 'Followings List : ',
#                 'IFwerSS': 'Followers List : ',
#                 'IPostSS': 'Posts : ',
#                 'IMessSS': 'Messages : ',
#                 'Summery': 'Summery : '
#             }

#             for folder_name in folder_titles.keys():
#                 if not os.path.exists(folder_name):
#                     os.makedirs(folder_name)

#             create_pdf_from_screenshots(name, title, folder_titles, following, followers, sug_followers, summ, links)
#             img_remover(folder_titles)

#             yield "PDF generated successfully."
#             yield "Scraping complete!"
#             return {"success": True, "report": f"{name}.pdf"}

#         except Exception as e:
#             yield f"Error during PDF generation: {e}"
#             return {"error": f"Error during PDF generation: {e}"}

#     except Exception as e:
#         yield f"Unexpected error: {e}"
#         return {"error": f"Unexpected error: {e}"}


# # if __name__ == "__main__":
# #     main()






from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image
from fpdf import FPDF
import time
from time import sleep
import os
import pytesseract
import cv2
import google.generativeai as genai
from selenium.webdriver.chrome.options import Options



def extract_text(image_path):
    try:
        image = cv2.imread(image_path)
        TEXT_THRESHOLD = 5
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, TEXT_THRESHOLD, 255, cv2.THRESH_BINARY_INV)
        
        mask = cv2.bitwise_not(thresh)
        occlusion_mask = cv2.dilate(mask, None, iterations=2)
        occluded_image = cv2.bitwise_and(gray, gray, mask=occlusion_mask)
        text = pytesseract.image_to_string(Image.fromarray(occluded_image))
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

import os

def parse(text_to_parse, ch):
    """
    Parses the given text (comma-separated words) to search for occurrences in images from specified folders.
    
    :param text_to_parse: Comma-separated string of words to search for in the images
    :param ch: 1 for Instagram, 2 for Facebook (used to determine the folder titles)
    :return: A string containing the results of the search with the source of each match
    """
    # Split the input string into a list of words to search for
    search_words = [word.strip().lower() for word in text_to_parse.split(",")]

    # Set the folder titles based on the platform (Instagram or Facebook)
    if ch == 1:
        folder_titles = ['IPostSS', 'IMessSS']  # Instagram folders
    elif ch == 2:
        folder_titles = ['FbPosts', 'FbMessages']  # Facebook folders
    else:
        return "Invalid choice for platform."

    # Data structure to store results
    result_data = []

    # Process each folder
    for folder in folder_titles:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(current_directory, folder)

        # Get all images (PNG files) in the folder
        images = [img for img in os.listdir(folder_path) if img.endswith('.png')]

        # Function to check each image for matching text
        def add_images_to_pdf(images):
            for image_file in images:
                image_path = os.path.join(folder_path, image_file)
                extracted_text = extract_text(image_path).lower()
                found = False
                
                # Check if any search word is found in the extracted text
                for word in search_words:
                    if word in extracted_text:
                        found = True
                        result_data.append(f"Found '{word}' in {folder} -> {image_file}")

                # Only append if the word is found
                if not found:
                    continue

        # Process the images in the current folder
        if images:
            add_images_to_pdf(images)
        else:
            result_data.append(f"Empty Folder: {folder}")

    # Return the results as a formatted string
    return "\n".join(result_data)




def clean_text(text, words_to_remove):
    words_to_remove = [word.lower() for word in words_to_remove]
    cleaned_words = [word for word in text.split() if word.lower() not in words_to_remove]
    return ' '.join(cleaned_words)

def summery(ch):
    full_text = ""
    words_to_remove = ['Comments', 'Start' ,'conversation', 'Home','Search','Explore','Reels','Messages','Notifications','Create','Profile','More',]
    if(ch==1):
        folder_titles = [
                'IPostSS',
                'IMessSS'
                ]
    if(ch==2):
        folder_titles = [
                'FbPosts',
                'FbMessages'
                ]
    if(ch==3):
        folder_titles = [
                'XPosts',
                'XMessages'
                ]
    if(ch==4):
        folder_titles = [
                'Mails',
                ]

    for folder in folder_titles:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(current_directory, folder)
        images = [img for img in os.listdir(folder_path) if img.endswith('.png')]

        def add_images_to_pdf(images):
            nonlocal full_text
            for i,image_file in enumerate(images):
                image_path = os.path.join(folder_path, image_file)
                t = extract_text(image_path).lower()
                full_text += t + "\n"

        if images:
            add_images_to_pdf(images)

    current_directory = os.path.dirname(os.path.abspath(__file__))
    parse_file_path = os.path.join(current_directory, 'parse.txt')

    with open(parse_file_path, 'w') as f:
        f.write(full_text)

    with open(parse_file_path, 'r') as f:
        file_content = f.read()

    cleaned_text = clean_text(file_content, words_to_remove)
    
    return cleaned_text

def generate_sum(text):

    GOOGLE_API_KEY='env'
    genai.configure(api_key=GOOGLE_API_KEY)
    pass_text = text
    if(text!=""):
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

        try:
            response = model.generate_content([pass_text, 
                                                '''Generate overall summary for the person based on these texts in its posts and messages.''' 
                                            ])
            
            info = response.text 

            return info

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    else:
        return ""

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
    reel_links = []
    posts = driver.find_elements(By.XPATH, '//div//a[contains(@href, "/p/") or contains(@href, "/reel/")]')

    for post in posts[:100]:
        try:
            post_link = post.get_attribute('href')
            if "/p/" in post_link:
                post_links.append(post_link)
            else:
                reel_links.append(post_link)
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
    return reel_links

def get_followers_following(driver, username):
    li = []
    li2 = []
    sug = []
    count = []
    
    driver.get(f"https://www.instagram.com/{username}/")
    time.sleep(3)

    ele = driver.find_elements(By.XPATH, "//span[contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'xexx8yu') and contains(@class, 'x4uap5') and contains(@class, 'x18d9i69') and contains(@class, 'xkhd6sd') and contains(@class, 'x1hl2dhg') and contains(@class, 'x16tdsg8') and contains(@class, 'x1vvkbs')]")
    time.sleep(3)
    
    try:
        followers_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/followers/")]'))
        )
        followers_button.click()
        time.sleep(3)
        elements = driver.find_elements(By.XPATH, "//span[contains(@class, '_ap3a') and contains(@class, '_aaco') and contains(@class, '_aacw') and contains(@class, '_aacx') and contains(@class, '_aad7') and contains(@class, '_aade')]")

        for element in elements:
            t = element.text
            li.append(t)
        for e in ele:
            t = int(e.text)
            count.append(t)
        sug = li[count[1]::]
        li = li[0:count[1]]
        
    except Exception as e:
        print(f"An error occurred while handling followers: {e}")
    

    try:
        driver.get(f"https://www.instagram.com/{username}/")
        following_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/following/")]'))
        )
        following_button.click()
        time.sleep(3)

        elements = driver.find_elements(By.XPATH, "//span[contains(@class, '_ap3a') and contains(@class, '_aaco') and contains(@class, '_aacw') and contains(@class, '_aacx') and contains(@class, '_aad7') and contains(@class, '_aade')]")

        for element in elements:
            t = element.text
            li2.append(t)
        li2 = li2[0:count[2]]

    except Exception as e:
        print(f"An error occurred while handling following: {e}")

    return li,li2,sug

# def get_messages(driver):
#     folder = "IMessSS"
#     message_url = 'https://www.instagram.com/direct/inbox/'
#     driver.get(message_url)
    

#     try:
#         not_now_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))
#         )
#         not_now_button.click()
#     except Exception as e:
#         print(f"No 'Turn on Notifications' popup found: {e}")

#     message_links = set()
#     time.sleep(3)

#     try:
#         scrollable_panel = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//div[@role="region" and contains(@class, "scrollable")]'))
#         )
#         scrollable = True
#     except TimeoutException:
#         print("Scrollable panel not found. Proceeding without scrolling.")
#         scrollable = False

#     if scrollable:
#         last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_panel)

#         while True:
#             try:
#                 driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_panel)
#                 time.sleep(5)

#             except Exception as e:
#                 print(f"An error occurred while scrolling or finding messages: {e}")
#                 break

#     for i, message in enumerate(driver.find_elements(By.XPATH, '//div[@role="listitem"]')):
#         try:
#             message.click()
#             time.sleep(5)
#             capture_screenshot(driver, folder, f'message_{i}.png')
#             message_url = 'https://www.instagram.com/direct/inbox/'
#             time.sleep(3) 
#         except Exception as e:
#             print(f"An error occurred for message {i}: {e}")

def get_messages(driver):
    folder = "IMessSS"
    message_url = 'https://www.instagram.com/direct/inbox/'
    driver.get(message_url)
    yield "Navigating to messages page..."

    try:
        not_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))
        )
        not_now_button.click()
        yield "Clicked 'Not Now' button on notifications popup."
    except Exception as e:
        yield f"No 'Turn on Notifications' popup found: {e}"

    message_links = set()
    time.sleep(3)

    try:
        scrollable_panel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="region" and contains(@class, "scrollable")]'))
        )
        yield "Found the scrollable panel for messages."
        scrollable = True
    except TimeoutException:
        yield "Scrollable panel not found. Proceeding without scrolling."
        scrollable = False

    if scrollable:
        last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_panel)
        scroll_attempts = 0
        max_scroll_attempts = 10  # Set a maximum number of scroll attempts

        while scroll_attempts < max_scroll_attempts:
            try:
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_panel)
                time.sleep(5)
                yield f"Scrolling attempt {scroll_attempts + 1}..."

                # Check if we've reached the end of the scrollable panel
                new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_panel)
                if new_height == last_height:
                    yield "No more messages to scroll. Reached the end of the panel."
                    break

                last_height = new_height
                scroll_attempts += 1
            except Exception as e:
                yield f"Error during scrolling: {e}"
                break

        if scroll_attempts >= max_scroll_attempts:
            yield "Reached maximum scroll attempts. Stopping further scrolling."

    for i, message in enumerate(driver.find_elements(By.XPATH, '//div[@role="listitem"]')):
        try:
            message.click()
            yield f"Clicked on message {i}."
            time.sleep(5)
            capture_screenshot(driver, folder, f'message_{i}.png')
            yield f"Captured screenshot for message {i}."
            driver.get(message_url)  # Navigate back to the messages page
            time.sleep(3)
        except Exception as e:
            yield f"An error occurred for message {i}: {e}"



# def create_pdf_from_screenshots(name, pdf_title, folder_titles,fn_list,fr_list,fr_sug,summ,links):
#     check = 0
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", 'B', 18)
#     pdf.cell(0, 10, pdf_title, 0, 1, 'C')

#     def add_images_to_pdf(images, pdf, subheading):
#         x_margin = 10
#         y_margin = 10
#         image_size = (pdf.w - 2 * x_margin)
        
#         pdf.ln(10)
#         pdf.set_font("Arial", 'B', 14)
#         pdf.cell(0, 10, subheading, 0, 1, 'L')
#         pdf.ln(10)

#         for i, image_file in enumerate(images):
#             image_path = os.path.join(folder_path, image_file)
#             img = Image.open(image_path)
#             width = min(image_size, img.width * 0.75)  
#             height = (img.height / img.width) * width

#             if pdf.get_y() + height + y_margin > pdf.h - y_margin:
#                 pdf.add_page()

#             x = (pdf.w - width) / 2
#             pdf.image(image_path, x, pdf.get_y(), width, height)
#             pdf.ln(height + y_margin)
#         pdf.ln(10)

#     for folder, subheading in folder_titles.items():
#         current_directory = os.path.dirname(os.path.abspath(__file__))
#         folder_path = os.path.join(current_directory, folder)
#         images = [img for img in os.listdir(folder_path) if img.endswith('.png')]
        
#         if images:
#             add_images_to_pdf(images, pdf, subheading)
#             if(len(links)!=0) and subheading == "Posts : ":
#                 pdf.set_font("Arial", size=12)
#                 data2 = links
#                 pdf.ln(5)
#                 sno_width = 20
#                 data_width = 150
#                 for i in range(0, 1):
#                     pdf.cell(sno_width, 10, "S no.", border=1, align='C')
#                     pdf.cell(data_width, 10, "Reels Link", border=1, align='C')
#                 pdf.ln()
#                 for i in range(0, len(data2), 1):
#                     pdf.cell(sno_width, 10, f"{i+1}.", border=1, align='C')  
#                     pdf.cell(data_width, 10, data2[i], border=1, align='C')  
#                     pdf.ln()

#         elif subheading == "Followings List : " and len(fn_list) !=0 :
#             # pdf.add_page()
#             pdf.set_font("Arial", 'B', 14)
#             pdf.cell(0, 10, subheading, 0, 1, 'L')
#             pdf.ln(5)
#             pdf.set_font("Arial", size=12)
#             data = fn_list
#             data2 = fr_sug

#             sno_width = 20
#             data_width = 75
#             if(len(fn_list)>1):
#                 for i in range(0, 2):
#                     pdf.cell(sno_width, 10, "S no.", border=1, align='C')
#                     pdf.cell(data_width, 10, "Username", border=1, align='C')
#                 pdf.ln()
#             else:
#                 for i in range(0, 1):
#                     pdf.cell(sno_width, 10, "S no.", border=1, align='C')
#                     pdf.cell(data_width, 10, "Username", border=1, align='C')
#                 pdf.ln()

#             for i in range(0, len(data), 2):
#                 pdf.cell(sno_width, 10, f"{i+1}.", border=1, align='C')  
#                 pdf.cell(data_width, 10, data[i], border=1, align='C')  
                
#                 if i+1 < len(data):
#                     pdf.cell(sno_width, 10, f"{i+2}.", border=1, align='C') 
#                     pdf.cell(data_width, 10, data[i+1], border=1, align='C') 

#                 pdf.ln()
#             if(len(fr_sug)!=0):
#                 pdf.ln(5)
#                 check = 1
#                 sno_width = 20
#                 data_width = 75
#                 for i in range(0, 2):
#                     pdf.cell(sno_width, 10, "S no.", border=1, align='C')
#                     pdf.cell(data_width, 10, "Suggested Connection", border=1, align='C')
#                 pdf.ln()
#                 for i in range(0, len(data2), 2):
#                     pdf.cell(sno_width, 10, f"{i+1}.", border=1, align='C')  
#                     pdf.cell(data_width, 10, data2[i], border=1, align='C')  
                    
#                     if i+1 < len(data2):
#                         pdf.cell(sno_width, 10, f"{i+2}.", border=1, align='C') 
#                         pdf.cell(data_width, 10, data2[i+1], border=1, align='C') 

#                     pdf.ln()

#         elif subheading == "Followers List : " and len(fr_list) != 0:
#             # pdf.add_page()
#             pdf.ln(10)
#             pdf.set_font("Arial", 'B', 14)
#             pdf.cell(0, 10, subheading, 0, 1, 'L')
#             pdf.ln(5)
#             pdf.set_font("Arial", size=12)
#             data = fr_list
#             data2 = fr_sug

#             sno_width = 20
#             data_width = 75
#             if(len(fr_list)>1):
#                 for i in range(0, 2):
#                     pdf.cell(sno_width, 10, "S no.", border=1, align='C')
#                     pdf.cell(data_width, 10, "Username", border=1, align='C')
#                 pdf.ln()
#             else:
#                 for i in range(0, 1):
#                     pdf.cell(sno_width, 10, "S no.", border=1, align='C')
#                     pdf.cell(data_width, 10, "Username", border=1, align='C')
#                 pdf.ln()

#             for i in range(0, len(data), 2):
#                 pdf.cell(sno_width, 10, f"{i+1}.", border=1, align='C')  
#                 pdf.cell(data_width, 10, data[i], border=1, align='C')  
                
#                 if i+1 < len(data):
#                     pdf.cell(sno_width, 10, f"{i+2}.", border=1, align='C') 
#                     pdf.cell(data_width, 10, data[i+1], border=1, align='C') 

#                 pdf.ln()
            
#             if(len(fr_sug)!=0) and check == 0:
#                 pdf.ln(5)
#                 sno_width = 20
#                 data_width = 75
#                 for i in range(0, 2):
#                     pdf.cell(sno_width, 10, "S no.", border=1, align='C')
#                     pdf.cell(data_width, 10, "Suggested Connection", border=1, align='C')
#                 pdf.ln()
#                 for i in range(0, len(data2), 2):
#                     pdf.cell(sno_width, 10, f"{i+1}.", border=1, align='C')  
#                     pdf.cell(data_width, 10, data2[i], border=1, align='C')  
                    
#                     if i+1 < len(data2):
#                         pdf.cell(sno_width, 10, f"{i+2}.", border=1, align='C') 
#                         pdf.cell(data_width, 10, data2[i+1], border=1, align='C') 

#                     pdf.ln()

#         elif subheading == "Summery : " and summ != "":
#             pdf.set_font("Arial", 'B', 14)
#             pdf.cell(0, 10, subheading, 0, 1, 'L')
#             pdf.ln(5)
#             pdf.set_font("Arial", size=12)
#             pdf.multi_cell(0, 10, summ)

#         else:
#             # pdf.add_page()
#             pdf.ln(10)
#             pdf.set_font("Arial", 'B', 14)
#             pdf.cell(0, 10, subheading, 0, 1, 'L')
#             pdf.ln(5)
#             pdf.set_font("Arial", 'I', 12)
#             pdf.cell(0, 10, "No data found", 0, 1, 'C')
#             pdf.ln(10)

#     output_dir = os.path.join(current_directory, "Output")
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
    
#     pdf_output = f'{name}.pdf'
#     file_save = os.path.join(output_dir, pdf_output)
#     pdf.output(file_save)
#     print(f"PDF created: {file_save}")



import os
from fpdf import FPDF
from PIL import Image  # Ensure Pillow is installed for image handling

def create_pdf_from_screenshots(name, pdf_title, folder_titles, fn_list, fr_list, fr_sug, summ, links, result):
    check = 0
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 10, pdf_title, 0, 1, 'C')

    def add_images_to_pdf(images, pdf, subheading, folder_path):
        x_margin = 10
        y_margin = 10
        image_size = (pdf.w - 2 * x_margin)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, subheading, 0, 1, 'L')
        pdf.ln(10)

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
        pdf.ln(10)

    # Add the parsed results to the PDF under a "Parsed Results" section
    if result:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Parsed Results: ", 0, 1, 'L')
        pdf.ln(5)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, result)
        pdf.ln(10)

    # Iterate over folder_titles and images in the specified directories
    for folder, subheading in folder_titles.items():
        current_directory = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(current_directory, folder)
        images = [img for img in os.listdir(folder_path) if img.endswith('.png')]
        
        if images:
            add_images_to_pdf(images, pdf, subheading, folder_path)
            if len(links) != 0 and subheading == "Posts : ":
                pdf.set_font("Arial", size=12)
                data2 = links
                pdf.ln(5)
                sno_width = 20
                data_width = 150
                for i in range(0, 1):
                    pdf.cell(sno_width, 10, "S no.", border=1, align='C')
                    pdf.cell(data_width, 10, "Reels Link", border=1, align='C')
                pdf.ln()
                for i in range(0, len(data2), 1):
                    pdf.cell(sno_width, 10, f"{i+1}.", border=1, align='C')  
                    pdf.cell(data_width, 10, data2[i], border=1, align='C')  
                    pdf.ln()

        elif subheading == "Followings List : " and len(fn_list) != 0:
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, subheading, 0, 1, 'L')
            pdf.ln(5)
            pdf.set_font("Arial", size=12)
            data = fn_list
            data2 = fr_sug

            sno_width = 20
            data_width = 75
            if len(fn_list) > 1:
                for i in range(0, 2):
                    pdf.cell(sno_width, 10, "S no.", border=1, align='C')
                    pdf.cell(data_width, 10, "Username", border=1, align='C')
                pdf.ln()
            else:
                for i in range(0, 1):
                    pdf.cell(sno_width, 10, "S no.", border=1, align='C')
                    pdf.cell(data_width, 10, "Username", border=1, align='C')
                pdf.ln()

            for i in range(0, len(data), 2):
                pdf.cell(sno_width, 10, f"{i+1}.", border=1, align='C')  
                pdf.cell(data_width, 10, data[i], border=1, align='C')  
                
                if i+1 < len(data):
                    pdf.cell(sno_width, 10, f"{i+2}.", border=1, align='C') 
                    pdf.cell(data_width, 10, data[i+1], border=1, align='C') 

                pdf.ln()
            if len(fr_sug) != 0:
                pdf.ln(5)
                check = 1
                sno_width = 20
                data_width = 75
                for i in range(0, 2):
                    pdf.cell(sno_width, 10, "S no.", border=1, align='C')
                    pdf.cell(data_width, 10, "Suggested Connection", border=1, align='C')
                pdf.ln()
                for i in range(0, len(data2), 2):
                    pdf.cell(sno_width, 10, f"{i+1}.", border=1, align='C')  
                    pdf.cell(data_width, 10, data2[i], border=1, align='C')  
                    
                    if i+1 < len(data2):
                        pdf.cell(sno_width, 10, f"{i+2}.", border=1, align='C') 
                        pdf.cell(data_width, 10, data2[i+1], border=1, align='C') 

                    pdf.ln()

        elif subheading == "Followers List : " and len(fr_list) != 0:
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, subheading, 0, 1, 'L')
            pdf.ln(5)
            pdf.set_font("Arial", size=12)
            data = fr_list
            data2 = fr_sug

            sno_width = 20
            data_width = 75
            if len(fr_list) > 1:
                for i in range(0, 2):
                    pdf.cell(sno_width, 10, "S no.", border=1, align='C')
                    pdf.cell(data_width, 10, "Username", border=1, align='C')
                pdf.ln()
            else:
                for i in range(0, 1):
                    pdf.cell(sno_width, 10, "S no.", border=1, align='C')
                    pdf.cell(data_width, 10, "Username", border=1, align='C')
                pdf.ln()

            for i in range(0, len(data), 2):
                pdf.cell(sno_width, 10, f"{i+1}.", border=1, align='C')  
                pdf.cell(data_width, 10, data[i], border=1, align='C')  
                
                if i+1 < len(data):
                    pdf.cell(sno_width, 10, f"{i+2}.", border=1, align='C') 
                    pdf.cell(data_width, 10, data[i+1], border=1, align='C') 

                pdf.ln()
            
            if len(fr_sug) != 0 and check == 0:
                pdf.ln(5)
                sno_width = 20
                data_width = 75
                for i in range(0, 2):
                    pdf.cell(sno_width, 10, "S no.", border=1, align='C')
                    pdf.cell(data_width, 10, "Suggested Connection", border=1, align='C')
                pdf.ln()
                for i in range(0, len(data2), 2):
                    pdf.cell(sno_width, 10, f"{i+1}.", border=1, align='C')  
                    pdf.cell(data_width, 10, data2[i], border=1, align='C')  
                    
                    if i+1 < len(data2):
                        pdf.cell(sno_width, 10, f"{i+2}.", border=1, align='C') 
                        pdf.cell(data_width, 10, data2[i+1], border=1, align='C') 

                    pdf.ln()

        elif subheading == "Summery : " and summ != "":
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, subheading, 0, 1, 'L')
            pdf.ln(5)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, summ)

        else:
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, subheading, 0, 1, 'L')
            pdf.ln(5)
            pdf.set_font("Arial", 'I', 12)
            pdf.cell(0, 10, "No data found", 0, 1, 'C')
            pdf.ln(10)

    # Output directory for saving the PDF
    output_dir = os.path.join(current_directory, "Output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the PDF file path
    pdf_output = f'{name}.pdf'
    file_save = os.path.join(output_dir, pdf_output)

    # Save the PDF file to the Output directory
    pdf.output(file_save)
    print(f"PDF created: {file_save}")
    return file_save  # Optionally, return the path of the saved PDF file


 
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



# def parse(ch):
#     a  = input("Enter words , seprated value : ")
#     a = [b.strip() for b in a.split(",")]
#     if(ch==1):
#         folder_titles = [
#                 'IPostSS',
#                 'IMessSS'
#                 ]
#     if(ch==2):
#         folder_titles = [
#                 'FbPosts',
#                 'FbMessages'
#                 ]

#     for folder in folder_titles:
#         current_directory = os.path.dirname(os.path.abspath(__file__))
#         folder_path = os.path.join(current_directory, folder)
#         images = [img for img in os.listdir(folder_path) if img.endswith('.png')]

#         def add_images_to_pdf(images):
#             for image_file in images:
#                 check = 0
#                 image_path = os.path.join(folder_path, image_file)
#                 t = extract_text(image_path).lower()
#                 for b in a:
#                     if b in t:
#                         print("Found")
#                         check += 1
#             if check == 0:
#                 print("Not Found")
#                 os.remove(image_path)


#         if images:
#             add_images_to_pdf(images)
#         else:
#             print("Empty Folder")


# def perform_scraping(username, password):
#     try:
#         folder = "IProfileSS"

#         # Set Chrome options to run in headless mode
#         options = Options()
#         options.add_argument("--headless")  # Run in headless mode (without opening the window)
#         options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration (optional but recommended for headless)
#         options.add_argument("--window-size=1920x1080")  # Set window size (optional)

#         # driver = webdriver.Chrome()
#         # driver.maximize_window()

#         # Initialize Selenium WebDriver with headless mode
#         driver = webdriver.Chrome(options=options)

#         # Login to Instagram
#         yield "Logging in..."
#         driver.get("https://www.instagram.com/accounts/login/")
#         sleep(3)

#         username_input = driver.find_element(By.NAME, "username")
#         username_input.send_keys(username)

#         password_input = driver.find_element(By.NAME, "password")
#         password_input.send_keys(password)

#         password_input.send_keys(Keys.RETURN)
#         sleep(5)

#         # Start scraping
#         try:
#             yield "Navigating to profile page..."
#             driver.get(f"https://www.instagram.com/{username}/")
#             sleep(3)
#             capture_screenshot(driver, folder, 'profile.png')

#             yield "Fetching followers, following, and suggested followers..."
#             followers, following, sug_followers = get_followers_following(driver, username)
#             yield f"Followers: {followers}"
#             yield f"Following: {following}"
#             yield f"Suggested Followers: {sug_followers}"

#         except Exception as e:
#             yield f"Error during profile, followers, or following scraping: {e}"
#             return {"error": f"Error during profile, followers, or following scraping: {e}"}

#         sleep(3)

#         # Scrape posts and messages
#         try:
#             yield "Scraping posts..."
#             links = get_posts(driver, username)
#             yield f"Post Links: {links}"

#             sleep(3)

#             yield "Scraping messages..."
#             get_messages(driver)
#             yield "Scraping complete!"
#         except Exception as e:
#             yield f"Error during posts or messages scraping: {e}"
#             return {"error": f"Error during posts or messages scraping: {e}"}

#         if text:
#             parse(1, text)
#         # Generate summary
#         try:
#             yield "Generating summary..."
#             su = summery(1)
#             summ = generate_sum(su)
#             yield f"Summary: {summ}"
#         except Exception as e:
#             yield f"Error during summary generation: {e}"
#             return {"error": f"Error during summary generation: {e}"}

        
        
#         # Quit the WebDriver
#         yield "Scraping complete, quitting WebDriver..."
#         driver.quit()

#         # Generate the final PDF
#         try:
#             yield "Generating final PDF..."
#             name = f"{username}_Instagram_Report"
#             title = f"{username}'s Instagram Activity Report"
#             folder_titles = {
#                 'IProfileSS': 'Profile Information :',
#                 'IFwingSS': 'Followings List : ',
#                 'IFwerSS': 'Followers List : ',
#                 'IPostSS': 'Posts : ',
#                 'IMessSS': 'Messages : ',
#                 'Summery': 'Summery : '
#             }

#             for folder_name in folder_titles.keys():
#                 if not os.path.exists(folder_name):
#                     os.makedirs(folder_name)

#             create_pdf_from_screenshots(name, title, folder_titles, following, followers, sug_followers, summ, links)
#             img_remover(folder_titles)

#             yield "PDF generated successfully."
            
#             return {"success": True, "report": f"{name}.pdf"}

#         except Exception as e:
#             yield f"Error during PDF generation: {e}"
#             return {"error": f"Error during PDF generation: {e}"}

#     except Exception as e:
#         yield f"Unexpected error: {e}"
#         return {"error": f"Unexpected error: {e}"}
def perform_scraping(username, password):
    # driver = None  # Initialize driver as None to ensure a single instance

    try:
        folder = "IProfileSS"

        # Initialize WebDriver only once
        # options = webdriver.ChromeOptions()
        # options.add_argument("--disable-notifications")
        # driver = webdriver.Chrome(options=options)
        # driver.maximize_window()

        driver = webdriver.Chrome()
        driver.maximize_window()

        # Logging in
        yield "Logging in..."
        driver.get("https://www.instagram.com/accounts/login/")
        sleep(3)

        username_input = driver.find_element(By.NAME, "username")
        username_input.send_keys(username)

        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(password)

        password_input.send_keys(Keys.RETURN)
        sleep(5)

        # Scraping profile data
        yield "Navigating to profile page..."
        driver.get(f"https://www.instagram.com/{username}/")
        sleep(3)
        capture_screenshot(driver, folder, 'profile.png')

        yield "Fetching followers, following, and suggested followers..."
        followers, following, sug_followers = get_followers_following(driver, username)
        yield f"Followers: {len(followers)}"
        yield f"Following: {len(following)}"
        yield f"Suggested Followers: {len(sug_followers)}"

        sleep(3)

        # Scraping posts and messages
        yield "Scraping posts..."
        links = get_posts(driver, username)
        yield f"Post Links: {len(links)} links scraped"

        sleep(3)

        yield "Scraping messages..."
        message_results = get_messages(driver)
        for message_update in message_results:
            yield message_update
        
        yield "Scraping complete!"

    except Exception as e:
        yield f"Unexpected error: {e}"
    finally:
        # Ensure WebDriver is quit properly
        if driver:
            driver.quit()

        yield "Scraping complete, quitting WebDriver..."

def generate_summary_and_apply_filter(filter_enabled, filter_text, summary_enabled):
    summ = None
    result = None

    if summary_enabled:
        su = summery(1)  # Assuming summery() generates some initial summary data
        summ = generate_sum(su)  # Assuming generate_sum() processes the summary
        
        if isinstance(summ, str):  # Ensure it's not a string, it should be a dict or object
            raise ValueError(f"Unexpected type for summary: {type(summ)}. Expected a dict.")

    if filter_enabled and filter_text:
        result = parse(filter_text, 1)  # Assuming parse() applies the filter using filter_text
        
        if isinstance(result, str):  # Ensure it's not a string, it should be a dict or object
            raise ValueError(f"Unexpected type for result: {type(result)}. Expected a dict.")

    return summ, result


# Function consuming realized data instead of generator
def generate_pdf(username, summ=None, result=None):
    try:
        # Validate types
        if isinstance(summ, str):
            raise ValueError(f"Expected a dictionary for 'summ', but got a string: {summ}")
        if isinstance(result, str):
            raise ValueError(f"Expected a dictionary for 'result', but got a string: {result}")

        # Generate the PDF
        folder_titles = {
            'IProfileSS': 'Profile Information :',
            'IFwingSS': 'Followings List :',
            'IFwerSS': 'Followers List :',
            'IPostSS': 'Posts :',
            'IMessSS': 'Messages :',
            'Summery': f'Summary : {summ if summ else "(Empty)"}'
        }

        create_pdf_from_screenshots(
            f"{username}_Instagram_Report", 
            f"{username}'s Instagram Activity Report",
            folder_titles, following, followers, suggested_followers, summ, result
        )

        yield "PDF generated successfully."
        return {"success": True, "report": f"{username}_Instagram_Report.pdf"}

    except Exception as e:
        yield f"Error during PDF generation: {e}"
        return {"error": f"Error during PDF generation: {e}"}


# perform_scraping(username, password)

# if __name__ == "__main__":
#     main()
