#import customtkinter
from customtkinter import  *

app= CTk()

app.title("my app")
app.geometry("400x150")

def clicked():
    print("button pressed")

button = CTkButton(app, text="my button", command=clicked)
button.grid(row=0, column=0, padx=20, pady=20)



# run the app
app.mainloop()