from customtkinter import *
import tkinter
import time

# dark mode
set_appearance_mode("dark")

# Основен прозорец (скрит при стартиране)
app = CTk()
app.title("Cinema Vision v1.0")
app.geometry("400x300")
app.iconbitmap("favicon.ico")
app.withdraw()  # Hide the main window initially


def center_window(window, parent=None):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    
    if parent:
        # Center relative to parent window
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
    else:
        # Center on screen
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
    
    window.geometry(f'+{x}+{y}')
    window.lift()  # Bring to top
    window.focus_force()  # Force focus
    window.grab_set()  # Make it modal (optional)



# ---------- ФУНКЦИИ ЗА БУТОНИ ----------
def open_films():
    films_window = CTkToplevel(app)
    films_window.title("Филми")
    films_window.geometry("400x300")
    films_window.iconbitmap("favicon.ico")
    films_window.resizable(False, False)
    
    # Center relative to main window and bring to front
    center_window(films_window, parent=app)
    
    label = CTkLabel(films_window, text="Филми", font=("Arial", 16))
    label.pack(pady=20)

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
loading_window = CTkToplevel(app)  # Changed to Toplevel instead of CTk
loading_window.title("Стартиране...")
loading_window.geometry("400x100")
loading_window.resizable(False, False)
loading_window.overrideredirect(True)  # Remove window decorations

# Center loading window
loading_window.update_idletasks()
width = loading_window.winfo_width()
height = loading_window.winfo_height()
x = (loading_window.winfo_screenwidth() // 2) - (width // 2)
y = (loading_window.winfo_screenheight() // 2) - (height // 2)
loading_window.geometry(f'+{x}+{y}')

progress_label = CTkLabel(loading_window, text="Моля, изчакайте...")
progress_label.pack(pady=10)

progressbar = CTkProgressBar(loading_window, width=300)
progressbar.pack(pady=10)
progressbar.set(0)

def simulate_loading():
    for i in range(101):
        progressbar.set(i/100)
        loading_window.update()
        time.sleep(0.02)
    
    loading_window.grab_release()  
    loading_window.destroy()  # Destroy the loading window
    app.deiconify()  # Show the main window
    app.eval('tk::PlaceWindow . center')  # Center the main window

# Start the loading process after a short delay
app.after(100, simulate_loading)

# Run the main application loop
app.mainloop()