Graph Coloring Optimization with Genetic Algorithm
Course: BLM22332E / BLM20364E – Heuristic Optimization Algorithms
Term Project – Final Exam Submission

1. Project Overview
   This project implements a Genetic Algorithm (GA) combined with Simulated Annealing (SA) to solve the Graph Coloring Problem. The goal is to assign colors to vertices in a graph such that no two adjacent vertices share the same color, while minimizing the total number of colors used.

The algorithm is tested on DIMACS benchmark instances ranging from 50 to 500 nodes. In addition to the core optimization, the project includes visual output (PNG/GIF) and an interactive GUI for usability.

2. Group Members
   Asma Alrifai

Ahmet Bozkır

Burak Girgin

3. How to Run
   Requirements
   Python 3.10+

Required libraries:

nginx
Copy
Edit
pip install matplotlib networkx pillow
Running the Project
Place your DIMACS .col graph file in the root folder.

Run the main script:

bash
Copy
Edit
python main.py
The script will:

Run the hybrid GA + SA optimization

Save the best result as best*pic*<filename>.png

Generate animation.gif showing improvement over generations

To use the GUI (if included):

bash
Copy
Edit
python gui.py 4. File Structure
bash
Copy
Edit
.
├── main.py # Entry point for batch graph optimization
├── ga.py # Genetic Algorithm implementation
├── graph*utils.py # Graph loader (DIMACS format)
├── visualization.py # PNG/GIF generation
├── generate_gif.py # GIF exporter
├── frames/ # Saved frames for animation (auto-generated)
├── best_pic*<file>.png # Output image
├── animation.gif # Optional animation of progress
├── gui.py # GUI interface (if applicable)
├── gc_50_9, gc_70_9, ... # DIMACS graph instances
└── README.md # This file 5. Features Implemented
Complete Genetic Algorithm (population, selection, crossover, mutation, elitism)

Adaptive mutation control

Tournament selection and custom elitism strategy

Problem-specific crossover (color-aware)

Local repair to fix coloring conflicts

Hybridization with Simulated Annealing

PNG and GIF visualization

GUI to load, run, and display results

6. Notes
   Output images and animations are generated automatically.

The algorithm uses adaptive parameters for improved performance on large graphs.

The project meets and exceeds the advanced feature requirements outlined in the project specification.

7. Problem Instances
   The algorithm was tested on the following DIMACS benchmark files:

gc_50_9

gc_70_9

gc_100_9

gc_250_9

gc_500_9

8. Contact
   For any issues or questions related to this project, please contact the team members listed above.
