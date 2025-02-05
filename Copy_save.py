#!/usr/bin/env python
# coding: utf-8

# In[5]:


pip install pillow pyperclip



# In[6]:


pip install pystray


# In[3]:


import os
import time
from PIL import ImageGrab, Image

# Folder where images will be saved
save_folder = r"C:\Users\uzair\Pictures\Screenshots"
os.makedirs(save_folder, exist_ok=True)

# Function to save an image with a unique name
def save_image(image, folder):
    file_name = f"{int(time.time())}.png"  # Unique file name using timestamp
    image_path = os.path.join(folder, file_name)
    image.save(image_path, "PNG")
    print(f"Image saved as {image_path}")

# Function to continuously check clipboard for images
def monitor_clipboard():
    print("Monitoring clipboard for images. Press Ctrl+C to stop.")
    last_clipboard_image = None

    while True:
        try:
            # Check if there's an image in the clipboard
            clipboard_image = ImageGrab.grabclipboard()
            
            # If an image is found and it's different from the last one, save it
            if isinstance(clipboard_image, Image.Image) and clipboard_image != last_clipboard_image:
                save_image(clipboard_image, save_folder)
                last_clipboard_image = clipboard_image

            time.sleep(1)  # Check every second

        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    monitor_clipboard()


# In[1]:


import time
import os
from PIL import ImageGrab, Image
import threading
import tkinter as tk
from tkinter import messagebox
import pystray
from pystray import MenuItem as item
from PIL import Image as PILImage

save_folder = r"C:\Users\uzair\Pictures\Screenshots"
os.makedirs(save_folder, exist_ok=True)

monitoring = False

def save_image(image):
    file_name = f"{int(time.time())}.png"
    image_path = os.path.join(save_folder, file_name)
    image.save(image_path, "PNG")
    print(f"Image saved as {image_path}")

# Modified monitor_clipboard function with retry mechanism
def monitor_clipboard():
    last_clipboard_image = None
    global monitoring
    while monitoring:
        try:
            clipboard_image = ImageGrab.grabclipboard()
            if isinstance(clipboard_image, Image.Image) and clipboard_image != last_clipboard_image:
                save_image(clipboard_image)
                last_clipboard_image = clipboard_image

            time.sleep(1)  # Check every second
            
        except OSError:
            print("Clipboard is temporarily unavailable. Retrying...")
            time.sleep(0.5)  # Wait and retry if clipboard is unavailable
        except Exception as e:
            print(f"Unexpected error: {e}")

def toggle_monitoring():
    global monitoring
    if monitoring:
        monitoring = False
        start_button.config(text="Start Monitoring")
    else:
        monitoring = True
        start_button.config(text="Stop Monitoring")
        threading.Thread(target=monitor_clipboard, daemon=True).start()

def create_gui():
    global start_button
    root = tk.Tk()
    root.title("Clipboard Image Saver")
    root.geometry("300x100")
    start_button = tk.Button(root, text="Start Monitoring", command=toggle_monitoring, width=20)
    start_button.pack(pady=20)
    root.protocol("WM_DELETE_WINDOW", lambda: hide_window(root))
    root.mainloop()

def hide_window(root):
    root.withdraw()
    icon.run()

def show_window(icon, item):
    icon.stop()
    root.deiconify()

def quit_program(icon, item):
    global monitoring
    monitoring = False
    icon.stop()
    root.quit()

image = PILImage.new("RGB", (64, 64), color=(255, 0, 0))
icon = pystray.Icon("clipboard_image_saver", image, menu=pystray.Menu(
    item("Show", show_window),
    item("Quit", quit_program)
))

if __name__ == "__main__":
    threading.Thread(target=create_gui).start()


# In[9]:


pip install pyinstaller


# In[2]:




