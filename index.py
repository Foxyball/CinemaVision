from customtkinter import *
import tkinter

# dark mode
set_appearance_mode("dark")

# Основен прозорец (скрит при стартиране)
app = CTk()
app.title("Cinema Vision v1.0")
app.geometry("400x300")
app.iconbitmap("favicon.ico")
app.withdraw()

# ---------- ФУНКЦИИ ЗА БУТОНИ ----------
def open_films():
    print("Филми")

def open_projections():
    print("Прожекции")

def open_sales():
    print("Продажби")

def open_reports():
    print("Отчети")


# ---------- СЪЗДАВАНЕ НА МЕНЮ ----------
menu = tkinter.Menu(app)

file_menu = tkinter.Menu(menu, tearoff=0)
file_menu.add_command(label="Нов филм", command=open_films)
file_menu.add_command(label="Нова прожекция", command=open_projections)
file_menu.add_command(label="Нова продажба", command=open_sales)
file_menu.add_separator()
file_menu.add_command(label="Изход", command=app.quit)
menu.add_cascade(label="Файл", menu=file_menu)

help_menu = tkinter.Menu(menu, tearoff=0)
help_menu.add_command(label="За приложението", command=lambda: print("Cinema Vision v1.0"))
menu.add_cascade(label="Помощ", menu=help_menu)

app.config(menu=menu)


# ---------- СЪДЪРЖАНИЕ НА ОСНОВНИЯ ПРОЗОРЕЦ ----------
label_title = CTkLabel(app, text="Cinema Vision", font=("Arial", 20))
label_title.pack(pady=10)

CTkButton(app, text="Филми", fg_color="red", command=open_films).pack(pady=5)
CTkButton(app, text="Прожекции", command=open_projections).pack(pady=5)
CTkButton(app, text="Продажби", command=open_sales).pack(pady=5)
CTkButton(app, text="Отчети", command=open_reports).pack(pady=5)


# ---------- ПРОЗОРЕЦ ЗА ЗАРЕЖДАНЕ ----------
loading_window = CTk()
loading_window.title("Стартиране...")
loading_window.geometry("400x100")
loading_window.eval('tk::PlaceWindow . center')
loading_window.resizable(False, False)

progress_label = CTkLabel(loading_window, text="Моля, изчакайте...")
progress_label.pack(pady=10)

progressbar = CTkProgressBar(loading_window, width=300)
progressbar.pack(pady=10)
progressbar.set(0)

def start_main_app():
    loading_window.destroy()
    app.deiconify()

def simulate_loading(i=0):
    if i <= 100:
        progressbar.set(i / 100)
        loading_window.after(15, lambda: simulate_loading(i + 1))
    else:
        start_main_app()

simulate_loading()
loading_window.mainloop()
