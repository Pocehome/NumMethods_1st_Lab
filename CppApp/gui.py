import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker
import numpy as np
from Lab_1_Module import TestTask, FirstTask, SecondTask

class Window:
    def __init__(self, master):
        # variables
        self.table_data = None
        self.A = None
        self.B = None
        self.U0 = None
        self.step_size = None
        self.max_e_error = None
        self.e_border = None
        self.max_steps = None
        self.alpha = None
        self.final_ref = None
        self.mode = 1
        self.task_num = 0

        # window master
        self.master = master
        self.master.title("Задача Коши для ОДУ")
        self.master.geometry("1300x600")

        # Create interface elements for task selection
        tk.Label(self.master, text="Задача").grid(row=0, column=0, sticky='w')
        
        # Dropdown for task selection
        self.task_selector = ttk.Combobox(self.master, values=["Тестовая", "Первая", "Вторая"])
        self.task_selector.grid(row=1, column=0, sticky='we')
        self.task_selector.set("Тестовая")  # Default value
        self.task_selector.bind("<<ComboboxSelected>>", self.on_task_selected)

        # Toggle button
        tk.Label(self.master, text="Режим работы").grid(row=4, column=0, sticky='w')
        self.button_mode = tk.Button(self.master, text="С ОЛП", command=self.toggle_mode)
        self.button_mode.grid(row=5, column=0, sticky='we')

        # Display widgets for "Тестовая задача" by default
        self.create_test_task_widgets()

    def on_task_selected(self, event):
        selected_task = self.task_selector.get()
        self.clear_widgets()

        # Re-add dropdown and label after clearing
        tk.Label(self.master, text="Задача").grid(row=0, column=0, sticky='w')
        self.task_selector.grid(row=1, column=0, sticky='we')

        # Toggle button
        tk.Label(self.master, text="Режим работы").grid(row=4, column=0, sticky='w')
        self.button_mode = tk.Button(self.master, text="С ОЛП", command=self.toggle_mode)
        self.button_mode.grid(row=5, column=0, sticky='we')
        self.mode = 1

        # Choose which widgets to display based on selected task
        if selected_task == "Тестовая":
            self.task_num = 0
            self.create_test_task_widgets()
        elif selected_task == "Первая":
            self.task_num = 1
            self.create_first_task_widgets()
        elif selected_task == "Вторая":
            self.task_num = 2
            self.create_second_task_widgets()

    def clear_widgets(self):
        # Remove all widgets except the dropdown
        for widget in self.master.winfo_children():
            if widget not in [self.task_selector, tk.Label(self.master, text="Задача")]:
                widget.destroy()
        
        # Clear variables
        self.table_data = None
        self.A = None
        self.B = None
        self.U0 = None
        self.step_size = None
        self.max_e_error = None
        self.e_border = None
        self.max_steps = None
        self.alpha = None
        self.final_ref = None

    def create_test_task_widgets(self):
        self.master.grid_columnconfigure(0, weight=100)
        self.master.grid_columnconfigure(1, weight=2)
        self.master.grid_columnconfigure(2, weight=2)
        self.master.grid_columnconfigure(3, weight=2)

        # Input fields for test task
        tk.Label(self.master, text="A:").grid(row=0, column=1, sticky='e')
        tk.Label(self.master, text="B:").grid(row=1, column=1, sticky='e')
        tk.Label(self.master, text="U0:").grid(row=2, column=1, sticky='e')
        tk.Label(self.master, text="Начальный шаг:").grid(row=3, column=1, sticky='e')
        tk.Label(self.master, text="Макс. число шагов:").grid(row=4, column=1, sticky='e')
        tk.Label(self.master, text="Точность выхода на границу:").grid(row=5, column=1, sticky='e')
        if self.mode == 1:
            tk.Label(self.master, text="Контроль лок. погрешности:").grid(row=6, column=1, sticky='e')

        # Input fields
        self.entry_a = tk.Entry(self.master)
        self.entry_b = tk.Entry(self.master)
        self.entry_u0 = tk.Entry(self.master)
        self.entry_step_size = tk.Entry(self.master)
        self.entry_max_steps = tk.Entry(self.master)
        self.entry_e_border = tk.Entry(self.master)
        if self.mode == 1:
            self.entry_max_e_error = tk.Entry(self.master)

        # Set default values
        self.entry_a.insert(0, "0.0")
        self.entry_b.insert(0, "1.0")
        self.entry_u0.insert(0, "1.0")
        self.entry_step_size.insert(0, "0.1")
        self.entry_max_steps.insert(0, "10000")
        self.entry_e_border.insert(0, "1e-6")
        if self.mode == 1:
            self.entry_max_e_error.insert(0, "1e-6")

        # Placement of input fields
        self.entry_a.grid(row=0, column=2, sticky='ew')
        self.entry_b.grid(row=1, column=2, sticky='ew')
        self.entry_u0.grid(row=2, column=2, sticky='ew')
        self.entry_step_size.grid(row=3, column=2, sticky='ew')
        self.entry_max_steps.grid(row=4, column=2, sticky='ew')
        self.entry_e_border.grid(row=5, column=2, sticky='ew')
        if self.mode == 1:
            self.entry_max_e_error.grid(row=6, column=2, sticky='ew')

        # Calculate button
        self.calculate_button = tk.Button(self.master, text="Вычислить", command=self.calculate_values)
        self.calculate_button.grid(row=6, column=0, sticky='we')

        # Create Treeview to display the table
        self.tree = ttk.Treeview(self.master, columns=["Col"+str(i) for i in range(10)], show="headings")
        self.tree.grid(row=8, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)  # Place the table under input fields

        # Add horizontal and vertical scrolling
        vsb = ttk.Scrollbar(self.master, orient="vertical", command=self.tree.yview)
        vsb.grid(row=7, column=2, sticky='sne', rowspan=3)
        self.tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(self.master, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=9, column=0, columnspan=3, sticky='esw')
        self.tree.configure(xscrollcommand=hsb.set)

        # Configure stretching
        self.master.grid_rowconfigure(8, weight=1)  # Allows the table to expand vertically
        self.master.grid_columnconfigure(0, weight=1)  # Allows the table to expand horizontally

        # Create figure for the plot
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)

        # Create a Text widget for final report
        self.final_report_text = tk.Text(self.master, height=10, width=50)
        self.final_report_text.grid(row=0, column=4, rowspan=7, sticky='nwe', padx=5, pady=5)

        # Place the canvas (the graph) in the bottom right
        self.canvas.get_tk_widget().grid(row=6, column=4, rowspan=5, sticky='se', padx=5, pady=5)

    def create_first_task_widgets(self):
        self.master.grid_columnconfigure(0, weight=100)
        self.master.grid_columnconfigure(1, weight=2)
        self.master.grid_columnconfigure(2, weight=2)
        self.master.grid_columnconfigure(3, weight=2)

        # Input fields for test task
        tk.Label(self.master, text="A:").grid(row=0, column=1, sticky='e')
        tk.Label(self.master, text="B:").grid(row=1, column=1, sticky='e')
        tk.Label(self.master, text="U0:").grid(row=2, column=1, sticky='e')
        tk.Label(self.master, text="Начальный шаг:").grid(row=3, column=1, sticky='e')
        tk.Label(self.master, text="Макс. число шагов:").grid(row=4, column=1, sticky='e')
        tk.Label(self.master, text="Точность выхода на границу:").grid(row=5, column=1, sticky='e')
        if self.mode == 1:
            tk.Label(self.master, text="Контроль лок. погрешности:").grid(row=6, column=1, sticky='e')

        # Input fields
        self.entry_a = tk.Entry(self.master)
        self.entry_b = tk.Entry(self.master)
        self.entry_u0 = tk.Entry(self.master)
        self.entry_step_size = tk.Entry(self.master)
        self.entry_max_steps = tk.Entry(self.master)
        self.entry_e_border = tk.Entry(self.master)
        if self.mode == 1:
            self.entry_max_e_error = tk.Entry(self.master)

        # Set default values
        self.entry_a.insert(0, "0.0")
        self.entry_b.insert(0, "1.0")
        self.entry_u0.insert(0, "1.0")
        self.entry_step_size.insert(0, "0.1")
        self.entry_max_steps.insert(0, "10000")
        self.entry_e_border.insert(0, "1e-6")
        if self.mode == 1:
            self.entry_max_e_error.insert(0, "1e-6")

        # Placement of input fields
        self.entry_a.grid(row=0, column=2, sticky='ew')
        self.entry_b.grid(row=1, column=2, sticky='ew')
        self.entry_u0.grid(row=2, column=2, sticky='ew')
        self.entry_step_size.grid(row=3, column=2, sticky='ew')
        self.entry_max_steps.grid(row=4, column=2, sticky='ew')
        self.entry_e_border.grid(row=5, column=2, sticky='ew')
        if self.mode == 1:
            self.entry_max_e_error.grid(row=6, column=2, sticky='ew')

        # Calculate button
        self.calculate_button = tk.Button(self.master, text="Вычислить", command=self.calculate_values)
        self.calculate_button.grid(row=6, column=0, sticky='we')

        # Create Treeview to display the table
        self.tree = ttk.Treeview(self.master, columns=["Col"+str(i) for i in range(10)], show="headings")
        self.tree.grid(row=8, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)  # Place the table under input fields

        # Add horizontal and vertical scrolling
        vsb = ttk.Scrollbar(self.master, orient="vertical", command=self.tree.yview)
        vsb.grid(row=7, column=2, sticky='sne', rowspan=3)
        self.tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(self.master, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=9, column=0, columnspan=3, sticky='esw')
        self.tree.configure(xscrollcommand=hsb.set)

        # Configure stretching
        self.master.grid_rowconfigure(8, weight=1)  # Allows the table to expand vertically
        self.master.grid_columnconfigure(0, weight=1)  # Allows the table to expand horizontally

        # Create figure for the plot
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)

        # Create a Text widget for final report
        self.final_report_text = tk.Text(self.master, height=10, width=50)
        self.final_report_text.grid(row=0, column=4, rowspan=7, sticky='nwe', padx=5, pady=5)

        # Place the canvas (the graph) in the bottom right
        self.canvas.get_tk_widget().grid(row=6, column=4, rowspan=5, sticky='se', padx=5, pady=5)

    def create_second_task_widgets(self):
        self.master.grid_columnconfigure(0, weight=100)
        self.master.grid_columnconfigure(1, weight=2)
        self.master.grid_columnconfigure(2, weight=2)
        self.master.grid_columnconfigure(3, weight=2)

        # Input fields for test task
        tk.Label(self.master, text="A:").grid(row=0, column=1, sticky='e')
        tk.Label(self.master, text="B:").grid(row=1, column=1, sticky='e')
        tk.Label(self.master, text="U0:").grid(row=2, column=1, sticky='e')
        tk.Label(self.master, text="Начальный шаг:").grid(row=3, column=1, sticky='e')
        tk.Label(self.master, text="Макс. число шагов:").grid(row=4, column=1, sticky='e')
        tk.Label(self.master, text="Точность выхода на границу:").grid(row=5, column=1, sticky='e')
        if self.mode == 1:
            tk.Label(self.master, text="Контроль лок. погрешности:").grid(row=6, column=1, sticky='e')
        tk.Label(self.master, text="Альфа:").grid(row=2, column=0, sticky='w')

        # Input fields
        self.entry_a = tk.Entry(self.master)
        self.entry_b = tk.Entry(self.master)
        self.entry_u0 = tk.Entry(self.master)
        self.entry_step_size = tk.Entry(self.master)
        self.entry_max_steps = tk.Entry(self.master)
        self.entry_e_border = tk.Entry(self.master)
        if self.mode == 1:
            self.entry_max_e_error = tk.Entry(self.master)
        self.entry_alpha = tk.Entry(self.master)

        # Set default values
        self.entry_a.insert(0, "0.0")
        self.entry_b.insert(0, "10.0")
        self.entry_u0.insert(0, "1.0")
        self.entry_step_size.insert(0, "0.1")
        self.entry_max_steps.insert(0, "10000")
        self.entry_e_border.insert(0, "1e-6")
        if self.mode == 1:
            self.entry_max_e_error.insert(0, "1e-6")
        self.entry_alpha.insert(0, "1")

        # Placement of input fields
        self.entry_a.grid(row=0, column=2, sticky='ew')
        self.entry_b.grid(row=1, column=2, sticky='ew')
        self.entry_u0.grid(row=2, column=2, sticky='ew')
        self.entry_step_size.grid(row=3, column=2, sticky='ew')
        self.entry_max_steps.grid(row=4, column=2, sticky='ew')
        self.entry_e_border.grid(row=6, column=2, sticky='ew')
        if self.mode == 1:
            self.entry_max_e_error.grid(row=5, column=2, sticky='ew')
        self.entry_alpha.grid(row=3, column=0, sticky='ew')

        # Calculate button
        self.calculate_button = tk.Button(self.master, text="Вычислить", command=self.calculate_values)
        self.calculate_button.grid(row=6, column=0, sticky='we')

        # Create Treeview to display the table
        self.tree = ttk.Treeview(self.master, columns=["Col"+str(i) for i in range(10)], show="headings")
        self.tree.grid(row=7, rowspan=2, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)  # Place the table under input fields

        # Add horizontal and vertical scrolling
        vsb = ttk.Scrollbar(self.master, orient="vertical", command=self.tree.yview)
        vsb.grid(row=7, column=2, sticky='sne', rowspan=3)
        self.tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(self.master, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=9, column=0, columnspan=3, sticky='esw')
        self.tree.configure(xscrollcommand=hsb.set)

        # Configure stretching
        self.master.grid_rowconfigure(8, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Create figure for the plot
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)

        # Create a Text widget for final report
        self.final_report_text = tk.Text(self.master, height=10, width=50)
        self.final_report_text.grid(row=0, column=4, rowspan=7, sticky='nwe', padx=5, pady=5)

        # Place the canvas (the graph) in the bottom right
        self.canvas.get_tk_widget().grid(row=6, column=4, rowspan=5, sticky='se', padx=5, pady=5)

        # Кнопка для построения графика V'(V)
        self.plot_button = tk.Button(self.master, text="Построить график V'(V)", command=self.toggle_plot)
        self.plot_button.grid(row=7, column=4, sticky='we', padx=5, pady=5)

    def calculate_values(self):
        try:
            selected_task = self.task_selector.get()

            # Получение значений из полей ввода
            self.A = float(self.entry_a.get())
            self.B = float(self.entry_b.get())
            self.U0 = float(self.entry_u0.get())
            self.step_size = float(self.entry_step_size.get())
            self.max_steps = int(self.entry_max_steps.get())
            self.e_border = float(self.entry_e_border.get())
            if self.mode == 1:
                self.max_e_error = float(self.entry_max_e_error.get())
            else:
                self.max_e_error = 0

            if self.task_num == 2:
                self.alpha = float(self.entry_alpha.get())

            # Проверки на корректность значений
            if self.A >= self.B:
                messagebox.showerror("Ошибка", "Значение A должно быть меньше B.")
                return
            if self.max_steps <= 1:
                messagebox.showerror("Ошибка", "Максимальное количество шагов должно быть больше 1.")
                return

            # Выбор задачи на основе выбранного элемента в ComboBox
            if self.task_num == 0:
                task = TestTask(self.A, self.B, self.step_size, self.max_e_error, self.e_border, self.max_steps, self.U0)
            elif self.task_num == 1:
                task = FirstTask(self.A, self.B, self.step_size, self.max_e_error, self.e_border, self.max_steps, self.U0)
            elif self.task_num == 2:
                task = SecondTask(self.A, self.B, self.step_size, self.max_e_error, self.e_border, self.max_steps, self.U0)
                task.set_alpha(self.alpha)

            # Вычисление
            if self.mode == 1:
                task.Solve_With_Error_Control()
            else:
                task.Solve_Without_Error_Control()
            self.table_data = task.get_table_information()
            self.update_table()

            # Отчет
            self.final_ref = task.get_final_reference()
            self.show_final_reference()

            # Обновление графика
            if self.task_num == 2:
                if self.plot_button.cget('text') == "Построить график V'(V)":
                    self.plot_graph_V_X()
                else:
                    self.plot_v0_v1()
            else:
                self.plot_graph_V_X()

        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные значения.")

    # Функция для переключения между режимами
    def toggle_mode(self):
        self.clear_widgets()

        # Re-add dropdown and label after clearing
        tk.Label(self.master, text="Задача").grid(row=0, column=0, sticky='w')
        self.task_selector.grid(row=1, column=0, sticky='we')

        # Toggle button
        tk.Label(self.master, text="Режим работы").grid(row=4, column=0, sticky='w')
        self.button_mode = tk.Button(self.master, command=self.toggle_mode)
        self.button_mode.grid(row=5, column=0, sticky='we')

        if self.mode == 1:
            self.button_mode.config(text='Без ОЛП')
            self.mode = 0
        else:
            self.button_mode.config(text='С ОЛП')
            self.mode = 1

        # Choose which widgets to display based on selected task
        if self.task_num == 0:
            self.create_test_task_widgets()
        elif self.task_num == 1:
            self.create_first_task_widgets()
        elif self.task_num == 2:
            self.create_second_task_widgets()

    # Функция для переключения между графиками
    def toggle_plot(self):
        if self.plot_button.cget('text') == "Построить график V'(V)":
            self.plot_v0_v1()
            self.plot_button.config(text="Построить график V(X)")
        else:
            self.plot_graph_V_X()
            self.plot_button.config(text="Построить график V'(V)")

    def update_table(self):
        # Clear Treeview before updating
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Set column headers
        if self.task_num == 0:
            if self.mode == 0:
                columns = ["i", "X", "V", "h", "U", "|U-V|"]
                arr_width = [50, 100, 100, 100, 100, 100]
            else:
                columns = ["i", "X", "V", "V^", "V-V^", "ОЛП", "h", "/2", "*2", "U", "|U-V|"]
                arr_width = [50, 100, 100, 100, 100, 100, 100, 50, 50, 100, 100]

        elif self.task_num == 1:
            if self.mode == 0:
                columns = ["i", "X", "V", "h"]
                arr_width = [50, 100, 100, 100]
            else:
                columns = ["i", "X", "V", "V^", "V-V^", "ОЛП", "h", "/2", "*2"]
                arr_width = [50, 100, 100, 100, 100, 100, 100, 50, 50]
        
        elif self.task_num == 2:
            if self.mode == 0:
                columns = ["i", "X", "V0", "V1", "h"]
                arr_width = [50, 100, 100, 100, 100]
            else:
                columns = ["i", "X", "V0", "V1", "V0^", "V1^", "V0-V0^", "V1-V1^", "ОЛП", "h", "/2", "*2"]
                arr_width = [50, 100, 100, 100, 100, 100, 100, 100, 100, 100, 50, 50]
            

        if list(self.tree["columns"]) != columns:
            self.tree["columns"] = columns
            for i in range(len(columns)):
                self.tree.heading(columns[i], text=columns[i])
                self.tree.column(columns[i], width=arr_width[i], minwidth=arr_width[i])  # Set column width

        # Add data to the table with formatting
        for row in self.table_data:
            formatted_row = [f"{value:.6g}" if isinstance(value, float) else value for value in row]
            self.tree.insert("", "end", values=formatted_row)

    def plot_graph_V_X(self):
        # Очистка графика
        self.ax.clear()

        # Построение графика истинного решения
        if self.task_num == 0:
            X = np.linspace(self.A, self.B, 100)
            U = self.U0 * np.exp(-X / 2)

            # Plot U(X)
            self.ax.plot(X, U, label=f'U(X) = {self.U0} * exp(-X/2)', color='blue', alpha=0.7)

        # Extract X and V values from table data for the second plot
        X_values = [row[1] for row in self.table_data]
        V_values = [row[2] for row in self.table_data]

        # Построение графика численного решения
        self.ax.plot(X_values, V_values, label='V(X)', color='red', alpha=0.7)

        # Set log scale for Y-axis if task is "Первая"
        if self.task_num == 1 and self.U0 > 0:
            self.ax.set_yscale("log")
        else:
            self.ax.set_yscale("linear")  # Ensure other tasks use a linear scale

        # Customize the plot
        self.ax.set_xlabel('X')
        # self.ax.xaxis.set_tick_params(labelsize=8)
        # self.ax.yaxis.set_tick_params(labelsize=8)
        self.ax.legend()
        self.ax.grid()

        # Автоматическая настройка размещения элементов графика
        self.ax.figure.tight_layout()

        # Update the plot
        self.canvas.draw()

    def plot_v0_v1(self):
        try:
            # Extract X and V values from table data for the second plot
            V0_values = [row[2] for row in self.table_data]
            V1_values = [row[3] for row in self.table_data]

            # Очистка и построение графика
            self.ax.clear()
            self.ax.plot(V0_values, V1_values, label="V'(V)", color='blue')

            # Customize the plot
            self.ax.set_xlabel("V")
            #self.ax.set_ylabel("V1")
            self.ax.legend()
            self.ax.grid()

            # Update the plot
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить график: {e}")

    def show_final_reference(self):
        # Clear the previous report text
        self.final_report_text.delete(1.0, tk.END)

        # Insert new information into the Text widget
        if self.mode == 0:
            info = (
                f"Кол-во итераций: {self.final_ref.ITERATIONS_COUNT}\n"
                f"Расстояние до последней точки: {self.final_ref.DISTANCE_B_LAST_POINT}\n"
            )
        else:
            info = (
                f"Кол-во итераций: {self.final_ref.ITERATIONS_COUNT}\n"
                f"Расстояние до последней точки: {self.final_ref.DISTANCE_B_LAST_POINT}\n"
                f"Кол-во удвоений шага: {self.final_ref.STEP_DOUBLING_COUNT}\n"
                f"Кол-во уменьшений шага: {self.final_ref.STEP_REDUCTION_COUNT}\n"
                f"Макс. шаг с X: {self.final_ref.MAX_STEP_WITH_X}\n"
                f"Мин. шаг с X: {self.final_ref.MIN_STEP_WITH_X}\n"
                f"Макс. значение оценки олп: {self.final_ref.MAX_ERROR}\n"
            )
        if self.task_num == 0:
            info += (
                f"Макс. расстояние U-V: {self.final_ref.MAX_DISTANCE_U_V}"
            )
        if self.final_ref.IS_INF:
            info += (
                "На следующем шаге значение X перейдёт через асимптоту, поэтому вычисление следующего значения V невозможно"
            )

        self.final_report_text.insert(tk.END, info)

def create_gui():
    root = tk.Tk()
    app = Window(root)
    root.mainloop()

if __name__ == "__main__":
    create_gui()