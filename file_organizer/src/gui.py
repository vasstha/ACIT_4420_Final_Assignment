import tkinter as tk
from tkinter import filedialog, messagebox
from src.sorter import organize_files
from src.logger import log_error
import tkinter as tk
from tkinter import filedialog, messagebox
from src.sorter import organize_files

def launch_gui():
    global directory_label
    app = tk.Tk()
    app.title("File Organizer")
    app.geometry("500x200")

    # Instructions
    instructions = tk.Label(app, text="Select a folder to organize files into subfolders.", wraplength=400)
    instructions.pack(pady=10)

    # Folder selection
    directory_label = tk.Label(app, text="No folder selected", fg="gray")
    directory_label.pack(pady=5)

    # Buttons
    def select_directory():
        folder_selected = filedialog.askdirectory(title="Select Folder")
        if folder_selected:
            directory_label.config(text=folder_selected)

    def organize_directory():
        directory = directory_label.cget("text")
        if not directory or directory == "No folder selected":
            messagebox.showerror("Error", "Please select a folder first.")
            return
        
        try:
            organize_files(directory)
            messagebox.showinfo("Success", "Files organized successfully!")

        except Exception as e:

            messagebox.showerror("Error", str(e))
    
    
    select_button = tk.Button(app, text="Select Folder", command=select_directory)
    select_button.pack(pady=5)

    organize_button = tk.Button(app, text="Organize Files", command=organize_directory)
    organize_button.pack(pady=20)

    app.mainloop()
