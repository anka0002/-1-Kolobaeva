class CalculatorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.root.bind('<Return>', lambda event: self.calculate_expression())
    
    def calculate_expression(self, expression=None):
        """Обработка вычисления выражения"""
        if expression is None:
            expression = self.view.expression_entry.get()
        
        if not expression:
            self.view.show_error("Введите математическое выражение")
            return
        
        try:
            result = self.model.calculate(expression)

            self.view.show_result(expression, result)
            
        except ValueError as e:
            self.view.show_error(str(e))
        except ZeroDivisionError:
            self.view.show_error("Деление на ноль")
        except Exception as e:
            self.view.show_error(f"Неизвестная ошибка: {str(e)}")
