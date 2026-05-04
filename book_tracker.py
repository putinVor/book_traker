import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ========== GitHub репозиторий ==========
GITHUB_URL = "https://github.com/putinVor/book_traker" 
class BookTracker:
    """
    Приложение "Book Tracker" - Трекер прочитанных книг.
    Позволяет добавлять, просматривать, фильтровать и удалять книги.
    Данные сохраняются в JSON-файл.
    """
    
    def __init__(self):
        # Создание главного окна
        self.window = tk.Tk()
        self.window.title("📚 Book Tracker - Трекер прочитанных книг")
        self.window.geometry("800x550")
        self.window.configure(bg="#f5f0e8")
        
        # Загрузка данных из файла
        self.books = self.load_data()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление таблицы
        self.update_table()
    
    # ========== Работа с JSON ==========
    def load_data(self):
        """Загружает список книг из JSON-файла."""
        try:
            with open("books.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_data(self):
        """Сохраняет список книг в JSON-файл."""
        with open("books.json", "w", encoding="utf-8") as file:
            json.dump(self.books, file, ensure_ascii=False, indent=4)
    
    # ========== Интерфейс ==========
    def create_widgets(self):
        """Создаёт все элементы интерфейса."""
        
        # Заголовок
        title_label = tk.Label(
            self.window,
            text="📚 Book Tracker - Мои прочитанные книги",
            font=("Arial", 18, "bold"),
            bg="#f5f0e8",
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # ===== Фрейм для ввода данных =====
        input_frame = tk.LabelFrame(
            self.window,
            text="📖 Добавить новую книгу",
            font=("Arial", 12, "bold"),
            bg="#f5f0e8",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        input_frame.pack(pady=10, padx=20, fill="x")
        
        # Название книги
        tk.Label(input_frame, text="📕 Название книги:", bg="#f5f0e8", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Автор
        tk.Label(input_frame, text="✍️ Автор:", bg="#f5f0e8", font=("Arial", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.author_entry = tk.Entry(input_frame, width=20, font=("Arial", 10))
        self.author_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Жанр
        tk.Label(input_frame, text="🎭 Жанр:", bg="#f5f0e8", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.genre_entry = tk.Entry(input_frame, width=20, font=("Arial", 10))
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Количество страниц
        tk.Label(input_frame, text="📄 Количество страниц:", bg="#f5f0e8", font=("Arial", 10)).grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.pages_entry = tk.Entry(input_frame, width=10, font=("Arial", 10))
        self.pages_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Кнопка "Добавить книгу"
        add_button = tk.Button(
            input_frame,
            text="➕ Добавить книгу",
            command=self.add_book,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            padx=10,
            pady=5
        )
        add_button.grid(row=2, column=0, columnspan=4, pady=10)
        
        # ===== Фрейм для фильтрации =====
        filter_frame = tk.LabelFrame(
            self.window,
            text="🔍 Фильтрация книг",
            font=("Arial", 12, "bold"),
            bg="#f5f0e8",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        filter_frame.pack(pady=10, padx=20, fill="x")
        
        # Фильтр по жанру
        tk.Label(filter_frame, text="🎭 Фильтр по жанру:", bg="#f5f0e8", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.filter_genre_entry = tk.Entry(filter_frame, width=20, font=("Arial", 10))
        self.filter_genre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Фильтр по страницам (>)
        tk.Label(filter_frame, text="📄 Страниц больше (>):", bg="#f5f0e8", font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5)
        self.filter_pages_entry = tk.Entry(filter_frame, width=10, font=("Arial", 10))
        self.filter_pages_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Кнопка "Применить фильтр"
        filter_button = tk.Button(
            filter_frame,
            text="🔍 Применить фильтр",
            command=self.apply_filter,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        filter_button.grid(row=0, column=4, padx=10, pady=5)
        
        # Кнопка "Сбросить фильтр"
        reset_button = tk.Button(
            filter_frame,
            text="🔄 Сбросить фильтр",
            command=self.reset_filter,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        reset_button.grid(row=0, column=5, padx=10, pady=5)
        
        # ===== Таблица для отображения книг =====
        table_frame = tk.Frame(self.window, bg="#f5f0e8")
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview (таблица)
        columns = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Настройка колонок
        self.tree.heading("title", text="📕 Название книги")
        self.tree.heading("author", text="✍️ Автор")
        self.tree.heading("genre", text="🎭 Жанр")
        self.tree.heading("pages", text="📄 Страниц")
        
        self.tree.column("title", width=250)
        self.tree.column("author", width=150)
        self.tree.column("genre", width=150)
        self.tree.column("pages", width=80)
        
        self.tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Кнопка "Удалить выбранную"
        delete_button = tk.Button(
            self.window,
            text="🗑️ Удалить выбранную книгу",
            command=self.delete_book,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            padx=10,
            pady=5
        )
        delete_button.pack(pady=5)
        
        # Строка с ссылкой на GitHub
        github_label = tk.Label(
            self.window,
            text=f"📂 GitHub: {GITHUB_URL}",
            font=("Arial", 8),
            bg="#f5f0e8",
            fg="#7f8c8d"
        )
        github_label.pack(side=tk.BOTTOM, pady=5)
    
    # ========== Логика работы ==========
    def add_book(self):
        """Добавляет новую книгу в список."""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()
        
        # ===== ВАЛИДАЦИЯ =====
        if not title:
            messagebox.showwarning("Ошибка", "Введите название книги!")
            return
        
        if not author:
            messagebox.showwarning("Ошибка", "Введите автора книги!")
            return
        
        if not genre:
            messagebox.showwarning("Ошибка", "Введите жанр книги!")
            return
        
        if not pages:
            messagebox.showwarning("Ошибка", "Введите количество страниц!")
            return
        
        try:
            pages_int = int(pages)
            if pages_int <= 0:
                messagebox.showwarning("Ошибка", "Количество страниц должно быть положительным числом!")
                return
        except ValueError:
            messagebox.showwarning("Ошибка", "Количество страниц должно быть числом!")
            return
        
        # Добавление книги
        new_book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages_int
        }
        self.books.append(new_book)
        self.save_data()
        
        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)
        
        # Обновление таблицы
        self.update_table()
        
        messagebox.showinfo("Успех", f"Книга \"{title}\" добавлена!")
    
    def delete_book(self):
        """Удаляет выбранную книгу."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите книгу для удаления!")
            return
        
        index = int(selected[0])
        removed_book = self.books.pop(index)
        self.save_data()
        self.update_table()
        
        messagebox.showinfo("Удалено", f"Книга \"{removed_book['title']}\" удалена!")
    
    def update_table(self, filtered_books=None):
        """Обновляет таблицу книг."""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Данные для отображения
        display_books = filtered_books if filtered_books is not None else self.books
        
        # Заполнение таблицы
        for i, book in enumerate(display_books):
            self.tree.insert("", tk.END, iid=i, values=(
                book["title"],
                book["author"],
                book["genre"],
                book["pages"]
            ))
    
    def apply_filter(self):
        """Применяет фильтрацию книг."""
        filter_genre = self.filter_genre_entry.get().strip()
        filter_pages_str = self.filter_pages_entry.get().strip()
        
        filtered = self.books.copy()
        
        # Фильтр по жанру (точное совпадение, без учёта регистра)
        if filter_genre:
            filtered = [b for b in filtered if b["genre"].lower() == filter_genre.lower()]
        
        # Фильтр по страницам (>)
        if filter_pages_str:
            try:
                filter_pages = int(filter_pages_str)
                filtered = [b for b in filtered if b["pages"] > filter_pages]
            except ValueError:
                messagebox.showwarning("Ошибка", "Количество страниц для фильтра должно быть числом!")
                return
        
        self.update_table(filtered)
        
        if filtered:
            messagebox.showinfo("Фильтр", f"Найдено {len(filtered)} книг")
        else:
            messagebox.showinfo("Фильтр", "Книг не найдено")
    
    def reset_filter(self):
        """Сбрасывает фильтрацию."""
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_pages_entry.delete(0, tk.END)
        self.update_table()
    
    def run(self):
        """Запускает главный цикл приложения."""
        self.window.mainloop()


# ========== Запуск программы ==========
if __name__ == "__main__":
    app = BookTracker()
    app.run()
