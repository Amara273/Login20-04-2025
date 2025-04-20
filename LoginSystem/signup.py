import smtplib
import csv
import os
import random
import string
import pandas as pd
from tkinter import messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import *
import customtkinter
from customtkinter import CTkImage, CTkLabel
import customtkinter as CTk
from customtkinter import CTkButton
from PIL import Image, ImageTk


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.title("Smart Grocery Expiry Tracker")
app.geometry("600x400")

# Create frame
container = customtkinter.CTkFrame(master=app, corner_radius=0, fg_color="#0f2440")
container.pack(padx=20, pady=20, fill="both", expand=True)

image = customtkinter.CTkImage(light_image=Image.open("login/icon.png"),
                            dark_image=Image.open("login/icon.png"),
                            size=(270, 400))  # Adjust size as needed

img_label = customtkinter.CTkLabel(master=container, image=image, text="")
img_label.pack(side="left", padx=0, pady=0)

# --- Right: Your custom frame ---
frame = customtkinter.CTkFrame(master=container, corner_radius=15, fg_color="#0f2440")
frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)
# Main Label for Sign Up/Login
my_label = customtkinter.CTkLabel(master=frame, text="Sign Up/Sign In",  font=("Sans Serif", 24, "bold"), text_color="white")
my_label.pack(pady=12, padx=10)

# Entry fields
email_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Email")
email_entry.pack(pady=5, padx=15)

username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
username_entry.pack(pady=5, padx=10)

password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
password_entry.pack(pady=5, padx=10)

confirm_password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Confirm Password", show="*")
confirm_password_entry.pack(pady=5, padx=10)

btn_sign_up = CTkButton(master=app, text="Sign Up",width=90, command=lambda: signup())
btn_sign_up.place(relx=0.72,rely= 0.65, anchor=CENTER)

my_text = customtkinter.CTkLabel(master=frame, text="Already have an account?", text_color="white")
my_text.place(relx=0.31, rely=0.85, anchor=CENTER)

btn_signin = CTkButton(master=app, fg_color="green", text="Sign In", width=90, command=lambda: sign_in())
btn_signin.place(relx=0.87, rely=0.78, anchor=CENTER)  

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
            messagebox.showinfo("Success", "An email has been sent to reset your password.")
        except smtplib.SMTPAuthenticationError:
            messagebox.showerror("Error", "Authentication failed. Check your email credentials.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    @staticmethod
    def generate_temp_password():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    @staticmethod
    def signup(email, username, password, password2):
        if not os.path.exists(UserAuth.FILE_NAME):
            with open(UserAuth.FILE_NAME, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["email", "username", "password","password2"])

        with open(UserAuth.FILE_NAME, mode="r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None) 
            for row in reader:
                if row[0] == email:
                    return

        if password == password2:
            with open(UserAuth.FILE_NAME, mode="a", newline="") as file: 
                writer = csv.writer(file)
                writer.writerow([email, username, password])
                
        else:
            messagebox.showerror("Error", "Passwords do not match. Please check and try again.")

def signup():

    if email_entry.get() == "" or username_entry.get() == "" or password_entry.get() == "" or confirm_password_entry.get() == "":
        messagebox.showerror("Error", "Please fill in all fields.")

    elif email_entry.get() in UserAuth.FILE_NAME and os.path.exists(UserAuth.FILE_NAME):
        with open(UserAuth.FILE_NAME, mode="r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if row[0] == email_entry.get():
                    messagebox.showerror("Error", "User already exists. Please sign in.")
    elif password_entry.get() != confirm_password_entry.get():
        messagebox.showerror("Error", "Passwords do not match. Please check and try again.")
    elif email_entry.get() not in UserAuth.FILE_NAME and os.path.exists(UserAuth.FILE_NAME):
        with open(UserAuth.FILE_NAME, mode="a", newline="") as file:
            writer = csv.writer(file)
            # writer.writerow(email_entry.getconfirm_password_entry.get() == password_entry.get())
        UserAuth.signup(email_entry.get(), username_entry.get(), password_entry.get(), confirm_password_entry.get())
        messagebox.showinfo("Success", "Registration successful! Welcome to SMART GROCERY EXPIRY TRACKER!")
def sign_in():
    app.destroy()

def go_to_sign_up():
    app.destroy()
    import signup
    signup.app.mainloop()
app.mainloop()
