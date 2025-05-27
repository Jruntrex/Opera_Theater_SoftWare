import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import auth
from models.theater_seating import TheaterSeating
from ui.theater_seating_ui import TheaterSeatingUI

COLORS = {
    "primary": "#A71A1F",
    "primary_hover": "#871619",
    "background": "#F5F5F5",
    "white": "#FFFFFF",
    "text": "#000000",
    "secondary_text": "#666666",
    "accent": "#D4A017"
}
FONTS = {
    "header": ("Times New Roman", 32, "bold"),
    "title": ("Times New Roman", 22, "bold"),
    "regular": ("Arial", 14),
    "large": ("Arial", 16),
    "date": ("Arial", 32, "bold")
}

class PerformanceDetailsWindow(ctk.CTkToplevel):
    def __init__(self, parent, performance_data, on_back):
        super().__init__(parent)
        self.performance_data = performance_data
        self.on_back = on_back
        self.title(f"{performance_data['title']} - Деталі")
        self.geometry("1000x600")
        self.configure(fg_color=COLORS["background"])
        self.resizable(False, False)
        self.grab_set()
        self.header_frame = ctk.CTkFrame(self, fg_color=COLORS["white"], height=80, corner_radius=0)
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=4)
        self.back_button = ctk.CTkButton(
            self.header_frame,
            text="← Назад",
            fg_color=COLORS["white"],
            hover_color="#E0E0E0",
            text_color=COLORS["text"],
            font=FONTS["regular"],
            corner_radius=5,
            width=120,
            height=40,
            command=self.go_back
        )
        self.back_button.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=performance_data["title"],
            font=FONTS["header"],
            text_color=COLORS["text"]
        )
        self.title_label.grid(row=0, column=1, pady=20)
        self.content_frame = ctk.CTkFrame(self, fg_color=COLORS["background"])
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=0)
        self.content_frame.grid_columnconfigure(1, weight=1)
        image_label = self.load_performance_image(performance_data["image"])
        image_label.grid(row=0, column=0, padx=(0, 20), pady=10, sticky="n")
        self.info_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["white"], corner_radius=10)
        self.info_frame.grid(row=0, column=1, sticky="nsew", pady=10)
        self.info_frame.grid_columnconfigure(0, weight=1)
        author_label = ctk.CTkLabel(
            self.info_frame,
            text=f"Автор: {performance_data['author']}",
            font=FONTS["large"],
            text_color=COLORS["text"],
            anchor="w"
        )
        author_label.pack(fill="x", padx=20, pady=(20, 5))
        date_time_label = ctk.CTkLabel(
            self.info_frame,
            text=f"{performance_data['date']} | {performance_data['time'].split(', ')[1]}",
            font=FONTS["regular"],
            text_color=COLORS["secondary_text"],
            anchor="w"
        )
        date_time_label.pack(fill="x", padx=20, pady=5)
        price_label = ctk.CTkLabel(
            self.info_frame,
            text=f"Ціна: {performance_data['price']} грн",
            font=FONTS["large"],
            text_color=COLORS["primary"],
            anchor="w"
        )
        price_label.pack(fill="x", padx=20, pady=5)
        description_label = ctk.CTkLabel(
            self.info_frame,
            text=performance_data["description"],
            font=FONTS["regular"],
            text_color=COLORS["text"],
            anchor="w",
            wraplength=500,
            justify="left"
        )
        description_label.pack(fill="x", padx=20, pady=(5, 20))
        buy_button = ctk.CTkButton(
            self.info_frame,
            text="Купити квиток",
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["white"],
            font=FONTS["regular"],
            corner_radius=5,
            width=200,
            height=40,
            command=self.buy_ticket
        )
        buy_button.pack(pady=(0, 20))

    def load_performance_image(self, image_path):
        target_width = 400
        max_height = 500
        placeholder_path = "ui/images_performance/placeholder.jpg"
        try:
            print(f"Спроба завантажити зображення: {image_path}")
            img = Image.open(image_path)
            aspect_ratio = img.height / img.width
            new_height = int(target_width * aspect_ratio)
            if new_height > max_height:
                new_height = max_height
                target_width = int(new_height / aspect_ratio)
            img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)
            image = ctk.CTkImage(img, size=(target_width, new_height))
            return ctk.CTkLabel(
                self.content_frame,
                image=image,
                text="",
                corner_radius=10
            )
        except FileNotFoundError:
            print(f"Зображення {image_path} не знайдено, пробую placeholder")
            try:
                img = Image.open(placeholder_path)
                aspect_ratio = img.height / img.width
                new_height = int(target_width * aspect_ratio)
                if new_height > max_height:
                    new_height = max_height
                    target_width = int(new_height / aspect_ratio)
                img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)
                image = ctk.CTkImage(img, size=(target_width, new_height))
                return ctk.CTkLabel(
                    self.content_frame,
                    image=image,
                    text="",
                    corner_radius=10
                )
            except FileNotFoundError:
                print(f"Placeholder {placeholder_path} також відсутній")
                return ctk.CTkLabel(
                    self.content_frame,
                    text="Зображення відсутнє",
                    font=FONTS["regular"],
                    text_color=COLORS["secondary_text"],
                    width=target_width,
                    height=max_height
                )

    def buy_ticket(self):
        """Відкриває TheaterSeatingUI для вибору місць."""
        print(f"Відкривається TheaterSeatingUI для {self.performance_data['title']}")
        if not auth.IS_USER_LOGGED_IN:
            CTkMessagebox(
                title="Помилка",
                message="Будь ласка, увійдіть в систему, щоб купити квиток!",
                icon="warning",
                fg_color=COLORS["white"],
                title_color=COLORS["text"],
                button_color=COLORS["primary"],
                button_hover_color=COLORS["primary_hover"]
            )
            return False
        try:
            theater_seating = TheaterSeating(self.performance_data)
            TheaterSeatingUI(self, theater_seating, "ui/orders.json", self.performance_data)
            return True
        except Exception as e:
            CTkMessagebox(
                title="Помилка",
                message=f"Не вдалося відкрити схему залу: {str(e)}",
                icon="warning",
                fg_color=COLORS["white"],
                title_color=COLORS["text"],
                button_color=COLORS["primary"],
                button_hover_color=COLORS["primary_hover"]
            )
            return False

    def go_back(self):
        self.destroy()
        self.on_back()