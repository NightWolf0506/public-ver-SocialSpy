import customtkinter
from PIL import Image
import os
import threading
import time
import tkinter as tk
import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image
from fpdf import FPDF
from tkinter import messagebox
import subprocess
try:
    import win32print
except ImportError:
    win32print = None


customtkinter.set_appearance_mode("dark")

class App(customtkinter.CTk):
    width = 1920
    height = 1080
    current_path = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry(f'{self.width}x{self.height}+0+0')
        self.title("Login")
        self.resizable(True, True)

        # Background Image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "\Images\wallpaper.png"), size=(self.screen_width, self.screen_height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # Main Frame
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        for a in range(7):
            self.main_frame.grid_rowconfigure(a, weight=1)
        for i in range(6):
            self.main_frame.grid_columnconfigure(i, weight = 1)
        self.main_frame.grid(row=0, column=0)

        self.social_spy_label = customtkinter.CTkLabel(self.main_frame, text="Social Spy", font=customtkinter.CTkFont(family = 'cascadia code', size=28, weight="bold"))
        self.social_spy_label.grid(row=0, column=0, columnspan = 6, padx = 10, pady=(17, 17))
        self.select_platform_label = customtkinter.CTkLabel(self.main_frame, text="Select Platform", font=customtkinter.CTkFont(family = 'cascadia code', size=20))
        self.select_platform_label.grid(row=1, column=0, columnspan = 6, padx = 10, pady=(17, 17))

        instagram = customtkinter.CTkImage(Image.open(current_path + "\Images\instagram.jpg"), size=(20, 20))
        self.instagram_button = customtkinter.CTkButton(self.main_frame, image = instagram, fg_color = "#C22C8B", hover_color = "#811D5C", text = "", height = 100, width = 100, command = self.instagram)
        self.instagram_button.grid(row = 2, column = 0, sticky="ns", padx = 10, pady=(17, 17))
        self.instagram_label = customtkinter.CTkLabel(self.main_frame, text="Instagram", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"))
        self.instagram_label.grid(row=3, column=0, padx = 10, pady=(17, 17))

        facebook = customtkinter.CTkImage(Image.open(current_path + "\\Images\\facebook.png"), size=(20, 20))
        self.facebook_button = customtkinter.CTkButton(self.main_frame, image = facebook, fg_color = "#3B579E", hover_color = "#273A69", text = "", height = 100, width = 100, command = self.facebook)
        self.facebook_button.grid(row = 2, column = 1, sticky="ns", padx = 10, pady=(17, 17))
        self.facebook_label = customtkinter.CTkLabel(self.main_frame, text="Facebook", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"))
        self.facebook_label.grid(row=3, column=1, padx = 10, pady=(17, 17))

        telegram = customtkinter.CTkImage(Image.open(current_path + "\Images\Telegram.png"), size=(20, 20))
        self.telegram = customtkinter.CTkButton(self.main_frame, image = telegram, fg_color = "#30A7DD", hover_color = "#206F93", text = "", height = 100, width = 100, command = self.telegram)
        self.telegram.grid(row = 2, column = 2, sticky="ns", padx = 10, pady=(17, 17))
        self.telegram_label = customtkinter.CTkLabel(self.main_frame, text="Telegram", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"))
        self.telegram_label.grid(row=3, column=2, padx = 10, pady=(17, 17))

        whatsapp = customtkinter.CTkImage(Image.open(current_path + "\Images\Whatsapp.png"), size=(20, 20))
        self.whatsapp_button = customtkinter.CTkButton(self.main_frame, image = whatsapp, fg_color = "#00A853", hover_color = "#007037", text = "", height = 100, width = 100, command = self.whatsapp)
        self.whatsapp_button.grid(row = 2, column = 3, sticky="ns", padx = 10, pady=(17, 17))
        self.whatsapp_label = customtkinter.CTkLabel(self.main_frame, text="Whatsapp", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"))
        self.whatsapp_label.grid(row=3, column=3, padx = 10, pady=(17, 17))

        X = customtkinter.CTkImage(Image.open(current_path + "\Images\X.jpg"), size=(20, 20))
        self.X_button = customtkinter.CTkButton(self.main_frame, image = X, fg_color = "#000000", hover_color = "#1C1C1C", text = "", height = 100, width = 100, command = self.X)
        self.X_button.grid(row = 2, column = 4, sticky="ns", padx = 10, pady=(17, 17))
        self.X_label = customtkinter.CTkLabel(self.main_frame, text="X", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"))
        self.X_label.grid(row=3, column=4, padx = 10, pady=(17, 17))

        google = customtkinter.CTkImage(Image.open(current_path + "\Images\Google.png"), size=(20, 20))
        self.google_button = customtkinter.CTkButton(self.main_frame, image = google, text = "", height = 100, width = 100, command = self.google)
        self.google_button.grid(row = 2, column = 5, sticky="ns", padx = 10, pady=(17, 17))
        self.google_label = customtkinter.CTkLabel(self.main_frame, text="Google", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"))
        self.google_label.grid(row=3, column=5, padx = 10, pady=(17, 17))

        self.team_label = customtkinter.CTkLabel(self.main_frame, text="Team:-", font=customtkinter.CTkFont(family = 'cascadia code', size=27, weight="bold"), text_color=("purple", "#4e09a3"))
        self.team_label.grid(row=4, column=0, padx = 10, pady=(17, 17), sticky = "w")
        self.shagun_label = customtkinter.CTkLabel(self.main_frame, text="Shagun Yadav", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"), text_color=("cyan", "#09f0f0"))
        self.shagun_label.grid(row=5, column=0, columnspan = 2)
        self.alok_label = customtkinter.CTkLabel(self.main_frame, text="Alok Yadav", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"), text_color=("cyan", "#09f0f0"))
        self.alok_label.grid(row=6, column=0, columnspan = 2)
        self.Aryan_label = customtkinter.CTkLabel(self.main_frame, text="Aryan Pathak", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"), text_color=("cyan", "#09f0f0"))
        self.Aryan_label.grid(row=5, column=2, columnspan = 2)
        self.Nitesh_label = customtkinter.CTkLabel(self.main_frame, text="Nitesh Mishra", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"), text_color=("cyan", "#09f0f0"))
        self.Nitesh_label.grid(row=6, column=2, columnspan = 2)
        self.Adarsh_label = customtkinter.CTkLabel(self.main_frame, text="Adarsh Thakur", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"), text_color=("cyan", "#09f0f0"))
        self.Adarsh_label.grid(row=5, column=4, columnspan = 2)
        self.monalisa_label = customtkinter.CTkLabel(self.main_frame, text="Monalisa Kole", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"), text_color=("cyan", "#09f0f0"))
        self.monalisa_label.grid(row=6, column=4, columnspan = 2)

        # Instagram Frame
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.ig_image = customtkinter.CTkImage(Image.open(current_path + "\Images\InstagramBackground.jpg"), size=(self.screen_width, self.screen_height))
        self.ig_image_label = customtkinter.CTkLabel(self, image=self.ig_image, text = "")

        self.ig_frame = customtkinter.CTkFrame(self, corner_radius=0)
        for a in range(10):
            self.ig_frame.grid_rowconfigure(a, weight=1)
        for i in range(4):
            self.ig_frame.grid_columnconfigure(i, weight = 1)

        # Instagram Frame (Top Bar)
        self.ig_top_bar = customtkinter.CTkFrame(self.ig_frame, corner_radius = 0, border_width = 1)
        self.ig_top_bar.grid_rowconfigure(0, weight=1)
        for i in range(10):
            self.ig_top_bar.grid_columnconfigure(i, weight = 1)
        self.ig_top_bar.grid(row=0, column=0, columnspan = 4, sticky="new")
        
        self.ig_label = customtkinter.CTkLabel(self.ig_top_bar, text="Instagram Spy", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"))
        self.ig_label.grid(row=0, column=0, padx = 10, pady=(17, 17))

        # self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.ig_top_bar, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        # self.scaling_optionemenu.grid(row=0, column=8, sticky="ns", pady=(17, 17))

        self.back_button = customtkinter.CTkButton(self.ig_top_bar, text = "Main Menu", width = 50, height = 50, command = self.mainmenu)
        self.back_button.grid(row = 0, column = 9, sticky="ns", pady=(17, 17))

        # Instagram Frame (Instagram Left Frame)
        self.ig_left_frame = customtkinter.CTkFrame(self.ig_frame, corner_radius = 0, border_width = 1)
        for i in range(11):
            self.ig_left_frame.grid_rowconfigure(i, weight=1)
        self.ig_left_frame.grid_columnconfigure(0, weight = 1)
        self.ig_left_frame.grid(row=1, column=0, columnspan = 2, rowspan = 9, sticky="nsw")

        self.username_label = customtkinter.CTkLabel(self.ig_left_frame, text="Username", font=customtkinter.CTkFont(family = 'cascadia code', size=17))
        self.username_label.grid(row=0, column=0, padx=30, sticky="w")
        self.username_entry = customtkinter.CTkEntry(self.ig_left_frame, width = 500, placeholder_text="Username")
        self.username_entry.grid(row=1, column=0, padx=30)
        self.password_label = customtkinter.CTkLabel(self.ig_left_frame, text="Password", font=customtkinter.CTkFont(family = 'cascadia code', size=17))
        self.password_label.grid(row=2, column=0, padx=30, sticky="w")
        self.password_entry = customtkinter.CTkEntry(self.ig_left_frame, width = 500, placeholder_text="Password")
        self.password_entry.grid(row=3, column=0, padx=30)

        self.info_label = customtkinter.CTkLabel(self.ig_left_frame, text="", text_color = "#00FF00", font=customtkinter.CTkFont(family = 'cascadia code', size=10))
        self.info_label.grid(row=4, column=0, padx=30, sticky="w")

        self.progressbar_1 = customtkinter.CTkProgressBar(self.ig_left_frame, width = 500)
        self.progressbar_1.set(1)
        self.progressbar_1.grid(row=5, column=0, padx=30)

        self.Get_Info_button = customtkinter.CTkButton(self.ig_left_frame, width = 500, text="Get Info", command=self.gettingInfo)
        self.Get_Info_button.grid(row = 6, column=0, padx=30)

        self.clear_button = customtkinter.CTkButton(self.ig_left_frame, width = 500, text="Clear All", command=self.clear)
        self.clear_button.grid(row = 7, column=0, padx=30, sticky="nw")

        self.log_label = customtkinter.CTkLabel(self.ig_left_frame, text="Log:-", font=customtkinter.CTkFont(family = 'cascadia code', size=17))
        self.log_label.grid(row=8, column=0, padx=30, sticky="nw")
        
        self.textbox = customtkinter.CTkTextbox(self.ig_left_frame, width = 500, height = 100)
        self.textbox.grid(row=9, column=0, rowspan = 2, padx=30, sticky="nw")

        # Instagram Frame (Instagram Right Frame)
        self.ig_right_frame = customtkinter.CTkFrame(self.ig_frame, corner_radius = 0, border_width = 1)
        for i in range(10):
            self.ig_right_frame.grid_rowconfigure(i, weight=1)
        self.ig_right_frame.grid_columnconfigure(0, weight = 1)
        self.ig_right_frame.grid(row=1, column = 3, columnspan = 2, rowspan = 9, sticky="nse")

        self.data_label = customtkinter.CTkLabel(self.ig_right_frame, text="Data:-", font=customtkinter.CTkFont(family = 'cascadia code', size=17))
        self.data_label.grid(row=0, column=0, padx=30, sticky="w")

        self.listbox_frame = ctk.CTkFrame(self.ig_right_frame)  # Create a frame to hold the listbox
        self.listbox_frame.grid(row = 1, column=0, rowspan = 5, padx=30, pady=(15, 15), sticky = "n")
        self.listbox = tk.Listbox(self.listbox_frame, width = 100, height = 15, background = "#333333", foreground = "#FFFFFF")  # Standard tkinter Listbox
        self.listbox.grid(row = 0, column=0, padx=30, pady=(15, 15))

        # Adding a scrollbar to the listbox
        self.scrollbar = tk.Scrollbar(self.listbox_frame, orient="vertical", command=self.listbox.yview)
        self.scrollbar.grid(row = 0, column=0, sticky = "nse")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        folder_path = current_path + "\Output"  # Get folder path from the entry widget
        if os.path.isdir(folder_path):
            files = os.listdir(folder_path)  # List all files in the directory
            self.listbox.delete(0, tk.END)  # Clear the listbox
            for file in files:
                self.listbox.insert(tk.END, file)  # Insert files into the listbox
        else:
            self.listbox.delete(0, tk.END)  # Clear the listbox if directory doesn't exist
            self.listbox.insert(tk.END, "Directory not found")

        self.Get_Info_button = customtkinter.CTkButton(self.ig_right_frame, width = 500, text="Open", command=self.open)
        self.Get_Info_button.grid(row = 5, column=0, padx=30, pady = 15, sticky = "nw")
        self.Get_Info_button = customtkinter.CTkButton(self.ig_right_frame, width = 500, fg_color = "#FF0000", hover_color = "#840808", text="Delete", command=self.deleting)
        self.Get_Info_button.grid(row = 6, column=0, padx=30, pady = 15, sticky = "nw")
        self.Get_Info_button = customtkinter.CTkButton(self.ig_right_frame, width = 500, text="Print", command=self.printing)
        self.Get_Info_button.grid(row = 7, column=0, padx=30, pady=(15, 15), sticky = "nw")

    # def change_scaling_event(self, new_scaling: str):
    #     new_scaling_float = int(new_scaling.replace("%", "")) / 100
    #     customtkinter.set_widget_scaling(new_scaling_float)

    def open(self):
        selected_file = self.listbox.get(tk.ACTIVE)  # Get the currently selected file from the listbox
        if selected_file:
            folder_path = self.current_path + "\Output"
            full_path = os.path.join(folder_path, selected_file)  # Full path of the selected file
            try:
                if os.path.isfile(full_path):
                    # Open the file using the default application
                    if os.name == 'nt':  # For Windows
                        os.startfile(full_path)
                    elif os.name == 'posix':  # For Unix/Linux/Mac
                        subprocess.call(('open', full_path))
                    else:
                        messagebox.showerror("Unsupported OS", "Your operating system is not supported for this action.")
                else:
                    messagebox.showerror("Error", "Selected item is not a file.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")
        else:
            messagebox.showwarning("No selection", "Please select a file to open.")

    def delete(self):
        selected_file = self.listbox.get(tk.ACTIVE)  # Get the currently selected file from the listbox
        if selected_file:
            folder_path = self.current_path + "\Output"
            full_path = os.path.join(folder_path, selected_file)  # Full path of the selected file
            try:
                if os.path.isfile(full_path):
                    os.remove(full_path)  # Delete the file
                    self.list_files()  # Refresh the listbox
                    messagebox.showinfo("Success", f"File '{selected_file}' deleted.")
                else:
                    messagebox.showerror("Error", "Selected item is not a file.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file: {e}")
        else:
            messagebox.showwarning("No selection", "Please select a file to delete.")

    def list_files(self):
        folder_path = self.current_path + "\Output"  # Get folder path from the entry widget
        if os.path.isdir(folder_path):
            files = os.listdir(folder_path)  # List all files in the directory
            self.listbox.delete(0, tk.END)  # Clear the listbox
            for file in files:
                self.listbox.insert(tk.END, file)  # Insert files into the listbox
        else:
            self.listbox.delete(0, tk.END)  # Clear the listbox if directory doesn't exist
            self.listbox.insert(tk.END, "Directory not found")

    def clear(self):
        self.textbox.delete('1.0', tk.END)
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.info_label.configure(text = "")

    def print(self):
        selected_file = self.listbox.get(tk.ACTIVE)  # Get the currently selected file from the listbox
        if selected_file:
            folder_path = self.current_path + "\Output"
            full_path = os.path.join(folder_path, selected_file)  # Full path of the selected file
            try:
                if os.path.isfile(full_path):
                    if os.name == 'nt' and win32print:  # For Windows
                        # Using win32print to send the file to the default printer
                        printer_name = win32print.GetDefaultPrinter()
                        if printer_name:
                            hPrinter = win32print.OpenPrinter(printer_name)
                            try:
                                with open(full_path, "rb") as f:
                                    raw_data = f.read()
                                    job = win32print.StartDocPrinter(hPrinter, 1, (selected_file, None, "RAW"))
                                    win32print.StartPagePrinter(hPrinter)
                                    win32print.WritePrinter(hPrinter, raw_data)
                                    win32print.EndPagePrinter(hPrinter)
                                    win32print.EndDocPrinter(hPrinter)
                                messagebox.showinfo("Success", f"File '{selected_file}' sent to printer.")
                            finally:
                                win32print.ClosePrinter(hPrinter)
                        else:
                            messagebox.showerror("Error", "No default printer found.")
                    elif os.name == 'posix':  # For Unix/Linux/Mac
                        # Using lpr command to print the file
                        subprocess.run(['lpr', full_path])
                        messagebox.showinfo("Success", f"File '{selected_file}' sent to printer.")
                    else:
                        messagebox.showerror("Unsupported OS", "Printing is not supported on this operating system.")
                else:
                    messagebox.showerror("Error", "Selected item is not a file.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to print file: {e}")
        else:
            messagebox.showwarning("No selection", "Please select a file to print.")

    def google(self):
        pass
    
    def telegram(self):
        pass

    def whatsapp(self):
        pass

    def X(self):
        pass

    def facebook(self):
        pass

    def instagram(self):
        self.main_frame.grid_forget()
        self.bg_image_label.grid_forget()
        self.title("Instagram Spy")
        self.state("zoomed")
        self.ig_image_label.grid(row=0, column=0)
        self.ig_frame.grid(row=0, column=0, sticky = "nsw")

    def GetInfo(self):
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        self.info_label.configure(text = "Fetching Data", text_color = "#00FF00")
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.spy(username, password)
        self.list_files()
        self.progressbar_1.stop()
        self.progressbar_1.configure(mode="determinate")
        self.progressbar_1.set(1)  # Set progress to 50%
        self.info_label.configure(text = "Data Fetched Successfully", text_color = "#00FF00")

    def mainmenu(self):
        self.ig_frame.grid_forget()
        self.ig_image_label.grid_forget()
        self.title("Social Spy")
        self.bg_image_label.grid(row=0, column=0)
        self.main_frame.grid(row=0, column=0)

    def capture_screenshot(self, driver,folder ,filename):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, folder)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_save = os.path.join(file_path, filename)
        driver.save_screenshot(file_save)
        self.textbox.insert("end", f"Screenshot saved as {filename}\n")

    def get_posts(self, driver, username):
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
                self.textbox.insert("end", f"An error occurred while retrieving post link: {e}\n")

        for i, post_link in enumerate(post_links):
            try:
                driver.get(post_link)
                time.sleep(3)
                self.capture_screenshot(driver,folder,f'post_{i}.png')
                self.textbox.insert("end", f"Screenshot for post {i} taken.\n")
            except Exception as e:
                self.textbox.insert("end", f"An error occurred for post {i}: {e}\n")

    def get_followers_following(self, driver, username):
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
                
                self.capture_screenshot(driver, folder_followers, f'followers_{screenshot_count}.png')
                screenshot_count += 1
                
                try:
                    driver.find_element(By.XPATH, '//span[contains(text(), "Suggested for you")]')
                    self.textbox.insert("end", "Suggested for you section found. Stopping the followers process.\n")
                    break
                except:
                    pass
                
                new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_panel)
                if new_height == last_height:
                    break
                last_height = new_height
        except Exception as e:
            self.textbox.insert("end", f"An error occurred while handling followers: {e}\n")
        

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
                
                self.capture_screenshot(driver, folder_following, f'following_{screenshot_count}.png')
                screenshot_count += 1
                
                try:
                    driver.find_element(By.XPATH, '//span[contains(text(), "Suggested for you")]')
                    self.textbox.insert("end", "Suggested for you section found. Stopping the following process.\n")
                    break
                except:
                    pass
                
                new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_panel)
                if new_height == last_height:
                    break
                last_height = new_height
        except Exception as e:
            self.textbox.insert("end", f"An error occurred while handling following: {e}\n")

    def get_messages(self, driver):
        folder = "IMessSS"
        message_url = 'https://www.instagram.com/direct/inbox/'
        driver.get(message_url)
        

        try:
            not_now_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))
            )
            not_now_button.click()
        except Exception as e:
            self.textbox.insert("end", f"No 'Turn on Notifications' popup found: {e}\n")

        message_links = set()
        time.sleep(3)

        try:
            scrollable_panel = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@role="region" and contains(@class, "scrollable")]'))
            )
            scrollable = True
        except TimeoutException:
            self.textbox.insert("end", "Scrollable panel not found. Proceeding without scrolling.\n")
            scrollable = False

        if scrollable:
            last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_panel)

            while True:
                try:
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_panel)
                    time.sleep(5)

                except Exception as e:
                    self.textbox.insert("end", f"An error occurred while scrolling or finding messages: {e}\n")
                    break

        for i, message in enumerate(driver.find_elements(By.XPATH, '//div[@role="listitem"]')):
            try:
                message.click()
                time.sleep(5)
                self.capture_screenshot(driver, folder, f'message_{i}.png')
                message_url = 'https://www.instagram.com/direct/inbox/'
                time.sleep(3) 
            except Exception as e:
                self.textbox.insert("end", f"An error occurred for message {i}: {e}\n")


    def create_pdf_from_screenshots(self, name, pdf_title, folder_titles):
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
        self.textbox.insert("end", f"PDF created: {file_save}\n")


    def img_remover(self, folder_titles):
        current_directory = os.path.dirname(os.path.abspath(__file__))

        for folder in folder_titles.keys():
            folder_path = os.path.join(current_directory, folder)
            
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                image_extensions = ('.png')

                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    
                    if os.path.isfile(file_path) and file_path.lower().endswith(image_extensions):
                        os.remove(file_path)
                        self.textbox.insert("end", f"Removed: {file_path}\n")

    def spy(self, u, p):
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
            self.capture_screenshot(driver, folder,'profile.png')
            self.get_followers_following(driver,username)
        except Exception as e:
            self.textbox.insert("end", f"An error occurred while handling profile, followers, or following: {e}\n")

        time.sleep(3)

        self.get_posts(driver, username)
        time.sleep(3)

        self.get_messages(driver)

        driver.quit()

        self.report()

    def report(self):
        self.popup = customtkinter.CTk()
        self.popup.geometry("800x400")
        self.popup.title("Report")
        self.popup.resizable(False, False)

        # self.popup_bg_image = customtkinter.CTkImage(Image.open(self.current_path + "\Images\ReportReview.png"), size=(800, 400))
        # self.popup_bg_image_label = customtkinter.CTkLabel(popup, image=self.popup_bg_image)
        # self.popup_bg_image_label.grid(row=0, column=0)

        # Popup Left Frame
        self.left_frame = customtkinter.CTkFrame(self.popup, corner_radius = 0)
        self.left_frame.grid(row=0, column=0, sticky="nsw")
        for i in range(10):
            self.left_frame.grid_rowconfigure(i, weight=1)
        self.left_frame.grid_columnconfigure(0, weight = 1)

        # Popup Right Frame
        self.right_frame = customtkinter.CTkFrame(self.popup, corner_radius = 0)
        self.right_frame.grid(row=0, column=1, sticky="nse")
        for i in range(10):
            self.right_frame.grid_rowconfigure(i, weight=1)
        self.right_frame.grid_columnconfigure(0, weight = 1)

        # Left Frame
        self.open_post_button = customtkinter.CTkButton(self.left_frame, width = 340, text="Review Post", command = self.postFolder)
        self.open_post_button.grid(row=0, column=0, padx=30, pady=(20, 0))
        self.open_message_button = customtkinter.CTkButton(self.left_frame, width = 340, text="Review Message", command = self.messageFolder)
        self.open_message_button.grid(row=1, column=0, padx=30, pady=(20, 0))

        self.summary_checkbox = customtkinter.CTkCheckBox(self.left_frame, text="Add Summary")
        self.summary_checkbox.grid(row=2, column=0, padx=30, pady=(20, 0))
        # self.summary_checkbox.select()

        self.generate_pdf_button = customtkinter.CTkButton(self.left_frame, width = 340, text="Generate PDF", command = self.generatingPDF)
        self.generate_pdf_button.grid(row=3, column=0, padx=30, pady=(10, 0))

        # Right Frame
        self.enter_text_label = customtkinter.CTkLabel(self.right_frame, text="Enter text", font=customtkinter.CTkFont(family = 'cascadia code', size = 17))
        self.enter_text_label.grid(row=0, column=0, padx=30, pady=(20, 0))
        self.text_entry = customtkinter.CTkEntry(self.right_frame, width = 340, placeholder_text="Disabled", state="disabled")
        self.text_entry.grid(row=1, column=0, padx=30, pady=(10, 0))
        self.text_switch = customtkinter.CTkSwitch(self.right_frame, text = "Text Search", command = self.textEnable)
        self.text_switch.grid(row=2, column=0, padx=30, pady=(10, 0))

        self.popup.mainloop()

    def textEnable(self):
        if self.text_switch.get() == 1:
            self.text_entry.configure(state="normal", placeholder_text="Text")
        else:
            self.text_entry.configure(state="disabled", placeholder_text="Disabled")

    def postFolder(self):
        file_path = self.current_path + "\IPostSS"
        os.startfile(file_path)

    def messageFolder(self):
        file_path = self.current_path + "\IMessSS"
        os.startfile(file_path)

    def generatePDF(self):
        name = self.fileName()
        title = username
        folder_titles = {
        'IProfileSS': 'Profile Information :',
        'IFwingSS': 'Followings List : ',
        'IFwerSS': 'Followers List : ',
        'IPostSS': 'Posts : ',
        'IMessSS': 'Messages : '
        }
        self.create_pdf_from_screenshots(name,title,folder_titles)
        self.popup.destroy()
        self.img_remover(folder_titles)

    def fileName(self):
        text_box_dialog = customtkinter.CTkInputDialog(text="Enter file name", title="Save File")
        user = text_box_dialog.get_input()
        self.textbox.insert("end", f"\nFile saved as: {user}\n")
        return user

    def start_thread(self, target):
        # Making Threads
        thread = threading.Thread(target=target)
        thread.start()

    def gettingInfo(self):
        self.start_thread(self.GetInfo)

    def printing(self):
        self.start_thread(self.print)

    def deleting(self):
        self.start_thread(self.delete)

    def generatingPDF(self):
        self.start_thread(self.generatePDF)

if __name__ == "__main__":
    app = App()
    app.mainloop()