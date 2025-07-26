import tkinter as tk
from tkinter import messagebox
from Calculator import (CalculatorContext, NormalArithmeticStrategy, PolynomialStrategy, LogCommand, SinCommand, CosCommand)

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.expression = ""
        self.context = CalculatorContext(NormalArithmeticStrategy())
        self.root.attributes("-fullscreen", True)
        self.current_coefficient = None
        self.coefficients = {'a': None, 'b': None, 'const': None}

        self.display = tk.Label(root, text="", anchor='e', font=('TimesNewRoman', 36), bg="white", height=3, relief='sunken')
        self.display.grid(row=0, column=0, columnspan=5, sticky='nsew')

        root.grid_rowconfigure(0, weight=2)  # Top display row with more space
        for i in range(2, 8):
            root.grid_rowconfigure(i, weight=1)
        for i in range(5):
            root.grid_columnconfigure(i, weight=1)

        for idx, num in enumerate("7894561230", start=1):
            row, col = divmod(idx - 1, 3)
            tk.Button(root, text=num, font=('Times New Roman',24), bg='#B0C4DE', command=lambda n=num: self.add_to_expression(n)).grid(row=row + 2, column=col, sticky='nsew')

        tk.Button(root, text='C', font=('Times New Roman',24), bg='#FF6347', command=self.clear_expression).grid(row=5, column=1, sticky='nsew')
        tk.Button(root, text='=', font=('Times New Roman',24), bg='#48D1CC', command=self.calculate).grid(row=5, column=2, sticky='nsew')

        for symbol, pos in zip("+-*/", range(1, 5)):
            tk.Button(root, text=symbol, font=('Times New Roman',24), bg='#E6BE8A', command=lambda op=symbol: self.add_to_expression(op)).grid(row=pos + 1, column=3, sticky='nsew')

        tk.Button(root, text='log', font=('Times New Roman',24), bg='#FAFAD2', command=lambda: self.apply_decorator(LogCommand)).grid(row=2, column=4, sticky='nsew')
        tk.Button(root, text='sin', font=('Times New Roman',24), bg='#FAFAD2', command=lambda: self.apply_decorator(SinCommand)).grid(row=3, column=4, sticky='nsew')
        tk.Button(root, text='cos', font=('Times New Roman',24), bg='#FAFAD2', command=lambda: self.apply_decorator(CosCommand)).grid(row=4, column=4, sticky='nsew')

        tk.Button(root, text='Quadratic', font=('Times New Roman',24), bg='#FFB6C1', command=self.set_polynomial_strategy).grid(row=6, column=0, columnspan=2, sticky='nsew')
        tk.Button(root, text='Arithmetic', font=('Times New Roman',24), bg='#FFB6C1', command=self.set_arithmetic_strategy).grid(row=7, column=0, columnspan=2, sticky='nsew')

        tk.Button(root, text='Coeff a', font=('Times New Roman',24), bg='#FFD966', command=lambda: self.set_coefficient('a')).grid(row=6, column=2, sticky='nsew')
        tk.Button(root, text='Coeff b', font=('Times New Roman',24), bg='#FFD966', command=lambda: self.set_coefficient('b')).grid(row=6, column=3, sticky='nsew')
        tk.Button(root, text='Const', font=('Times New Roman',24), bg='#FFD966', command=lambda: self.set_coefficient('const')).grid(row=6, column=4, sticky='nsew')

    def add_to_expression(self, char):
        if self.current_coefficient:
            if self.coefficients[self.current_coefficient] is None:
                self.coefficients[self.current_coefficient] = char
            else:
                self.coefficients[self.current_coefficient] += char
            self.display['text'] = f"Set {self.current_coefficient} = {self.coefficients[self.current_coefficient]}"
        else:
            self.expression += char
            self.display['text'] = self.expression

    def clear_expression(self):
        self.expression = ""
        self.current_coefficient = None
        self.coefficients = {'a': None, 'b': None, 'const': None}
        self.display['text'] = ""

    def calculate(self):
        if isinstance(self.context.strategy, PolynomialStrategy):
            try:
                a = float(self.coefficients['a'])
                b = float(self.coefficients['b'])
                const = float(self.coefficients['const'])
                coefficients = [a, b, const]

                result = self.context.calculate(coefficients)
                self.display['text'] = str(result)
            except ValueError:
                messagebox.showerror("Input Error", "Please provide valid numeric values for all coefficients.")
            except TypeError:
                messagebox.showerror("Input Error", "All coefficients must be set before solving.")
        else:
            result = self.context.calculate(self.expression)
            self.display['text'] = str(result)
            self.expression = ""

    def apply_decorator(self, CommandClass):
        try:
            result = float(self.display['text'])
            command = CommandClass(result)
            self.display['text'] = f"{command.execute()}"
        except ValueError:
            self.display['text'] = "Error"

    def set_polynomial_strategy(self):
        self.context.set_strategy(PolynomialStrategy())
        self.display['text'] = "Quadratic mode set."

    def set_arithmetic_strategy(self):
        self.context.set_strategy(NormalArithmeticStrategy())
        self.display['text'] = "Arithmetic mode set."

    def set_coefficient(self, coefficient):
        self.current_coefficient = coefficient
        self.display['text'] = f"Setting {coefficient}"

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="white")
    app = CalculatorApp(root)
    root.mainloop()
