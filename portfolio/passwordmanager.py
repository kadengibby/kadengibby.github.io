import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import random
import string
from cryptography.fernet import Fernet
import cryptography

# If no password given then "random"
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# database and key
def initialize_database():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                 (id INTEGER PRIMARY KEY, website TEXT, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

    # generate key
    if not os.path.exists('key.key'):
        key = Fernet.generate_key()
        with open('key.key', 'wb') as key_file:
            key_file.write(key)

# encrypt
def encrypt_data(data):
    key = load_key()
    f = Fernet(key)
    return f.encrypt(data.encode())

#decrypt data
def decrypt_data(encrypted_data):
    try:
        key = load_key()
        f = Fernet(key)
        return f.decrypt(encrypted_data).decode()
    except cryptography.fernet.InvalidToken:
        print('Invalid or corrupted password data.')
        return ''

# load encryption key
def load_key():
    return open('key.key', 'rb').read()

def add_password(website, username, password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    encrypted_password = encrypt_data(password)
    c.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)", (website, username, encrypted_password))
    conn.commit()
    conn.close()

def get_password(website):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT website, username, password FROM passwords WHERE website=?", (website,))
    row = c.fetchone()
    if row:
        website, username, encrypted_password = row
        password = decrypt_data(encrypted_password)
        if password:
            messagebox.showinfo("Password Retrieved", f'Website: {website}\nUsername: {username}\nPassword: {password}')
        else:
            messagebox.showerror("Error", 'Failed to decrypt password.')
    else:
        messagebox.showerror("Error", 'Password not found for the specified website.')
    conn.close()

def display_all_passwords():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT * FROM passwords")
    rows = c.fetchall()
    if rows:
        password_list = ""
        for row in rows:
            website, username, encrypted_password = row[1], row[2], row[3]
            password = decrypt_data(encrypted_password)
            password_list += f'Website: {website}, Username: {username}, Password: {password}\n'
        messagebox.showinfo("All Passwords", password_list)
    else:
        messagebox.showinfo("All Passwords", 'No passwords stored in the database.')
    conn.close()



def on_add_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not website or not username or not password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    add_password(website, username, password)
    messagebox.showinfo("Success", "Password added successfully.")

def on_get_password():
    website = website_entry.get()
    if not website:
        messagebox.showerror("Error", "Please enter a website.")
        return
    get_password(website)

def on_display_passwords():
    display_all_passwords()

# Initialize the database and key
initialize_database()

# Create the main window
root = tk.Tk()
root.title("Password Manager")

# Create labels and entries
website_label = tk.Label(root, text="Website:")
website_label.grid(row=0, column=0, sticky="e")
website_entry = tk.Entry(root)
website_entry.grid(row=0, column=1)

username_label = tk.Label(root, text="Username:")
username_label.grid(row=1, column=0, sticky="e")
username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1)

password_label = tk.Label(root, text="Password:")
password_label.grid(row=2, column=0, sticky="e")
password_entry = tk.Entry(root)
password_entry.grid(row=2, column=1)

# Create buttons
add_button = tk.Button(root, text="Add Password", command=on_add_password)
add_button.grid(row=3, column=0, columnspan=2, pady=5)

get_button = tk.Button(root, text="Get Password", command=on_get_password)
get_button.grid(row=4, column=0, columnspan=2, pady=5)

display_button = tk.Button(root, text="Display All Passwords", command=on_display_passwords)
display_button.grid(row=5, column=0, columnspan=2, pady=5)

# Run the GUI
root.mainloop()

