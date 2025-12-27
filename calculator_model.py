import re

class CalculatorModel:
    def __init__(self):
        self.operators = {
            '+': (1, lambda x, y: x + y),
            '-': (1, lambda x, y: x - y),
            '*': (2, lambda x, y: x * y),
            '/': (2, lambda x, y: x / y if y != 0 else float('inf')),
            '^': (3, lambda x, y: x ** y),
            '//': (2, lambda x, y: x // y if y != 0 else float('inf'))
        }
        self.pattern = r'(\d+\.?\d*|[+\-*/^]|//)'
        
    def validate_expression(self, expression):
        """Проверка корректности выражения"""
        expression = expression.replace(' ', '')

        if not expression:
            return False, "Выражение пустое"

        if not expression[0].isdigit() and expression[0] != '-':
            return False, "Выражение должно начинаться с числа"
        
        if not expression[-1].isdigit():
            return False, "Выражение должно заканчиваться числом"

        tokens = re.findall(self.pattern, expression)
        numbers = [t for t in tokens if re.match(r'^-?\d+\.?\d*$', t)]
        
        if len(numbers) > 100:
            return False, "Превышено максимальное количество слагаемых (100)"

        for i in range(len(tokens) - 1):
            curr = tokens[i]
            next_token = tokens[i + 1]
            
            if re.match(r'^-?\d+\.?\d*$', curr) and re.match(r'^-?\d+\.?\d*$', next_token):
                return False, "Два числа подряд без оператора"
            
            if curr in self.operators and next_token in self.operators and next_token != '-':
                return False, "Два оператора подряд"
        
        return True, "Выражение корректно"
    
    def shunting_yard(self, expression):
        """Алгоритм сортировочной станции (Shunting-yard)"""
        expression = expression.replace(' ', '')
        tokens = re.findall(r'(\d+\.?\d*|[+\-*/^]|//|[()])', expression)
        
        output = []
        operators = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if re.match(r'^-?\d+\.?\d*$', token):
                output.append(float(token))
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()  # Удаляем '('
            elif token in self.operators:
                if token == '-' and (i == 0 or tokens[i-1] in self.operators or tokens[i-1] == '('):
                    tokens[i] = '~'
                    continue
                
                while (operators and operators[-1] != '(' and 
                       operators[-1] in self.operators and
                       self.operators[operators[-1]][0] >= self.operators[token][0]):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '~':
                output.append(0)
                operators.append('-')
            
            i += 1
        
        while operators:
            output.append(operators.pop())
        
        return output
    
    def calculate_rpn(self, rpn):
        """Вычисление выражения в обратной польской записи"""
        stack = []
        
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.operators:
                if len(stack) < 2:
                    raise ValueError("Недостаточно операндов")
                b = stack.pop()
                a = stack.pop()
                result = self.operators[token][1](a, b)
                stack.append(result)
            else:
                if token == '~':
                    if not stack:
                        raise ValueError("Недостаточно операндов")
                    a = stack.pop()
                    stack.append(-a)
        
        if len(stack) != 1:
            raise ValueError("Ошибка в вычислениях")
        
        return stack[0]
    
    def calculate(self, expression):
        """Основной метод вычисления выражения"""
        is_valid, message = self.validate_expression(expression)
        if not is_valid:
            raise ValueError(message)

        expression_with_parentheses = expression

        rpn = self.shunting_yard(expression_with_parentheses)

        result = self.calculate_rpn(rpn)
        
        return result
