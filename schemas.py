import tkinter as tk
from tkinter import ttk

# =====================================================================
# 1. ARCHITECTURE SCHEMAS (Extensible Configuration Objects)
# =====================================================================

class LinearArchitecture:
    name = "Linear"
    def build_widgets(self, frame):
        ### ADD NUMBER OF CHAINS IN THE SYSTEM
        ### Add size of the start core
        """Draws parameters specific to linear chains."""
        ttk.Label(frame, text="Total Chain Length (N):").grid(row=0, column=0, sticky="w", pady=5)
        self.N = ttk.Entry(frame, width=10)
        self.N.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        self.N.insert(0, "100") # Default value
        ttk.Label(frame, text="Number of chains:").grid(row=1, column=0, sticky="w", pady=5)
        self.mol = ttk.Entry(frame, width=10)
        self.mol.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        self.mol.insert(0, "1")
        ttk.Label(frame, text="Half length of the box side from which the chains start:").grid(row=2, column=0, sticky="w", pady=5)
        self.a = ttk.Entry(frame, width=10)
        self.a.grid(row=2, column=1, sticky="w", pady=5, padx=5)
        self.a.insert(0, "10")
        ttk.Label(frame, text="k parameter of Zimm-Scultz distribution:").grid(row=3, column=0, sticky="w", pady=5)
        self.k_entry = ttk.Entry(frame, width=10)
        self.k_entry.grid(row=3, column=1, sticky="w", pady=5, padx=5)
        self.k_entry.insert(0, "None")

        ttk.Label(frame, text="Number of pivot steps in production run:").grid(row=4, column=0, sticky="w", pady=5)
        self.time = ttk.Entry(frame, width=10)
        self.time.grid(row=4, column=1, sticky="w", pady=5, padx=5)
        self.time.insert(0, "100000")

        ttk.Label(frame, text="Number or replicas for aa polydisperce simulations:").grid(row=5, column=0, sticky="w", pady=5)
        self.replicas = ttk.Entry(frame, width=10)
        self.replicas.grid(row=5, column=1, sticky="w", pady=5, padx=5)
        self.replicas.insert(0, "200")

class StarArchitecture:
    name = "Star"
    def build_widgets(self, frame):
        """Draws parameters specific to star polymers."""
        ttk.Label(frame, text="Number of Arms (f):").grid(row=0, column=0, sticky="w", pady=5)
        self.arms = ttk.Spinbox(frame, from_=3, to=24, width=5)
        self.arms.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        self.arms.set(4)
        
        ttk.Label(frame, text="Arm Length (N_arm):").grid(row=1, column=0, sticky="w", pady=5)
        self.length = ttk.Entry(frame, width=10)
        self.length.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        self.length.insert(0, "50")

        ttk.Label(frame, text="k parameter of Zimm-Scultz distribution:").grid(row=2, column=0, sticky="w", pady=5)
        self.k_entry = ttk.Entry(frame, width=10)
        self.k_entry.grid(row=2, column=1, sticky="w", pady=5, padx=5)
        self.k_entry.insert(0, "None")

        ttk.Label(frame, text="Number of pivot steps in production run:").grid(row=3, column=0, sticky="w", pady=5)
        self.time = ttk.Entry(frame, width=10)
        self.time.grid(row=3, column=1, sticky="w", pady=5, padx=5)
        self.time.insert(0, "100000")

        ttk.Label(frame, text="Number or replicas for aa polydisperce simulations:").grid(row=4, column=0, sticky="w", pady=5)
        self.replicas = ttk.Entry(frame, width=10)
        self.replicas.grid(row=4, column=1, sticky="w", pady=5, padx=5)
        self.replicas.insert(0, "200")
        


class CombArchitecture:
    name = "Comb"
    def build_widgets(self, frame):
        """Draws parameters specific to comb polymers."""
        ttk.Label(frame, text="Backbone Length (N_b):").grid(row=0, column=0, sticky="w", pady=5)
        self.nb = ttk.Entry(frame, width=10)
        self.nb.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        
        ttk.Label(frame, text="Side Chain Length (N_s):").grid(row=1, column=0, sticky="w", pady=5)
        self.ns = ttk.Entry(frame, width=10)
        self.ns.grid(row=1, column=1, sticky="w", pady=5, padx=5)


# =====================================================================
# 2. DISORDER SCHEMAS (Extensible Configuration Objects)
# =====================================================================

class NoDisorder:
    name = "None"
    def build_widgets(self, frame):
        ttk.Label(frame, text="Pure solution", 
                  font=("Helvetica", 10, "italic")).grid(row=0, column=0, columnspan=2, pady=5)

class UncorrelatedDissorder:
    name = "Uncorrelated Dissorder"
    def build_widgets(self, frame):
        ttk.Label(frame, text="Uncorrelated Dissorder:").grid(row=0, column=0, sticky="w", pady=5)
        self.concentration = ttk.Entry(frame, width=10)
        self.concentration.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        self.concentration.insert(0, "0.1")

# =====================================================================
# 3. CENTRAL REGISTRY (The expansion switchboard)
# =====================================================================
# To add a new option in the future, just create its class above 
# and register it down here in these mappings. The UI handles the rest.

ARCHITECTURES = {
    "Linear": LinearArchitecture(),
    "Star": StarArchitecture(),
    "Comb": CombArchitecture()
}

DISORDERS = {
    "None": NoDisorder(),
    "Uncorrelated Dissorder": UncorrelatedDissorder()
}