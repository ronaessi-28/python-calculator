import tkinter as tk
import math
import re

root = tk.Tk()
root.title("Colorful Calculator")
root.geometry("550x480")
root.config(bg="#000000")

entry_var = tk.StringVar()
last_answer = ""
angle_mode = "RAD"
history = []

# ------------------- Entry Field and History Button --------------------
entry_frame = tk.Frame(root, bg="#000000")
entry_frame.pack(pady=10, fill="x")

def show_history():
    history_win = tk.Toplevel(root)
    history_win.title("History")
    history_win.geometry("300x400")
    history_win.config(bg="#000000")
    for item in history:
        tk.Label(history_win, text=item, bg="#000000", fg="white", font=("Segoe UI", 14)).pack(anchor='w', padx=10, pady=5)

history_btn = tk.Button(entry_frame, text="📜", command=show_history, bg="#2a2a3b", fg="white", bd=0)
history_btn.pack(side="left", padx=(10, 5), pady=10)

entry = tk.Entry(entry_frame, textvariable=entry_var, font=("Segoe UI", 24), justify="right", bd=0, bg="#2a2a3b", fg="white")
entry.pack(padx=5, pady=10, fill="x", expand=True)

# ------------------- Calculator Logic --------------------
def append_char(char):
    current = entry_var.get()

    if char in ['sin', 'cos', 'tan', 'log', 'ln']:
        entry_var.set(current + f"{char}(")
    elif char == ')':
        if current.count('(') > current.count(')'):
            entry_var.set(current + ')')
    elif char == 'Rad':
        global angle_mode
        angle_mode = "RAD"
    elif char == 'Deg':
        angle_mode = "DEG"
    elif char == 'Ans':
        entry_var.set(current + last_answer)
    elif char == 'π':
        entry_var.set(current + str(math.pi))
    elif char == 'e':
        entry_var.set(current + str(math.e))
    elif char == 'EXP':
        entry_var.set(current + "e")
    elif char == 'Inv':
        entry_var.set(current + "1/(")
    elif char == '√':
        entry_var.set(current + "√(")
    elif char == 'xⁿ':
        entry_var.set(current + "^")
    elif char == '÷':
        entry_var.set(current + "/")
    elif char == '×':
        entry_var.set(current + "*")
    elif char == '%':
        entry_var.set(current + "/100")
    else:
        entry_var.set(current + str(char))

def clear():
    entry_var.set("")

def apply_factorial():
    try:
        expr = entry_var.get()
        num = ''
        i = len(expr) - 1
        while i >= 0 and (expr[i].isdigit() or expr[i] == '.'):
            num = expr[i] + num
            i -= 1
        if num:
            fact = math.factorial(int(float(num)))
            new_expr = expr[:i+1] + str(fact)
            entry_var.set(new_expr)
            history.append(expr + "!" + " = " + str(fact))
    except:
        entry_var.set("Error")

def evaluate_expression():
    global last_answer
    try:
        expr = entry_var.get()
        original_expr = expr

        # --- Replace constants and operators ---
        expr = expr.replace('^', '**')
        expr = expr.replace('π', str(math.pi))
        expr = re.sub(r'(?<![a-zA-Z])e(?![a-zA-Z])', str(math.e), expr)
        expr = re.sub(r'(\d)(?=\()', r'\1*', expr)
        expr = re.sub(r'(\))(\d)', r'\1*\2', expr)

        # --- Replace square root ---
        expr = re.sub(r'√\((.*?)\)', r'math.sqrt(\1)', expr)

        # --- Replace log10 and ln with safe parsing ---
        expr = re.sub(r'log\(([^()]+)\)', r'math.log10(\1)', expr)
        expr = re.sub(r'ln\(([^()]+)\)', r'math.log(\1)', expr)

        # --- Replace trigonometric functions ---
        def convert_trig(match):
            func = match.group(1)
            val = match.group(2)
            if angle_mode == "DEG":
                return f"math.{func}(math.radians({val}))"
            return f"math.{func}({val})"

        expr = re.sub(r'\b(sin|cos|tan)\((.*?)\)', convert_trig, expr)

        result = str(round(eval(expr), 5))
        history.append(original_expr + " = " + result)
        last_answer = result
        entry_var.set(result)

    except Exception as e:
        entry_var.set("Error")
        print("Error:", e)

# ------------------- Special Commands --------------------
special_commands = {
    'AC': clear,
    '=': evaluate_expression,
    'x!': apply_factorial,
}

# ------------------- Button Layout (5x7 Grid) --------------------
buttons = [
    ['Rad', 'Deg', 'x!', '(', ')', '%', 'AC'],
    ['Inv', 'sin', 'ln', '7', '8', '9', '÷'],
    ['π', 'cos', 'log', '4', '5', '6', '×'],
    ['e', 'tan', '√', '1', '2', '3', '-'],
    ['Ans', 'EXP', 'xⁿ', '0', '.', '=', '+'],
]

# ------------------- Button Colors --------------------
button_colors = {
    'AC': "#FF0000", '=': "#008000",
    '÷': "#191970", '×': "#191970", '-': "#191970", '+': "#191970",
    '(': "#FF8C00", ')': "#FF8C00", '%': "#FF8C00",
    'Rad': "#808000", 'Deg': "#808000",
    'sin': "#800000", 'cos': "#800000", 'tan': "#800000",
    'Inv': "#B22222", 'π': "#B22222", 'e': "#B22222", 'Ans': "#B22222",
    'x!': "#800080", 'ln': "#800080", 'log': "#800080", '√': "#800080", 'xⁿ': "#800080", 'EXP': "#800080",
}

# ------------------- Hover Effect --------------------
def on_enter(btn, color):
    btn.config(bg="gray25")

def on_leave(btn, original):
    btn.config(bg=original)

# ------------------- Button Rendering --------------------
button_frame = tk.Frame(root, bg="#000000")
button_frame.pack()

for r in range(5):
    for c in range(7):
        text = buttons[r][c]
        btn_color = button_colors.get(text, "#444444")
        action = special_commands.get(text, lambda ch=text: append_char(ch))
        btn = tk.Button(button_frame, text=text, font=("Segoe UI", 14), bg=btn_color, fg="white",
                        width=5, height=2, bd=0, command=action)
        btn.bind("<Enter>", lambda e, b=btn: on_enter(b, "#2a2a3b"))
        btn.bind("<Leave>", lambda e, b=btn, col=btn_color: on_leave(b, col))
        btn.grid(row=r, column=c, padx=5, pady=5)

root.mainloop()
