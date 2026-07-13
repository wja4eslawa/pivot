import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
from tkinter import filedialog

import core_simulation # type: ignore
from Functions import *

def simulation_worker_thread(progress_queue, sim_kwargs):
    # Capture step name, internal percent, and which replica loop is active
    def ui_callback(stage_name, stage_percent, replica_index):
        if stage_name == "Plot":
            # stage_percent holds the tuple of (Cx, Cy, Cz) arrays here
            progress_queue.put(("Plot", stage_percent, replica_index))
        else:
            progress_queue.put(("Progress", stage_name, stage_percent, replica_index))
        
    try:
        sim_kwargs = sim_kwargs.copy()
        if "config_desc" in sim_kwargs:
            del sim_kwargs["config_desc"]
        sim_kwargs["update_callback"] = ui_callback
        if "architecture" in sim_kwargs:
            core_simulation.LAMMPS_setup(**sim_kwargs)
        else:
            core_simulation.Polydisperce_star(**sim_kwargs) ## Here in final file should be the function that runs
        progress_queue.put(("Complete", None, None, None))
    except Exception as e:
        progress_queue.put(("Error", str(e), None, None))

class SimulationProgressWindow:
    def __init__(self, parent, sim_kwargs):
        self.window = tk.Toplevel(parent)
        self.window.title("Simulation Runtime Tracking")
        self.window.geometry("450x320")
        
        self.window.transient(parent)
        self.window.grab_set()

        config_frame = ttk.LabelFrame(self.window, text=" Current Configuration ", padding=10)
        config_frame.pack(pady=10, padx=20, fill="x")
        
        # Retrieve the description we created in window_flows
        config_text = sim_kwargs.get("config_desc", "Unknown Configuration")
        
        # wraplength ensures the text breaks into multiple lines if it's too long
        self.config_label = ttk.Label(config_frame, text=config_text, font=("Helvetica", 12), wraplength=400)
        self.config_label.pack()
        # Save total replicas count to calculate batch percentages correctly
        self.total_replicas = sim_kwargs.get("replicas", 1)
        
        # --- PROGRESS BAR 1: STAGE INTERFACES (Micro level) ---
        self.stage_label = ttk.Label(self.window, text="Initializing Stage...", font=("Helvetica", 10, "bold"))
        self.stage_label.pack(pady=(15, 2), padx=20, anchor="w")
        
        self.stage_progress = ttk.Progressbar(self.window, orient="horizontal", mode="determinate")
        self.stage_progress.pack(pady=(0, 10), padx=20, fill="x")
        
        # --- PROGRESS BAR 2: REPLICA BATCH INTERFACES (Macro level) ---
        self.batch_label = ttk.Label(self.window, text="Batch Runs: 0 / {} Replicas Complete".format(self.total_replicas), font=("Helvetica", 10, "bold"))
        self.batch_label.pack(pady=(10, 2), padx=20, anchor="w")
        
        self.batch_progress = ttk.Progressbar(self.window, orient="horizontal", mode="determinate")
        self.batch_progress.pack(pady=(0, 15), padx=20, fill="x")
        
        # Bottom Status Context Footnote
        self.status_foot = ttk.Label(self.window, text="Allocating local computation space...", font=("Helvetica", 9, "italic"))
        self.status_foot.pack(padx=20, anchor="w")
        # Track the active trajectory window instance so we can close it programmatically
        self.active_plot_window = None
        # Thread Launch Engine Setup
        self.progress_queue = queue.Queue()
        self.sim_thread = threading.Thread(
            target=simulation_worker_thread,
            args=(self.progress_queue, sim_kwargs),
            daemon=True
        )
        self.sim_thread.start()
        self.window.after(50, self.check_queue)

    def check_queue(self):
        try:
            while True:
                packet = self.progress_queue.get_nowait()
                msg_type = packet[0]
                if msg_type == "Complete":
                    if self.active_plot_window and self.active_plot_window.winfo_exists():
                        self.active_plot_window.destroy()
                    self.stage_label.config(text="Status: Finished")
                    self.batch_label.config(text=f"Batch Complete: {self.total_replicas}/{self.total_replicas} Replicas")
                    self.stage_progress["value"] = 100
                    self.batch_progress["value"] = 100
                    self.status_foot.config(text="✓ All operations successfully exported to files.")
                    
                    ttk.Button(self.window, text="Finish", command=self.window.destroy).pack(pady=10)
                    return
                    
                elif msg_type == "Error":
                    if self.active_plot_window and self.active_plot_window.winfo_exists():
                        self.active_plot_window.destroy()
                    messagebox.showerror("Execution Error", f"Simulation failed:\n{stage}")
                    self.window.destroy()
                    return
                
                elif msg_type == "Plot":
                    # --- AUTOMATIC CLOSING & RE-PLOTTING ---
                    # 1. Close the previous window if it's open
                    data_payload = packet[1]
                    rep_idx = packet[2]
                    if self.active_plot_window and self.active_plot_window.winfo_exists():
                        self.active_plot_window.destroy()
                    
                    # 2. Create a new window specifically for this batch's plot
                    self.active_plot_window = tk.Toplevel(self.window)
                    self.active_plot_window.title(f"Trajectory Batch Plot - Replica {rep_idx + 1}")
                    self.active_plot_window.geometry("500x450")
                    
                    # 3. Extract your coordinates package
                    Cx_arr, Cy_arr, Cz_arr = data_payload
                    
                    # 4. Call your custom plotting function, passing the target window handle
                    # See Step 4 for how to tweak your plotting function to accept a window target
                    plot_3d_walk(Cx_arr, Cy_arr, Cz_arr, target_window=self.active_plot_window)

                elif msg_type == "Progress":
                    stage = packet[1]    
                    percent = packet[2]  
                    rep_idx = packet[3]
                    # 1. Update Micro Progress Bar (Current Stage)
                    self.stage_label.config(text=f"Current Task: {stage} Stage")
                    self.stage_progress["value"] = percent
                    
                    # 2. Update Macro Progress Bar (Replicas Batches)
                    # Calculates progress based on completed replicas plus fractional progress of current replica
                    macro_percent = ((rep_idx + (percent / 100.0)) / self.total_replicas) * 100
                    
                    self.batch_label.config(text=f"Batch Runs: Replica {rep_idx + 1} of {self.total_replicas} processing...")
                    self.batch_progress["value"] = macro_percent
                    self.status_foot.config(text=f"Active Stage Progress: {percent}% done")
                    
                self.progress_queue.task_done()
                
        except queue.Empty:
            self.window.after(100, self.check_queue)

class LAMPPSProgressWindow:
    def __init__(self, parent, sim_kwargs):
        self.window = tk.Toplevel(parent)
        self.window.title("Simulation Runtime Tracking")
        self.window.geometry("450x320")
        
        self.window.transient(parent)
        self.window.grab_set()

        config_frame = ttk.LabelFrame(self.window, text=" Current Configuration ", padding=10)
        config_frame.pack(pady=10, padx=20, fill="x")
        
        # Retrieve the description we created in window_flows
        config_text = sim_kwargs.get("config_desc", "Unknown Configuration")
        
        # wraplength ensures the text breaks into multiple lines if it's too long
        self.config_label = ttk.Label(config_frame, text=config_text, font=("Helvetica", 12), wraplength=400)
        self.config_label.pack()
        # Save total replicas count to calculate batch percentages correctly
        self.total_replicas = sim_kwargs.get("replicas", 1)
        
        # --- PROGRESS BAR 1: STAGE INTERFACES (Micro level) ---
        self.stage_label = ttk.Label(self.window, text="Initializing Stage...", font=("Helvetica", 10, "bold"))
        self.stage_label.pack(pady=(15, 2), padx=20, anchor="w")
        
        self.stage_progress = ttk.Progressbar(self.window, orient="horizontal", mode="determinate")
        self.stage_progress.pack(pady=(0, 10), padx=20, fill="x")
        
        # Bottom Status Context Footnote
        self.status_foot = ttk.Label(self.window, text="Allocating local computation space...", font=("Helvetica", 9, "italic"))
        self.status_foot.pack(padx=20, anchor="w")

        # Thread Launch Engine Setup
        self.progress_queue = queue.Queue()
        self.sim_thread = threading.Thread(
            target=simulation_worker_thread,
            args=(self.progress_queue, sim_kwargs),
            daemon=True
        )
        self.sim_thread.start()
        self.window.after(50, self.check_queue)

    def check_queue(self):
        try:
            while True:
                msg_type, stage, percent, rep_idx = self.progress_queue.get_nowait()
                
                if msg_type == "Complete":
                    self.stage_label.config(text="Status: Finished")
                    self.stage_progress["value"] = 100
                    self.status_foot.config(text="✓ All operations successfully exported to files.")
                    
                    ttk.Button(self.window, text="Finish", command=self.window.destroy).pack(pady=10)
                    return
                    
                elif msg_type == "Error":
                    messagebox.showerror("Execution Error", f"Simulation failed:\n{stage}")
                    self.window.destroy()
                    return
                    
                elif msg_type == "Progress":
                    # 1. Update Micro Progress Bar (Current Stage)
                    self.stage_label.config(text=f"Current Task: {stage} Stage")
                    self.stage_progress["value"] = percent
                    
                    # 2. Update Macro Progress Bar (Replicas Batches)
                    # Calculates progress based on completed replicas plus fractional progress of current replica
                    macro_percent = ((rep_idx + (percent / 100.0)) / self.total_replicas) * 100

                    self.status_foot.config(text=f"Active Stage Progress: {percent}% done")
                    
                self.progress_queue.task_done()
                
        except queue.Empty:
            self.window.after(100, self.check_queue)


class FolderBrowseWidget:
    def __init__(self, parent, label_text="Output Directory:"):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="x", padx=15, pady=10)
        
        # Grid weight configuration makes the entry field stretch automatically
        self.frame.columnconfigure(1, weight=1)
        
        # 1. Label
        ttk.Label(self.frame, text=label_text).grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        # 2. Path Entry Box
        self.path_var = tk.StringVar()
        self.entry = ttk.Entry(self.frame, textvariable=self.path_var)
        self.entry.grid(row=0, column=1, sticky="ew", padx=5)
        
        # 3. Browse Button
        self.browse_btn = ttk.Button(self.frame, text="Browse...", command=self.choose_directory)
        self.browse_btn.grid(row=0, column=2, sticky="e", padx=(5, 0))

    def choose_directory(self):
        """Opens native folder picker and updates the text field."""
        selected_dir = filedialog.askdirectory(title="Select Simulation Output Folder")
        if selected_dir:  # If user didn't hit cancel
            self.path_var.set(selected_dir)
            
    def get_path(self):
        """Call this method to retrieve the final string path for your scripts."""
        return self.path_var.get()
