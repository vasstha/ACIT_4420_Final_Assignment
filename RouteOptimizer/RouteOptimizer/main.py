import matplotlib.pyplot as plt
from tkinter import ttk, messagebox
from data.relatives_data import relatives, transport_modes
from modules.optimizer import find_optimal_route
from modules.visualizer import plot_route
import threading
import time
import logging
from tkinter import Text
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Set up logging
logging.basicConfig(filename="route_optimizer.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class RouteOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Route Optimizer")
        self.root.geometry("600x400")

        # Input frame
        self.input_frame = ttk.LabelFrame(self.root, text="Input Parameters")
        self.input_frame.pack(padx=10, pady=10, fill="both")

        ttk.Label(self.input_frame, text="Optimization Criteria:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.criteria_var = ttk.Combobox(self.input_frame, values=["time", "cost", "transfers"], state="readonly")
        self.criteria_var.grid(row=0, column=1, padx=10, pady=5)
        self.criteria_var.set("time")

        self.run_button = ttk.Button(self.input_frame, text="Run Optimization", command=self.run_optimization)
        self.run_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Output frame
        self.output_frame = ttk.LabelFrame(self.root, text="Results")
        self.output_frame.pack(padx=10, pady=10, fill="both")

        # Replace Label with a Text widget
        self.output_text = Text(self.output_frame, wrap="word", state="disabled", height=10)
        self.output_text.pack(fill="both", expand=True)

    def run_optimization(self):
        def background_task():
            try:
                start_time = time.time()
                criteria = self.criteria_var.get()
                best_route, best_value, best_modes = find_optimal_route(relatives, transport_modes, criteria)
                elapsed_time = time.time() - start_time

                # Schedule GUI updates and graph plotting on the main thread
                self.root.after(
                    0,
                    lambda: self.update_gui_and_plot(criteria, best_route, best_value, best_modes, elapsed_time)
                )
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))

        threading.Thread(target=background_task).start()

    def update_gui_and_plot(self, criteria, best_route, best_value, best_modes, elapsed_time):
        """Update the GUI with results and display the graph in a separate window."""
        # Update the results in the Text widget
        results_text = (
            f"Criteria: {criteria}\n"
            f"Route Order: {best_route}\n"
            f"Transport Modes: {best_modes}\n"
            f"Optimal {criteria.capitalize()}: {best_value:.2f}\n"
            f"Execution Time: {elapsed_time:.2f} seconds"
        )

        # Enable editing temporarily to update the content
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, "end")  # Clear previous content
        self.output_text.insert("end", results_text)  # Add new content
        self.output_text.config(state="disabled")  # Disable editing again

        # Plot the graph in a separate Matplotlib window
        self.plot_graph(best_route, best_modes)


    def plot_graph(self, best_route, best_modes):
        """Plot the optimized route with transport modes in a separate Matplotlib window."""
        latitudes = [relatives[i]['latitude'] for i in best_route] + [relatives[best_route[0]]['latitude']]
        longitudes = [relatives[i]['longitude'] for i in best_route] + [relatives[best_route[0]]['longitude']]

        transport_mode_colors = {
            'walking': 'blue',
            'bicycle': 'green',
            'bus': 'orange',
            'train': 'red'
        }

        fig = plt.figure(figsize=(10, 6))  # Correct usage of plt.figure
        for i in range(len(best_route)):
            start_lat, start_lon = latitudes[i], longitudes[i]
            end_lat, end_lon = latitudes[i + 1], longitudes[i + 1]
            mode = best_modes[i]
            color = transport_mode_colors[mode]

            # Plot the segment with the appropriate color
            plt.plot(
                [start_lon, end_lon],
                [start_lat, end_lat],
                color=color,
                label=mode if i == 0 else "",
                linewidth=2
            )

            # Annotate transport mode
            mid_lat = (start_lat + end_lat) / 2
            mid_lon = (start_lon + end_lon) / 2
            plt.text(mid_lon, mid_lat, mode, fontsize=8, color=color, ha="center")

        plt.scatter(longitudes, latitudes, color="black", s=50)
        for i, rel in enumerate(best_route):
            plt.text(longitudes[i], latitudes[i], f"R{i + 1}", fontsize=10, color="black", ha="center")

        plt.title("Optimized Route with Transport Modes")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.legend(loc="upper left", title="Transport Modes")
        plt.grid(True)
        plt.show()  # Opens the graph in a separate Matplotlib window

# Main GUI entry point
if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    app = RouteOptimizerApp(root)
    root.mainloop()

