from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
               'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    password_list += [choice(letters) for i in range(randint(8, 10))]
    password_list += [choice(symbols) for i in range(randint(2, 4))]
    password_list += [choice(numbers) for i in range(randint(2, 4))]

    # for char in range(nr_letters):
    #     password_list.append(random.choice(letters))

    # for char in range(nr_symbols):
    #     password_list += random.choice(symbols)

    # for char in range(nr_numbers):
    #     password_list += random.choice(numbers)

    shuffle(password_list)

    password = "".join(password_list)
    # for char in password_list:
    #     password += char
    password_input.delete(0, END)
    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- Search For Password ------------------------- #


def search():
    website = site_input.get()
    if website == "":
        return
    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(
                title="Password", message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showerror(
                title="Password", message="No details for the website exists.")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():

    website = site_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if not website.strip() or not password.strip():
        messagebox.showerror(title="Empty Fields Found",
                             message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(
            title=website, message=f"These are the details entered: \nEmail: {email}\nPassword: {password} \nIs it ok to save?")

        if is_ok:
            try:
                with open("passwords.json", "r") as file:
                    # file.write(
                    #     f"{website} | {email} | {password}\n")
                    # How to write to a JSON file
                    # json.dump(new_data, file, indent=4)

                    # Reading old data
                    data = json.load(file)

            except FileNotFoundError:
                with open("passwords.json", "w")as file:
                    json.dump(new_data, file, indent=4)
            else:

                # Updating old data with new data
                data.update(new_data)

                with open("passwords.json", "w") as file:
                    # Saving updated data
                    json.dump(data, file, indent=4)
            finally:
                site_input.delete(0, END)
                password_input.delete(0, END)
                email_input.delete(0, END)
                email_input.insert(0, "test@email.com")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, width=500, height=300)

canvas = Canvas(width=200, height=200)
password_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=password_img)
canvas.grid(row=0, column=1)

# Labels
website = Label(text="Website: ")
website.grid(row=1, column=0)

email = Label(text="Email/Username:")
email.grid(row=2, column=0)

password = Label(text="Password:")
password.grid(row=3, column=0)

# Inputs
site_input = Entry(width=33)
site_input.grid(row=1, column=1)
site_input.focus()

email_input = Entry(width=52)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0, "test@email.com")

password_input = Entry(width=33)
password_input.grid(row=3, column=1)

# Buttons
gen_password = Button(text="Generate Password", command=generate_password)
gen_password.grid(row=3, column=2)

add = Button(text="Add", width=44, command=save_password)
add.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=14, command=search)
search_button.grid(row=1, column=2)

window.mainloop()
