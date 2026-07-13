import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



  # Must be explicitly imported



import schemas
import window_flows



# =====================================================================
# 5. FIRST WINDOW ROOT INTERFACE
# =====================================================================

root = tk.Tk()
root.title("System Selection Panel")
root.geometry("380x220")

frame = ttk.Frame(root, padding="20")
frame.pack(fill="both", expand=True)

# Generate list choices directly from our central registry keys
architecture_var = tk.StringVar(value=list(schemas.ARCHITECTURES.keys())[0])
disorder_var = tk.StringVar(value=list(schemas.DISORDERS.keys())[0])

# Layout selections
ttk.Label(frame, text="Select Architecture:").grid(row=0, column=0, sticky="w", pady=10)
ttk.Combobox(frame, textvariable=architecture_var, values=list(schemas.ARCHITECTURES.keys()), state="readonly", width=22).grid(row=0, column=1, pady=10, padx=10)

ttk.Label(frame, text="Select Disorder Type:").grid(row=1, column=0, sticky="w", pady=10)
ttk.Combobox(frame, textvariable=disorder_var, values=list(schemas.DISORDERS.keys()), state="readonly", width=22).grid(row=1, column=1, pady=10, padx=10)

# Trigger Launch Executions
btn_box = ttk.Frame(frame)
btn_box.grid(row=2, column=0, columnspan=2, pady=20)

ttk.Button(btn_box, text="Pivot", command=lambda: window_flows.open_configuration_window(root,"Pivot", architecture_var, disorder_var)).pack(side="left", padx=10)
ttk.Button(btn_box, text="LAMMPS set up", command=lambda: window_flows.open_configuration_window(root,"LAMMPS set up", architecture_var, disorder_var)).pack(side="left", padx=10)

root.mainloop()
