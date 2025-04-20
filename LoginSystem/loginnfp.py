import smtplib
import  subprocess
import csv
import os
import sys
import random
import string
import pandas as pd
from tkinter import messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import *
import customtkinter 
from customtkinter import CTkButton
from PIL import Image
from signup import app

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("600x400")
app.title("Smart Grocery Expiry Tracker")
container = customtkinter.CTkFrame(master=app, corner_radius=0, fg_color="#0f2440")
container.pack(padx=20, pady=20, fill="both", expand=True)

image = customtkinter.CTkImage(light_image=Image.open("login/icon.png"),
                            dark_image=Image.open("login/icon.png"),
                            size=(270, 400))

img_label = customtkinter.CTkLabel(master=container, image=image, text="")
img_label.pack(side="left", padx=0, pady=0)

frame = customtkinter.CTkFrame(master=container, corner_radius=15, fg_color="#0f2440")
frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)

my_label = customtkinter.CTkLabel(master=frame, text="Sign In",  font=("Sans Serif", 24, "bold"), text_color="white")
my_label.pack(pady=12, padx=10)

email_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Email")
email_entry.pack(pady=10, padx=15)

password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
password_entry.pack(pady=10, padx=10)

my_text = customtkinter.CTkLabel(master=frame, text="Forgot Password?", text_color="white")
my_text.place(relx=0.2, rely=0.67, anchor=CENTER)

btn_forgot = CTkButton(master=app, text="Forgot Password", width=120, command=lambda: forgot_password())
btn_forgot.place(relx=0.82, rely=0.63, anchor=CENTER)

btn_login = CTkButton(master=app, text="Login", width=70, command=lambda: login())
btn_login.place(relx=0.72, rely=0.52, anchor=CENTER)

class UserAuth:

    FILE_NAME = "users.csv"
    SENDER_EMAIL = "smartgrocerytracker@gmail.com"
    SENDER_PASSWORD = "gyaa oicw mfbj ypve" 
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    @staticmethod
    def send_email(receiver_email, subject, body):
        try:
            msg = MIMEMultipart()
            msg["From"] = UserAuth.SENDER_EMAIL
            msg["To"] = receiver_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP(UserAuth.SMTP_SERVER, UserAuth.SMTP_PORT)
            server.starttls()
            server.login(UserAuth.SENDER_EMAIL, UserAuth.SENDER_PASSWORD)
            server.sendmail(UserAuth.SENDER_EMAIL, receiver_email, msg.as_string())
            server.quit()
        except smtplib.SMTPAuthenticationError:
            messagebox.showerror("Error", "Authentication failed. Check your email credentials.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    @staticmethod
    def generate_temp_password():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    @staticmethod
    def forgot_password():
        email = email_entry.get()
        if not os.path.exists(UserAuth.FILE_NAME):
            return
        
        users = []
        found = False
        with open(UserAuth.FILE_NAME, mode="r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if row[0] == email:
                    temp_password = UserAuth.generate_temp_password()
                    row[2] = temp_password

                    found = True
                    UserAuth.send_email(email, "Password Reset", f"Your new temporary password is: {temp_password}. Please use this password to log in and update it for security reasons.")
                users.append(row)

        if found:
            with open(UserAuth.FILE_NAME, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["email", "username", "password"])
                writer.writerows(users)
        else:
            messagebox.showerror("Error", "Your email is not found. Please try again.")

    @staticmethod
    def login(email, password):
        if not os.path.exists(UserAuth.FILE_NAME):
            messagebox.showerror("Error", "No users registered yet. Please sign up first.")
            return False

        with open(UserAuth.FILE_NAME, mode="r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None) 
            for row in reader:
                if row[0] == email and row[2] == password:
                    messagebox.showinfo("Success", f"Welcome back, {row[1]}! You are logged in.")
                    return True

def btn_login():
    import signup
    signup.UserAuth.sign_up()
   
def login():
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if email == "" or password == "":
        messagebox.showerror("Error", "Please enter your email and password.")
        return

    if not os.path.exists(UserAuth.FILE_NAME):
        messagebox.showerror("Error", "User database not found. Please sign up first.")
        return

    with open(UserAuth.FILE_NAME, mode="r", newline="") as file:
        reader = csv.reader(file)
        next(reader, None) 

        for row in reader:
            if row[0].strip() == email and row[2].strip() == password:
                messagebox.showinfo("Success", f"Welcome back, {row[1]}! You are logged in.")
                return
    messagebox.showerror("Error", "Invalid email or password.")

def forgot_password():
    email = email_entry.get()
    if not os.path.exists(UserAuth.FILE_NAME):
        return
    
    users = []
    found = False
    with open(UserAuth.FILE_NAME, mode="r", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if row[0] == email:
                temp_password = UserAuth.generate_temp_password()
                row[2] = temp_password

                found = True
                UserAuth.send_email(email, "Password Reset", f"Your new temporary password is: {temp_password}. Please use this password to log in and update it for security reasons.")
                users.append(row)
            messagebox.showinfo("Success","Temporary password sent to your email address. Please use this password to log in and update it for security reasons.")
    if not found:
        messagebox.showerror("Error", "Your email is not found. Please try again.")
def go_to_signup(): 
    app.destroy() 
    subprocess.Popen([sys.executable, os.path.abspath("signup.py")])

btn_back = CTkButton(master=app, text="Back",width=60, command=go_to_signup)
btn_back.place(relx=0.05, rely=0.05, anchor=CENTER)      
email = email_entry.get()
password = password_entry.get()
UserAuth.login(email, password)
app.mainloop()

