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
        return f"📌 You are underweight.\n→ Gain at least **{gain} kg** to reach a normal BMI."
    elif bmi >= 25:
        lose = round(weight - max_normal, 2)
        return f"📌 You are overweight/obese.\n→ Lose at least **{lose} kg** to reach a normal BMI."
    else:
        return "🎉 You are in the normal BMI range.\n→ Keep maintaining your current weight!"

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
    plt.title("📈 BMI History Over Time")
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

        min_normal = round(18.5 * (height ** 2), 2)
        max_normal = round(24.9 * (height ** 2), 2)

        emoji = {
            "Underweight": "🟦",
            "Normal weight": "✅",
            "Overweight": "⚠️",
            "Obese": "❗"
        }

        result_label.config(
            text=f"📊 Your BMI: **{bmi}**\n"
                 f"{emoji[category]} Category: {category}\n\n"
                 f"🎯 Normal BMI Range: 18.5 - 24.9\n"
                 f"💡 Ideal Weight Range: {min_normal}kg - {max_normal}kg\n\n"
                 f"{suggestion}",
            fg="navy"
        )
        save_data(bmi)

    except ValueError:
        messagebox.showerror("Input Error", "⚠️ Please enter valid positive numbers.")

# GUI Setup
root = tk.Tk()
root.title("🌟 Smart BMI Calculator")
root.configure(bg="#f0f8ff")

tk.Label(root, text="Weight (kg):", bg="#f0f8ff", font=("Segoe UI", 10)).grid(row=0, column=0, padx=10, pady=5)
weight_entry = tk.Entry(root, font=("Segoe UI", 10))
weight_entry.grid(row=0, column=1)

tk.Label(root, text="Height (m):", bg="#f0f8ff", font=("Segoe UI", 10)).grid(row=1, column=0, padx=10, pady=5)
height_entry = tk.Entry(root, font=("Segoe UI", 10))
height_entry.grid(row=1, column=1)

tk.Button(root, text="Calculate BMI", command=calculate, font=("Segoe UI", 10)).grid(row=2, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="", bg="#f0f8ff", fg="darkgreen", font=("Segoe UI", 11, "bold"), wraplength=350, justify="left")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

tk.Button(root, text="📈 View History Graph", command=show_history_graph, font=("Segoe UI", 10)).grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
