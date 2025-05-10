from customtkinter import *
import tkinter
from tkinter import messagebox
import time
from PIL import Image, ImageTk
import csv
from datetime import datetime

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


# load projections (id, movie_id, room, date, time, price)
def load_projections():
    projections = []
    with open("seeders/projections.csv", newline='', encoding='windows-1251') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            projection = {
                "id": row[0],
                "movie_id": row[1],
                "room": row[2],
                "date": row[3],
                "time": row[4],
                "price": row[5],
                "tickets": row[6]
            }
            projections.append(projection)
    return projections



def load_sales():
    sales = []
    with open("seeders/sales.csv", newline='', encoding='windows-1251') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            sale = {
                "sale_id": row[0],
                "projection_id": row[1],
                "client": row[2],
                "tickets_count": row[3],
                "total_amount": row[4]
            }
            sales.append(sale)
    return sales



# ---------- FUNCTIONS ----------

# open films form
def open_films():
    # refresh the table function
    def refresh_table():
        films_window.destroy()
        open_films()


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
    def refresh_table(projections):
        projections_window.destroy()
        open_projections()

    def save_projections_to_csv(projections):
        with open("seeders/projections.csv", "w", newline="", encoding="windows-1251") as file:
            writer = csv.writer(file)
            for proj in projections:
                writer.writerow(proj)

    def open_add_projection(projections):
        def save_new_projection(projections):
            selected_movie = movie_combobox.get()
            movie_id = movie_title_to_id.get(selected_movie)
            date_str = entry_date.get().strip()
            time_str = entry_time.get().strip()
            hall = entry_hall.get().strip()
            price = entry_price.get().strip()
            tickets = entry_tickets.get().strip()

            if not (movie_id and date_str and time_str and hall and price and tickets):
                messagebox.showerror("Грешка", "Всички полета са задължителни.")
                return

            try:
                datetime.strptime(date_str, "%d.%m.%Y")
                datetime.strptime(time_str, "%H:%M")
                float(price)
                int(tickets)
            except:
                messagebox.showerror("Грешка", "Невалидна дата, час, цена или брой билети.")
                return

            new_id = str(max([int(p[0]) for p in projections] + [0]) + 1)
            projections.append([new_id, movie_id, date_str, time_str, hall, price, tickets])
            save_projections_to_csv(projections)
            add_window.destroy()
            refresh_table(projections)

        add_window = CTkToplevel(projections_window)
        add_window.title("Добавяне на прожекция")
        add_window.geometry("300x400")
        center_window(add_window, parent=projections_window)

        CTkLabel(add_window, text="Филм:").pack(pady=2)
        movie_combobox = CTkComboBox(add_window, values=list(movie_title_to_id.keys()))
        movie_combobox.pack()

        CTkLabel(add_window, text="Дата (д.м.г):").pack(pady=2)
        entry_date = CTkEntry(add_window)
        entry_date.pack()

        CTkLabel(add_window, text="Час (ч:м):").pack(pady=2)
        entry_time = CTkEntry(add_window)
        entry_time.pack()

        CTkLabel(add_window, text="Зала:").pack(pady=2)
        entry_hall = CTkEntry(add_window)
        entry_hall.pack()

        CTkLabel(add_window, text="Цена (лв):").pack(pady=2)
        entry_price = CTkEntry(add_window)
        entry_price.pack()

        CTkLabel(add_window, text="Брой билети:").pack(pady=2)
        entry_tickets = CTkEntry(add_window)
        entry_tickets.pack()

        CTkButton(add_window, text="Запази", command=lambda: save_new_projection(projections)).pack(pady=10)
        CTkButton(add_window, text="Отказ", fg_color="darkred", command=add_window.destroy).pack()

    def open_edit_projection(proj_id, projections):
        proj = [p for p in projections if p[0] == proj_id][0]

        def save_changes(projections):
            selected_movie = movie_combobox.get()
            movie_id = movie_title_to_id.get(selected_movie)
            date_str = entry_date.get().strip()
            time_str = entry_time.get().strip()
            hall = entry_hall.get().strip()
            price = entry_price.get().strip()
            tickets = entry_tickets.get().strip()

            if not (movie_id and date_str and time_str and hall and price and tickets):
                messagebox.showerror("Грешка", "Всички полета са задължителни.")
                return

            try:
                datetime.strptime(date_str, "%d.%m.%Y")
                datetime.strptime(time_str, "%H:%M")
                float(price)
                int(tickets)
            except:
                messagebox.showerror("Грешка", "Невалидна дата, час, цена или брой билети.")
                return

            proj[1] = movie_id
            proj[2] = date_str
            proj[3] = time_str
            proj[4] = hall
            proj[5] = price
            proj[6] = tickets
            save_projections_to_csv(projections)
            edit_window.destroy()
            refresh_table(projections)

        edit_window = CTkToplevel(projections_window)
        edit_window.title("Редактиране на прожекция")
        edit_window.geometry("300x400")
        center_window(edit_window, parent=projections_window)

        CTkLabel(edit_window, text="Филм:").pack(pady=2)
        movie_combobox = CTkComboBox(edit_window, values=list(movie_title_to_id.keys()))
        movie_combobox.set(movie_id_to_title.get(proj[1], ""))
        movie_combobox.pack()

        CTkLabel(edit_window, text="Дата (д.м.г):").pack(pady=2)
        entry_date = CTkEntry(edit_window)
        entry_date.insert(0, proj[2])
        entry_date.pack()

        CTkLabel(edit_window, text="Час (ч:м):").pack(pady=2)
        entry_time = CTkEntry(edit_window)
        entry_time.insert(0, proj[3])
        entry_time.pack()

        CTkLabel(edit_window, text="Зала:").pack(pady=2)
        entry_hall = CTkEntry(edit_window)
        entry_hall.insert(0, proj[4])
        entry_hall.pack()

        CTkLabel(edit_window, text="Цена (лв):").pack(pady=2)
        entry_price = CTkEntry(edit_window)
        entry_price.insert(0, proj[5])
        entry_price.pack()

        CTkLabel(edit_window, text="Брой билети:").pack(pady=2)
        entry_tickets = CTkEntry(edit_window)
        entry_tickets.insert(0, proj[6])
        entry_tickets.pack()

        CTkButton(edit_window, text="Запази", command=lambda: save_changes(projections)).pack(pady=10)
        CTkButton(edit_window, text="Отказ", fg_color="darkred", command=edit_window.destroy).pack()

    def confirm_delete_projection(proj_id, projections):
        if messagebox.askyesno("Потвърждение", "Наистина ли искате да изтриете тази прожекция?"):
            updated_projections = [p for p in projections if p[0] != proj_id]
            save_projections_to_csv(updated_projections)
            refresh_table(updated_projections)

    movies = load_movies()
    movie_id_to_title = {m["id"]: m["title"] for m in movies}
    movie_title_to_id = {v: k for k, v in movie_id_to_title.items()}

    with open("seeders/projections.csv", newline="", encoding="windows-1251") as file:
        reader = csv.reader(file)
        projections = list(reader)

    unique_halls = sorted(set(p[4] for p in projections))
    hall_var = StringVar(value="Всички")

    projections_window = CTkToplevel(app)
    projections_window.title("Прожекции")
    projections_window.geometry("700x500")
    projections_window.iconbitmap("favicon.ico")
    center_window(projections_window, parent=app)

    CTkLabel(projections_window, text="Списък с прожекции", font=("Arial", 16)).pack(pady=10)

    filter_frame = CTkFrame(projections_window)
    filter_frame.pack(pady=5)

    CTkLabel(filter_frame, text="Филтрирай по зала:").pack(side="left", padx=5)
    CTkComboBox(filter_frame, values=["Всички"] + unique_halls, variable=hall_var, width=150).pack(side="left", padx=5)

    scroll_frame = CTkScrollableFrame(projections_window, width=660, height=350)
    scroll_frame.pack()

    headers = ["ID", "Филм", "Дата", "Час", "Зала", "Цена", "Билети", "", ""]
    for i, h in enumerate(headers):
        CTkLabel(scroll_frame, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=5, pady=5)

    def draw_table(data):
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        for i, h in enumerate(headers):
            CTkLabel(scroll_frame, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=5, pady=5)

        for row_num, proj in enumerate(data, start=1):
            values = [
                proj[0],
                movie_id_to_title.get(proj[1], "Неизвестен"),
                proj[2],
                proj[3],
                proj[4],
                proj[5],
                proj[6]
            ]
            for col_num, val in enumerate(values):
                CTkLabel(scroll_frame, text=val).grid(row=row_num, column=col_num, padx=5, pady=2, sticky="w")
            CTkButton(scroll_frame, text="🖊️ ", width=30, command=lambda pid=proj[0]: open_edit_projection(pid, projections)).grid(row=row_num, column=7, padx=2)
            CTkButton(scroll_frame, text="🗑️ ", width=30, fg_color="darkred", command=lambda pid=proj[0]: confirm_delete_projection(pid, projections)).grid(row=row_num, column=8, padx=2)

    def filter_by_hall():
        selected = hall_var.get()
        filtered = [p for p in projections if p[4] == selected] if selected != "Всички" else projections
        draw_table(filtered)

    CTkButton(filter_frame, text="Филтрирай", command=filter_by_hall).pack(side="left", padx=5)

    draw_table(projections)

    CTkButton(projections_window, text="➕ Добави прожекция", command=lambda: open_add_projection(projections)).pack(pady=10)



def open_sales():
    def refresh_table(sales):
        sales_window.destroy()
        open_sales()

    def save_sales_to_csv(sales):
        with open("seeders/sales.csv", "w", newline="", encoding="windows-1251") as file:
            writer = csv.writer(file)
            for sale in sales:
                writer.writerow([sale["sale_id"], sale["projection_id"], sale["client"], sale["tickets_count"], sale["total_amount"]])

    def save_projections_to_csv(projections):
        with open("seeders/projections.csv", "w", newline="", encoding="windows-1251") as file:
            writer = csv.writer(file)
            for proj in projections:
                writer.writerow([
                    proj["id"],
                    proj["movie_id"],
                    proj["room"],
                    proj["date"],
                    proj["time"],
                    proj["price"],
                    proj["tickets"]
                ])

    def filter_sales_by_price(sales, min_price, max_price):
        try:
            min_price = float(min_price) if min_price else 0
            max_price = float(max_price) if max_price else float('inf')
        except ValueError:
            messagebox.showerror("Грешка", "Невалидни стойности за цена.")
            return

        filtered_sales = [sale for sale in sales if min_price <= float(sale["total_amount"]) <= max_price]
        draw_table(filtered_sales)

    def open_add_sale(sales):
        def save_new_sale(sales):
            selected_projection = projection_combobox.get()
            projection_id = projection_name_to_id.get(selected_projection)
            client = entry_client.get().strip()
            tickets_count = entry_tickets.get().strip()

            if not (projection_id and client and tickets_count):
                messagebox.showerror("Грешка", "Всички полета са задължителни.")
                return

            try:
                tickets_count = int(tickets_count)
            except ValueError:
                messagebox.showerror("Грешка", "Невалидна стойност за брой билети.")
                return

            # Check if enough tickets are available
            available_tickets = int(projections_by_id[projection_id]["tickets"])
            if tickets_count > available_tickets:
                messagebox.showerror("Грешка", "Недостатъчно налични билети.")
                return

            # Calculate total amount
            projection_price = float(projections_by_id[projection_id]["price"])
            total_amount = tickets_count * projection_price

            # Update available tickets
            projections_by_id[projection_id]["tickets"] = str(available_tickets - tickets_count)
            save_projections_to_csv(list(projections_by_id.values()))

            new_id = str(max([int(s["sale_id"]) for s in sales] + [0]) + 1)
            sales.append({
                "sale_id": new_id,
                "projection_id": projection_id,
                "client": client,
                "tickets_count": tickets_count,
                "total_amount": f"{total_amount:.2f}"
            })
            save_sales_to_csv(sales)
            add_window.destroy()
            refresh_table(sales)

        add_window = CTkToplevel(sales_window)
        add_window.title("Добавяне на продажба")
        add_window.geometry("300x300")
        center_window(add_window, parent=sales_window)

        CTkLabel(add_window, text="Прожекция:").pack(pady=2)
        projection_combobox = CTkComboBox(add_window, values=list(projection_name_to_id.keys()))
        projection_combobox.pack()

        CTkLabel(add_window, text="Клиент:").pack(pady=2)
        entry_client = CTkEntry(add_window)
        entry_client.pack()

        CTkLabel(add_window, text="Брой билети:").pack(pady=2)
        entry_tickets = CTkEntry(add_window)
        entry_tickets.pack()

        CTkButton(add_window, text="Запази", command=lambda: save_new_sale(sales)).pack(pady=10)
        CTkButton(add_window, text="Отказ", fg_color="darkred", command=add_window.destroy).pack()

    def open_edit_sale(sale_id, sales):
        sale = [s for s in sales if s["sale_id"] == sale_id][0]

        def save_changes(sales):
            selected_projection = projection_combobox.get()
            projection_id = projection_name_to_id.get(selected_projection)
            client = entry_client.get().strip()
            tickets_count = entry_tickets.get().strip()
            total_amount = entry_total_amount.get().strip()

            if not (projection_id and client and tickets_count and total_amount):
                messagebox.showerror("Грешка", "Всички полета са задължителни.")
                return

            try:
                int(tickets_count)
                float(total_amount)
            except:
                messagebox.showerror("Грешка", "Невалидни стойности за билети или сума.")
                return

            sale["projection_id"] = projection_id
            sale["client"] = client
            sale["tickets_count"] = tickets_count
            sale["total_amount"] = total_amount
            save_sales_to_csv(sales)
            edit_window.destroy()
            refresh_table(sales)

        edit_window = CTkToplevel(sales_window)
        edit_window.title("Редактиране на продажба")
        edit_window.geometry("300x400")
        center_window(edit_window, parent=sales_window)

        CTkLabel(edit_window, text="Прожекция:").pack(pady=2)
        projection_combobox = CTkComboBox(edit_window, values=list(projection_name_to_id.keys()))
        projection_combobox.set(projection_id_to_name.get(sale["projection_id"], ""))
        projection_combobox.pack()

        CTkLabel(edit_window, text="Клиент:").pack(pady=2)
        entry_client = CTkEntry(edit_window)
        entry_client.insert(0, sale["client"])
        entry_client.pack()

        CTkLabel(edit_window, text="Брой билети:").pack(pady=2)
        entry_tickets = CTkEntry(edit_window)
        entry_tickets.insert(0, sale["tickets_count"])
        entry_tickets.pack()

        CTkLabel(edit_window, text="Обща сума:").pack(pady=2)
        entry_total_amount = CTkEntry(edit_window)
        entry_total_amount.insert(0, sale["total_amount"])
        entry_total_amount.pack()

        CTkButton(edit_window, text="Запази", command=lambda: save_changes(sales)).pack(pady=10)
        CTkButton(edit_window, text="Отказ", fg_color="darkred", command=edit_window.destroy).pack()

    def confirm_delete_sale(sale_id, sales):
        if messagebox.askyesno("Потвърждение", "Наистина ли искате да изтриете тази продажба?"):
            updated_sales = [s for s in sales if s["sale_id"] != sale_id]
            save_sales_to_csv(updated_sales)
            refresh_table(updated_sales)


    def export_sales_to_report(sales):
        try:
            with open("report.txt", "w", encoding="utf-8") as file:
                file.write("Продажби:\n")
                file.write(f"{'ID':<5} {'Прожекция':<20} {'Клиент':<15} {'Билети':<10} {'Сума':<10}\n")
                file.write("-" * 60 + "\n")
                total_profit = 0
                for sale in sales:
                    projection_name = projection_id_to_name.get(sale["projection_id"])
                    file.write(f"{sale['sale_id']:<5} {projection_name:<20} {sale['client']:<15} {sale['tickets_count']:<10} {sale['total_amount']:<10}\n")
                    total_profit += float(sale["total_amount"])
                file.write("-" * 60 + "\n")
                file.write(f"Обща печалба: {total_profit:.2f} лв\n")
            messagebox.showinfo("Успех", "Докладът е успешно експортиран в 'report.txt'.")
        except Exception as e:
            messagebox.showerror("Грешка", f"Неуспешно експортиране: {e}")



    def draw_table(data):
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        headers = ["ID", "Прожекция", "Филм", "Клиент", "Брой билети", "Обща сума", "", ""]
        for i, h in enumerate(headers):
            CTkLabel(scroll_frame, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=5, pady=5)

        for row_num, sale in enumerate(data, start=1):
            projection = projections_by_id.get(sale["projection_id"], {})
            movie_name = movies_by_id.get(projection.get("movie_id", ""), "Неизвестен филм")
            values = [
                sale["sale_id"],
                projection_id_to_name.get(sale["projection_id"], "Неизвестна прожекция"),
                movie_name,
                sale["client"],
                sale["tickets_count"],
                sale["total_amount"]
            ]
            for col_num, val in enumerate(values):
                CTkLabel(scroll_frame, text=val).grid(row=row_num, column=col_num, padx=5, pady=2, sticky="w")
            CTkButton(scroll_frame, text="🖊️ ", width=30, command=lambda sid=sale["sale_id"]: open_edit_sale(sid, sales)).grid(row=row_num, column=6, padx=2)
            CTkButton(scroll_frame, text="🗑️ ", width=30, fg_color="darkred", command=lambda sid=sale["sale_id"]: confirm_delete_sale(sid, sales)).grid(row=row_num, column=7, padx=2)

    projections = load_projections()
    sales = load_sales()
    movies = load_movies()

    projections_by_id = {p["id"]: p for p in projections}
    movies_by_id = {m["id"]: m["title"] for m in movies}
    projection_id_to_name = {p["id"]: f'{p["date"]} {p["time"]} - {p["room"]}' for p in projections}
    projection_name_to_id = {v: k for k, v in projection_id_to_name.items()}

    sales_window = CTkToplevel(app)
    sales_window.title("Продажби")
    sales_window.geometry("700x550")
    sales_window.iconbitmap("favicon.ico")
    center_window(sales_window, parent=app)

    CTkLabel(sales_window, text="Списък с продажби", font=("Arial", 16)).pack(pady=10)

    # Filter frame for price search
    filter_frame = CTkFrame(sales_window)
    filter_frame.pack(pady=5)

    CTkLabel(filter_frame, text="Минимална цена:").pack(side="left", padx=5)
    entry_min_price = CTkEntry(filter_frame, width=100)
    entry_min_price.pack(side="left", padx=5)

    CTkLabel(filter_frame, text="Максимална цена:").pack(side="left", padx=5)
    entry_max_price = CTkEntry(filter_frame, width=100)
    entry_max_price.pack(side="left", padx=5)

    CTkButton(filter_frame, text="Търси", command=lambda: filter_sales_by_price(sales, entry_min_price.get(), entry_max_price.get())).pack(side="left", padx=5)

    scroll_frame = CTkScrollableFrame(sales_window, width=660, height=350)
    scroll_frame.pack()

    draw_table(sales)

    CTkButton(sales_window, text="➕ Добави продажба", command=lambda: open_add_sale(sales)).pack(pady=10)
    CTkButton(sales_window, text="📄 Експортирай", command=lambda: export_sales_to_report(sales)).pack(pady=10)



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