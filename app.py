import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from bmi_utils import calculate_bmi, get_bmi_category

DATA_FILE = "data/bmi_data.json"

def suggest_weight_change(weight, height, bmi):
    min_normal = 18.5 * (height ** 2)
    max_normal = 24.9 * (height ** 2)

    if bmi < 18.5:
        gain = round(min_normal - weight, 2)
        return f"You are underweight.\n→ You need to gain at least {gain} kg to reach normal BMI."
    elif bmi >= 25:
        lose = round(weight - max_normal, 2)
        return f"You are overweight/obese.\n→ You need to lose at least {lose} kg to reach normal BMI."
    else:
        return "You are in the normal BMI range.\n→ Maintain your current weight!"

def save_data(bmi):
    os.makedirs("data", exist_ok=True)
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass
    data.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "bmi": bmi
    })
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def show_history_graph():
    if not os.path.exists(DATA_FILE):
        messagebox.showinfo("No Data", "No BMI data found.")
        return
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    if not data:
        messagebox.showinfo("No Data", "No BMI data found.")
        return

    dates = [entry["date"] for entry in data]
    bmis = [entry["bmi"] for entry in data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, bmis, marker='o', linestyle='-', color='green')
    plt.title("BMI History Over Time")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def calculate():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            raise ValueError

        bmi = calculate_bmi(weight, height)
        category = get_bmi_category(bmi)
        suggestion = suggest_weight_change(weight, height, bmi)

        result_label.config(
            text=f"BMI: {bmi}\nCategory: {category}\n\n{suggestion}",
            fg="darkblue"
        )
        save_data(bmi)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid positive numbers.")

# GUI
root = tk.Tk()
root.title("BMI Calculator")

tk.Label(root, text="Weight (kg):").grid(row=0, column=0, padx=10, pady=5)
weight_entry = tk.Entry(root)
weight_entry.grid(row=0, column=1)

tk.Label(root, text="Height (m):").grid(row=1, column=0, padx=10, pady=5)
height_entry = tk.Entry(root)
height_entry.grid(row=1, column=1)

tk.Button(root, text="Calculate BMI", command=calculate).grid(row=2, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="", font=("Arial", 11), wraplength=320, justify="left")
result_label.grid(row=3, column=0, columnspan=2, pady=5)

tk.Button(root, text="View History Graph", command=show_history_graph).grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
