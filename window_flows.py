
# window_flows.py
import tkinter as tk
from tkinter import ttk, messagebox

# IMPORT FILE 1 & 2: Pull widgets and registry schemas
import window_components # type: ignore
import schemas # type: ignore

# =====================================================================
# 4. WINDOW MANAGEMENT LOGIC
# =====================================================================

def open_configuration_window(root_window, action_type, architecture_var, disorder_var):
    arch_key = architecture_var.get()
    disorder_key = disorder_var.get()
    
    # Retrieve the registered schema objects mapping to selections
    arch_schema = schemas.ARCHITECTURES.get(arch_key)
    disorder_schema = schemas.DISORDERS.get(disorder_key)
    
    if not arch_schema or not disorder_schema:
        messagebox.showerror("Error", "Invalid selection schema encountered.")
        return

    # Master Top-Level Setup
    window = tk.Toplevel(root_window)
    window.title(f"{action_type} - System Parameters Setup")
    window.geometry("450x500")
    
    header = ttk.Label(window, text=f"Configure System for {action_type}", font=("Helvetica", 13, "bold"))
    header.pack(pady=10)
    
    # --- Structural Parameter Frame ---
    arch_frame = ttk.LabelFrame(window, text=f" 1. Structural Parameters ({arch_schema.name}) ", padding="10")
    arch_frame.pack(fill="x", padx=15, pady=5)
    # The selected schema object draws its own custom widgets dynamically here:
    arch_schema.build_widgets(arch_frame)
    
    # --- Disorder Parameter Frame ---
    disorder_frame = ttk.LabelFrame(window, text=f" 2. Statistical Variation ({disorder_schema.name}) ", padding="10")
    disorder_frame.pack(fill="x", padx=15, pady=5)
    # The chosen disorder configuration handles its own design layout:
    disorder_schema.build_widgets(disorder_frame)

    # Simply instantiate the component frame directly in the window hierarchy
    output_folder_browser = window_components.FolderBrowseWidget(window, label_text="Save Simulation to:")
    
    # 4. Action Lower Bar
    action_frame = ttk.Frame(window, padding="10")
    action_frame.pack(fill="x", side="bottom")
    
    run_text = "Generate Data & Input" if action_type == "LAMMPS set up" else "Execute"
    
    # Handle the submission while passing out the chosen directory path
    def run_simulation_flow():
        """
        Triggers when clicking the 'Execute Transformation' button inside this settings window.
        """
        # A. Pull destination path safely from the browser widget
        target_path = output_folder_browser.get_path()
        if not target_path:
            messagebox.showwarning("Missing Path", "Please select a target output directory first.")
            return

        # B. Handle structural parameters specifically for your Star Polymer setup
        if arch_schema.name == "Star":
            try:
                # Safely extract text entries built dynamically by the active schemas
                f_arms = int(arch_schema.arms.get().strip())
                n_avg = int(arch_schema.length.get().strip())
                t_production=int(arch_schema.time.get().strip())
                replicas=int(arch_schema.replicas.get().strip())

                if hasattr(arch_schema, 'k_entry'):
                    raw_k = arch_schema.k_entry.get().strip()
                    # Handle empty strings, "None", or uniform cases safely
                    if not raw_k or raw_k.lower() == "none":
                        k_val = None
                    else:
                        raw_k = raw_k.replace(",", ".") # sanitize European decimals
                        k_val = float(raw_k)
                else:
                    # Fallback if it's a uniform/monodisperse star variant
                    k_val = None
                print(disorder_schema.name)
                if disorder_schema.name == "None":
                    conc = None
                else:
                    conc = float(disorder_schema.concentration.get())
                
                    
            except (ValueError, AttributeError):
                messagebox.showerror(
                    "Invalid Parameters", 
                    ("Could not parse numeric parameters. Please check your Arm Length, Counts, or 'k' settings."
                    )
                )
                return
            k_text = k_val if k_val is not None else "Uniform"
            description = f"Architecture: Star \n Arms (f): {f_arms} | Length (N): {n_avg} | Polydispersity (k): {k_text}"
            # Pack configurations to hand down to background thread execution blocks
            simulation_kwargs = {
                "N_average": n_avg,
                "k": k_val,
                "number_arms": f_arms,
                "target_dir": target_path,
                "t_production": t_production,  
                "replicas": replicas,
                "a":1,        
                "config_desc": description
            }
            # C. Close the secondary settings configuration window safely
            window.destroy() 
         
            # D. Fire up the dual progress bar monitoring modal overlay window
            window_components.SimulationProgressWindow(root_window, simulation_kwargs)
        elif  arch_schema.name == "Linear":
            try:
                # Safely extract text entries built dynamically by the active schemas
                n_chains = int(arch_schema.mol.get().strip())
                n_avg = int(arch_schema.N.get().strip())
                a=int(arch_schema.N.get().strip())
                t_production=int(arch_schema.time.get().strip())
                replicas=int(arch_schema.replicas.get().strip())

                if hasattr(arch_schema, 'k_entry'):
                    raw_k = arch_schema.k_entry.get().strip()
                    # Handle empty strings, "None", or uniform cases safely
                    if not raw_k or raw_k.lower() == "none":
                        k_val = None
                    else:
                        raw_k = raw_k.replace(",", ".") # sanitize European decimals
                        k_val = float(raw_k)
                else:
                    # Fallback if it's a uniform/monodisperse star variant
                    k_val = None
                print(disorder_schema.name)
                if disorder_schema.name == "None":
                    conc = None
                else:
                    conc = float(disorder_schema.concentration.get())
                
                    
            except (ValueError, AttributeError):
                messagebox.showerror(
                    "Invalid Parameters", 
                    ("Could not parse numeric parameters. Please check your Arm Length, Counts, or 'k' settings."
                    )
                )
                return
            k_text = k_val if k_val is not None else "Uniform"
            description = f"Architecture: Linear \n Number of chains: {n_chains} | Length (N): {n_avg}  \n | Polydispersity (k): {k_text}"
            # Pack configurations to hand down to background thread execution blocks
            simulation_kwargs = {
                "N_average": n_avg,
                "k": k_val,
                "number_arms": n_chains,
                "target_dir": target_path,
                "t_production": t_production,   # Change or dynamically map to an Entry widget if needed
                "replicas": replicas, 
                 "a": a,                 # Change or dynamically map to an Entry widget if needed
                "config_desc": description
            }
            # C. Close the secondary settings configuration window safely
            window.destroy() 
         
            # D. Fire up the dual progress bar monitoring modal overlay window
            window_components.SimulationProgressWindow(root_window, simulation_kwargs)


        else:
            # Fallback wrapper placeholder for linear/comb systems
            messagebox.showinfo("Work In Progress", f"Simulation engine setup for {arch_schema.name} is under construction.")
    def run_simulation_setup():
        """
        Triggers when clicking the 'Execute Transformation' button inside this settings window.
        """
        # A. Pull destination path safely from the browser widget
        target_path = output_folder_browser.get_path()
        if not target_path:
            messagebox.showwarning("Missing Path", "Please select a target output directory first.")
            return

        # B. Handle structural parameters specifically for your Star Polymer setup
        if arch_schema.name == "Star":
            try:
                # Safely extract text entries built dynamically by the active schemas

                f_arms = int(arch_schema.arms.get().strip())
                n_avg = int(arch_schema.length.get().strip())

                if hasattr(arch_schema, 'k_entry'):
                    raw_k = arch_schema.k_entry.get().strip()
                    # Handle empty strings, "None", or uniform cases safely
                    if not raw_k or raw_k.lower() == "none":
                        k_val = None
                    else:
                        raw_k = raw_k.replace(",", ".") # sanitize European decimals
                        k_val = float(raw_k)
                else:
                    # Fallback if it's a uniform/monodisperse star variant
                    k_val = None
                print(disorder_schema.name)
                if disorder_schema.name == "None":
                    conc = None
                else:
                    conc = float(disorder_schema.concentration.get())
                
                    
            except (ValueError, AttributeError):
                messagebox.showerror(
                    "Invalid Parameters", 
                    ("Could not parse numeric parameters. Please check your Arm Length, Counts, or 'k' settings."
                    )
                )
                return
            k_text = k_val if k_val is not None else "Uniform"
            description = f"Architecture: Star \n Arms (f): {f_arms} | Length (N): {n_avg} | Polydispersity (k): {k_text}"
            # Pack configurations to hand down to background thread execution blocks
            simulation_kwargs = {
                "architecture": "Star",
                "N_average": n_avg,
                "k": k_val,
                "number_arms": f_arms,
                "target_dir": target_path,
                "a":1,
                "concentration": conc,        
                "config_desc": description
            }
            # C. Close the secondary settings configuration window safely
            window.destroy() 
         
            # D. Fire up the dual progress bar monitoring modal overlay window
            window_components.LAMPPSProgressWindow(root_window, simulation_kwargs)
        elif  arch_schema.name == "Linear":
            try:
                # Safely extract text entries built dynamically by the active schemas
                n_chains = int(arch_schema.mol.get().strip())
                n_avg = int(arch_schema.N.get().strip())
                a=int(arch_schema.N.get().strip())
                if hasattr(arch_schema, 'k_entry'):
                    raw_k = arch_schema.k_entry.get().strip()
                    # Handle empty strings, "None", or uniform cases safely
                    if not raw_k or raw_k.lower() == "none":
                        k_val = None
                    else:
                        raw_k = raw_k.replace(",", ".") # sanitize European decimals
                        k_val = float(raw_k)
                else:
                    # Fallback if it's a uniform/monodisperse star variant
                    k_val = None
                print(disorder_schema.name)
                if disorder_schema.name == "None":
                    conc = None
                else:
                    conc = float(disorder_schema.concentration.get())
                
                    
            except (ValueError, AttributeError):
                messagebox.showerror(
                    "Invalid Parameters", 
                    ("Could not parse numeric parameters. Please check your Arm Length, Counts, or 'k' settings."
                    )
                )
                return
            k_text = k_val if k_val is not None else "Uniform"
            description = f"Architecture: Linear \n Number of chains: {n_chains} | Length (N): {n_avg}  \n | Polydispersity (k): {k_text}"
            # Pack configurations to hand down to background thread execution blocks
            simulation_kwargs = {
                "architecture": "Linear",
                "N_average": n_avg,
                "k": k_val,
                "number_arms": n_chains,
                "target_dir": target_path,
                 "a": a, 
                 "concentration": conc,        
                "config_desc": description
            }
            # C. Close the secondary settings configuration window safely
            window.destroy() 
         
            # D. Fire up the dual progress bar monitoring modal overlay window
            window_components.LAMPPSProgressWindow(root_window, simulation_kwargs)


        else:
            # Fallback wrapper placeholder for linear/comb systems
            messagebox.showinfo("Work In Progress", f"Simulation engine setup for {arch_schema.name} is under construction.")

    # --- Static Action Lower Bar ---
    action_frame = ttk.Frame(window, padding="10")
    action_frame.pack(fill="x", side="bottom")
    
    if action_type == "LAMMPS set up":
        confirm_btn = ttk.Button(action_frame, text="Run Simulation Setup", command=run_simulation_setup)
        confirm_btn.pack(side="right", padx=5)
    else:
        confirm_btn = ttk.Button(action_frame, text="Run Pivot Simulation", command=run_simulation_flow)
        confirm_btn.pack(side="right", padx=5)
    
    cancel_btn = ttk.Button(action_frame, text="Cancel", command=window.destroy)
    cancel_btn.pack(side="right", padx=5)


