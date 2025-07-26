import math
from abc import ABC, abstractmethod
import re

# Command Pattern
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class AddCommand(Command):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def execute(self):
        return self.a + self.b

class SubtractCommand(Command):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def execute(self):
        return self.a - self.b

class MultiplyCommand(Command):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def execute(self):
        return self.a * self.b

class DivideCommand(Command):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def execute(self):
        if self.b == 0:
            return "Error: Division by zero"
        return self.a / self.b

class LogCommand(Command):
    def __init__(self, value):
        self.value = value

    def execute(self):
        if self.value <= 0:
            return "Error: Logarithm undefined for non-positive values"
        return math.log(self.value)

class SinCommand(Command):
    def __init__(self, value):
        self.value = value

    def execute(self):
        return math.sin(self.value)

class CosCommand(Command):
    def __init__(self, value):
        self.value = value

    def execute(self):
        return math.cos(self.value)

# Decorator Pattern
class CommandDecorator(Command):
    def __init__(self, command):
        self.command = command

    def execute(self):
        return self.command.execute()

class LogDecorator(CommandDecorator):
    def execute(self):
        value = super().execute()
        if value <= 0:
            return "Error: Logarithm undefined for non-positive values"
        result = math.log(value)
        return result

class SinDecorator(CommandDecorator):
    def execute(self):
        value = super().execute()
        result = math.sin(value)
        return result

class CosDecorator(CommandDecorator):
    def execute(self):
        value = super().execute()
        result = math.cos(value)
        return result

# Strategy Pattern
class CalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, expression):
        pass

class NormalArithmeticStrategy(CalculationStrategy):
    def parse_expression(self, expression):
        return re.findall(r'\d+|\+|\-|\*|\/', expression)

    def evaluate_expression(self, expression):
        tokens = self.parse_expression(expression)
        
        i = 0
        while i < len(tokens):
            if tokens[i] == '*':
                result = MultiplyCommand(float(tokens[i - 1]), float(tokens[i + 1])).execute()
                tokens[i - 1:i + 2] = [result]
                i -= 1
            elif tokens[i] == '/':
                result = DivideCommand(float(tokens[i - 1]), float(tokens[i + 1])).execute()
                tokens[i - 1:i + 2] = [result]
                i -= 1
            else:
                i += 1

        i = 0
        while i < len(tokens):
            if tokens[i] == '+':
                result = AddCommand(float(tokens[i - 1]), float(tokens[i + 1])).execute()
                tokens[i - 1:i + 2] = [result]
                i -= 1
            elif tokens[i] == '-':
                result = SubtractCommand(float(tokens[i - 1]), float(tokens[i + 1])).execute()
                tokens[i - 1:i + 2] = [result]
                i -= 1
            else:
                i += 1

        return tokens[0] if tokens else "Invalid expression"

    def calculate(self, expression):
        return self.evaluate_expression(expression)

class PolynomialStrategy(CalculationStrategy):
    def calculate(self, coefficients_str):
        # Split the string into individual coefficients and convert them to floats
        coefficients = [float(coef) for coef in coefficients_str]

        if len(coefficients) != 3:
            return "Error: Please provide exactly three coefficients for a quadratic equation."

        a, b, c = coefficients
        discriminant = b**2 - 4*a*c

        if discriminant > 0:
            root1 = (-b + math.sqrt(discriminant)) / (2 * a)
            root2 = (-b - math.sqrt(discriminant)) / (2 * a)
            return f"Roots are {root1} and {root2}"
        elif discriminant == 0:
            root = -b / (2 * a)
            return f"Root is {root}"
        else:
            return "No real roots"

class CalculatorContext:
    def __init__(self, strategy: CalculationStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: CalculationStrategy):
        self.strategy = strategy

    def calculate(self, expression):
        return self.strategy.calculate(expression)

if __name__ == "__main__":
    print("Direct Calculations with Command Pattern:")
    direct_log = LogCommand(10)
    print(f"Direct log(10): {direct_log.execute()}")

    direct_sin = SinCommand(1)
    print(f"Direct sin(1): {direct_sin.execute()}")

    context = CalculatorContext(NormalArithmeticStrategy())
    expression = "10 + 2 * 5 - 3 / 2"
    result = context.calculate(expression)
    print(f"\nResult for '{expression}': {result}")

    print("\nApplying Decorators to Result:")
    arithmetic_command = AddCommand(10, 5)
    log_wrapped_result = LogDecorator(arithmetic_command)
    log_result = log_wrapped_result.execute()

    sin_wrapped_result = SinDecorator(log_wrapped_result)
    sin_result = sin_wrapped_result.execute()

    cos_wrapped_result = CosDecorator(sin_wrapped_result)
    cos_result = cos_wrapped_result.execute()
    print(f"Result after applying Log, Sin, and Cos decorators: {cos_result}")

    # Polynomial example
    coefficients_input = "134"  # Representing 1, 3, and 4 for the quadratic equation
    polynomial_context = CalculatorContext(PolynomialStrategy())
    polynomial_result = polynomial_context.calculate(coefficients_input)
    print(f"\nPolynomial result for coefficients '{coefficients_input}': {polynomial_result}")
