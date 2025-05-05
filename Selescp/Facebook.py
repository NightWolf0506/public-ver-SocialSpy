from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import os
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


username = "adarshayush1128@gmail.com"
password = "MightGuy@8"
pin="123456"
options=webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=options)
driver.maximize_window()

driver.get("https://www.facebook.com/login.php/")
time.sleep(3)

username_input = driver.find_element(By.NAME, "email")
username_input.send_keys(username)

password_input = driver.find_element(By.NAME, "pass")
password_input.send_keys(password)
element=driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
element.click()

time.sleep(5)

print("Login Done!")

folders = ["FbPosts", "FbMessages", "FbProfile","FbFriends"]
current_directory = os.path.dirname(os.path.abspath(__file__))
for i,folder in enumerate(folders):
    file_path = os.path.join(current_directory, folder)
    folders[i] = file_path
    if not os.path.exists(file_path):
        os.makedirs(file_path)

driver.get("https://www.facebook.com/me/")
time.sleep(5)


def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  


def capture_posts():
    driver.get("https://www.facebook.com/me/")
    time.sleep(3) 
    attempt=0
    last_height = driver.execute_script("return document.body.scrollHeight")
    K=True

  
    try:
        # driver.execute_script("document.body.style.transform = 'scale(0.70)';")
        # driver.execute_script("document.body.style.transformOrigin = '0 0';")
        child_element = driver.find_elements(By.XPATH, '//div[contains(@class, "x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")]')


        if child_element:  # If the element is found
            print("Child element found. Finding grandparent div.")
            
            # Find the grandparent div using XPath
            div = driver.find_element(By.XPATH, '(//div[contains(@class, "x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")])')
            grandparent_div = div.find_element(By.XPATH, '//div[@class="x1yztbdb"]/following-sibling::div[1]')
            #grandparent_div = div.find_element(By.XPATH, '..//..')
            
            
            # Now you can interact with the grandparent div
            print("Grandparent div found.")

            while K:
                try:
                    # Locate the container where the posts are located using the provided XPath
                    post_container = grandparent_div
                    
                    # Find all child divs that represent posts
                    posts = post_container.find_elements(By.XPATH, './div')  # Assuming each post is a direct child div

                    print(f"Attempting to load more post")
                    if attempt>2:
                        print(f"Total posts found: {len(posts)-1}")
                        for index in range(len(posts)-1):
                            try:
                                # Refresh the list of posts each time
                                posts = post_container.find_elements(By.XPATH, './div') 
                                post = posts[index]

                                driver.execute_script("arguments[0].scrollIntoView(true);", post)
                                time.sleep(0.5)
                                
                                #Hide the overlay if needed
                                overlay = driver.find_element(By.XPATH, '//div[@class="x9f619 x1ja2u2z x1xzczws x7wzq59"]')
                                driver.execute_script("arguments[0].style.display = 'none';", overlay)
                                overlay = driver.find_element(By.XPATH, '//div[@class="xds687c x17qophe xixxii4 x13vifvy x1vjfegm"]')
                                driver.execute_script("arguments[0].style.display = 'none';", overlay)
                    
                                post_height = post.size['height']
                                post_width = post.size['width']

                                window_height = driver.execute_script("return window.innerHeight")
                                window_width = driver.execute_script("return window.innerWidth")

                                # Zoom out if the post is larger than the viewport
                                # if post_height > window_height or post_width > window_width:
                                #     driver.execute_script("document.body.style.transform = 'scale(0.75)';")
                                #     driver.execute_script("document.body.style.transformOrigin = '0 0';")
                                #     time.sleep(0.5)

                                # Capture the screenshot of the post
                                post.screenshot(f"{folders[0]}\\Post_{index + 1}.png")
                                
                                # Reset the zoom after the screenshot
                                driver.execute_script("document.body.style.transform = 'scale(1)';")

                                print(f"Captured Post {index + 1}")
                                time.sleep(1)


                            
                            except Exception as e:
                                print(f"Error capturing Post {index + 1}: {e}")
                                K=False
                                break
                        K=False
                        break

                    
                    current_height = driver.execute_script("return window.scrollY")
                    target_height = last_height

                    # Smooth scrolling
                    for i in range(current_height, target_height, 100):  # Scroll in increments of 100 pixels
                        driver.execute_script(f"window.scrollTo(0, {i});")
                        time.sleep(0.1)  # Wait for a short moment to allow content to load

                    # time.sleep(1.5)
                    print("hmmmm")

                    new_height = driver.execute_script("return document.body.scrollHeight")
                
                    if new_height == last_height:
                        print("Reached the bottom of the page.")
                        time.sleep(1.5)
                        attempt+=1
                        

                    last_height = new_height

                except Exception as e:
                    print(f"Error capturing posts: {e}")
                    break
    except:
        K=False
        print("No Post Found")

    

def capture_message_screenshots():
    driver.get("https://www.facebook.com/messages/t/")
    time.sleep(3)

    try:
        # Check if the PIN dialog box is present
        pin_dialog = driver.find_elements(By.XPATH, '//div[@class="x1n2onr6 x1ja2u2z x1afcbsf x78zum5 xdt5ytf x1a2a7pz x6ikm8r x10wlt62 x71s49j x1jx94hy x1qpq9i9 xdney7k xu5ydu1 xt3gfkd x104qc98 x1g2kw80 x16n5opg xl7ujzl xhkep3z x1n7qst7 xh8yej3"]')

        # If the dialog exists, handle the PIN entry
        if pin_dialog:
            print("PIN dialog detected. Entering PIN...")
            while True:
                # Locate the PIN input field
                pin_input = driver.find_elements(By.XPATH, '//input[@id="mw-numeric-code-input-prevent-composer-focus-steal"]')
                
                if pin_input:
                    # Assuming the PIN is obtained or prompted from the user
                    pin_code = pin  # You can change this to a predefined PIN if applicable
                    
                    # Enter the PIN into the input field
                    pin_input[0].send_keys(pin_code)

                    # Locate and click the submit button (update the XPath according to the actual structure)

                    # Wait for the dialog to disappear (adjust the time as needed)
                    time.sleep(5)
                    
                    # Check if the dialog is still present
                    # pin_dialog = driver.find_elements(By.XPATH, '//div[@class="x1n2onr6"]')
                    # if not pin_dialog:
                    #     print("PIN dialog closed. Proceeding to messages.")
                    #     break
                    print("pin entered")
                    break
                else:
                    print("PIN input field not found.")
                    break
        else:
            print("No PIN dialog detected. Proceeding to messages.")


        try:
            driver.get("https://www.facebook.com/messages/t/")
            time.sleep(3)
            messages_container = driver.find_element(By.XPATH, '//div[@aria-label="Chats"]//div[@class="x1n2onr6"]')
            print(1)
        
            message_recipients = messages_container.find_elements(By.XPATH, './div')  

            # extra_div_xpath = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div/div/div[5]/div/div/div/div/div/div/div[2]/div/div[3]' 
            print(2) # Adjust this XPath according to your layout
            # extra_div = messages_container.find_element(By.XPATH, extra_div_xpath)
            # message_recipients.remove(extra_div)
            print(f"Total message recipients found: {len(message_recipients)}")
            
            for index in range(len(message_recipients)):
                try:

                    message_recipients = messages_container.find_elements(By.XPATH, './div') 
                    recipient = message_recipients[index]

                    driver.execute_script("arguments[0].scrollIntoView(true);", recipient)

                    time.sleep(2.5)

                    driver.save_screenshot(f"{folders[1]}\\Message_{index + 1}.png")
                    print(f"Captured Message for Recipient {index + 1}")
                    if index+1<len(message_recipients)-1:
                        recipientnext = message_recipients[index+1]
                        recipientnext.click()
                        print("Click kiya next par")
                    else:
                        break


                except Exception as e:
                    print(f"Error capturing message for Recipient {index + 1}: {e}")
                    break  

        except Exception as e:
            print(f"Error capturing message recipients: {e}")
    except:
        print("NO")





def capture_cropped_profile_screenshot():
    from selenium.webdriver.support import expected_conditions as EC
    try:
        
        div = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="x6s0dn4 x78zum5 xvrxa7q x9w375v xxfedj9 x1roke11 x1es02x0"]'))
        )
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        # driver.execute_script("arguments[0].scrollIntoView(true);", div)
        # time.sleep(1)  

        # location = div.location
        # size = div.size

        driver.save_screenshot(f'{folders[2]}\\PF.png')

    except Exception as e:
        print(f"Error capturing cropped profile screenshot: {e}")


def friend_ss():
    driver.get("https://www.facebook.com/me/")
    time.sleep(3)
    friend_names=[]
    try:
        gradual_scroll(driver, target_position=300, duration=1.5)
        time.sleep(1)
        friends_tab = driver.find_element(By.XPATH, '//a[contains(@class, "x1i10hfl") and contains(@href, "sk=friends")]')
        driver.execute_script("arguments[0].scrollIntoView(true);", friends_tab)
        driver.execute_script("arguments[0].click();", friends_tab)

        banner = driver.find_element(By.XPATH, '//div[@role="banner"]')
        driver.execute_script("arguments[0].style.display = 'none';", banner)
        time.sleep(3)
  
        div = driver.find_element(By.XPATH, '//div[contains(@class,"x1n2onr6 x1ja2u2z x1jx94hy x1qpq9i9 xdney7k xu5ydu1 xt3gfkd x9f619 xh8yej3 x6ikm8r x10wlt62 xquyuld")]//div[contains(@class, "x78zum5 x1q0g3np x1a02dak x1qughib")]')
        posts = div.find_elements(By.XPATH, './div')  
        
        print(f"Total posts found: {len(posts)}")
        old=0
        index=0

        while True:
            try:

                posts = div.find_elements(By.XPATH, './div')
                new=len(posts)
                
                # print(f"Total posts found: {len(posts)}")
                if old==new and index==new-1:
                    break
                post = posts[index]

                driver.execute_script("arguments[0].scrollIntoView(true);", post)
                #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # time.sleep(0.5)  
                
                overlay = driver.find_element(By.XPATH, '//div[@class="x9f619 x1ja2u2z x1xzczws x7wzq59"]')
                driver.execute_script("arguments[0].style.display = 'none';", overlay)
                overlay = driver.find_element(By.XPATH, '//div[@class="xds687c x17qophe xixxii4 x13vifvy x1vjfegm"]')
                driver.execute_script("arguments[0].style.display = 'none';", overlay)

                # Capture the screenshot of the post
                #post.screenshot(f"{folders[3]}\\Friend_{index + 1}.png")
                friend_name_element = post.find_element(By.XPATH, './/span[@dir="auto"]')
                friend_name = friend_name_element.text
                friend_names.append(friend_name)

                print(f"Captured Friend: {friend_name}")
                print(f"Captured Friend {index + 1}")
                # time.sleep(1)
                index+=1
                old=new

            except Exception as e:
                print(f"Error capturing Friend {index + 1}: {e}")
                break
        print(friend_names)

        return friend_names
        
    except Exception as e:
        print(f'Error while processing friend list: {e}')




def click_element_with_retry(driver, xpath, retries=3):
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            driver.execute_script("arguments[0].click();", element)
            return
        except StaleElementReferenceException:
            print(f"StaleElementReferenceException on attempt {attempt + 1}. Retrying...")
    print("Failed to click the element after multiple attempts.")

def gradual_scroll(driver, target_position, duration=1.0):
    """
    Gradually scrolls the window to a target position.

    :param driver: Selenium WebDriver instance.
    :param target_position: The target scroll position in pixels.
    :param duration: Duration over which to perform the scroll in seconds.
    """
    start_position = driver.execute_script("return window.pageYOffset;")  # Current scroll position
    distance = target_position - start_position
    steps = 30  # Number of scroll steps
    scroll_step = distance / steps
    pause_time = duration / steps  # Time to wait between scroll steps

    for _ in range(steps):
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        time.sleep(pause_time)

def about_ss():
    driver.get("https://www.facebook.com/me/")
    time.sleep(3)

    try:
        gradual_scroll(driver, target_position=300, duration=2.5)
        time.sleep(2)
        # Click on the "About" tab
        about_tab_xpath = "//div[contains(@class, 'x9f619 x1ja2u2z x1xzczws x7wzq59')]//a[contains(@class, 'x1i10hfl') and contains(@href, 'sk=about')]"
        click_element_with_retry(driver, about_tab_xpath)
        print("Clicked on About tab.")
        overlay = driver.find_element(By.XPATH, '//div[@class="x9f619 x1ja2u2z x1xzczws x7wzq59"]')
        driver.execute_script("arguments[0].style.display = 'none';", overlay)
        overlay = driver.find_element(By.XPATH, '//div[@class="xds687c x17qophe xixxii4 x13vifvy x1vjfegm"]')
        driver.execute_script("arguments[0].style.display = 'none';", overlay)
        banner = driver.find_element(By.XPATH, '//div[@role="banner"]')
        driver.execute_script("arguments[0].style.display = 'none';", banner)
        
        time.sleep(3)  # Wait for the About section to load

        # Take screenshot of the initial overview div class "x1iyjqo2"
        target_div_xpath = '//div[contains(@class,"x78zum5 x19xhxss")]//div[contains(@class, "x1iyjqo2")]'
        target_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, target_div_xpath)))

        # Scroll to the div to make it visible and take a screenshot
        driver.execute_script("arguments[0].scrollIntoView(true);", target_div)
        time.sleep(1)
        target_div.screenshot('overview_div_screenshot.png')
        print("Screenshot taken successfully!")

        list_about_types = ["about_work_and_education", "about_places", "about_contact_and_basic_info", 
                            "about_family_and_relationships", "about_details", "about_life_events"]

        for i in list_about_types:
            work_xpath = f"//div[contains(@class, 'x9f619 xyamay9 xsyo7zv x1l90r2v x16hj40l x16jcvb6 x15k2jg5 x1dg0hrn x1vcm9qs xnbfqra x1fqxu61 xpxhm9j xkcp7i7')]//a[contains(@class, 'x1i10hfl') and contains(@href, 'sk={i}')]"
            click_element_with_retry(driver, work_xpath)
            time.sleep(2)

            # Re-locate the target_div after navigation
            target_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, target_div_xpath)))

            # Scroll to the div and take a screenshot
            driver.execute_script("arguments[0].scrollIntoView(true);", target_div)
            time.sleep(1)
            target_div.screenshot(f'{folders[2]}/{i}_screenshot.png')
            print(f"Screenshot for {i} taken successfully!")

    except Exception as e:
        print(f"Error while processing About section: {e}")

#2. Capture all posts
capture_cropped_profile_screenshot()
print("Profile Done")
time.sleep(2)
about_ss()
print("About Done")
time.sleep(2)
friend_ss()
print("Friend Done")
time.sleep(2)
capture_posts()
print("Post Done")
time.sleep(2)
capture_message_screenshots()
print("ScreenShot Done")


driver.quit()
