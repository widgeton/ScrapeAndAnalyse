import os

import customtkinter as ctk
import show_graphs as shg
import work_with_data as wwd


class ProgressbarWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x100")
        self.title('Сбор статистики')

        self.label = ctk.CTkLabel(self, text="Идет сбор статистики...", height=30)
        self.label.place(x=10, y=10)

        self.bar = ctk.CTkProgressBar(self, width=380)
        self.bar.place(x=10, y=50)
        self.bar.set(0)


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # настройки темы
        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('dark-blue')

        # настройки окна
        self.geometry('480x250')
        self.title('Исследование статистики')
        self.resizable(False, False)

        # создание рамки для вывода статистики по датам
        self.frm1 = ctk.CTkFrame(self, width=220, height=165)
        self.frm1.place(x=10, y=10)

        # создание надписи для рамки вывода статистики по дате
        self.lbl_frm1 = ctk.CTkLabel(self.frm1, text='Вывод статистики по дате', font=('Cambria', 17), height=30)
        self.lbl_frm1.place(x=10, y=10)

        # кнопка для вывода количества книг издательств в топе по дате
        self.btn1 = ctk.CTkButton(self.frm1, text='Кол-во книг', command=self.show_books_amount,
                                  font=ctk.CTkFont('Cambria'), height=30, width=180)
        self.btn1.place(x=20, y=50)

        # кнопка для вывода средней цены книг издательств по дате
        self.btn2 = ctk.CTkButton(self.frm1, text='Ср. цена', command=self.show_middle_price,
                                  font=ctk.CTkFont('Cambria'), height=30, width=180)
        self.btn2.place(x=20, y=90)

        # создание выпадающего меня для выбора даты
        self.dates = [i.strip('.csv') for i in os.listdir('./data')]
        self.var = ctk.StringVar(value=self.dates[0])
        self.cmbox = ctk.CTkComboBox(self.frm1, values=self.dates, variable=self.var, height=25, width=180)
        self.cmbox.place(x=20, y=130)

        # создание рамки для вывода общей статистики
        self.frm2 = ctk.CTkFrame(self, width=220, height=165)
        self.frm2.place(x=250, y=10)

        # создание надписи для рамки вывода общей статистики
        self.lbl_frm2 = ctk.CTkLabel(self.frm2, text='Вывод общей статистики', font=('Cambria', 17), height=30)
        self.lbl_frm2.place(x=10, y=10)

        # кнопка во второй рамке для вывода изменений количества книг издательств в топе
        self.btn3 = ctk.CTkButton(self.frm2, text='Изменения кол-ва книг', command=self.show_changes_of_books_amount,
                                  font=ctk.CTkFont('Cambria'), height=30, width=180)
        self.btn3.place(x=20, y=55)

        # кнопка во второй рамке для вывода изменений средних цен нна книги издательств в топе
        self.btn4 = ctk.CTkButton(self.frm2, text='Изменения ср. цен', command=self.show_changes_of_middle_prices,
                                  font=ctk.CTkFont('Cambria'), height=30, width=180)
        self.btn4.place(x=20, y=110)

        # кнопка для сбора статистики за текущий день
        self.btn5 = ctk.CTkButton(self, text='Собрать статистику за текущий день', command=self.pick_statistic,
                                  font=ctk.CTkFont('Cambria', 14), width=440, height=40)
        self.btn5.place(x=20, y=190)
        # окно для progressbar
        self.wnd2 = None

    def show_books_amount(self):
        shg.show_books_amount(self.var.get(), 16)

    def show_middle_price(self):
        shg.show_middle_price(self.var.get(), 16)

    def show_changes_of_books_amount(self):
        shg.show_changes_of_books_amount(self.dates[0], 16)

    def show_changes_of_middle_prices(self):
        shg.show_changes_of_middle_prices(self.dates[0], 16)

    def pick_statistic(self):
        if self.wnd2 is None or not self.wnd2.winfo_exists():
            self.wnd2 = ProgressbarWindow(self)
        self.wnd2.grab_set()
        wwd.write(self.wnd2.bar)
        self.wnd2.label.configure(text='Сбор завершен!')

        self.dates = [i.strip('.csv') for i in os.listdir('./data')]
        self.cmbox.configure(values=self.dates)
