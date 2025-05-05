import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw

# Initialize the main window
root = ctk.CTk()
root.geometry("600x400")

# Load the original image
image = Image.open("S:\Coding\Hackathon\Images\wallpaper.png")  # Replace 'your_image.jpg' with your actual image path

# Create a semi-transparent overlay image
overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))  # White with 50% transparency
combined = Image.alpha_composite(image.convert('RGBA'), overlay)

# Convert to ImageTk format for tkinter
photo = ImageTk.PhotoImage(combined)

# Create a canvas to display the image
canvas = ctk.CTkCanvas(root, width=image.width, height=image.height)
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=photo)

root.mainloop()