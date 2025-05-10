from customtkinter import *
import tkinter
from tkinter import messagebox
import time
from PIL import Image, ImageTk
import csv

# dark mode
set_appearance_mode("dark")

# main form
app = CTk()
app.title("Cinema Vision v1.0")
app.geometry("400x300")
app.iconbitmap("favicon.ico")
app.withdraw()  # Hide the form on start

# end of main form


# Load the background image
bg_image = Image.open("cover.jpg")
bg_image = bg_image.resize((2000, 1000))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = CTkLabel(app, image=bg_photo, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# end of background image



def center_window(window, parent=None):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    
    if parent:
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
    else:
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
    
    window.geometry(f'+{x}+{y}')
    window.lift()  # Bring to top
    window.focus_force()  # Force focus
    window.grab_set()  # Make it modal

# end of center window function




# load genres (id, name)
def load_genres():
    genres = {}
    with open("seeders/genres.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            genres[row[0]] = row[1]
    return genres

# end of load genres


#  load movies (id, title, genre_id, duration, rating)
def load_movies():
    movies = []
    with open("seeders/movies.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            movie = {
                "id": row[0],
                "title": row[1],
                "genre_id": row[2],
                "duration": row[3],
                "rating": row[4]
            }
            movies.append(movie)
    return movies

# end of load movies

# ---------- FUNCTIONS ----------
# save movies to CSV
def save_movies(movies):
    with open("seeders/movies.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for movie in movies:
            writer.writerow([
                movie["id"],
                movie["title"],
                movie["genre_id"],
                movie["duration"],
                movie["rating"]
            ])

# end of save movies

# open films form
def open_films():
    # refresh the table function
    def refresh_table():
        films_window.destroy()
        open_films()


    # confirm delete movie
    def confirm_delete(movie_to_delete):
        response = messagebox.askyesno(
            title="Потвърждение за изтриване",
            message=f'Наистина ли искате да изтриете "{movie_to_delete["title"]}"?'
        )
        if response:
            updated_movies = [m for m in movies if m["id"] != movie_to_delete["id"]]
            save_movies(updated_movies)
            refresh_table()


    # open add movie form
    def open_add_form():
        # function to save new movie
        def save_new_movie():
            new_title = entry_title.get()
            new_genre = genre_combobox.get()
            new_duration = entry_duration.get()
            new_rating = entry_rating.get()

            # check if all fields are filled [validation]
            if not (new_title and new_genre and new_duration and new_rating):
                messagebox.showerror("Грешка", "Всички полета са задължителни.")
                return

           # auto increment id +1
            new_id = max(int(m["id"]) for m in movies) + 1 

            movies.append({
                "id": new_id,
                "title": new_title,
                "genre_id": genre_reverse[new_genre],
                "duration": new_duration,
                "rating": new_rating
            })
            save_movies(movies)
            add_window.destroy()
            refresh_table()

        add_window = CTkToplevel(films_window)
        add_window.title("Добавяне на филм")
        add_window.geometry("300x300")
        center_window(add_window, parent=films_window)

        CTkLabel(add_window, text="Заглавие:").pack(pady=2)
        entry_title = CTkEntry(add_window)
        entry_title.pack(pady=2)

        CTkLabel(add_window, text="Жанр:").pack(pady=2)
        genre_combobox = CTkComboBox(add_window, values=list(genre_reverse.keys()))
        genre_combobox.pack(pady=2)

        CTkLabel(add_window, text="Продължителност:").pack(pady=2)
        entry_duration = CTkEntry(add_window)
        entry_duration.pack(pady=2)

        CTkLabel(add_window, text="Рейтинг:").pack(pady=2)
        entry_rating = CTkEntry(add_window)
        entry_rating.pack(pady=2)

        CTkButton(add_window, text="Запази", command=save_new_movie).pack(pady=10)
        CTkButton(add_window, text="Отказ", fg_color="darkred", hover_color="darkred", command=add_window.destroy).pack(pady=2)

# end of add movie form

    # open edit movie form
    def open_edit_form(movie):
        def save_changes():
            movie["title"] = entry_title.get()
            movie["genre_id"] = genre_reverse[genre_combobox.get()]
            movie["duration"] = entry_duration.get()
            movie["rating"] = entry_rating.get()
            save_movies(movies)
            edit_window.destroy()
            refresh_table()

        edit_window = CTkToplevel(films_window)
        edit_window.title("Редактиране на филм")
        edit_window.geometry("300x250")
        center_window(edit_window, parent=films_window)

        CTkLabel(edit_window, text="Заглавие:").pack(pady=2)
        entry_title = CTkEntry(edit_window)
        entry_title.insert(0, movie["title"])
        entry_title.pack(pady=2)

        CTkLabel(edit_window, text="Жанр:").pack(pady=2)
        genre_combobox = CTkComboBox(edit_window, values=list(genre_reverse.keys()))
        genre_combobox.set(genres.get(movie["genre_id"], "Неизвестен"))
        genre_combobox.pack(pady=2)

        CTkLabel(edit_window, text="Продължителност:").pack(pady=2)
        entry_duration = CTkEntry(edit_window)
        entry_duration.insert(0, movie["duration"])
        entry_duration.pack(pady=2)

        CTkLabel(edit_window, text="Рейтинг:").pack(pady=2)
        entry_rating = CTkEntry(edit_window)
        entry_rating.insert(0, movie["rating"])
        entry_rating.pack(pady=2)

        CTkButton(edit_window, text="Запази промените", command=save_changes).pack(pady=10)
        CTkButton(edit_window, text="Отказ", fg_color="darkred", hover_color="darkred", command=edit_window.destroy).pack(pady=2)

# end of edit movie form

    # load genres and movies
    genres = load_genres()
    genre_reverse = {v: k for k, v in genres.items()}
    movies = load_movies()

    films_window = CTkToplevel(app)
    films_window.title("Филми")
    films_window.geometry("640x440")
    films_window.iconbitmap("favicon.ico")
    films_window.resizable(False, False)
    center_window(films_window, parent=app)

    CTkLabel(films_window, text="Списък с филми", font=("Arial", 16)).pack(pady=10)

    scroll_frame = CTkScrollableFrame(films_window, width=600, height=300)
    scroll_frame.pack()

    headers = ["ID", "Заглавие", "Жанр", "Продълж.", "Рейтинг", "", ""]

    for col, h in enumerate(headers):
        CTkLabel(scroll_frame, text=h, font=("Arial", 12, "bold")).grid(row=0, column=col, padx=5, pady=5)

    for row, movie in enumerate(movies, start=1):
        CTkLabel(scroll_frame, text=movie["id"]).grid(row=row, column=0, sticky="nsew", padx=2, pady=2)
        CTkLabel(scroll_frame, text=movie["title"]).grid(row=row, column=1, sticky="nsew", padx=2, pady=2)
        CTkLabel(scroll_frame, text=genres.get(movie["genre_id"], "Неизвестен")).grid(row=row, column=2, sticky="nsew", padx=2, pady=2)
        CTkLabel(scroll_frame, text=movie["duration"]).grid(row=row, column=3, sticky="nsew", padx=2, pady=2)
        CTkLabel(scroll_frame, text=movie["rating"]).grid(row=row, column=4, sticky="nsew", padx=2, pady=2)

        CTkButton(scroll_frame, text="🖊️", width=30, command=lambda m=movie: open_edit_form(m)).grid(row=row, column=5, padx=2, pady=2)
        CTkButton(scroll_frame, text="🗑️", width=30, fg_color="darkred", command=lambda m=movie: confirm_delete(m)).grid(row=row, column=6, padx=2, pady=2)

    CTkButton(films_window, text="➕ Добави нов филм", command=open_add_form).pack(pady=10)

# end of open_films


def open_projections():
    print("Прожекции")

def open_sales():
    print("Продажби")

def open_reports():
    print("Отчети")

def open_genres():
    def refresh_table():
        genres_window.destroy()
        open_genres()

    def save_genres_to_csv():
        with open("seeders/genres.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for genre_id, name in genres.items():
                writer.writerow([genre_id, name])

    def open_add_genre():
        def save_new_genre():
            new_name = entry_name.get().strip()
            if not new_name:
                messagebox.showerror("Грешка", "Името е задължително.")
                return
            
            new_id = str(max([int(i) for i in genres.keys()] + [0]) + 1)
            genres[new_id] = new_name
            save_genres_to_csv()
            add_window.destroy()
            refresh_table()

        add_window = CTkToplevel(genres_window)
        add_window.title("Добавяне на жанр")
        add_window.geometry("250x150")
        center_window(add_window, parent=genres_window)

        CTkLabel(add_window, text="Име на жанр:").pack(pady=5)
        entry_name = CTkEntry(add_window)
        entry_name.pack(pady=5)

        CTkButton(add_window, text="Запази", command=save_new_genre).pack(pady=10)
        CTkButton(add_window, text="Отказ", fg_color="darkred", command=add_window.destroy).pack()

    def open_edit_genre(genre_id):
        def save_changes():
            new_name = entry_name.get().strip()
            if not new_name:
                messagebox.showerror("Грешка", "Името е задължително.")
                return
            genres[genre_id] = new_name
            save_genres_to_csv()
            edit_window.destroy()
            refresh_table()

        edit_window = CTkToplevel(genres_window)
        edit_window.title("Редактиране на жанр")
        edit_window.geometry("250x150")
        center_window(edit_window, parent=genres_window)

        CTkLabel(edit_window, text="Име на жанр:").pack(pady=5)
        entry_name = CTkEntry(edit_window)
        entry_name.insert(0, genres[genre_id])
        entry_name.pack(pady=5)

        CTkButton(edit_window, text="Запази", command=save_changes).pack(pady=10)
        CTkButton(edit_window, text="Отказ", fg_color="darkred", command=edit_window.destroy).pack()

    def confirm_delete_genre(genre_id):
        if messagebox.askyesno("Потвърждение", f"Наистина ли искате да изтриете жанра: {genres[genre_id]}?"):
            del genres[genre_id]
            save_genres_to_csv()
            refresh_table()

    genres = load_genres()

    genres_window = CTkToplevel(app)
    genres_window.title("Жанрове")
    genres_window.geometry("400x400")
    genres_window.iconbitmap("favicon.ico")
    center_window(genres_window, parent=app)

    CTkLabel(genres_window, text="Списък с жанрове", font=("Arial", 16)).pack(pady=10)

    scroll_frame = CTkScrollableFrame(genres_window, width=360, height=250)
    scroll_frame.pack()

    CTkLabel(scroll_frame, text="ID", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
    CTkLabel(scroll_frame, text="Име", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=5)

    row = 1
    for genre_id, name in genres.items():
        CTkLabel(scroll_frame, text=genre_id).grid(row=row, column=0, padx=5, pady=2, sticky="w")
        CTkLabel(scroll_frame, text=name).grid(row=row, column=1, padx=5, pady=2, sticky="w")
        CTkButton(scroll_frame, text="🖊️", width=30, command=lambda g=genre_id: open_edit_genre(g)).grid(row=row, column=2, padx=2)
        CTkButton(scroll_frame, text="🗑️", width=30, fg_color="darkred", command=lambda g=genre_id: confirm_delete_genre(g)).grid(row=row, column=3, padx=2)
        row += 1

    CTkButton(genres_window, text="➕ Добави нов жанр", command=open_add_genre).pack(pady=10)

# end of functions





# Context menu navigation
menu = tkinter.Menu(app)

file_menu = tkinter.Menu(menu, tearoff=0)
file_menu.add_command(label="Нов филм", command=open_films)
file_menu.add_command(label="Нов жанр", command=open_genres)
file_menu.add_command(label="Нова прожекция", command=open_projections)
file_menu.add_command(label="Нова продажба", command=open_sales)
file_menu.add_separator()
file_menu.add_command(label="Изход", command=app.quit)
menu.add_cascade(label="Файл", menu=file_menu)

help_menu = tkinter.Menu(menu, tearoff=0)
help_menu.add_command(label="За приложението", command=lambda: print("Cinema Vision v1.0"))
menu.add_cascade(label="Помощ", menu=help_menu)

app.config(menu=menu)

#end of menu navigation

# buttons in main window
label_title = CTkLabel(app, text="Cinema Vision", font=("Arial", 20))
label_title.pack(pady=10)

CTkButton(app, text="Филми",  command=open_films).pack(pady=5)
CTkButton(app, text="Жанрове", command=open_genres).pack(pady=5)
CTkButton(app, text="Прожекции", command=open_projections).pack(pady=5)
CTkButton(app, text="Продажби", command=open_sales).pack(pady=5)
CTkButton(app, text="Отчети", command=open_reports).pack(pady=5)

# end of buttons in main window

# end of main window




# loading window on start
loading_window = CTkToplevel(app)
loading_window.title("Стартиране...")
loading_window.geometry("400x100")
loading_window.resizable(False, False)
loading_window.overrideredirect(True)  # removes close button and title bar

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

# simulate loading process
def simulate_loading():
    for i in range(101):
        progressbar.set(i/100)
        loading_window.update()
        time.sleep(0.02)
    
    loading_window.grab_release()  
    loading_window.destroy()
    app.deiconify()
    app.eval('tk::PlaceWindow . center')

# delay for 1 second
app.after(100, simulate_loading)

# Run the main application loop
app.mainloop()