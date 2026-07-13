# Pivot Algorithm Implementation for Complex Polymer Systems

This program is designed to perform two main operations using the [pivot algorithm](https://doi.org/10.1007/bf01022990):

1. **Run simulations** using the pivot algorithm to calculate conformational properties: the radius of gyration, asphericity, and prolateness.
2. **Execute a relaxation stage** via the pivot algorithm to generate initial starting configurations for LAMMPS molecular dynamics simulations.

## Input Parameters

* **Architecture:** Linear or Star (with additional architectures planned for future updates). 
    * *Linear chains:* The program generates a user-defined number of chains, all originating from the surface of a cube with a user-defined half-length. The chains can either possess a uniform degree of polymerization or be sampled from a Zimm-Schultz distribution with a specified shape parameter $k$, where the input chain length $N$ is treated as the number-average degree of polymerization.
    * *Star polymers:* The program generates a single star polymer, which can be configured with arms of varying lengths (polydisperse arms governed by the parameter $k$).

* **Disorder Type:** None or point-like uncorrelated disorder.

> **Note:** Running pivot simulations for a system containing multiple chains will yield conformational parameter values calculated around the common center of mass of the entire system. System disorder is introduced *after* the relaxation stage and is only accounted for when generating the LAMMPS output, as it is a well-established fact that static, point-like disorder does not affect the equilibrium conformational properties of polymers.
