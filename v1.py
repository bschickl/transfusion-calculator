import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        starting_hct = float(entry_starting_hct.get())
        ending_hct = float(entry_ending_hct.get())
        weight = float(entry_weight.get())

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

        # Display Results
        label_result.config(text=f"Desired Increase Hct: {desired_increase_hct:.2f}\n"
                                 f"Transfusion Coefficient: {transfusion_coefficient:.2f}\n"
                                 f"Volume to Transfuse: {volume_to_transfuse:.2f} mL")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Create GUI window
root = tk.Tk()
root.title("Transfusion Calculator")

# Labels and Input Fields
tk.Label(root, text="Starting Hct:").grid(row=0, column=0, padx=10, pady=5)
entry_starting_hct = tk.Entry(root)
entry_starting_hct.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Ending Hct:").grid(row=1, column=0, padx=10, pady=5)
entry_ending_hct = tk.Entry(root)
entry_ending_hct.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Weight (g):").grid(row=2, column=0, padx=10, pady=5)
entry_weight = tk.Entry(root)
entry_weight.grid(row=2, column=1, padx=10, pady=5)

# Calculate Button
btn_calculate = tk.Button(root, text="Calculate", command=calculate)
btn_calculate.grid(row=3, column=0, columnspan=2, pady=10)

# Results Display
label_result = tk.Label(root, text="Results will be displayed here", fg="blue")
label_result.grid(row=4, column=0, columnspan=2, pady=10)

# Run the GUI
root.mainloop()
