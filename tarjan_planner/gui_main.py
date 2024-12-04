import logging
import time
from tkinter.colorchooser import askcolor
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from evolutionary_optimizer import EvolutionaryOptimizer
from relatives_data import relatives, transport_modes


class RouteOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Route Optimizer")
        self.root.geometry("900x600")
        self.relatives = relatives
        self.route_color = "blue"  # Default route color
        self.point_color = "red"  # Default point color

        # Configure logging
        logging.basicConfig(
            filename="execution_log.txt",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        self.setup_gui()

    def setup_gui(self):
        # Input Section
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, fill="x")

        ttk.Label(input_frame, text="Optimization Criteria:").grid(row=0, column=0, padx=10, sticky="w")
        self.criteria_var = tk.StringVar(value="time")
        self.criteria_menu = ttk.Combobox(input_frame, textvariable=self.criteria_var, state="readonly")
        self.criteria_menu["values"] = ("time", "cost", "transfers")
        self.criteria_menu.grid(row=0, column=1, padx=10)

        ttk.Label(input_frame, text="Population Size:").grid(row=1, column=0, padx=10, sticky="w")
        self.population_size_var = tk.StringVar(value="50")
        ttk.Entry(input_frame, textvariable=self.population_size_var).grid(row=1, column=1, padx=10)

        ttk.Label(input_frame, text="Generations:").grid(row=2, column=0, padx=10, sticky="w")
        self.generations_var = tk.StringVar(value="200")
        ttk.Entry(input_frame, textvariable=self.generations_var).grid(row=2, column=1, padx=10)

        # Add color selection buttons
        ttk.Button(input_frame, text="Select Route Color", command=self.select_route_color).grid(row=3, column=0, pady=10)
        ttk.Button(input_frame, text="Select Point Color", command=self.select_point_color).grid(row=3, column=1, pady=10)

        self.run_button = ttk.Button(self.root, text="Run Optimizer", command=self.run_optimizer)
        self.run_button.pack(pady=10)

        # Output Section
        self.output_frame = ttk.LabelFrame(self.root, text="Results")
        self.output_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.output_text = tk.Text(self.output_frame, height=10, wrap="word", state="disabled")
        self.output_text.pack(fill="both", expand=True)

        # Graph Section
        self.graph_frame = ttk.LabelFrame(self.root, text="Route Visualization")
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def select_route_color(self):
        """Open a color picker to select the route color."""
        color = askcolor(title="Select Route Color")[1]  # Get hex color
        if color:
            self.route_color = color

    def select_point_color(self):
        """Open a color picker to select the point color."""
        color = askcolor(title="Select Point Color")[1]  # Get hex color
        if color:
            self.point_color = color

    def run_optimizer(self):
        try:
            # Log the start time
            start_time = time.time()

            optimizer = EvolutionaryOptimizer(
                relatives=self.relatives,
                transport_modes=transport_modes,
                population_size=int(self.population_size_var.get()),
                generations=int(self.generations_var.get()),
                criteria=self.criteria_var.get()
            )
            result = optimizer.optimize()

            # Log the end time
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Log execution details
            logging.info(
                f"Optimization Criteria: {self.criteria_var.get()}, "
                f"Population Size: {self.population_size_var.get()}, "
                f"Generations: {self.generations_var.get()}, "
                f"Elapsed Time: {elapsed_time:.2f} seconds, "
                f"Optimal Route: {result['order']}, "
                f"Total Time: {result['total_time']:.2f}, "
                f"Total Cost: {result['total_cost']:.2f}"
            )

            # Display results
            self.output_text.configure(state="normal")
            self.output_text.delete(1.0, "end")
            self.output_text.insert("end", f"Optimal Route: {result['order']}\n")
            self.output_text.insert("end", f"Total Time: {result['total_time']:.2f} hrs\n")
            self.output_text.insert("end", f"Total Cost: {result['total_cost']:.2f}\n")
            self.output_text.insert("end", f"Transport Modes: {result['transport_modes']}\n")
            self.output_text.insert("end", f"Execution Time: {elapsed_time:.2f} seconds\n")
            self.output_text.configure(state="disabled")

            # Visualize the route with custom colors
            self.plot_graph(result)

        except Exception as e:
            logging.error(f"Error during optimization: {e}")
            messagebox.showerror("Error", str(e))

    def plot_graph(self, result):
        # Clear any existing graph
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Prepare data for plotting
        latitudes = [self.relatives[i]['latitude'] for i in result['order']]
        longitudes = [self.relatives[i]['longitude'] for i in result['order']]
        labels = [self.relatives[i]['relative'] for i in result['order']]

        # Add the first point again to complete the loop
        latitudes.append(latitudes[0])
        longitudes.append(longitudes[0])
        labels.append(labels[0])

        # Create Matplotlib figure
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(longitudes, latitudes, marker="o", linestyle="-", color=self.route_color, label="Route")

        # Annotate the points
        for i, label in enumerate(labels):
            ax.scatter(longitudes[i], latitudes[i], color=self.point_color, s=50, label="Relatives" if i == 0 else "")
            ax.text(longitudes[i], latitudes[i], label, fontsize=8)

        ax.set_title("Route Visualization")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.legend(loc="upper left")

        # Embed Matplotlib figure into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = RouteOptimizerApp(root)
    root.mainloop()
