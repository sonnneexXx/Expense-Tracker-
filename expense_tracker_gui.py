#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox, font
from tkcalendar import DateEntry  # pip install tkcalendar

class ExpenseTrackerGUI:
    """GUI приложение для отслеживания расходов"""

    def __init__(self, root):
        self.root = root
        self.root.title("💰 Expense Tracker - Трекер расходов")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)

        # Файл для хранения данных
        self.data_file = "expenses.json"
        self.expenses = []
        self.next_id = 1

        # Загрузка данных
        self.load_data()

        # Стиль
        self.setup_styles()

        # Создание интерфейса
        self.create_widgets()

        # Обновление таблицы
        self.refresh_table()

    def setup_styles(self):
        """Настройка стилей интерфейса"""
        # Цветовая схема
        self.colors = {
            'bg': '#f0f0f0',
            'primary': '#2c3e50',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'info': '#3498db',
            'light': '#ecf0f1'
        }

        self.root.configure(bg=self.colors['bg'])

        # Настройка шрифтов
        self.fonts = {
            'title': ('Arial', 16, 'bold'),
            'heading': ('Arial', 12, 'bold'),
            'normal': ('Arial', 10),
            'small': ('Arial', 9)
        }

    def create_widgets(self):
        """Создание всех виджетов"""

        # Верхняя панель с заголовком
        self.create_header()

        # Панель ввода данных
        self.create_input_panel()

        # Панель фильтрации
        self.create_filter_panel()

        # Панель статистики
        self.create_stats_panel()

        # Таблица с расходами
        self.create_table()

        # Нижняя панель с кнопками
        self.create_bottom_panel()

    def create_header(self):
        """Создание заголовка"""
        header_frame = Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=X)
        header_frame.pack_propagate(False)

        title_label = Label(header_frame, text="💰 EXPENSE TRACKER",
                           font=self.fonts['title'],
                           fg='white', bg=self.colors['primary'])
        title_label.pack(pady=20)

    def create_input_panel(self):
        """Панель для добавления расходов"""
        input_frame = LabelFrame(self.root, text="➕ Добавить расход",
                                 font=self.fonts['heading'],
                                 padx=10, pady=10, bg=self.colors['bg'])
        input_frame.pack(fill=X, padx=10, pady=10)

        # Поле для суммы
        Label(input_frame, text="Сумма (₽):", font=self.fonts['normal'],
              bg=self.colors['bg']).grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.amount_entry = Entry(input_frame, font=self.fonts['normal'], width=20)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        # Поле для категории (выпадающий список)
        Label(input_frame, text="Категория:", font=self.fonts['normal'],
              bg=self.colors['bg']).grid(row=0, column=2, sticky=W, padx=5, pady=5)
        self.categories = ["Еда", "Транспорт", "Развлечения",
                          "Коммунальные", "Здоровье", "Одежда",
                          "Образование", "Другое"]
        self.category_combo = ttk.Combobox(input_frame, values=self.categories,
                                           font=self.fonts['normal'], width=15)
        self.category_combo.grid(row=0, column=3, padx=5, pady=5)
        self.category_combo.set("Выберите...")

        # Поле для даты
        Label(input_frame, text="Дата:", font=self.fonts['normal'],
              bg=self.colors['bg']).grid(row=0, column=4, sticky=W, padx=5, pady=5)
        self.date_entry = DateEntry(input_frame, width=12, background='darkblue',
                                    foreground='white', borderwidth=2,
                                    date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=5, padx=5, pady=5)

        # Кнопка добавления
        add_btn = Button(input_frame, text="Добавить расход",
                        command=self.add_expense,
                        bg=self.colors['success'], fg='white',
                        font=self.fonts['heading'], padx=20, pady=5)
        add_btn.grid(row=0, column=6, padx=20, pady=5)

    def create_filter_panel(self):
        """Панель фильтрации"""
        filter_frame = LabelFrame(self.root, text="🔍 Фильтрация",
                                  font=self.fonts['heading'],
                                  padx=10, pady=10, bg=self.colors['bg'])
        filter_frame.pack(fill=X, padx=10, pady=5)

        # Фильтр по категории
        Label(filter_frame, text="Категория:", font=self.fonts['normal'],
              bg=self.colors['bg']).grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.filter_category = ttk.Combobox(filter_frame, values=["Все"] + self.categories,
                                            font=self.fonts['normal'], width=15)
        self.filter_category.grid(row=0, column=1, padx=5, pady=5)
        self.filter_category.set("Все")

        # Фильтр по дате
        Label(filter_frame, text="Дата от:", font=self.fonts['normal'],
              bg=self.colors['bg']).grid(row=0, column=2, sticky=W, padx=5, pady=5)
        self.filter_date_from = DateEntry(filter_frame, width=12,
                                          date_pattern='yyyy-mm-dd')
        self.filter_date_from.grid(row=0, column=3, padx=5, pady=5)

        Label(filter_frame, text="Дата до:", font=self.fonts['normal'],
              bg=self.colors['bg']).grid(row=0, column=4, sticky=W, padx=5, pady=5)
        self.filter_date_to = DateEntry(filter_frame, width=12,
                                        date_pattern='yyyy-mm-dd')
        self.filter_date_to.grid(row=0, column=5, padx=5, pady=5)

        # Кнопка применения фильтра
        apply_btn = Button(filter_frame, text="Применить фильтр",
                          command=self.apply_filter,
                          bg=self.colors['info'], fg='white',
                          font=self.fonts['normal'])
        apply_btn.grid(row=0, column=6, padx=10, pady=5)

        # Кнопка сброса фильтра
        reset_btn = Button(filter_frame, text="Сбросить",
                          command=self.reset_filter,
                          bg=self.colors['warning'], fg='white',
                          font=self.fonts['normal'])
        reset_btn.grid(row=0, column=7, padx=5, pady=5)

    def create_stats_panel(self):
        """Панель статистики"""
        stats_frame = LabelFrame(self.root, text="📊 Статистика",
                                 font=self.fonts['heading'],
                                 padx=10, pady=10, bg=self.colors['bg'])
        stats_frame.pack(fill=X, padx=10, pady=5)

        # Общая сумма за период
        Label(stats_frame, text="Сумма за период:", font=self.fonts['normal'],
              bg=self.colors['bg']).grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.total_amount_label = Label(stats_frame, text="0.00 ₽",
                                        font=('Arial', 14, 'bold'),
                                        fg=self.colors['success'],
                                        bg=self.colors['bg'])
        self.total_amount_label.grid(row=0, column=1, padx=5, pady=5)

        # Количество записей
        Label(stats_frame, text="Количество:", font=self.fonts['normal'],
              bg=self.colors['bg']).grid(row=0, column=2, sticky=W, padx=5, pady=5)
        self.count_label = Label(stats_frame, text="0",
                                 font=('Arial', 12, 'bold'),
                                 fg=self.colors['primary'],
                                 bg=self.colors['bg'])
        self.count_label.grid(row=0, column=3, padx=5, pady=5)

        # Кнопка обновления статистики
        refresh_stats_btn = Button(stats_frame, text="Обновить статистику",
                                   command=self.update_stats,
                                   bg=self.colors['primary'], fg='white',
                                   font=self.fonts['normal'])
        refresh_stats_btn.grid(row=0, column=4, padx=20, pady=5)

    def create_table(self):
        """Создание таблицы с расходами"""
        # Фрейм для таблицы и скролла
        table_frame = Frame(self.root, bg=self.colors['bg'])
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Создание скроллов
        scrollbar_y = Scrollbar(table_frame)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        scrollbar_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        # Создание таблицы
        columns = ('ID', 'Дата', 'Категория', 'Сумма')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                                 yscrollcommand=scrollbar_y.set,
                                 xscrollcommand=scrollbar_x.set)

        # Настройка колонок
        self.tree.heading('ID', text='ID')
        self.tree.heading('Дата', text='Дата')
        self.tree.heading('Категория', text='Категория')
        self.tree.heading('Сумма', text='Сумма (₽)')

        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Дата', width=100, anchor='center')
        self.tree.column('Категория', width=150, anchor='w')
        self.tree.column('Сумма', width=100, anchor='e')

        self.tree.pack(fill=BOTH, expand=True)

        # Настройка скроллов
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        # Привязка события двойного клика для удаления
        self.tree.bind('<Double-Button-1>', self.delete_selected)

    def create_bottom_panel(self):
        """Нижняя панель с кнопками"""
        bottom_frame = Frame(self.root, bg=self.colors['bg'])
        bottom_frame.pack(fill=X, padx=10, pady=10)

        # Кнопка удаления выбранного
        delete_btn = Button(bottom_frame, text="🗑️ Удалить выбранный расход",
                           command=self.delete_selected,
                           bg=self.colors['danger'], fg='white',
                           font=self.fonts['normal'], padx=20)
        delete_btn.pack(side=LEFT, padx=5)

        # Кнопка экспорта в JSON
        export_btn = Button(bottom_frame, text="💾 Экспорт в JSON",
                           command=self.export_data,
                           bg=self.colors['info'], fg='white',
                           font=self.fonts['normal'], padx=20)
        export_btn.pack(side=LEFT, padx=5)

        # Кнопка импорта из JSON
        import_btn = Button(bottom_frame, text="📁 Импорт из JSON",
                           command=self.import_data,
                           bg=self.colors['warning'], fg='white',
                           font=self.fonts['normal'], padx=20)
        import_btn.pack(side=LEFT, padx=5)

        # Кнопка очистки всех данных
        clear_btn = Button(bottom_frame, text="⚠️ Очистить всё",
                           command=self.clear_all_data,
                           bg='gray', fg='white',
                           font=self.fonts['normal'], padx=20)
        clear_btn.pack(side=RIGHT, padx=5)

    def add_expense(self):
        """Добавление нового расхода"""
        try:
            # Проверка суммы
            amount_str = self.amount_entry.get().strip()
            if not amount_str:
                messagebox.showwarning("Ошибка", "Введите сумму расхода!")
                return

            amount = float(amount_str)
            if amount <= 0:
                messagebox.showwarning("Ошибка", "Сумма должна быть положительной!")
                return
            if amount > 1000000:
                messagebox.showwarning("Ошибка", "Сумма не может превышать 1,000,000 ₽!")
                return

            # Проверка категории
            category = self.category_combo.get()
            if category == "Выберите..." or not category:
                messagebox.showwarning("Ошибка", "Выберите категорию!")
                return

            # Получение даты
            date = self.date_entry.get()

            # Проверка формата даты
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат даты!")
                return

            # Добавление расхода
            expense = {
                'id': self.next_id,
                'amount': amount,
                'category': category,
                'date': date,
                'created_at': datetime.now().isoformat()
            }

            self.expenses.append(expense)
            self.next_id += 1

            # Сохранение и обновление
            self.save_data()
            self.refresh_table()
            self.update_stats()

            # Очистка полей ввода
            self.amount_entry.delete(0, END)
            self.category_combo.set("Выберите...")

            messagebox.showinfo("Успех", "Расход успешно добавлен!")

        except ValueError:
            messagebox.showwarning("Ошибка", "Введите корректное число в поле суммы!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def delete_selected(self, event=None):
        """Удаление выбранного расхода"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите расход для удаления!")
            return

        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранный расход?"):
            for item in selected:
                values = self.tree.item(item, 'values')
                expense_id = int(values[0])

                # Удаление из списка
                self.expenses = [e for e in self.expenses if e['id'] != expense_id]

            # Сохранение и обновление
            self.save_data()
            self.refresh_table()
            self.update_stats()

            messagebox.showinfo("Успех", "Расход(ы) удалены!")

    def apply_filter(self):
        """Применение фильтрации"""
        self.refresh_table()

    def reset_filter(self):
        """Сброс фильтрации"""
        self.filter_category.set("Все")
        self.filter_date_from.set_date(datetime.now().replace(month=1, day=1))
        self.filter_date_to.set_date(datetime.now())
        self.refresh_table()

    def refresh_table(self):
        """Обновление таблицы с учётом фильтров"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Получение фильтров
        filter_cat = self.filter_category.get()
        filter_from = self.filter_date_from.get()
        filter_to = self.filter_date_to.get()

        # Фильтрация расходов
        filtered_expenses = self.expenses.copy()

        if filter_cat != "Все":
            filtered_expenses = [e for e in filtered_expenses if e['category'] == filter_cat]

        if filter_from and filter_to:
            filtered_expenses = [e for e in filtered_expenses
                                if filter_from <= e['date'] <= filter_to]

        # Сортировка по дате (новые сверху)
        filtered_expenses.sort(key=lambda x: x['date'], reverse=True)

        # Добавление в таблицу
        for expense in filtered_expenses:
            self.tree.insert('', END, values=(
                expense['id'],
                expense['date'],
                expense['category'],
                f"{expense['amount']:.2f}"
            ))

        # Обновление статистики
        self.update_stats_for_list(filtered_expenses)

    def update_stats(self):
        """Обновление панели статистики"""
        self.refresh_table()

    def update_stats_for_list(self, expenses_list):
        """Обновление статистики для переданного списка"""
        total = sum(e['amount'] for e in expenses_list)
        count = len(expenses_list)

        self.total_amount_label.config(text=f"{total:.2f} ₽")
        self.count_label.config(text=str(count))

        # Изменение цвета в зависимости от суммы
        if total > 50000:
            self.total_amount_label.config(fg='red')
        elif total > 20000:
            self.total_amount_label.config(fg='orange')
        else:
            self.total_amount_label.config(fg=self.colors['success'])

    def save_data(self):
        """Сохранение данных в JSON"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.expenses, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")

    def load_data(self):
        """Загрузка данных из JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.expenses = json.load(f)
                    if self.expenses:
                        self.next_id = max(e['id'] for e in self.expenses) + 1
                    else:
                        self.next_id = 1
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
                self.expenses = []
                self.next_id = 1

    def export_data(self):
        """Экспорт данных в JSON файл"""
        from tkinter import filedialog

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Сохранить как"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.expenses, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Успех", f"Данные экспортированы в {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось экспортировать данные: {str(e)}")

    def import_data(self):
        """Импорт данных из JSON файла"""
        from tkinter import filedialog

        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Выберите файл для импорта"
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    imported = json.load(f)

                    if messagebox.askyesno("Подтверждение",
                                          f"Найдено {len(imported)} записей. Импортировать их?"):
                        # Обновление ID
                        for expense in imported:
                            expense['id'] = self.next_id
                            self.next_id += 1
                            self.expenses.append(expense)

                        self.save_data()
                        self.refresh_table()
                        messagebox.showinfo("Успех", f"Импортировано {len(imported)} записей!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось импортировать данные: {str(e)}")

    def clear_all_data(self):
        """Очистка всех данных"""
        if messagebox.askyesno("Подтверждение",
                              "⚠️ ВНИМАНИЕ! Это действие удалит ВСЕ расходы!\n\nВы уверены?"):
            self.expenses = []
            self.next_id = 1
            self.save_data()
            self.refresh_table()
            messagebox.showinfo("Успех", "Все данные удалены!")


def main():
    """Запуск приложения"""
    root = Tk()

    # Установка иконки (опционально)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass

    app = ExpenseTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
