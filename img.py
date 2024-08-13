import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import os
import logging
import subprocess

def process_images():
    # Retrieve dimensions from input
    try:
        width = int(width_entry.get())
        height = int(height_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid integer dimensions.")
        return

    # Process selected files
    if not file_paths:
        messagebox.showerror("No Files", "Please upload images first.")
        return

    for filepath in file_paths:
        try:
            filename = os.path.basename(filepath)
            with Image.open(filepath) as img:
                if img.mode == 'CMYK':
                    img = img.convert('RGB')
                img_resized = img.resize((width, height))
                output_file = os.path.join(converted_folder, f"{os.path.splitext(filename)[0]}.png")
                img_resized.save(output_file, format='PNG')
                logging.info(f"Successfully processed: {filename}")
        except Exception as e:
            logging.error(f"Error processing {filename}: {e}")

    messagebox.showinfo("Success", "Conversion and resizing complete.")

def upload_files():
    global file_paths
    file_paths = filedialog.askopenfilenames(
        filetypes=[
            ("JPEG Files", "*.jpg"),
            ("JPEG Files", "*.jpeg"),
            ("PNG Files", "*.png"),
            ("All Files", "*.*")  # Optional: to allow other files to be visible but not selectable
        ]
    )
    file_listbox.delete(0, tk.END)
    for file in file_paths:
        file_listbox.insert(tk.END, os.path.basename(file))

def open_output_folder():
    try:
        if os.name == 'nt':  # For Windows
            os.startfile(converted_folder)
        elif os.name == 'posix':  # For macOS and Linux
            subprocess.Popen(['open', converted_folder])  # For macOS
            # subprocess.Popen(['xdg-open', converted_folder])  # For Linux
    except Exception as e:
        messagebox.showerror("Error", f"Could not open folder: {e}")

# Setup logging
logging.basicConfig(filename='image_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create the main window
root = tk.Tk()
root.title("Image Morio")

# Configure colors
header_color = '#ffc03d'
footer_color = '#ffc03d'
text_color = 'black'
bg_color = 'white'
button_color = '#ffc03d'

# Create the header
header_frame = tk.Frame(root, bg=header_color)
header_frame.pack(fill=tk.X)

header_label = tk.Label(header_frame, text="Image Morio", bg=header_color, fg=text_color, font=('Arial', 24, 'bold'))
header_label.pack(pady=10)

# Create the content frame
content_frame = tk.Frame(root, bg=bg_color)
content_frame.pack(pady=20, padx=20)

# Section A: Upload Media
upload_frame = tk.Frame(content_frame, bg=bg_color)
upload_frame.pack(pady=10)

upload_button = tk.Button(upload_frame, text="Upload Images", command=upload_files, bg=button_color, fg=text_color, width=20, height=2)
upload_button.pack(pady=5)

file_listbox = tk.Listbox(upload_frame, width=50, height=10)
file_listbox.pack(pady=5)

# Section B: Enter Dimensions
dimensions_frame = tk.Frame(content_frame, bg=bg_color)
dimensions_frame.pack(pady=10)

width_label = tk.Label(dimensions_frame, text="Width:", bg=bg_color, fg=text_color)
width_label.grid(row=0, column=0, padx=5)

width_entry = tk.Entry(dimensions_frame)
width_entry.grid(row=0, column=1, padx=5)

height_label = tk.Label(dimensions_frame, text="Height:", bg=bg_color, fg=text_color)
height_label.grid(row=1, column=0, padx=5)

height_entry = tk.Entry(dimensions_frame)
height_entry.grid(row=1, column=1, padx=5)

process_button = tk.Button(content_frame, text="Process Images", command=process_images, bg=button_color, fg=text_color, width=20, height=2)
process_button.pack(pady=10)

# Add button to open the output folder
open_folder_button = tk.Button(content_frame, text="Open Output Folder", command=open_output_folder, bg=button_color, fg=text_color, width=20, height=2)
open_folder_button.pack(pady=10)

# Create the footer
footer_frame = tk.Frame(root, bg=footer_color)
footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

footer_label = tk.Label(footer_frame, text="GoHybrid Developers 2024", bg=footer_color, fg=text_color, font=('Arial', 12))
footer_label.pack(pady=10)

# Create converted_files folder if it doesn't exist
ims_folder = os.path.dirname(os.path.abspath(__file__))
converted_folder = os.path.join(ims_folder, 'converted_files')
os.makedirs(converted_folder, exist_ok=True)

file_paths = []

# Start the Tkinter event loop
root.mainloop()
