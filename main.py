import tkinter as tk
from calculator_model import CalculatorModel
from calculator_view import CalculatorView
from calculator_controller import CalculatorController

def main():
    root = tk.Tk()

    model = CalculatorModel()
    controller = CalculatorController(model, None)
    view = CalculatorView(root, controller)

    controller.view = view

    root.mainloop()

if __name__ == "__main__":
    main()
