import customtkinter as ctk
import tkinter as tk
import os

# Function to list files in a specified directory
def list_files():
    folder_path = folder_entry.get()  # Get folder path from the entry widget
    if os.path.isdir(folder_path):
        files = os.listdir(folder_path)  # List all files in the directory
        listbox.delete(0, tk.END)  # Clear the listbox
        for file in files:
            listbox.insert(tk.END, file)  # Insert files into the listbox
    else:
        listbox.delete(0, tk.END)  # Clear the listbox if directory doesn't exist
        listbox.insert(tk.END, "Directory not found")

# Initialize the main window
app = ctk.CTk()
app.geometry("400x300")
app.title("File Browser")

# Entry widget for folder path
folder_entry = ctk.CTkEntry(app, width=300)
folder_entry.pack(pady=10)

# Button to list files
list_button = ctk.CTkButton(app, text="List Files", command=list_files)
list_button.pack(pady=10)

# Listbox to display files (using tkinter Listbox)
listbox_frame = ctk.CTkFrame(app)  # Create a frame to hold the listbox
listbox_frame.pack(pady=10, fill="both", expand=True)
listbox = tk.Listbox(listbox_frame, width=50, height=10)  # Standard tkinter Listbox
listbox.pack(side="left", fill="both", expand=True)

# Adding a scrollbar to the listbox
scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=listbox.yview)
scrollbar.pack(side="right", fill="y")
listbox.config(yscrollcommand=scrollbar.set)

# Run the main loop
app.mainloop()
