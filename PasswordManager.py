#Created by Emma Hodor on 6/20/2023
import json
import tkinter
from tkinter import messagebox
import pyperclip
import pandas
import os

##password is generated with generate_pass() and saved to clipboard
import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
           'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_pass():
    letter = random.randint(6, 8)
    symbol = random.randint(3, 4)
    number = random.randint(3, 4)

    passwrd = random.choices(letters, k=letter) + random.choices(numbers, k=number) + random.choices(symbols, k=symbol)
    random.shuffle(passwrd)
    passwrd = ' '.join(passwrd)
    passwrd = passwrd.replace(" ", "")
    pyperclip.copy(passwrd)
    entry3.delete(0, len(entry3.get()))
    entry3.insert(0, passwrd)



##Setting up the UI
window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=40, pady=40, bg="white")


def search():
    search_for = entry1.get()
    if len(search_for) == 0:
        messagebox.showinfo(title="Empty Website Field", message= "Please enter the name of a website.")
    else:
        try:
            with open("account_data.json", "r") as json_file:
                json_data = json.load(json_file)
                found_data = json_data[search_for]


        except KeyError:
            messagebox.showinfo(title=f"{search_for} Data Missing", message=f"No account data for {search_for} found.")
        except FileNotFoundError:
            messagebox.showinfo(title=f"No File", message="No account info file has been generated yet.")
        else:
            messagebox.showinfo(title=f"{search_for} Account Information", message=f"User/Email: {found_data['User/Email: ']}\nPassword: {found_data['Password: ']}")

def add():
    if len(entry1.get()) == 0 or len(entry2.get()) == 0 or len(entry3.get()) == 0:
        messagebox.showinfo(title="Missing Field Entry", message="You must fill out all fields.")
    else:
        response = messagebox.askokcancel(title=f"{entry1.get()} Account Info",
                                          message=f"Are these details correct?\nWebsite: {entry1.get()}\nUsername: {entry2.get()}\nPassword: {entry3.get()}")
        if response:
            ##with open("account_data.txt", "a") as data_file:
            new_dict = {"Website": [entry1.get()],
                        "User/Email": [entry2.get()],
                        "Password": [entry3.get()],
                        }
            if os.path.isfile("account_data.csv"):
                data = pandas.read_csv("account_data.csv")
                df = pandas.DataFrame(new_dict)
                new_data = pandas.concat([data, df])
                os.remove("account_data.csv")
                new_data.to_csv("account_data.csv", index=False)

            else:
                new_data = pandas.DataFrame(new_dict)
                new_data.to_csv("account_data.csv", index=False)
            json_dict = {entry1.get(): {"User/Email: ":entry2.get(), "Password: ": entry3.get()}}
            if os.path.isfile("account_data.json"):
                with open("account_data.json", "r") as json_file:
                    json_data = json.load(json_file)
                    json_data.update(json_dict)
                with open("account_data.json", "w") as json_file:
                    json.dump(json_data, json_file, indent=4)
            else:
                with open("account_data.json", "w") as json_file:
                    json.dump(json_dict, json_file, indent=4)
            entry1.delete(0, len(entry1.get()))
            entry2.delete(0, len(entry2.get()))
            entry3.delete(0, len(entry3.get()))




lock_photo = tkinter.PhotoImage(file="lock.png")
canvas = tkinter.Canvas(width=320, height=320, highlightthickness=0, bg="white")
canvas.create_image(110, 160, image=lock_photo)
canvas.grid(column=1, row=0, columnspan=4)

##Labels
manager_text = tkinter.Label(text="Password Manager", font=("Courier", 50), fg="black", bg="white")
manager_text.grid(row=1, column=0, columnspan=4)
website = tkinter.Label(text="Website:", font=("Arial", 20), bg="white", fg="black")
website.grid(column=0, row=2)
entry1 = tkinter.Entry(width=23)
entry1.grid(row=2, column=1, columnspan=1)
entry1.config(bg="white", highlightthickness=0, fg="black")
entry1.focus()
search_button = tkinter.Button(text="Search", font=("Arial", 16), width=23, command=search)
search_button.grid(column=2, row=2)
search_button.config(highlightthickness=0, highlightbackground="white")

email = tkinter.Label(text="User/Email:", font=("Arial", 20), bg="white", fg="black")
email.grid(column=0, row=3)
entry2 = tkinter.Entry(width=50)
entry2.grid(row=3, column=1, columnspan=2)
entry2.insert(0, "johndoe@abc.com")
entry2.config(bg="white", highlightthickness=0, fg="black")

password = tkinter.Label(text="Password:", font=("Arial", 20), bg="white", fg="black")
password.grid(column=0, row=4)
entry3 = tkinter.Entry(width=23)
entry3.grid(row=4, column=1)
entry3.config(bg="white", highlightthickness=0, fg="black")
generate_button = tkinter.Button(text="Generate password", font=("Arial", 16), width=23, command=generate_pass)
generate_button.grid(row=4, column=2, columnspan=1)
generate_button.config(highlightthickness=0, highlightbackground="white")

add_button = tkinter.Button(text="Add Account", font=("Arial", 20), width=36, command=add)
add_button.grid(row=5, columnspan=2, column=1)
add_button.config(highlightthickness=0, highlightbackground="white")

window.mainloop()
