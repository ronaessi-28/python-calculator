import tkinter as tk
from tkinter import messagebox, filedialog
import math
import statistics

root = tk.Tk()
root.title("Python Calculator")
root.geometry("600x600")
#root.resizable(0, 0)

is_dark_mode = True
memory_value = ""
history = []
last_answer = ""

def update_theme():
    bg_color = "#000000" if is_dark_mode else "#FFFFFF"
    fg_color = "white" if is_dark_mode else "black"
    root.config(bg=bg_color)
    entry_frame.config(bg=bg_color)
    button_frame.config(bg=bg_color)
    entry.config(bg="#2a2a3b" if is_dark_mode else "#DDDDDD", fg=fg_color)

entry_frame = tk.Frame(root,bg="#000000")
entry_frame.pack(pady=10,fill="both")

entry_var = tk.StringVar()
entry = tk.Entry(entry_frame, textvariable=entry_var, font=("Segoe UI", 24), bd=5, relief="ridge", width=22, justify="right")
entry.pack(padx=5,pady=10,fill="x")

button_frame = tk.Frame(root)
button_frame.pack()

buttons = [
    ['Rad', 'Deg', 'x!', '(', ')', '%', 'AC'],
    ['Inv', 'sin', 'ln', '7', '8', '9', '÷'],
    ['π', 'cos', 'log', '4', '5', '6', '×'],
    ['e', 'tan', '√', '1', '2', '3', '-'],
    ['Ans', 'EXP', 'xⁿ', '0', '.', '=', '+'],
    ['Mean', 'Mode', 'Median', 'MR', 'MC', 'D/L', 'DEL'],
]

button_colors = {
    'AC': "#FF0000",
    'Ans': "#B22222",
    '=': "#008000",
    '+': "#191970",
    '-': "#191970",
    '÷': "#191970",
    '×': "#191970",
    '.': "#444444",
    '(': "#FF8C00",
    ')': "#FF8C00",
    'Rad': "#808000",
    'Deg': "#808000",
    'Inv': "#808000",
    'EXP': "#800080",
    'π': "#B22222",
    'e': "#B22222",
    'x!': "#28B463",
    '√': "#800080",
    'xⁿ': "#800080",
    'sin': "#800000",
    'cos': "#800000",
    'tan': "#800000",
    'log': "#28B463",
    'ln': "#28B463",
    '%': "#FF8C00",
    'Mean': "#20B2AA",
    'Mode': "#20B2AA",
    'Median': "#20B2AA",
    'MR': "#F4A460",
    'MC': "#F4A460",
    'D/L': "#2E8B57",
    'DEL': "#FF0000",
}

def insert_value(value):
    entry_var.set(entry_var.get() + value)

def clear_entry():
    entry_var.set("")

def calculate_ans():
    global last_answer
    entry_var.set(entry_var.get() + last_answer)

def evaluate_expression():
    global last_answer, memory_value
    try:
        expr = entry_var.get()
        expr = expr.replace('÷', '/').replace('×', '*').replace('π', str(math.pi)).replace('e', str(math.e))
        expr = expr.replace('√', 'math.sqrt').replace('xⁿ', '**').replace('sin', 'math.sin')
        expr = expr.replace('cos', 'math.cos').replace('tan', 'math.tan').replace('log', 'math.log10')
        expr = expr.replace('ln', 'math.log').replace('EXP', '*10**').replace('%', '/100')
        expr = expr.replace('Rad', '').replace('Deg', '')
        if 'x!' in expr:
            expr = expr.replace('x!', '')
            num = int(entry_var.get()[:-2])
            result = math.factorial(num)
        else:
            result = eval(expr)
        last_answer = str(result)
        memory_value = last_answer
        history.append(f"{entry_var.get()} = {result}")
        entry_var.set(str(result))
    except Exception as e:
        messagebox.showerror("Error", f"Invalid Input!\n\n{e}")
        entry_var.set("")



def delete_last_char():
    current = entry_var.get()
    entry_var.set(current[:-1])

def memory_recall():
    global memory_value
    entry_var.set(entry_var.get() + memory_value)

def memory_clear():
    global memory_value
    memory_value = ""

def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    update_theme()

def calculate_statistic(stat_type):
    global last_answer
    try:
        expr = entry_var.get()
        numbers = [float(n) for n in expr.split(',') if n.strip() != '']
        if stat_type == 'mean':
            result = statistics.mean(numbers)
            history.append(f"Mean = {result}")
        elif stat_type == 'mode':
            result = statistics.mode(numbers)
            history.append(f"Mode = {result}")
        elif stat_type == 'median':
            result = statistics.median(numbers)
            history.append(f"Median = {result}")
        else:
            raise ValueError("Invalid Statistical Operation")
        
        last_answer = str(result)
        entry_var.set(str(result))
    except statistics.StatisticsError as e:
        messagebox.showerror("Statistics Error", f"{e}")
        entry_var.set("")
    except Exception as e:
        messagebox.showerror("Error", f"{e}")
        entry_var.set("")


special_commands = {
    'AC': clear_entry,
    '=': evaluate_expression,
    'Ans': calculate_ans,
    'DEL': delete_last_char,
    'MR': memory_recall,
    'MC': memory_clear,
    'D/L': toggle_theme,
    'Mean': lambda: calculate_statistic('mean'),
    'Mode': lambda: calculate_statistic('mode'),
    'Median': lambda: calculate_statistic('median'),
}

def create_buttons():
    for r, row in enumerate(buttons):
        for c, char in enumerate(row):
            color = button_colors.get(char, "#444444")
            action = special_commands.get(char, lambda ch=char: insert_value(ch))
            btn = tk.Button(button_frame, text=char, bg=color, fg="white", font=("Segoe UI", 14), width=5, height=2, bd=3, relief="raised", command=action)
            btn.grid(row=r, column=c, padx=5, pady=5)

create_buttons()

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Calculation History")
    history_window.geometry("400x400")

    text_area = tk.Text(history_window, wrap="word")
    text_area.pack(expand=True, fill="both")

    for item in history:
        text_area.insert("end", item + "\n")

    menu = tk.Menu(history_window)
    history_window.config(menu=menu)

    file_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Save History", command=lambda: save_history(text_area.get("1.0", "end-1c")))

def save_history(content):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(content)
        messagebox.showinfo("Success", "History saved successfully!")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
menu_bar.add_command(label="History", command=show_history)

update_theme()
root.mainloop()
