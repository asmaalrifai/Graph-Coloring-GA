import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
from PIL import ImageTk, Image, ImageSequence
import os

from graph_utils import load_dimacs_graph
from ga import GeneticAlgorithm
from visualization import save_coloring_image
from generate_gif import generate_gif

class GraphColoringApp:
    def __init__(self, root):
        self.root = root

        self.graph_file = None
        self.result_image = None
        self.animation_job = None

        top_panel = tk.Frame(root, bg="#f0f0f0")
        top_panel.pack(side="left", fill="both", expand=True, padx=10)

        self.title_label = tk.Label(top_panel, text="Graph Coloring using Genetic Algorithm", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=10)

        param_frame = tk.Frame(top_panel, bg="#f0f0f0")
        param_frame.pack(pady=(0, 10))

        self.mutation_rate_var = tk.StringVar(value="0.1")
        self.max_gen_var = tk.StringVar(value="1000")
        self.tournament_k_var = tk.StringVar(value="5")
        self.selection_method_var = tk.StringVar(value="Tournament")
        self.crossover_type_var = tk.StringVar(value="Single Point")
        self.mutation_mode_var = tk.StringVar(value="Adaptive")

        tk.Label(param_frame, text="Mutation Rate:", bg="#f0f0f0").grid(row=0, column=0, sticky="e")
        tk.Entry(param_frame, textvariable=self.mutation_rate_var, width=10).grid(row=0, column=1)

        tk.Label(param_frame, text="Max Generations:", bg="#f0f0f0").grid(row=0, column=2, sticky="e")
        tk.Entry(param_frame, textvariable=self.max_gen_var, width=10).grid(row=0, column=3)

        tk.Label(param_frame, text="Tournament Size:", bg="#f0f0f0").grid(row=0, column=4, sticky="e")
        tk.Entry(param_frame, textvariable=self.tournament_k_var, width=10).grid(row=0, column=5)

        tk.Label(param_frame, text="Selection:", bg="#f0f0f0").grid(row=1, column=0, sticky="e")
        tk.OptionMenu(param_frame, self.selection_method_var, "Tournament", "Roulette").grid(row=1, column=1)

        tk.Label(param_frame, text="Crossover:", bg="#f0f0f0").grid(row=1, column=2, sticky="e")
        tk.OptionMenu(param_frame, self.crossover_type_var, "Single Point", "Uniform").grid(row=1, column=3)

        tk.Label(param_frame, text="Mutation Mode:", bg="#f0f0f0").grid(row=1, column=4, sticky="e")
        tk.OptionMenu(param_frame, self.mutation_mode_var, "Adaptive", "Fixed").grid(row=1, column=5)

        self.image_label = tk.Label(top_panel, bg="#f0f0f0")
        self.image_label.pack(pady=(10, 10))

        self.file_label = tk.Label(top_panel, text="No file selected", font=("Arial", 12), bg="#f0f0f0", fg="#666")
        self.file_label.pack(pady=5)

        self.browse_btn = tk.Button(top_panel, text="📂 Browse Graph File", font=("Arial", 12), width=30, command=self.browse_file)
        self.browse_btn.pack(pady=5)

        self.run_btn = tk.Button(top_panel, text="🚀 Run Genetic Algorithm", font=("Arial", 12), width=30, command=self.run_ga, state=tk.DISABLED)
        self.run_btn.pack(pady=5)

        self.generate_gif_btn = tk.Button(top_panel, text="🎞 Generate GIF Only", font=("Arial", 11), width=30, command=self.generate_gif_only, state=tk.DISABLED)
        self.generate_gif_btn.pack(pady=5)

        self.sim_annealing_btn = tk.Button(top_panel, text="❄️ Run Simulated Annealing", font=("Arial", 11), width=30, command=self.run_simulated_annealing, state=tk.DISABLED)
        self.sim_annealing_btn.pack(pady=5)

        self.show_png_btn = tk.Button(top_panel, text="🖼 Show PNG Image", font=("Arial", 11), width=25, command=self.display_png, state=tk.DISABLED)
        self.show_png_btn.pack(pady=2)

        self.show_gif_btn = tk.Button(top_panel, text="🌀 Show Animation (GIF)", font=("Arial", 11), width=25, command=self.display_gif, state=tk.DISABLED)
        self.show_gif_btn.pack(pady=2)

        self.reset_btn = tk.Button(top_panel, text="🔄 Reset", font=("Arial", 11), width=25, command=self.reset_interface)
        self.reset_btn.pack(pady=10)

        self.compare_btn = tk.Button(top_panel, text="📊 Compare GA vs SA", font=("Arial", 11), width=25, command=self.compare_results, state=tk.DISABLED)
        self.compare_btn.pack(pady=5)

        right_panel = tk.Frame(root, bg="#f0f0f0")
        right_panel.pack(side="right", fill="y", padx=10, pady=10)

        self.status_box = tk.Text(right_panel, height=45, width=50, state=tk.DISABLED, bg="#ffffff", fg="#333", font=("Consolas", 10), wrap=tk.WORD)
        self.status_box.pack(side="top", fill="both", expand=True)

    def browse_file(self):
        import shutil
        import glob

        file_path = filedialog.askopenfilename(filetypes=[("Graph Files", "gc_*")])
        if file_path:
            # Clear frames folder
            if os.path.exists("frames"):
                for f in glob.glob("frames/*.png"):
                    os.remove(f)
            else:
                os.makedirs("frames")

            self.graph_file = file_path
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")
            self.run_btn.config(state=tk.NORMAL)
            self.generate_gif_btn.config(state=tk.DISABLED)
            self.show_png_btn.config(state=tk.DISABLED)
            self.show_gif_btn.config(state=tk.DISABLED)
            self.sim_annealing_btn.config(state=tk.DISABLED)
            self.image_label.config(image='')
            self.image_label.image = None
            self.result_image_path = None
            self.gif_path = None
            if self.animation_job:
                self.root.after_cancel(self.animation_job)
                self.animation_job = None
            self.log_status(f" File selected: {file_path}")

    def run_ga(self):
        if not self.graph_file:
            messagebox.showwarning("No File", "Please select a graph file first.")
            return

        self.status_box.config(state=tk.NORMAL)
        self.status_box.delete("1.0", tk.END)
        self.log_status("🚧 Running Genetic Algorithm... Please wait.\n")

        try:
            num_nodes, edges = load_dimacs_graph(self.graph_file)

            ga = GeneticAlgorithm(
                num_nodes=num_nodes,
                edges=edges,
                pop_size=100,
                mutation_rate=float(self.mutation_rate_var.get()),
                max_gen=int(self.max_gen_var.get()),
                tournament_k=int(self.tournament_k_var.get()),
                selection_type=self.selection_method_var.get(),
                crossover_type=self.crossover_type_var.get(),
                mutation_mode=self.mutation_mode_var.get(),
                log_fn=self.log_status
            )

            coloring = ga.run()
            self.ga_coloring = coloring
            self.last_solution = coloring
            self.sim_annealing_btn.config(state=tk.NORMAL)
            self.compare_btn.config(state=tk.DISABLED)
            self.generate_gif_btn.config(state=tk.NORMAL)
            self.compare_btn.config(state=tk.DISABLED)

            output_img = f"output_{os.path.basename(self.graph_file)}.png"
            save_coloring_image(num_nodes, edges, coloring, output_img)
            self.result_image_path = output_img
            self.gif_path = "animation.gif"
            self.show_png_btn.config(state=tk.NORMAL)
            self.show_gif_btn.config(state=tk.NORMAL)
            self.display_png()

            used_colors = len(set(coloring))
            self.log_status(f"\n🎉 Done! Used colors: {used_colors}")
            self.log_status(f"🖼 Output image saved as: {output_img}")
            self.show_result_image(output_img)

        except Exception as e:
            self.log_status(f" Error: {e}")
            messagebox.showerror("Error", str(e))

    def generate_gif_only(self):
        try:
            generate_gif("frames", "animation.gif", duration=300)
            self.gif_path = "animation.gif"
            self.log_status("GIF generated from frames.")
        except Exception as e:
            self.log_status(f"GIF generation failed: {e}")

    def run_simulated_annealing(self):
        if not hasattr(self, "last_solution"):
            messagebox.showwarning("Warning", "Please run the Genetic Algorithm first.")
            return

        try:
            num_nodes, edges = load_dimacs_graph(self.graph_file)

            ga_temp = GeneticAlgorithm(
                num_nodes=num_nodes,
                edges=edges,
                mutation_mode=self.mutation_mode_var.get(),
                log_fn=self.log_status
            )
            improved = ga_temp.simulated_annealing(self.last_solution)
            self.last_solution = improved  # Update the stored solution
            self.sa_coloring = improved
            self.compare_btn.config(state=tk.NORMAL)

            # Save image and frame
            save_coloring_image(num_nodes, edges, improved, "simulated_annealing_result.png")
            from visualization import save_coloring_frame
            save_coloring_frame(num_nodes, edges, improved, 9999, folder="frames")

            self.log_status("Simulated Annealing complete. Saved as simulated_annealing_result.png")

        except Exception as e:
            self.log_status(f" Simulated Annealing Error: {e}")
            messagebox.showerror("Error", str(e))

        except Exception as e:
            self.log_status(f" Simulated Annealing Error: {e}")
            messagebox.showerror("Error", str(e))

    def log_status(self, msg):
        self.status_box.config(state=tk.NORMAL)
        self.status_box.insert(tk.END, msg + "\n")
        self.status_box.see(tk.END)
        self.status_box.config(state=tk.DISABLED)

    def show_result_image(self, image_path):
        if not os.path.exists(image_path):
            return

        image = Image.open(image_path)
        image.thumbnail((600, 300))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def display_png(self):
        if not self.result_image_path or not os.path.exists(self.result_image_path):
            self.log_status(" PNG image not found.")
            return

        if self.animation_job:
            self.root.after_cancel(self.animation_job)

        image = Image.open(self.result_image_path)
        image.thumbnail((700, 400))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        self.log_status("Showing PNG output.")

    def display_gif(self):
        if not self.gif_path or not os.path.exists(self.gif_path):
            self.log_status("GIF not found.")
            return

        self.play_animation(self.gif_path)
        self.log_status(" Playing GIF animation.")

    def compare_results(self):
        if self.animation_job:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None
        from PIL import ImageOps, ImageStat
        ga_image = f"output_{os.path.basename(self.graph_file)}.png"
        sa_image = "simulated_annealing_result.png"
        if not os.path.exists(ga_image) or not os.path.exists(sa_image):
            self.log_status(" Cannot compare: one or both images not found.")
            return

        try:
            img1 = Image.open(ga_image).resize((300, 300))
            img2 = Image.open("simulated_annealing_result.png").resize((300, 300))
            combined = Image.new("RGB", (600, 300))
            combined.paste(ImageOps.expand(img1, border=2, fill='black'), (0, 0))
            combined.paste(ImageOps.expand(img2, border=2, fill='black'), (300, 0))
            photo = ImageTk.PhotoImage(combined)
            self.image_label.config(image=photo)
            self.image_label.image = photo
                        # Count distinct colors
            from graph_utils import load_dimacs_graph
            num_nodes, _ = load_dimacs_graph(self.graph_file)
            ga_colors = set()
            sa_colors = set()

            # Compare based on actual coloring results
            used_ga_colors = len(set(self.ga_coloring)) if hasattr(self, 'ga_coloring') else 0
            used_sa_colors = len(set(self.sa_coloring)) if hasattr(self, 'sa_coloring') else 0
            ga_colors = used_ga_colors
            sa_colors = used_sa_colors

            self.log_status("Displaying GA vs SA comparison.")
            self.log_status(f"   GA colors used: {ga_colors}")
            self.log_status(f"   SA colors used: {sa_colors}")

            if ga_colors < sa_colors:
                self.log_status("GA performed better in terms of color usage.")
            elif ga_colors > sa_colors:
                self.log_status("SA performed better in terms of color usage.")
            else:
                self.log_status("GA and SA used the same number of colors.")
        except Exception as e:
            self.log_status(f"Comparison Error: {e}")


    def reset_interface(self):
        self.graph_file = None
        self.result_image_path = None
        self.gif_path = None
        self.last_solution = None
        self.file_label.config(text="No file selected")
        self.image_label.config(image='')
        self.image_label.image = None
        self.status_box.config(state=tk.NORMAL)
        self.status_box.delete("1.0", tk.END)
        self.status_box.config(state=tk.DISABLED)
        self.run_btn.config(state=tk.DISABLED)
        self.sim_annealing_btn.config(state=tk.DISABLED)
        self.generate_gif_btn.config(state=tk.DISABLED)
        self.show_png_btn.config(state=tk.DISABLED)
        self.show_gif_btn.config(state=tk.DISABLED)
        if self.animation_job:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None
        self.log_status("Interface has been reset.")

    def play_animation(self, gif_path):
        if not os.path.exists(gif_path):
            self.log_status("animation.gif not found.")
            return

        if self.animation_job:
            self.root.after_cancel(self.animation_job)

        gif = Image.open(gif_path)
        frames = [ImageTk.PhotoImage(frame.copy().resize((600, 300))) for frame in ImageSequence.Iterator(gif)]

        def update(idx=0):
            frame = frames[idx]
            self.image_label.config(image=frame)
            self.image_label.image = frame
            self.animation_job = self.root.after(200, update, (idx + 1) % len(frames))

        update()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Graph Coloring Solver")
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    container = tk.Frame(canvas)
    canvas.create_window((0, 0), window=container, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    container.bind("<Configure>", on_frame_configure)

    app = GraphColoringApp(container)
    root.geometry("1000x850")
    root.mainloop()
