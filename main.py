from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for char in range(nr_letters)]
    password_list += [random.choice(symbols) for char in range(nr_symbols)]
    password_list += [random.choice(numbers) for char in range(nr_numbers)]
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)



# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_text = website_entry.get()
    email_username_text = email_username_entry.get()
    password_text = password_entry.get()
    new_data = {
        website_text: {
            "email": email_username_text,
            "password": password_text,
        }
    }

    if len(website_text) == 0 or len(email_username_text) == 0 or len(password_text) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any field empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD------------------------------- #
def find_password():
    website_text = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            # Reading old data
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showwarning(
            title="Error", message="No Data File Found."
        )
    else:
        try:
            messagebox.showinfo(
                title=website_text, message=f"\nEmail:\n{data[website_text]['email']}"
                                            f"\nPassword:\n{data[website_text]['password']}")
        except KeyError:
            messagebox.showwarning(
                title="Error", message="No details for the website exists."
            )


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)


# Label
# website label
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
# email/username label
email_username_label = Label(text="Email/Username:")
email_username_label.grid(column=0, row=2)
# password label
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)


# Entry
# website entry
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()
# email/username entry
email_username_entry = Entry(width=39)
email_username_entry.grid(column=1, row=2, columnspan=2)
email_username_entry.insert(0, "username@gmail.com")
# password entry
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)


# Button
# generate password button
gen_password_button = Button(text="Generate Password", command=password_generator)
gen_password_button.grid(column=2, row=3)
# add button
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)
# search button
search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(column=2, row=1)


window.mainloop()

