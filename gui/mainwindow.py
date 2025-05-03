import customtkinter as ctk
from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkScrollableFrame, CTkButton, CTkTabview
from gui.autentefication_window import AuthWindow
from database.GarageBase import get_user_by_id


class MainWindow:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_data = get_user_by_id(user_id)

        self.root = CTk()
        self.root.title("GarageBook")
        self.root.geometry("1000x750")

        self.create_gui()

    def create_gui(self):
        # Главный контейнер с прокруткой
        main_frame = CTkScrollableFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Заголовок
        title_label = CTkLabel(main_frame, text="GarageBook", font=("Arial", 20, "bold"))
        title_label.pack(pady=(0, 10), anchor="w")

        # Информация о пользователе
        if self.user_data:
            user_label = CTkLabel(
                main_frame,
                text=f"{self.user_data[2]} ({self.user_data[1]})",
                font=("Arial", 14, "bold")
            )
            user_label.pack(anchor="w")
    def create_schedule_gui(self):
        # Настройка темы и цветов
        ctk.set_appearance_mode("light")  # "light" или "dark"
        ctk.set_default_color_theme("green")  # Возможные темы: "blue", "green", "dark-blue"

        root = CTk()
        root.title("Мое расписание")
        root.geometry("1000x750")

        # Главный контейнер с прокруткой
        main_frame = CTkScrollableFrame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Заголовок
        title_label = CTkLabel(main_frame, text="Мое расписание", font=("Arial", 20, "bold"))
        title_label.pack(pady=(0, 10), anchor="w")

        # Период
        period_label = CTkLabel(main_frame, text="14 – 20 апр. 2025 г.", font=("Arial", 14, "bold"))
        period_label.pack(anchor="w")

        # Дни недели в горизонтальном фрейме
        days_frame = CTkFrame(main_frame, fg_color="transparent")
        days_frame.pack(fill="x", pady=(5, 10))

        days = ["Над 15 пн.", "14.04 вт.", "15.04 ср.", "16.04 чт.", "17.04 пт.", "18.04 сб.", "19.04 вс."]
        for day in days:
            CTkLabel(days_frame, text=day).pack(side="left", padx=5)

        # Разделитель
        separator = CTkFrame(main_frame, height=2, fg_color="red")
        separator.pack(fill="x", pady=10)

        # Информация о пользователе
        user_label = CTkLabel(main_frame, text="Корсан Владимир Александрович", font=("Arial", 14, "bold"))
        user_label.pack(anchor="w")

        # Таблица расписания
        table_frame = CTkFrame(main_frame)
        table_frame.pack(fill="x", pady=10)

        headers = ["Имя расписания", "План №3", "Срок реализации", "Оборудование",
                   "Социальное обеспечение", "Управление образования", "Транспорт"]

        # Создаем заголовки таблицы
        for col, header in enumerate(headers):
            CTkLabel(table_frame, text=header, font=("Arial", 12, "bold"),
                     corner_radius=0, fg_color="#E5E5E5").grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

        # Строка "Моя оценка"
        CTkLabel(table_frame, text="Моя оценка", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", padx=5)
        for col in range(1, len(headers)):
            CTkEntry(table_frame, width=120, border_width=1, corner_radius=0).grid(row=1, column=col, padx=1, pady=1)

        # Настройка веса столбцов
        for col in range(len(headers)):
            table_frame.grid_columnconfigure(col, weight=1)

        # Разделитель
        separator = CTkFrame(main_frame, height=2, fg_color="orange")
        separator.pack(fill="x", pady=10)

        # Выбор модулей
        CTkLabel(main_frame, text="Выбор модулей", font=("Arial", 14, "bold")).pack(anchor="w")
        CTkLabel(main_frame, text="Справочная информация", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))

        # Таблица времени с вкладками
        tabview = CTkTabview(main_frame)
        tabview.pack(fill="x", pady=10)

        # Добавляем вкладки
        tabview.add("Расписание")
        tabview.add("Настройки")

        # Создаем таблицу на первой вкладке
        time_headers = ["Имя подписи", "10:00-11:45", "09:01/08:00", "12:05-13:45",
                        "12:05-14:45", "13:00-14:45", "14:00-15:45", "15:00-16:45", "16:00-17:45"]

        for col, header in enumerate(time_headers):
            CTkLabel(tabview.tab("Расписание"), text=header, font=("Arial", 10, "bold"),
                     fg_color="#E5E5E5", corner_radius=0).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

        # Добавляем данные
        modules_row = ["Выбор модулей"] + ["10:00 (Австралийская)"] * 8
        info_row = ["Справочная информация"] + [""] * 8

        for row, row_data in enumerate([modules_row, info_row], start=1):
            for col, cell in enumerate(row_data):
                if col == 0:
                    lbl = CTkLabel(tabview.tab("Расписание"), text=cell, font=("Arial", 10, "bold"))
                else:
                    lbl = CTkLabel(tabview.tab("Расписание"), text=cell)
                lbl.grid(row=row, column=col, sticky="w", padx=5, pady=2)

        # Настройка веса столбцов
        for col in range(len(time_headers)):
            tabview.tab("Расписание").grid_columnconfigure(col, weight=1)

        # Дополнительные разделы
        sections = [
            ("Связь подписи МОКШЭ", "За счет информации\n\nПолог:\n   - 10:00 - 12:35\n   - 12:35 (ОТ, УП / Лекция)"),
            ("Мое расписание", "Основное расписание заимов | Москва | Адреса корпусов и линейка"),
            ("Фильтра (1) | Индекс |", "нег. 20.04")
        ]

        for title, content in sections:
            separator = CTkFrame(main_frame, height=2, fg_color="yellow")
            separator.pack(fill="x", pady=10)

            CTkLabel(main_frame, text=title, font=("Arial", 14, "bold")).pack(anchor="w")
            CTkLabel(main_frame, text=content).pack(anchor="w", padx=20, pady=5)

        root.mainloop()

        logout_btn = CTkButton(
            main_frame,
            text="Выйти",
            command=self.logout,
            fg_color="red",
            hover_color="darkred"
        )
        logout_btn.pack(pady=20)


    def logout(self):
        self.root.destroy()
        show_auth_window()


    def run(self):
        self.root.mainloop()

def show_auth_window():
    auth_window = AuthWindow(on_login_success=lambda user_id: MainWindow(user_id).run())
    auth_window.run()

if __name__ == "__main__":
    show_auth_window()
