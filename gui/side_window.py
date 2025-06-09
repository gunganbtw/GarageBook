import customtkinter as ctk
from customtkinter import CTkToplevel, CTkFrame, CTkLabel, CTkButton, CTkScrollableFrame, CTkEntry
from database.GarageBase import *


class BreakHistoryDialog(CTkToplevel):
    """Диалоговое окно для добавления/редактирования записи о поломке"""

    def __init__(self, parent, title, car_id=None, record_data=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x300")
        self.resizable(False, False)
        self.grab_set()  # Делаем окно модальным

        self.car_id = car_id
        self.record_data = record_data
        self.result = None

        # Основной фрейм
        main_frame = CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Поля формы
        CTkLabel(main_frame, text="ID автомобиля:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.car_id_entry = CTkEntry(main_frame)
        self.car_id_entry.grid(row=0, column=1, padx=5, pady=5)
        if car_id:
            self.car_id_entry.insert(0, str(car_id))
            self.car_id_entry.configure(state="disabled")

        CTkLabel(main_frame, text="Описание поломки:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.break_desc_entry = CTkEntry(main_frame, width=300)
        self.break_desc_entry.grid(row=1, column=1, padx=5, pady=5)

        CTkLabel(main_frame, text="Код ошибки:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.error_code_entry = CTkEntry(main_frame)
        self.error_code_entry.grid(row=2, column=1, padx=5, pady=5)

        # Заполняем данные если это редактирование
        if record_data:
            self.break_desc_entry.insert(0, record_data[1])
            self.error_code_entry.insert(0, record_data[2])

        # Кнопки
        button_frame = CTkFrame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        CTkButton(button_frame, text="Отмена", command=self.cancel).pack(side="left", padx=10)
        CTkButton(button_frame, text="Сохранить", command=self.save).pack(side="left", padx=10)

    def save(self):
        """Сохранение данных"""
        self.result = (
            int(self.car_id_entry.get()),
            self.break_desc_entry.get(),
            self.error_code_entry.get()
        )
        self.destroy()

    def cancel(self):
        self.destroy()

class GarageCarDialog(CTkToplevel):
    """Диалог добавления/редактирования автомобиля"""
    def __init__(self, parent, title, car_data=None, user_id=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x400")  # Увеличим размер окна для новых полей
        self.resizable(False, False)
        self.grab_set()

        self.result = None
        self.car_data = car_data
        self.user_id = user_id

        main_frame = CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.entries = {}
        labels = ["Бренд", "Модель", "VIN", "Цвет", "Год выпуска", "Тип двигателя", "Тип топлива", "Объем двигателя", "Тип коробки"]
        keys = ["brand", "model", "vin", "color", "release_year", "engine_type", "fuel_type", "engine_capacity", "transmission_type"]

        for i, (label, key) in enumerate(zip(labels, keys)):
            CTkLabel(main_frame, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = CTkEntry(main_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[key] = entry

        if car_data:
            self.entries["brand"].insert(0, car_data[1])  # car_brand
            self.entries["model"].insert(0, car_data[2])  # car_model
            self.entries["vin"].insert(0, car_data[3])  # vin_code
            self.entries["color"].insert(0, car_data[4])  # car_color
            self.entries["release_year"].insert(0, str(car_data[5]))  # release_year
            self.entries["engine_type"].insert(0, car_data[6])  # engine_type
            self.entries["fuel_type"].insert(0, car_data[7])  # fuel_type
            self.entries["engine_capacity"].insert(0, str(car_data[8]))  # engine_capacity
            self.entries["transmission_type"].insert(0, car_data[9])  # transmission_type

        button_frame = CTkFrame(main_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)

        CTkButton(button_frame, text="Сохранить", command=self.save).pack(side="left", padx=10)
        CTkButton(button_frame, text="Отмена", command=self.cancel).pack(side="left", padx=10)

    def save(self):
        self.result = (
            self.entries["brand"].get(),
            self.entries["vin"].get(),
            self.entries["color"].get(),
            self.entries["model"].get(),
            self.entries["release_year"].get(),
            self.entries["engine_type"].get(),
            self.entries["fuel_type"].get(),
            self.entries["engine_capacity"].get(),
            self.entries["transmission_type"].get(),
            self.user_id  # Добавляем user_id в результат
        )
        self.destroy()

    def cancel(self):
        self.destroy()


def add_car_action(self):
    dialog = GarageCarDialog(self, "Добавить автомобиль", user_id=self.user_id)
    self.wait_window(dialog)

    if dialog.result:
        # Проверяем, что user_id передан и не None
        if not hasattr(self, 'user_id') or self.user_id is None:
            print("Ошибка: user_id не установлен")
            return False

        try:
            # Преобразуем user_id в int для уверенности
            user_id = int(self.user_id)
            result = add_car(*dialog.result, user_id=user_id)
            if result:
                load_garage(self, self.user_id)
        except Exception as e:
            print(f"Ошибка при добавлении автомобиля: {e}")

    def cancel(self):
        self.destroy()

def load_garage(self, user_id):
    """Отображает список машин"""
    for widget in self.content_frame.winfo_children():
        widget.destroy()

    self.car_list = get_cars()
    self.selected_car_id = None

    if not self.car_list:
        CTkLabel(self.content_frame, text="Гараж пуст").pack(pady=20)
        return

    for car in self.car_list:
        # Проверяем, что user_id в машине не None и соответствует текущему пользователю
        if car[5] is not None and int(user_id) == int(car[5]):
            frame = CTkFrame(self.content_frame, height=60, border_width=1, border_color="#ccc")
            frame.pack(fill="x", pady=3)
            frame.bind("<Button-1>", lambda e, c=car: select_car(self, c))

            CTkLabel(frame, text=f"{car[1]} | VIN: {car[3]}", font=("Arial", 12)).pack(side="left", padx=10)

            open_btn = CTkButton(frame, text="Открыть", width=80, command=lambda c=car: show_car_details(self, c))
            open_btn.pack(side="right", padx=10)


def select_car(self, car):
    self.selected_car_id = car[0]


def show_car_details(self, car):
    full_car = get_car_by_id(car[0])
    if not full_car:
        return

    dialog = CTkToplevel(self)
    dialog.title("Информация о машине")
    dialog.geometry("500x400")  # Увеличим размер окна для дополнительных полей
    dialog.grab_set()

    # Основной фрейм для данных
    main_frame = CTkFrame(dialog)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Список полей и их человеко-читаемые названия
    fields = [
        ("ID", full_car[0]),
        ("Бренд", full_car[1]),
        ("Модель", full_car[2]),
        ("VIN", full_car[3]),
        ("Цвет", full_car[4]),
        ("Год выпуска", full_car[5]),
        ("Тип двигателя", full_car[6]),
        ("Тип топлива", full_car[7]),
        ("Объём двигателя", full_car[8]),
        ("Тип трансмиссии", full_car[9])
    ]

    # Отображаем все поля
    for i, (field_name, value) in enumerate(fields):
        # Пропускаем пустые значения
        if value is None:
            continue

        row_frame = CTkFrame(main_frame)
        row_frame.pack(fill="x", pady=2)

        CTkLabel(
            row_frame,
            text=f"{field_name}:",
            font=("Arial", 12, "bold"),
            width=150,
            anchor="w"
        ).pack(side="left", padx=5)

        CTkLabel(
            row_frame,
            text=str(value),
            font=("Arial", 12),
            anchor="w"
        ).pack(side="left", padx=5)

    # Кнопка закрытия
    button_frame = CTkFrame(dialog)
    button_frame.pack(pady=10)

    CTkButton(
        button_frame,
        text="Закрыть",
        command=dialog.destroy
    ).pack(pady=5)


def add_car_action(self):
    dialog = GarageCarDialog(self, "Добавить автомобиль", user_id=self.user_id)
    self.wait_window(dialog)

    if dialog.result:
        # Добавляем проверку user_id
        if not hasattr(self, 'user_id') or self.user_id is None:
            print("Ошибка: user_id не установлен")
            return

        try:
            # Преобразуем user_id в int
            user_id = int(self.user_id)
            # Передаем все параметры, включая user_id
            result = add_car(
                dialog.result[0],  # brand
                dialog.result[1],  # vin
                dialog.result[2],  # color
                dialog.result[3],  # model
                dialog.result[4],  # release_year
                dialog.result[5],  # engine_type
                dialog.result[6],  # fuel_type
                dialog.result[7],  # engine_capacity
                dialog.result[8],  # transmission_type
                user_id  # user_id
            )
            if result:
                load_garage(self, self.user_id)
        except Exception as e:
            print(f"Ошибка при добавлении автомобиля: {e}")


def edit_car_action(self):
    if not self.selected_car_id:
        return

    car = get_car_by_id(self.selected_car_id)
    if not car:
        return

    dialog = GarageCarDialog(self, "Изменить автомобиль", car_data=car)
    self.wait_window(dialog)

    if dialog.result:
        # Обновляем все поля автомобиля
        result = update_car(
            self.selected_car_id,
            car_brand=dialog.result[0],
            vin=dialog.result[1],
            color=dialog.result[2],
            model=dialog.result[3],
            release_year=dialog.result[4],
            engine_type=dialog.result[5],
            fuel_type=dialog.result[6],
            engine_capacity=dialog.result[7],
            transmission_type=dialog.result[8]
        )
        if result:
            self.selected_car_id = None
            load_garage(self, self.user_id)


def delete_car_action(self):
    if not self.selected_car_id:
        return

    result = delete_car(self.selected_car_id)
    if result:
        self.selected_car_id = None
        load_garage(self, self.user_id)

class ServiceDialog(CTkToplevel):
    """Диалог для добавления или изменения записи о замене расходников"""
    def __init__(self, parent, title, car_id=None, data=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x700")
        self.grab_set()
        self.result = None

        main_frame = CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        CTkLabel(main_frame, text="ID машины:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.car_id_entry = CTkEntry(main_frame)
        self.car_id_entry.grid(row=0, column=1, padx=5, pady=5)

        CTkLabel(main_frame, text="Моторное масло:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.oil_entry = CTkEntry(main_frame)
        self.oil_entry.grid(row=1, column=1, padx=5, pady=5)

        CTkLabel(main_frame, text="Воздушный фильтр:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.filter_entry = CTkEntry(main_frame)
        self.filter_entry.grid(row=2, column=1, padx=5, pady=5)

        CTkLabel(main_frame, text="Трансмиссионное масло:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.filter_entry = CTkEntry(main_frame)
        self.filter_entry.grid(row=3, column=1, padx=5, pady=5)

        CTkLabel(main_frame, text="Салонный фильтр:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.filter_entry = CTkEntry(main_frame)
        self.filter_entry.grid(row=4, column=1, padx=5, pady=5)

        CTkLabel(main_frame, text="Маслянный фильтр:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.filter_entry = CTkEntry(main_frame)
        self.filter_entry.grid(row=5, column=1, padx=5, pady=5)

        CTkLabel(main_frame, text="Топливный фильтр:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.filter_entry = CTkEntry(main_frame)
        self.filter_entry.grid(row=6, column=1, padx=5, pady=5)

        CTkLabel(main_frame, text="Пробег:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.filter_entry = CTkEntry(main_frame)
        self.filter_entry.grid(row=7, column=1, padx=5, pady=5)

        if car_id:
            self.car_id_entry.insert(0, str(car_id))
        if data:
            self.oil_entry.insert(0, data[1])
            self.filter_entry.insert(0, data[2])
            self.car_id_entry.insert(0, str(data[0]))
            self.car_id_entry.configure(state="disabled")

        btns = CTkFrame(main_frame)
        btns.grid(row=8, column=0, columnspan=2, pady=15)

        CTkButton(btns, text="Сохранить", command=self.save).pack(side="left", padx=10)
        CTkButton(btns, text="Отмена", command=self.cancel).pack(side="left", padx=10)

    def save(self):
        self.result = (
            int(self.car_id_entry.get()),
            self.oil_entry.get(),
            self.filter_entry.get()
        )
        self.destroy()

    def cancel(self):
        self.destroy()


def load_service_history(self):
    """Загрузка списка замен расходников"""
    from database.GarageBase import get_break_history
    self.service_records = get_break_history()  # временно используем break_history как заглушку

    for widget in self.content_frame.winfo_children():
        widget.destroy()

    if not self.service_records:
        CTkLabel(self.content_frame, text="Нет данных о заменах").pack(pady=20)
        return

    headers = ["ID", "Моторное масло", "Фильтр"]

    header = CTkFrame(self.content_frame)
    header.pack(fill="x", pady=5)

    for text in headers:
        CTkLabel(header, text=text, font=("Arial", 12, "bold"), width=150).pack(side="left", padx=5)

    for record in self.service_records:
        row = CTkFrame(self.content_frame, height=50, border_width=1, border_color="#ccc")
        row.pack(fill="x", pady=2)
        row.bind("<Button-1>", lambda e, r=record: select_service_record(self, r))

        for i in range(3):
            CTkLabel(row, text=record[i], width=150).pack(side="left", padx=5)

    self.selected_service = None


def select_service_record(self, record):
    self.selected_service = record


def add_service_record(self):
    dialog = ServiceDialog(self, "Добавить замену")
    self.wait_window(dialog)

    if dialog.result:
        car_id, oil, filter_ = dialog.result
        if add_service_history(car_id, oil, filter_):
            load_service_history(self)


def edit_service_record(self):
    if not self.selected_service:
        return

    dialog = ServiceDialog(self, "Редактировать", data=self.selected_service)
    self.wait_window(dialog)

    if dialog.result:
        car_id, oil, filter_ = dialog.result
        msg = update_service_history(old_car_id=car_id, motor_oil=oil, air_filter=filter_)
        print(msg)
        self.selected_service = None
        load_service_history(self)


def delete_service_record(self):
    if not self.selected_service:
        return

    car_id = self.selected_service[0]
    msg = delete_service_history(car_id)
    print(msg)
    self.selected_service = None
    load_service_history(self)

class SideWindow(CTkToplevel):
    def __init__(self, parent, title, user_id=None):
        super().__init__(parent)
        self.user_id = user_id
        self.title_name = title
        self.selected_record = None  # Выбранная запись для редактирования/удаления

        # Настройки окна
        self.title(title)
        self.geometry("1200x900+{}+{}".format(
            parent.winfo_x() + 500,
            parent.winfo_y() + 100
        ))
        self.resizable(False, False)
        self.attributes("-alpha", 0.9)

        # Блокировка перемещения
        self.overrideredirect(True)
        self.bind("<B1-Motion>", lambda e: "break")

        # Создание интерфейса
        self.create_interface(title)

    def create_interface(self, title):
        # Основной контейнер
        main_frame = CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Заголовок
        header_frame = CTkFrame(main_frame, height=40)
        header_frame.pack(fill="x", pady=(0, 10))

        CTkLabel(
            header_frame,
            text=title,
            font=("Arial", 16, "bold")
        ).pack(side="left", padx=10)

        # Кнопка закрытия
        CTkButton(
            header_frame,
            text="×",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="#f0f0f0",
            command=self.destroy
        ).pack(side="right", padx=5)

        # Поисковая область
        self.search_frame = CTkFrame(main_frame)
        self.search_frame.pack(side="top", fill="x", pady=10)

        self.search_entry = CTkEntry(self.search_frame, width=1100, placeholder_text='Поиск🔍')
        self.search_entry.pack(side="left")

        CTkButton(
            self.search_frame, 
            width=100,
            text="Найти",
            command=self.search_result
        ).pack(side="right")        

        # Контентная область
        self.content_frame = CTkScrollableFrame(main_frame)
        self.content_frame.pack(fill="both", expand=True)

        # Загружаем данные в зависимости от типа окна
        if self.title_name == "История поломок":
            self.load_break_history()
        else:
            # Пример данных для других окон
            for i in range(5):
                item_frame = CTkFrame(
                    self.content_frame,
                    height=80,
                    border_width=1,
                    border_color="#e0e0e0"
                )
                item_frame.pack(fill="x", pady=3)

                CTkLabel(
                    item_frame,
                    text=f"Запись {i + 1}",
                    font=("Arial", 12)
                ).pack(side="left", padx=10)

        # Нижние кнопки
        footer_frame = CTkFrame(main_frame, height=60)
        footer_frame.pack(fill="x", pady=(10, 0))

        if self.title_name == "История поломок":
            # Кнопки для истории поломок
            self.add_btn = CTkButton(
                footer_frame,
                text="Добавить запись",
                width=120,
                height=35,
                command=self.add_break_record
            )
            self.add_btn.pack(side="left", padx=10, pady=5)

            self.edit_btn = CTkButton(
                footer_frame,
                text="Изменить запись",
                width=120,
                height=35,
                command=self.edit_break_record
            )
            self.edit_btn.pack(side="left", padx=10, pady=5)

            self.delete_btn = CTkButton(
                footer_frame,
                text="Удалить запись",
                width=120,
                height=35,
                command=self.delete_break_record
            )
            self.delete_btn.pack(side="left", padx=10, pady=5)

            # Кнопка обновить
            CTkButton(
                footer_frame,
                text="Обновить",
                width=120,
                height=35,
                command=self.load_break_history
            ).pack(side="right", padx=10, pady=5)

        if self.title_name == "Гараж":
            load_garage(self, self.user_id)

            self.add_btn = CTkButton(footer_frame, text="Добавить", command=lambda: add_car_action(self))
            self.add_btn.pack(side="left", padx=10)

            self.edit_btn = CTkButton(footer_frame, text="Изменить", command=lambda: edit_car_action(self))
            self.edit_btn.pack(side="left", padx=10)

            self.delete_btn = CTkButton(footer_frame, text="Удалить", command=lambda: delete_car_action(self))
            self.delete_btn.pack(side="left", padx=10)

        elif self.title_name == "Замена расходников":
            load_service_history(self)

            CTkButton(footer_frame, text="Добавить", width=120, command=lambda: add_service_record(self)).pack(
                side="left", padx=10)
            CTkButton(footer_frame, text="Изменить", width=120, command=lambda: edit_service_record(self)).pack(
                side="left", padx=10)
            CTkButton(footer_frame, text="Удалить", width=120, command=lambda: delete_service_record(self)).pack(
                side="left", padx=10)

    def load_break_history(self):
        """Загрузка истории поломок из базы данных"""
        # Очищаем контентную область
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Получаем данные из базы
        history = get_break_history()

        if not history:
            CTkLabel(
                self.content_frame,
                text="Нет данных о поломках",
                font=("Arial", 12)
            ).pack(pady=10)
            return

        # Отображаем данные в виде таблицы
        headers = ["ID автомобиля", "Описание поломки", "Код ошибки"]

        # Заголовки таблицы
        header_frame = CTkFrame(self.content_frame)
        header_frame.pack(fill="x", pady=(0, 5))

        for i, header in enumerate(headers):
            CTkLabel(
                header_frame,
                text=header,
                font=("Arial", 12, "bold"),
                width=200 if i == 1 else 100
            ).pack(side="left", padx=5)

        # Данные таблицы
        for record in history:
            record_frame = CTkFrame(
                self.content_frame,
                height=50,
                border_width=1,
                border_color="#e0e0e0"
            )
            record_frame.pack(fill="x", pady=2)
            record_frame.bind("<Button-1>", lambda e, r=record: self.select_record(r))

            # Подсветка выбранной записи
            if self.selected_record and self.selected_record[0] == record[0]:
                record_frame.configure(fg_color="#e0e0e0")

            CTkLabel(
                record_frame,
                text=record[0],  # car_id
                font=("Arial", 12),
                width=100
            ).pack(side="left", padx=5)

            CTkLabel(
                record_frame,
                text=record[1],  # break_desc
                font=("Arial", 12),
                width=200
            ).pack(side="left", padx=5)

            CTkLabel(
                record_frame,
                text=record[2],  # error_code
                font=("Arial", 12),
                width=100
            ).pack(side="left", padx=5)

    def select_record(self, record):
        """Выбор записи для редактирования/удаления"""
        self.selected_record = record
        self.load_break_history()  # Перезагружаем для подсветки

        # Активируем кнопки редактирования/удаления
        self.edit_btn.configure(state="normal")
        self.delete_btn.configure(state="normal")

    def add_break_record(self):
        """Добавление новой записи о поломке"""
        dialog = BreakHistoryDialog(self, "Добавить запись о поломке")
        self.wait_window(dialog)

        if dialog.result:
            car_id, break_desc, error_code = dialog.result
            result = add_break_history(
                car_id=car_id,
                break_desc=break_desc,
                error_code=error_code
            )

            if result:
                self.load_break_history()  # Обновляем список

    def edit_break_record(self):
        """Редактирование записи о поломке"""
        if not self.selected_record:
            return

        dialog = BreakHistoryDialog(
            self,
            "Редактировать запись о поломке",
            car_id=self.selected_record[0],
            record_data=self.selected_record
        )
        self.wait_window(dialog)

        if dialog.result:
            car_id, break_desc, error_code = dialog.result
            result = update_break_history(
                car_id=car_id,
                break_desc=break_desc,
                error_code=error_code
            )

            if result:
                self.selected_record = None
                self.edit_btn.configure(state="disabled")
                self.delete_btn.configure(state="disabled")
                self.load_break_history()  # Обновляем список

    def delete_break_record(self):
        """Удаление записи о поломке"""
        if not self.selected_record:
            return

        # Создаем свое окно подтверждения
        confirm = CTkToplevel(self)
        confirm.title("Подтверждение")
        confirm.geometry("300x150")
        confirm.resizable(False, False)
        confirm.grab_set()

        CTkLabel(
            confirm,
            text=f"Удалить запись о поломке\nдля автомобиля {self.selected_record[0]}?",
            font=("Arial", 12)
        ).pack(pady=20)

        button_frame = CTkFrame(confirm)
        button_frame.pack(pady=10)

        confirm_result = False

        def on_confirm():
            nonlocal confirm_result
            confirm_result = True
            confirm.destroy()

        def on_cancel():
            confirm.destroy()

        CTkButton(button_frame, text="Да", command=on_confirm).pack(side="left", padx=10)
        CTkButton(button_frame, text="Отмена", command=on_cancel).pack(side="left", padx=10)

        self.wait_window(confirm)

        if confirm_result:
            result = delete_break_history(
                car_id=self.selected_record[0]
            )

            if result:
                self.selected_record = None
                self.edit_btn.configure(state="disabled")
                self.delete_btn.configure(state="disabled")
                self.load_break_history()  # Обновляем список
       
    def search_result(self):
        order = self.search_entry.get()
        
        flag = 0
        if ' ' in order:
            order = order.split(' ')
            flag = 1

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        car_list = get_cars()

        if self.title_name == "Гараж":
            for car in car_list:
                if (flag == 0 and order in car) or (flag == 1 and (order[0] in car and order[1] in car)):

                    frame = CTkFrame(self.content_frame, height=60, border_width=1, border_color="#ccc")
                    frame.pack(fill="x", pady=3)
                    frame.bind("<Button-1>", lambda e, c=car: select_car(self, c))

                    CTkLabel(frame, text=f"{car[1]} | VIN: {car[3]}", font=("Arial", 12)).pack(side="left", padx=10)

                    open_btn = CTkButton(frame, text="Открыть", width=80, command=lambda c=car: show_car_details(self, c))
                    open_btn.pack(side="right", padx=10)

                # elif flag == 1 and (order[0] in car and order[1] in car)
                
            if order == '': load_garage(self, self.user_id)

        elif self.title_name == "История поломок":
            
            if order != '':
            
                from database.GarageBase import get_break_history
                history = get_break_history()

                ids_car = []
                for car in car_list:
                    if (flag == 0 and order in car) or (flag ==1 and (order[0] in car and order[1] in car)):
                        ids_car.append(car[0])

                needed_history = []
                for his in history:
                    if his[0] in ids_car:
                        needed_history.append(his)

                if not needed_history:
                    CTkLabel(
                        self.content_frame,
                        text="Нет данных о поломках",
                        font=("Arial", 12)
                    ).pack(pady=10)
                    return

                # Отображаем данные в виде таблицы
                headers = ["ID автомобиля", "Описание поломки", "Код ошибки"]

                # Заголовки таблицы
                header_frame = CTkFrame(self.content_frame)
                header_frame.pack(fill="x", pady=(0, 5))

                for i, header in enumerate(headers):
                    CTkLabel(
                        header_frame,
                        text=header,
                        font=("Arial", 12, "bold"),
                        width=200 if i == 1 else 100
                    ).pack(side="left", padx=5)

                # Данные таблицы
                for record in needed_history:
                    record_frame = CTkFrame(
                        self.content_frame,
                        height=50,
                        border_width=1,
                        border_color="#e0e0e0"
                    )
                    record_frame.pack(fill="x", pady=2)
                    record_frame.bind("<Button-1>", lambda e, r=record: self.select_record(r))

                    # Подсветка выбранной записи
                    if self.selected_record and self.selected_record[0] == record[0]:
                        record_frame.configure(fg_color="#e0e0e0")

                    CTkLabel(
                        record_frame,
                        text=record[0],  # car_id
                        font=("Arial", 12),
                        width=100
                    ).pack(side="left", padx=5)

                    CTkLabel(
                        record_frame,
                        text=record[1],  # break_desc
                        font=("Arial", 12),
                        width=200
                    ).pack(side="left", padx=5)

                    CTkLabel(
                        record_frame,
                        text=record[2],  # error_code
                        font=("Arial", 12),
                        width=100
                    ).pack(side="left", padx=5)
                    
            else: load_service_history(self)

        elif self.title_name == "Замена расходников":

            if order != '':
                from database.GarageBase import get_break_history
                self.service_records = get_break_history()

                if not self.service_records:
                    CTkLabel(self.content_frame, text="Нет данных о заменах").pack(pady=20)
                    return

                ids_car = []
                for car in car_list:
                    if (flag == 0 and order in car) or (flag == 1 and (order[0] in car and order[1] in car)):
                        ids_car.append(car[0])

                needed_service = []
                for ser in self.service_records:
                    if ser[0] in ids_car:
                        needed_service.append(ser)

                headers = ["ID", "Моторное масло", "Фильтр"]

                header = CTkFrame(self.content_frame)
                header.pack(fill="x", pady=5)

                for text in headers:
                    CTkLabel(header, text=text, font=("Arial", 12, "bold"), width=150).pack(side="left", padx=5)

                for record in needed_service:
                    row = CTkFrame(self.content_frame, height=50, border_width=1, border_color="#ccc")
                    row.pack(fill="x", pady=2)
                    row.bind("<Button-1>", lambda e, r=record: select_service_record(self, r))

                    for i in range(3):
                        CTkLabel(row, text=record[i], width=150).pack(side="left", padx=5)

                self.selected_service = None
            
            else: load_service_history(self)