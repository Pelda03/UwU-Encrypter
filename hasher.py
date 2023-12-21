import pyperclip
import customtkinter as ctk
import tkinter as tk
import tkinter.ttk as ttk
import os
import bcrypt as bc

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UwU Encrypter v1.0 by Pelda")
        self.resizable(False, False)
        self.geometry("650x450")
        ctk.set_appearance_mode("dark")    

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)  # Remove window decorations
        self.tooltip.wm_geometry(f"+{x}+{y}")  # Position tooltip

        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class Buttons:
    def __init__(self, root, commands):
        self.root = root
        self.commands = commands
        self.create_buttons()
        
    def create_buttons(self):
        self.gen_salt_button = ctk.CTkButton(self.root, text="Generate Salt", command=self.commands.generate_salt)
        self.gen_salt_button.grid(row=3, column=0)  # Use grid instead of pack
        ToolTip(self.gen_salt_button, "Click to generate a new salt")

        self.copy_button = ctk.CTkButton(self.root, text="Copy to Clipboard", command=self.commands.copy_to_clipboard)
        self.copy_button.grid(row=5, column=0)  # Use grid instead of pack
        ToolTip(self.copy_button, "Click to copy the hashed string to the clipboard")

        self.hash_button = ctk.CTkButton(self.root, text="Hash", command=self.commands.hashing)
        self.hash_button.grid(row=4, column=0)  # Use grid instead of pack
        ToolTip(self.hash_button, "Click to hash the input string with the provided salt")

class Commands:
    def __init__(self, root):
        self.root = root
        self.root.grid_columnconfigure(0, weight=1)  # Set weight for column
        self.root.grid_rowconfigure((0,1,2), weight=1)  # Set weight for rows
        self.salt_entry = ctk.CTkEntry(self.root, bg_color='white')
        self.salt_entry.insert(0, "Enter the salt here or click the button to get a new one")
        self.salt_entry.bind("<FocusIn>", self.clear_salt_entry)
        self.salt_entry.grid(row=0, column=0, sticky='ew')  # Use grid instead of pack
        self.string_entry = ctk.CTkEntry(self.root, bg_color='white')
        self.string_entry.insert(0, "Enter the string to be hashed here")
        self.string_entry.bind("<FocusIn>", self.clear_string_entry)
        self.string_entry.grid(row=1, column=0, sticky='ew')  # Use grid instead of pack
        self.result_entry = ctk.CTkEntry(self.root, width=70, bg_color='white')
        self.result_entry.grid(row=2, column=0, pady=20, sticky='ew')  # Use grid instead of pack
        self.result_entry.insert(0, "Generated hash will appear here")
        self.result_entry.configure(state='readonly')
        
        
    def copy_to_clipboard(self):
        hashed_string = self.result_entry.get()
        pyperclip.copy(hashed_string)
         
    def clear_salt_entry(self, event):
        if self.salt_entry.get() == "Enter the salt here or click the button to get a new one":
            self.salt_entry.delete('0', 'end')

    def clear_string_entry(self, event):
        if self.string_entry.get() == "Enter the string to be hashed here":
            self.string_entry.delete('0', 'end')

    def hashing(self):
        salt = self.salt_entry.get().strip()
        if not salt or salt == "Enter the salt here or click the button to get a new one":
            tk.messagebox.showerror("Error", "Salt is not present. Please generate a salt first.")
            return
        salt = salt.encode('utf-8')

        string = self.string_entry.get().strip()
        if not string or string == "Enter the string to be hashed here":
            tk.messagebox.showerror("Error", "Input string is not present. Please enter a string to be hashed.")
            return
        string = string.encode('utf-8')

        hashed = bc.hashpw(string, salt)
        self.result_entry.configure(state='normal')  # Use configure instead of config
        self.result_entry.delete(0, 'end')
        self.result_entry.insert(0, hashed.decode('utf-8'))
        self.result_entry.configure(state='readonly')  # Use configure instead of config

    def generate_salt(self):
        salt = bc.gensalt().decode('utf-8')
        self.salt_entry.delete(0, 'end')
        self.salt_entry.insert(0, salt)

if __name__ == "__main__":
    app = App()
    commands = Commands(app)
    buttons = Buttons(app, commands)
    app.mainloop()