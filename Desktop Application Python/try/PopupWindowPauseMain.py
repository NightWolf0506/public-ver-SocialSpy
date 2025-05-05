import customtkinter as ctk

def open_popup():
    # Create a popup window
    popup = ctk.CTkToplevel()
    popup.geometry("300x200")
    popup.title("Popup Window")
    
    # Add some content to the popup window
    label = ctk.CTkLabel(popup, text="Close this popup to resume.")
    label.pack(pady=20)

    close_button = ctk.CTkButton(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=20)
    
    # Pause the main window until the popup is closed
    popup.grab_set()  # Makes the popup modal (disables interactions with the main window)
    app.wait_window(popup)  # Blocks code execution until the popup is closed

# Initialize the main window
app = ctk.CTk()
app.geometry("400x300")

# Create a button to open the popup
button = ctk.CTkButton(app, text="Open Popup", command=open_popup)
button.pack(pady=50)

# Start the application
app.mainloop()