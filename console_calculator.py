from calculator_model import CalculatorModel

def console_calculator():
    """Консольная версия калькулятора"""
    model = CalculatorModel()
    
    print("=" * 60)
    print("КОНСОЛЬНЫЙ КАЛЬКУЛЯТОР МАТЕМАТИЧЕСКИХ ВЫРАЖЕНИЙ")
    print("=" * 60)
    print("\nПоддерживаемые операторы: +, -, *, /, ^, //")
    print("Пример: -3234+843/3234-4232123/(34+123+32+5)*3234")
    print("Для выхода введите 'exit'")
    print("-" * 60)
    
    while True:
        try:
            expression = input("\nВведите выражение: ").strip()
            
            if expression.lower() == 'exit':
                print("Выход из программы...")
                break
            
            if not expression:
                continue

            is_valid, message = model.validate_expression(expression)
            if not is_valid:
                print(f"Ошибка: {message}")
                continue

            result = model.calculate(expression)
            print(f"Результат: {result}")
            
        except ValueError as e:
            print(f"Ошибка: {e}")
        except ZeroDivisionError:
            print("Ошибка: Деление на ноль")
        except KeyboardInterrupt:
            print("\n\nПрограмма завершена.")
            break
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

if __name__ == "__main__":
    console_calculator()
