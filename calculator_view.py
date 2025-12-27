import tkinter as tk
from tkinter import ttk, messagebox

class CalculatorView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Калькулятор математических выражений")
        self.root.geometry("800x600")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 11))

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = ttk.Label(main_frame, 
                                text="Калькулятор математических выражений",
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        ttk.Label(main_frame, text="Введите математическое выражение:").grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.expression_entry = ttk.Entry(main_frame, width=70, font=("Arial", 12))
        self.expression_entry.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        operators_frame = ttk.Frame(main_frame)
        operators_frame.grid(row=3, column=0, columnspan=3, pady=(0, 20))
        
        operators = ['+', '-', '*', '/', '^', '//', '(', ')']
        for i, op in enumerate(operators):
            btn = ttk.Button(operators_frame, text=op, width=5,
                            command=lambda o=op: self.insert_operator(o))
            btn.grid(row=0, column=i, padx=2)

        example_frame = ttk.LabelFrame(main_frame, text="Пример", padding="10")
        example_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        example_label = ttk.Label(example_frame, 
                                 text="-3234+843/3234-4232123/(34+123+32+5)*3234",
                                 font=("Courier", 11))
        example_label.grid(row=0, column=0, sticky=tk.W)

        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=3, pady=(0, 20))
        
        ttk.Button(buttons_frame, text="Вычислить", 
                  command=self.calculate).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Очистить", 
                  command=self.clear).grid(row=0, column=1, padx=5)

        result_frame = ttk.LabelFrame(main_frame, text="Результат", padding="10")
        result_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.result_text = tk.Text(result_frame, height=10, width=70, 
                                  font=("Courier", 11), wrap=tk.WORD)
        self.result_text.grid(row=0, column=0)
        
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", 
                                 command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text.config(yscrollcommand=scrollbar.set)

        requirements_frame = ttk.LabelFrame(main_frame, text="Требования", padding="10")
        requirements_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        requirements = [
            "1. Поддерживаемые операторы: +, -, *, /, ^ (степень), // (целочисленное деление)",
            "2. Максимальное количество слагаемых: 100",
            "3. Выражение должно начинаться и заканчиваться числом",
            "4. Можно использовать скобки для задания приоритета операций"
        ]
        
        for i, req in enumerate(requirements):
            ttk.Label(requirements_frame, text=req).grid(row=i, column=0, sticky=tk.W, pady=2)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
    
    def insert_operator(self, operator):
        """Вставка оператора в поле ввода"""
        current = self.expression_entry.get()
        position = self.expression_entry.index(tk.INSERT)
        self.expression_entry.insert(position, operator)
    
    def calculate(self):
        """Обработка вычисления"""
        expression = self.expression_entry.get()
        self.controller.calculate_expression(expression)
    
    def clear(self):
        """Очистка полей"""
        self.expression_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)
    
    def show_result(self, expression, result, steps=None):
        """Отображение результата"""
        self.result_text.delete(1.0, tk.END)
        
        self.result_text.insert(tk.END, f"Выражение: {expression}\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n")
        
        if steps:
            for step in steps:
                self.result_text.insert(tk.END, f"{step}\n")
        
        self.result_text.insert(tk.END, f"\nРезультат: {result}\n")
    
    def show_error(self, error_message):
        """Отображение ошибки"""
        messagebox.showerror("Ошибка", error_message)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Ошибка: {error_message}")
