import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Database Setup
conn = sqlite3.connect("transfusion_data.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transfusion_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mrn TEXT,
        date TEXT,
        starting_hct REAL,
        ending_hct REAL,
        desired_increase_hct REAL,
        transfusion_coefficient REAL,
        weight REAL,
        volume_to_transfuse REAL
    )
""")
conn.commit()

def save_to_database(mrn, starting_hct, ending_hct, desired_increase_hct, transfusion_coefficient, weight, volume_to_transfuse):
    """Save transfusion calculation data into SQLite database."""
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO transfusion_records (mrn, date, starting_hct, ending_hct, desired_increase_hct, transfusion_coefficient, weight, volume_to_transfuse)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (mrn, date, starting_hct, ending_hct, desired_increase_hct, transfusion_coefficient, weight, volume_to_transfuse))
    conn.commit()

def retrieve_previous_data(mrn):
    """Retrieve previous calculations for a given MRN."""
    cursor.execute("SELECT date, starting_hct, ending_hct, desired_increase_hct, transfusion_coefficient, weight, volume_to_transfuse FROM transfusion_records WHERE mrn = ? ORDER BY date DESC", (mrn,))
    return cursor.fetchall()

def calculate():
    try:
        mrn = entry_mrn.get().strip()
        starting_hct = float(entry_starting_hct.get())
        ending_hct = float(entry_ending_hct.get())
        weight = float(entry_weight.get())

        if not mrn:
            messagebox.showerror("Input Error", "Please enter a Medical Record Number.")
            return

        # Calculate Desired Increase Hct
        desired_increase_hct = ending_hct - starting_hct

        # Determine Transfusion Coefficient
        if desired_increase_hct < 11:
            transfusion_coefficient = 0.02
        elif desired_increase_hct < 16:
            transfusion_coefficient = 0.03
        elif desired_increase_hct < 21:
            transfusion_coefficient = 0.04
        elif desired_increase_hct < 26:
            transfusion_coefficient = 0.05
        elif desired_increase_hct < 31:
            transfusion_coefficient = 0.06
        elif desired_increase_hct < 36:
            transfusion_coefficient = 0.07
        elif desired_increase_hct < 41:
            transfusion_coefficient = 0.08
        else:
            transfusion_coefficient = 0.08  # Default if Hct is too high

        # Calculate Volume to Transfuse
        volume_to_transfuse = transfusion_coefficient * weight

        # Save data to database
        save_to_database(mrn, starting_hct, ending_hct, desired_increase_hct, transfusion_coefficient, weight, volume_to_transfuse)

        # Display Results
        label_result.config(text=f"Desired Increase Hct: {desired_increase_hct:.2f}\n"
                                 f"Transfusion Coefficient: {transfusion_coefficient:.2f}\n"
                                 f"Volume to Transfuse: {volume_to_transfuse:.2f} mL")

        # Retrieve and display previous calculations
        previous_records = retrieve_previous_data(mrn)
        if previous_records:
            history_text = "Previous Calculations:\n"
            for record in previous_records:
                history_text += (f"{record[0]} - Start Hct: {record[1]}, End Hct: {record[2]}, "
                                 f"ΔHct: {record[3]:.2f}, Coeff: {record[4]:.2f}, "
                                 f"Weight: {record[5]}, Volume: {record[6]:.2f} mL\n")
            label_history.config(text=history_text)
        else:
            label_history.config(text="No previous records found.")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Create GUI window
root = tk.Tk()
root.title("Transfusion Calculator with Database")

# Labels and Input Fields
tk.Label(root, text="Medical Record Number (MRN):").grid(row=0, column=0, padx=10, pady=5)
entry_mrn = tk.Entry(root)
entry_mrn.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Starting Hct:").grid(row=1, column=0, padx=10, pady=5)
entry_starting_hct = tk.Entry(root)
entry_starting_hct.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Ending Hct:").grid(row=2, column=0, padx=10, pady=5)
entry_ending_hct = tk.Entry(root)
entry_ending_hct.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Weight (g):").grid(row=3, column=0, padx=10, pady=5)
entry_weight = tk.Entry(root)
entry_weight.grid(row=3, column=1, padx=10, pady=5)

# Calculate Button
btn_calculate = tk.Button(root, text="Calculate", command=calculate)
btn_calculate.grid(row=4, column=0, columnspan=2, pady=10)

# Results Display
label_result = tk.Label(root, text="Results will be displayed here", fg="blue")
label_result.grid(row=5, column=0, columnspan=2, pady=10)

# History Display
label_history = tk.Label(root, text="Previous calculations will be displayed here", fg="green", justify="left")
label_history.grid(row=6, column=0, columnspan=2, pady=10)

# Run the GUI
root.mainloop()
