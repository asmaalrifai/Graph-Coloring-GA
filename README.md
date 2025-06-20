# Graph Coloring Optimization with Genetic Algorithm

**Course:** BLM22332E / BLM20364E – Heuristic Optimization Algorithms  
**Term Project – Final Exam Submission**

---

## 1. Project Overview

This project implements a **Genetic Algorithm (GA)** combined with **Simulated Annealing (SA)** to solve the **Graph Coloring Problem**.  
The objective is to assign colors to graph vertices such that no two adjacent vertices share the same color, while minimizing the total number of colors used.

The algorithm is tested on **DIMACS benchmark instances** ranging from 50 to 500 nodes. It includes:
- Core GA and SA optimization
- PNG and GIF output generation
- Interactive GUI for usability

---

## 2. Group Members

- Asma Alrifai  
- Ahmet Bozkır  
- Burak Girgin

---

## 3. How to Run

### Requirements

- Python 3.10+
- Install required libraries:

### Requirements

- Python 3.10 or higher
- Required libraries:

```bash
pip install matplotlib networkx pillow

```
---
### 4.Running the Project
Place your benchmark graph files (e.g., gc_50_9, gc_100_9) in the project root folder.
These files are in DIMACS format and do not have file extensions.

Run the main algorithm:
```bash
python main.py

```
This will:

Execute the Genetic Algorithm with Simulated Annealing refinement

Save the best solution as best_pic_<filename>.png

Generate animation.gif showing progress across generations

(Optional) Run the GUI to interactively load and color graphs:
```bash
python gui.py

```

### The GUI allows you to:

Select one of the available graph files

Start the algorithm visually

View the result directly in the application window
