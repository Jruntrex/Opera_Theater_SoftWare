import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from datetime import datetime
import os
import json
from models.performance import Performance
from config import COLORS

FONTS = {
    "header": ("Arial", 24, "bold"),
    "title": ("Arial", 18, "bold"),
    "large": ("Arial", 16, "bold"),
    "regular": ("Arial", 14)
}

class AdminPerformanceManager(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Керування виставами")
        self.geometry("900x840+150+50")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.configure(fg_color=COLORS["background"])
        self.grab_set()

        self.minsize(800, 600)
        self.resizable(True, True)

        self.selected_performance = None
        self.json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_performance.json")

        # Створюємо порожній JSON, якщо файл не існує
        if not os.path.exists(self.json_path):
            os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump({"opera": [], "concert": [], "ballet": []}, f, ensure_ascii=False, indent=2)

        self.create_widgets()
        self.load_performances()

    def on_closing(self):
        self.destroy()

    def create_widgets(self):
        # Головний контейнер
        self.main_container = ctk.CTkFrame(self, fg_color=COLORS["background"], corner_radius=10)
        self.main_container.pack(fill="x", expand=True, padx=20, pady=10, anchor="center")

        # Заголовок
        ctk.CTkLabel(
            self.main_container,
            text="Керування виставами",
            font=FONTS["header"],
            text_color=COLORS["text"],
            anchor="center"
        ).pack(pady=(5, 10), fill="x")

        # Секція списку вистав
        self.performance_list_frame = ctk.CTkScrollableFrame(
            self.main_container,
            fg_color=COLORS["white"],
            height=400,
            corner_radius=10,
            border_width=2,
            border_color=COLORS["primary"]
        )
        self.performance_list_frame.pack(fill="x", padx=10, pady=5, anchor="center")

        # Секція форми
        self.form_frame = ctk.CTkFrame(self.main_container, fg_color=COLORS["white"], corner_radius=10)
        self.form_frame.pack(fill="x", padx=10, pady=5, anchor="center")

        fields = [
            ("Назва:", "title"),
            ("Дата (РРРР-ММ-ДД):", "date"),
            ("Час (ГГ:ХХ):", "time"),
            ("Опис:", "description"),
            ("Ціна квитка:", "price"),
            ("Автор:", "author"),
            ("Зображення (шлях):", "image")
        ]
        self.entries = {}
        for i, (label, key) in enumerate(fields):
            ctk.CTkLabel(
                self.form_frame,
                text=label,
                font=FONTS["regular"],
                text_color=COLORS["text"],
                anchor="e",
                width=150
            ).grid(row=i, column=0, padx=10, pady=3, sticky="e")
            entry = ctk.CTkEntry(
                self.form_frame,
                width=300,
                font=FONTS["regular"],
                fg_color=COLORS["white"],
                text_color=COLORS["text"],
                border_color=COLORS["primary"],
                corner_radius=5
            )
            entry.grid(row=i, column=1, padx=10, pady=3, sticky="w")
            self.entries[key] = entry

        ctk.CTkLabel(
            self.form_frame,
            text="Категорія:",
            font=FONTS["regular"],
            text_color=COLORS["text"],
            anchor="e",
            width=150
        ).grid(row=len(fields), column=0, padx=10, pady=3, sticky="e")
        self.category_combo = ctk.CTkComboBox(
            self.form_frame,
            values=["opera", "concert", "ballet"],
            font=FONTS["regular"],
            fg_color=COLORS["white"],
            text_color=COLORS["text"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"],
            border_color=COLORS["primary"],
            corner_radius=5,
            width=300
        )
        self.category_combo.grid(row=len(fields), column=1, padx=10, pady=3, sticky="w")

        # Секція кнопок
        self.button_frame = ctk.CTkFrame(self.main_container, fg_color=COLORS["background"])
        self.button_frame.pack(fill="x", padx=10, pady=5, anchor="center")

        buttons = [
            ("Додати", self.add_performance),
            ("Редагувати", self.edit_performance),
            ("Видалити", self.delete_performance),
            ("Скасувати", self.clear_form)
        ]
        for text, command in buttons:
            ctk.CTkButton(
                self.button_frame,
                text=text,
                command=command,
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_hover"],
                text_color=COLORS["white"],
                font=FONTS["large"],
                width=150,
                height=40,
                corner_radius=10,
                border_width=1,
                border_color=COLORS["text"]
            ).pack(side="left", padx=8, pady=5)

    def load_performances(self):
        for widget in self.performance_list_frame.winfo_children():
            widget.destroy()

        performances = Performance.load_performances(self.json_path)
        if not performances:
            ctk.CTkLabel(
                self.performance_list_frame,
                text="Немає доступних вистав. Додайте нову!",
                font=FONTS["regular"],
                text_color=COLORS["text"],
                anchor="w"
            ).pack(fill="x", padx=10, pady=10)
            return

        for perf in performances:
            frame = ctk.CTkFrame(
                self.performance_list_frame,
                fg_color=COLORS["white"],
                corner_radius=5,
                border_width=1,
                border_color=COLORS["primary"]
            )
            frame.pack(fill="x", padx=5, pady=5)
            label = ctk.CTkLabel(
                frame,
                text=f"{perf['category'].capitalize()}: {perf['title']} ({perf['date']}, {perf['time']})",
                font=FONTS["regular"],
                text_color=COLORS["text"],
                anchor="w"
            )
            label.pack(side="left", padx=10, fill="x", expand=True)
            label.bind("<Button-1>", lambda e, p=perf: self.select_performance(p))
            frame.bind("<Enter>", lambda e, f=frame: f.configure(fg_color=COLORS["primary"]))
            frame.bind("<Leave>", lambda e, f=frame: f.configure(fg_color=COLORS["white"]))
            label.bind("<Enter>", lambda e, f=frame: f.configure(fg_color=COLORS["primary"]))
            label.bind("<Leave>", lambda e, f=frame: f.configure(fg_color=COLORS["white"]))

    def select_performance(self, perf):
        self.selected_performance = perf
        try:
            self.entries["title"].delete(0, "end")
            self.entries["title"].insert(0, perf.get("title", ""))
            self.entries["date"].delete(0, "end")
            converted_date = Performance.convert_json_date(perf["date"])
            self.entries["date"].insert(0, converted_date)
            time_parts = perf.get("time", "").split(", ")
            if len(time_parts) != 2:
                raise ValueError("Некоректний формат часу в JSON")
            self.entries["time"].delete(0, "end")
            self.entries["time"].insert(0, time_parts[1])
            self.entries["description"].delete(0, "end")
            self.entries["description"].insert(0, perf.get("description", ""))
            self.entries["price"].delete(0, "end")
            self.entries["price"].insert(0, str(perf.get("price", 0)))
            self.entries["author"].delete(0, "end")
            self.entries["author"].insert(0, perf.get("author", ""))
            self.entries["image"].delete(0, "end")
            self.entries["image"].insert(0, perf.get("image", ""))
            self.category_combo.set(perf.get("category", "opera"))
        except Exception as e:
            CTkMessagebox(
                title="Помилка",
                message=f"Не вдалося вибрати виставу: {str(e)}",
                icon="warning"
            )
            self.clear_form()

    def validate_form(self):
        for key, entry in self.entries.items():
            if not entry.get().strip() and key != "image":
                raise ValueError(f"Поле '{key}' не може бути порожнім")
        try:
            price = float(self.entries["price"].get())
            if price < 0:
                raise ValueError("Ціна квитка не може бути від'ємною")
        except ValueError:
            raise ValueError("Ціна квитка має бути числом")
        try:
            datetime.strptime(self.entries["date"].get(), "%Y-%m-%d")
        except ValueError:
            raise ValueError("Некоректний формат дати. Використовуйте РРРР-ММ-ДД")
        try:
            datetime.strptime(self.entries["time"].get(), "%H:%M")
        except ValueError:
            raise ValueError("Некоректний формат часу. Використовуйте ГГ:ХХ")
        return True

    def add_performance(self):
        try:
            self.validate_form()
            Performance.add_performance(
                title=self.entries["title"].get(),
                date=self.entries["date"].get(),
                time=self.entries["time"].get(),
                description=self.entries["description"].get(),
                ticket_price=float(self.entries["price"].get()),
                author=self.entries["author"].get(),
                image=self.entries["image"].get(),
                category=self.category_combo.get(),
                file_path=self.json_path
            )
            CTkMessagebox(
                title="Успіх",
                message="Виставу додано!",
                icon="info"
            )
            self.clear_form()
            self.load_performances()
        except ValueError as e:
            CTkMessagebox(
                title="Помилка",
                message=str(e),
                icon="warning"
            )

    def edit_performance(self):
        if not self.selected_performance:
            CTkMessagebox(
                title="Помилка",
                message="Оберіть виставу для редагування!",
                icon="warning"
            )
            return

        try:
            self.validate_form()
            old_date = Performance.convert_json_date(self.selected_performance["date"])
            old_time_parts = self.selected_performance["time"].split(", ")
            if len(old_time_parts) != 2:
                raise ValueError("Некоректний формат старого часу")
            old_time = old_time_parts[1]
            old_category = self.selected_performance.get("category", self.category_combo.get())

            Performance.edit_performance(
                old_title=self.selected_performance["title"],
                old_date=old_date,
                old_time=old_time,
                category=old_category,
                new_title=self.entries["title"].get(),
                new_date=self.entries["date"].get(),
                new_time=self.entries["time"].get(),
                new_description=self.entries["description"].get(),
                new_ticket_price=float(self.entries["price"].get()),
                new_author=self.entries["author"].get(),
                new_image=self.entries["image"].get(),
                file_path=self.json_path
            )

            CTkMessagebox(
                title="Успіх",
                message="Виставу оновлено!",
                icon="info"
            )
            self.clear_form()
            self.load_performances()
        except ValueError as e:
            CTkMessagebox(
                title="Помилка",
                message=str(e),
                icon="warning"
            )

    def delete_performance(self):
        if not self.selected_performance:
            CTkMessagebox(
                title="Помилка",
                message="Оберіть виставу для видалення!",
                icon="warning"
            )
            return

        response = CTkMessagebox(
            title="Підтвердження",
            message=f"Ви впевнені, що хочете видалити '{self.selected_performance['title']}'?",
            icon="question",
            option_1="Так",
            option_2="Ні"
        )
        if response.get() != "Так":
            return

        try:
            old_date = Performance.convert_json_date(self.selected_performance["date"])
            old_time_parts = self.selected_performance["time"].split(", ")
            if len(old_time_parts) != 2:
                raise ValueError("Некоректний формат часу для видалення")
            old_time = old_time_parts[1]
            old_category = self.selected_performance.get("category", self.category_combo.get())

            Performance.delete_performance(
                title=self.selected_performance["title"],
                date=old_date,
                time=old_time,
                category=old_category,
                file_path=self.json_path
            )
            CTkMessagebox(
                title="Успіх",
                message="Виставу видалено!",
                icon="info"
            )
            self.clear_form()
            self.load_performances()
        except ValueError as e:
            CTkMessagebox(
                title="Помилка",
                message=str(e),
                icon="warning"
            )

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.category_combo.set("opera")
        self.selected_performance = None

if __name__ == "__main__":
    root = ctk.CTk()
    app = AdminPerformanceManager(root)
    root.mainloop()