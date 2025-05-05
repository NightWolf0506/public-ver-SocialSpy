import customtkinter
from PIL import Image
import os
import gspread
import threading
from tkcalendar import DateEntry
from datetime import datetime
import time
from bs4 import BeautifulSoup
import requests
import webbrowser
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import SocialSpy as ss


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
        for a in range(4):
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
        self.facebook_button = customtkinter.CTkButton(self.main_frame, image = facebook, fg_color = "#3B579E", hover_color = "#273A69", text = "", height = 100, width = 100, command = self.clogging_out)
        self.facebook_button.grid(row = 2, column = 1, sticky="ns", padx = 10, pady=(17, 17))
        self.facebook_label = customtkinter.CTkLabel(self.main_frame, text="Facebook", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"))
        self.facebook_label.grid(row=3, column=1, padx = 10, pady=(17, 17))

        telegram = customtkinter.CTkImage(Image.open(current_path + "\Images\Telegram.png"), size=(20, 20))
        self.telegram = customtkinter.CTkButton(self.main_frame, image = telegram, fg_color = "#30A7DD", hover_color = "#206F93", text = "", height = 100, width = 100, command = self.clogging_out)
        self.telegram.grid(row = 2, column = 2, sticky="ns", padx = 10, pady=(17, 17))
        self.telegram_label = customtkinter.CTkLabel(self.main_frame, text="Telegram", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"))
        self.telegram_label.grid(row=3, column=2, padx = 10, pady=(17, 17))

        whatsapp = customtkinter.CTkImage(Image.open(current_path + "\Images\Whatsapp.png"), size=(20, 20))
        self.whatsapp_button = customtkinter.CTkButton(self.main_frame, image = whatsapp, fg_color = "#00A853", hover_color = "#007037", text = "", height = 100, width = 100, command = self.clogging_out)
        self.whatsapp_button.grid(row = 2, column = 3, sticky="ns", padx = 10, pady=(17, 17))
        self.whatsapp_label = customtkinter.CTkLabel(self.main_frame, text="Whatsapp", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"))
        self.whatsapp_label.grid(row=3, column=3, padx = 10, pady=(17, 17))

        X = customtkinter.CTkImage(Image.open(current_path + "\Images\X.jpg"), size=(20, 20))
        self.X_button = customtkinter.CTkButton(self.main_frame, image = X, fg_color = "#000000", hover_color = "#1C1C1C", text = "", height = 100, width = 100, command = self.clogging_out)
        self.X_button.grid(row = 2, column = 4, sticky="ns", padx = 10, pady=(17, 17))
        self.X_label = customtkinter.CTkLabel(self.main_frame, text="X", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"))
        self.X_label.grid(row=3, column=4, padx = 10, pady=(17, 17))

        google = customtkinter.CTkImage(Image.open(current_path + "\Images\Google.png"), size=(20, 20))
        self.google_button = customtkinter.CTkButton(self.main_frame, image = google, text = "", height = 100, width = 100, command = self.clogging_out)
        self.google_button.grid(row = 2, column = 5, sticky="ns", padx = 10, pady=(17, 17))
        self.google_label = customtkinter.CTkLabel(self.main_frame, text="Google", font=customtkinter.CTkFont(family = 'cascadia code', size=17, weight="bold"))
        self.google_label.grid(row=3, column=5, padx = 10, pady=(17, 17))

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

        self.back_button = customtkinter.CTkButton(self.ig_top_bar, text = "Main Menu", width = 50, height = 50, command = self.mainmenu)
        self.back_button.grid(row = 0, column = 9, sticky="ns", pady=(17, 17))

        # Instagram Frame (Instagram Left Frame)
        self.ig_left_frame = customtkinter.CTkFrame(self.ig_frame, corner_radius = 0, border_width = 1)
        for i in range(10):
            self.ig_left_frame.grid_rowconfigure(i, weight=1)
        self.ig_left_frame.grid_columnconfigure(0, weight = 1)
        self.ig_left_frame.grid(row=1, column=0, columnspan = 2, rowspan = 9, sticky="nsw")

        self.username_label = customtkinter.CTkLabel(self.ig_left_frame, text="Username", font=customtkinter.CTkFont(family = 'cascadia code', size=17))
        self.username_label.grid(row=0, column=0, padx=30, sticky="w")
        self.username_entry = customtkinter.CTkEntry(self.ig_left_frame, width = 500, placeholder_text="Username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(0, 7))
        self.password_label = customtkinter.CTkLabel(self.ig_left_frame, text="Password", font=customtkinter.CTkFont(family = 'cascadia code', size=17))
        self.password_label.grid(row=2, column=0, padx=30, pady=(7, 0), sticky="w")
        self.password_entry = customtkinter.CTkEntry(self.ig_left_frame, width = 500, placeholder_text="Password")
        self.password_entry.grid(row=3, column=0, padx=30, pady=(0, 7))
        self.Get_Info_button = customtkinter.CTkButton(self.ig_left_frame, width = 500, text="Get Info", command=self.GetInfo)
        self.Get_Info_button.grid(row = 4, column=0, padx=30, pady=(15, 15))

        self.textbox = customtkinter.CTkTextbox(self.ig_left_frame, width = 500, height = 300)
        self.textbox.grid(row=5, column=0, rowspan = 5, padx=30, pady=(15, 15), sticky="nsew")

        # Instagram Frame (Instagram Right Frame)
        self.ig_right_frame = customtkinter.CTkFrame(self.ig_frame, corner_radius = 0, border_width = 1)
        for i in range(10):
            self.ig_right_frame.grid_rowconfigure(i, weight=1)
        self.ig_right_frame.grid_columnconfigure(0, weight = 1)
        self.ig_right_frame.grid(row=1, column = 3, columnspan = 2, rowspan = 9, sticky="nse")

        self.Get_Info_button = customtkinter.CTkButton(self.ig_right_frame, width = 500, text="Open", command=self.GetInfo)
        self.Get_Info_button.grid(row = 0, column=0, padx=30, pady=(15, 15))
        self.Get_Info_button = customtkinter.CTkButton(self.ig_right_frame, width = 500, text="Print", command=self.GetInfo)
        self.Get_Info_button.grid(row = 1, column=0, padx=30, pady=(15, 15))
        self.Get_Info_button = customtkinter.CTkButton(self.ig_right_frame, width = 500, text="Open File Location", command=self.GetInfo)
        self.Get_Info_button.grid(row = 2, column=0, padx=30, pady=(15, 15))


        
        

    def instagram(self):
        self.main_frame.grid_forget()
        self.bg_image_label.grid_forget()
        self.title("Instagram Spy")
        self.state("zoomed")
        self.ig_image_label.grid(row=0, column=0)
        self.ig_frame.grid(row=0, column=0, sticky = "nsw")

        # os.system("python Main.py")

    def GetInfo(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        ss.spy(username, password)

    def mainmenu(self):
        self.ig_frame.grid_forget()
        self.ig_image_label.grid_forget()
        self.title("Social Spy")
        self.bg_image_label.grid(row=0, column=0)
        self.main_frame.grid(row=0, column=0)

    def logging_in(self):
        pass

    def signup_event(self):
        pass

    def clogging_out(self):
        pass

    def start_thread(self, target):
        # Making Threads
        thread = threading.Thread(target=target)
        thread.start()

    event = threading.Event()

if __name__ == "__main__":
    app = App()
    app.mainloop()