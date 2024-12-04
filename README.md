# Project Overview

Welcome to the **Utility Suite** repository! This project comprises three core components: **FileOrganizer**, **RouteOptimizer**, and **TarjanPlanner**. Each module serves a distinct purpose aimed at optimizing tasks in file management, route planning, and optimization through graph algorithms.

---

## FileOrganizer

### Description
**FileOrganizer** is a utility tool designed to streamline the organization of files in a directory. It helps users declutter and categorize files based on their extensions, creation dates, or custom rules.

### Features
- Automatically sort files into folders based on:
  - File type (e.g., `.txt`, `.pdf`, `.jpg`).
  - Date of creation or modification.
  - User-defined categories or rules.
- Supports nested folder structures.
- Handles duplicate files by renaming or skipping.
- Cross-platform compatibility.

### Example Use Case
Organize a messy "Downloads" folder by sorting all images, documents, and other files into labeled subfolders.

---

## RouteOptimizer

### Description
**RouteOptimizer** calculates optimal travel routes based on various criteria, such as minimizing time, cost, or the number of transfers. It incorporates diverse transportation modes like walking, cycling, and public transit.

### Features
- Multi-criteria optimization (e.g., time, cost, and transfers).
- Supports multiple transport modes (e.g., bus, bicycle, walking).
- Configurable parameters for custom route planning.
- Outputs optimized route order, transport modes, and performance metrics.

### Example Use Case
Plan a multi-stop city trip while minimizing cost and travel time by dynamically selecting the best transport mode for each leg.

---

## TarjanPlanner

### Description
**TarjanPlanner** leverages graph algorithms to solve planning and optimization problems. It integrates a **Genetic Algorithm** for enhanced performance and adaptability in complex scenarios.

### Features
- Implements Tarjan's algorithm for strong connectivity detection in graphs.
- Optimizes planning problems using Genetic Algorithms.
- Handles directed and weighted graphs.
- Configurable for various real-world applications like logistics and network optimization.

### Example Use Case
Optimize the delivery routes of a logistics company by minimizing delivery time and maximizing resource utilization.

---

## Getting Started

### Prerequisites
- Python 3.8 or later
- Required Python packages (install via `requirements.txt`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/utility-suite.git
   cd utility-suite
