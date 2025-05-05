import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Credentials
email = "dummytweet12@outlook.com"
username = "sahay_soum28529"
password = "DuMM!123"

'''
email = "dummytweet123@gmail.com"
username = "dummyTweet123"
password = "DuMm!123"
'''

#Start Browser
options=webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=options)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

#Open Login Page
driver.get("https://x.com/i/flow/login")
#time.sleep(5)

wait.until(EC.presence_of_element_located((By.NAME, "text")))
#Detect Email Field, send Email Value, Find submit button and click button
email_input = driver.find_element(By.NAME, "text")
email_input.send_keys(email)
next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
next_button.click()

time.sleep(55)

#If unusual activity window then provide Username
try:
    unusual_activity_prompt = driver.find_element(By.XPATH, '//*[text()="There was unusual login activity on your account. To help keep your account safe, please enter your phone number or username to verify it’s you."]')
    if unusual_activity_prompt:
        print("Unusual activity window detected. Processing...")
        username_input = driver.find_element(By.NAME, "text")
        username_input.send_keys(username)
        next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
        next_button.click()
        #time.sleep(5)
    else:
        print("No unusual activity window detected. Proceeding to Password submit.")
except:
    pass

wait.until(EC.presence_of_element_located((By.NAME, "password")))
#Input password, find login button and submit.
password_input = driver.find_element(By.NAME, "password")
password_input.send_keys(password)
login_button=driver.find_element(By.XPATH, "//span[text()='Log in']")
login_button.click()
#time.sleep(5)

print("Login Done!")

folders = ["Posts", "Messages", "Profile", "Followers", "Followings"]
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)
#time.sleep(5)


def capture_x_profile():
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Profile']")))
        profile_tab = driver.find_element(By.XPATH, "//span[text()='Profile']")
        profile_tab.click()
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        driver.save_screenshot('Profile/PF.png')
    except Exception as e:
        print(f"Error capturing cropped profile screenshot: {e}")


def capture_x_posts():
    profile_tab = driver.find_element(By.XPATH, "//span[text()='Profile']")
    profile_tab.click()
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    container_div = driver.find_element(By.XPATH, "//section/div/div")
    posts = container_div.find_elements(By.XPATH, '//article')
    print(f"Total posts found: {len(posts)}")
    for counter, post in enumerate(posts):
        # Hide overlay
        overlay = driver.find_element(By.XPATH, '//div[@class="css-175oi2r r-aqfbo4 r-gtdqiz r-1gn8etr r-1g40b8q"]')
        driver.execute_script("arguments[0].style.display = 'none';", overlay)
        time.sleep(0.5)
        driver.execute_script("arguments[0].scrollIntoView(true);", post)
        time.sleep(0.5)
        try:
            # Use XPath to locate the <a> element with the specified class
            element = driver.find_element(
                By.XPATH,
                '//a[contains(@class, "css-146c3p1 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-xoduu5 r-1q142lx r-1w6e6rj r-9aw3ui r-3s2u2q r-1loqt21")]'
            )
            
            # Get the value of the 'aria-label' attribute
            aria_label = element.get_attribute("aria-label")
            
            if aria_label:
                print("Aria-label:", aria_label)
            else:
                print("Aria-label attribute not found for the specified element.")
        except Exception:
            print("The specified <a> element does not exist.")

        post.screenshot(f"Posts/Post_{counter + 1}.png")
        print(f"Captured Post {counter + 1}")
        time.sleep(1)
    posts_links_list = []
    post_link_elements = container_div.find_elements(By.XPATH, '//article//a[contains(@href, "/status/")]')
    for post_link_element in post_link_elements:
        post_link = post_link_element.get_attribute('href')
        posts_links_list.append(post_link)
    cleaned_posts_links_list = [link for link in posts_links_list if link.count('/') == 5]
    #print(cleaned_posts_links_list)
    return cleaned_posts_links_list


def capture_x_followers():
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Profile']")))
    profile_tab = driver.find_element(By.XPATH, "//span[text()='Profile']")
    profile_tab.click()
    #time.sleep(5)

    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Followers']")))

    followers_link = driver.find_element(By.XPATH, "//span[text()='Followers']")
    followers_link.click()
    #time.sleep(5)

    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Followers']")))

    #Reattempt if landing from previous attempt is "Verified followers" tab
    followers_link = driver.find_element(By.XPATH, "//span[text()='Followers']")
    followers_link.click()
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    container_div = driver.find_element(By.XPATH, "//section/div/div")
    followers = container_div.find_elements(By.XPATH, '//button[@data-testid="UserCell"]')
    print(f"Total followers found: {len(followers)}")
    for counter, follower in enumerate(followers):
        driver.execute_script("arguments[0].scrollIntoView(true);", follower)
        time.sleep(0.5)
        # Hide overlay
        overlay = driver.find_element(By.XPATH, '//div[@class="css-175oi2r r-aqfbo4 r-gtdqiz r-1gn8etr r-1g40b8q"]')
        driver.execute_script("arguments[0].style.display = 'none';", overlay)
        time.sleep(0.5)
        follower.screenshot(f"Followers/Follower_{counter + 1}.png")
        print(f"Captured Follower {counter + 1}")
        time.sleep(1)
    follower_links_list = set()
    follower_link_elements = container_div.find_elements(By.XPATH, '//button[@data-testid="UserCell"]//div[@class="css-175oi2r r-1wbh5a2 r-dnmrzs r-1ny4l3l"]//a')
    for follower_link_element in follower_link_elements:
        follower_link = follower_link_element.get_attribute('href')
        follower_links_list.add(follower_link)
    #print(follower_links_list)
    return follower_links_list


def capture_x_followings():
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Profile']")))
    profile_tab = driver.find_element(By.XPATH, "//span[text()='Profile']")
    profile_tab.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Following']")))

    #time.sleep(5)
    following_link = driver.find_element(By.XPATH, "//span[text()='Following']")
    following_link.click()

    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    container_div = driver.find_element(By.XPATH, "//section/div/div")
    followings = container_div.find_elements(By.XPATH, '//button[@data-testid="UserCell"]')
    print(f"Total followings found: {len(followings)}")
    for counter, following in enumerate(followings):
        driver.execute_script("arguments[0].scrollIntoView(true);", following)
        time.sleep(0.5)
        # Hide overlay
        overlay = driver.find_element(By.XPATH, '//div[@class="css-175oi2r r-aqfbo4 r-gtdqiz r-1gn8etr r-1g40b8q"]')
        driver.execute_script("arguments[0].style.display = 'none';", overlay)
        time.sleep(0.5)
        following.screenshot(f"Followings/Following_{counter + 1}.png") #to avoid over-writing
        print(f"Captured Following {counter + 1}")
        time.sleep(1)
    following_links_list = set()
    following_link_elements = container_div.find_elements(By.XPATH, '//button[@data-testid="UserCell"]//div[@class="css-175oi2r r-1wbh5a2 r-dnmrzs r-1ny4l3l"]//a')
    for following_link_element in following_link_elements:
        following_link = following_link_element.get_attribute('href')
        following_links_list.add(following_link)
    #print(following_links_list)
    return following_links_list
  


def capture_x_messages():
    # Navigate to the messages page
    driver.get("https://x.com/messages")
    time.sleep(3)

    # Locate the timeline div
    timeline_div = driver.find_element(By.XPATH, "//div[@aria-label='Timeline: Messages']//div[@role='tablist']")
    child_divs = timeline_div.find_elements(By.XPATH, "./div")
    
    # Skip the first div and exclude the last div
    divs_to_process = child_divs[1:-1]
    print(f"Total conversations to process: {len(divs_to_process)}")
    
    # Base directory for saving messages
    base_dir = "SocialSpy/Messages"
    os.makedirs(base_dir, exist_ok=True)
    
    # Process each conversation
    for i, div in enumerate(divs_to_process, start=1):
        div.click()  # Click on the conversation
        print(f"Processing conversation {i}")


        # Locate the section with detailed messages
        section_element = driver.find_element(By.XPATH, "//section[@aria-label='Section details' and @aria-labelledby='detail-header' and @role='region' and contains(@class, 'css-175oi2r')]")
        
        # Create a folder for this conversation
        conversation_folder = os.path.join(base_dir, f"Messages_{i}")
        os.makedirs(conversation_folder, exist_ok=True)

        # Locate the scrolling container within the section
        scroller_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//div[@class='css-175oi2r r-16y2uox r-10m9thr r-1h0z5md r-f8sm7e r-13qz1uu r-3pj75a r-1ye8kvj']//div"))
        ) # Allow any dynamic content to load
        element = scroller_container.find_element(By.XPATH, "//div[@data-viewportview='true' and contains(@class, 'css-175oi2r r-16y2uox')]")

        attempts = 0
        while attempts < 17:
            # Get the current scroll position and element's height to scroll from the center

            # Scroll by half of the element's height (to scroll from the center)
            

            # Scroll upwards from the center
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", element)

            time.sleep(1)  # Wait for any potential content to load
            
            # Check the current scroll position after scrolling
            current_scroll_position = driver.execute_script("return arguments[0].scrollTop;", element)
            
            # if current_scroll_position == 0:
            #     print("No further scroll possible. Stopping...")
            #     break  # Exit if no more scrolling is possible

            attempts += 1
            print(f"Attempt {attempts}: Scrolled from center, current position {current_scroll_position}")

        if attempts == 3:
            print("Reached maximum attempts to scroll.")

        child_messages = scroller_container.find_elements(By.XPATH, "./div")

        messages_to_process = child_messages[1:-2]
        print(f"Total messages to process: {len(messages_to_process)}")

        
        last_visible_div = None
        screenshot_counter = 1
        try:
            for j, msg_div in enumerate(messages_to_process):
                # Scroll the current div into view
                driver.execute_script("arguments[0].scrollIntoView(true);", msg_div)
                time.sleep(0.5)
                presentation_div = msg_div.find_element(By.XPATH, ".//div[@role='presentation']")
                
                # Check the background color of the presentation div
                background_color = presentation_div.value_of_css_property('background-color')
                if "r-gu4em3" in presentation_div.get_attribute('class'):
                    sender_type = "Respondent"
                else:
                    sender_type = "Suspect"
                # Find the tweet text element inside the message
                tweet_text_div = presentation_div.find_element(By.XPATH, ".//div[@data-testid='tweetText']")
                
                # Extract the text from the span inside the tweet text div
                tweet_text = tweet_text_div.find_element(By.XPATH, ".//span").text
                
                print(f"Message from {sender_type}: {tweet_text}")
                
                # Take a screenshot with the last div of the previous screenshot in view
                # screenshot_path = os.path.join(conversation_folder, f"Part_{screenshot_counter}.png")
                # scroller_container.screenshot(screenshot_path)
                # print(f"Saved screenshot: {screenshot_path}")
                # screenshot_counter += 1
                # last_visible_div = msg_div  # Track the last visible div
        except:
            print(2)
        # print(f"Captured all parts of conversation {i}")
        # time.sleep(1)  # Pause before moving to the next conversation





# Method calls after Login

capture_x_profile()
print("Profile Done")

print(capture_x_posts())
print("Posts Done")

# print(capture_x_followers())
# print("Followers Done")

# print(capture_x_followings())
# print("Followings Done")
time.sleep(3)
capture_x_messages()

driver.quit()
