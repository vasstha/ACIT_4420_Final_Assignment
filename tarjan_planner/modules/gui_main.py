import logging
import time
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from modules.evolutionary_optimizer import EvolutionaryOptimizer
from data.relatives_data import relatives, transport_modes
import ttkbootstrap as ttk
from ttkbootstrap.constants import SUCCESS, INFO, PRIMARY
from tkinter.filedialog import asksaveasfilename


class ToolTip:
    """A simple tooltip class for widgets."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        """Display the tooltip."""
        if self.tip_window or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + cy + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = ttk.Label(
            tw, text=self.text, justify="left", background="yellow", relief="solid", borderwidth=1, wraplength=200
        )
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        """Remove the tooltip."""
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class RouteOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Route Optimizer")
        self.root.geometry("900x600")
        self.relatives = relatives
        # Default colors
        self.route_color = "blue"  # Fixed route color
        self.point_color = "black"  # Fixed point color

        # Store results for replotting
        self.last_result = None
        self.optimizer = None

        self.setup_gui()

    def setup_gui(self):
        """Set up the GUI layout with a split view for parameter inputs, table, and graph."""
        # Main Paned Window for Upper and Lower Sections
        main_paned_window = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        main_paned_window.pack(fill="both", expand=True)

        # Upper Frame: Parameters and Table
        upper_frame = ttk.PanedWindow(main_paned_window, orient=tk.HORIZONTAL)
        main_paned_window.add(upper_frame, weight=1)

        # Left Frame: Parameter Selection
        left_frame = ttk.Frame(upper_frame, padding=10)
        upper_frame.add(left_frame, weight=1)

        ttk.Label(left_frame, text="Optimization Criteria:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.criteria_var = ttk.StringVar(value="time")
        self.criteria_menu = ttk.Combobox(left_frame, textvariable=self.criteria_var, values=("time", "cost", "transfers"), state="readonly")
        self.criteria_menu.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(left_frame, text="Population Size:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.population_size_var = ttk.StringVar(value="50")
        self.population_size_var_entry = ttk.Entry(left_frame, textvariable=self.population_size_var)
        self.population_size_var_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(left_frame, text="Generations:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.generations_var = ttk.StringVar(value="200")
        self.generations_var_entry = ttk.Entry(left_frame, textvariable=self.generations_var)
        self.generations_var_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.run_button = ttk.Button(left_frame, text="Run Optimizer", bootstyle=SUCCESS, command=self.run_optimizer)
        self.run_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.save_button = ttk.Button(left_frame, text="Save Graph", bootstyle=INFO, command=self.save_graph)
        self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Right Frame: Results Table
        right_frame = ttk.Frame(upper_frame, padding=10)
        upper_frame.add(right_frame, weight=2)

        self.output_frame = ttk.Labelframe(right_frame, text="Results", padding=10)
        self.output_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.output_text = ttk.Text(self.output_frame, height=10, wrap="word", state="disabled")
        self.output_text.pack(fill="both", expand=True)

        # Lower Frame: Graph Visualization
        self.graph_frame = ttk.Labelframe(main_paned_window, text="Route Visualization", padding=10)
        main_paned_window.add(self.graph_frame, weight=2)

        # Tooltips
        ToolTip(self.criteria_menu, "Select the optimization criteria: time, cost, or transfers.")
        ToolTip(self.population_size_var_entry, "Enter the population size (e.g., 50). Higher values increase runtime.")
        ToolTip(self.generations_var_entry, "Enter the number of generations (e.g., 200). Higher values improve results but take longer.")

    def reset_gui(self):
        """Clear and reset GUI elements."""
        for widget in self.output_frame.winfo_children():
            widget.destroy()

        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        self.last_result = None
    
    def run_optimizer(self):
        """Run optimizer and display results."""
        try:

            #Reset GUI before running
            self.reset_gui()

            #start timing
            start_time = time.time()

            #initialize the optimizer
            self.optimizer = EvolutionaryOptimizer(
                relatives=self.relatives,
                transport_modes=transport_modes,
                population_size=int(self.population_size_var.get()),
                generations=int(self.generations_var.get()),
                criteria=self.criteria_var.get()
            )

            #run the optimizer
            result = self.optimizer.optimize()
            #self.last_result = result
            
            #save the result for rendering
            self.last_result = result

            #log execution details
            elapsed_time = time.time() - start_time

            logging.info(
                f"Optimization Criteria: {self.criteria_var.get()}, "
                f"Population Size: {self.population_size_var.get()}, "
                f"Generations: {self.generations_var.get()}, "
                f"Elapsed Time: {elapsed_time:.2f} seconds, "
                f"Optimal Route: {result['order']}, "
                f"Total Time: {result['total_time']:.2f}, "
                f"Total Cost: {result['total_cost']:.2f}"
            )

            # Visualize route and table
            
            self.display_segments(result)
            self.plot_graph(result)
            
            

        except ValueError as ve:
            logging.error(f"Value error: {ve}")
            messagebox.showerror("Input Error", f"Invalid input: {ve}")
        except Exception as e:
            logging.error(f"Error during optimization: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")


    def plot_graph(self, result):
        """Plot the route visualization with fixed colors based on transport modes."""
        logging.info("Starting to plot graph.")
        try:
            # Validate result data
            order = result.get('order', [])
            transport_modes = result.get('transport_modes', [])

            if len(order) - 1 != len(transport_modes):
                logging.error(
                    f"Data mismatch: order length is {len(order)}, "
                    f"but transport_modes length is {len(transport_modes)}."
                )
                messagebox.showerror("Error", "Invalid optimization result. Cannot render graph.")
                return

            # Clear the graph frame
            for widget in self.graph_frame.winfo_children():
                widget.destroy()

            # Prepare data for plotting
            latitudes = [self.relatives[i]['latitude'] for i in order]
            longitudes = [self.relatives[i]['longitude'] for i in order]

            # Add first point to close the loop
            latitudes.append(latitudes[0])
            longitudes.append(longitudes[0])

            # Create the Matplotlib figure
            fig = Figure(figsize=(8, 6), dpi=100)
            ax = fig.add_subplot(111)

            # Define transport mode colors
            mode_colors = {
                'walking': 'green',
                'bicycle': 'yellow',
                'bus': 'blue',
                'train': 'red'
            }

            # Track labels added to the legend to avoid repetition
            labels_added = set()

            # Plot edges with transport mode-specific colors
            for i in range(len(order) - 1):
                mode = transport_modes[i]
                color = mode_colors.get(mode, 'gray')  # Default to gray if mode is unknown
                ax.plot(
                    [longitudes[i], longitudes[i + 1]],
                    [latitudes[i], latitudes[i + 1]],
                    color=color,
                    linestyle='-',
                    linewidth=2
                )

                # Add an arrow to indicate direction
                ax.annotate(
                    "",
                    xy=(longitudes[i + 1], latitudes[i + 1]),
                    xytext=(longitudes[i], latitudes[i]),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5)
                )

                # Add mode to legend if not already added
                if mode not in labels_added:
                    ax.plot([], [], color=color, label=f"{mode.capitalize()}")
                    labels_added.add(mode)

            # Plot relatives' nodes as black points
            ax.scatter(longitudes, latitudes, color="black", s=50, label="Relatives" if "Relatives" not in labels_added else "")

            # Annotate nodes with names
            for i, relative in enumerate(order):
                ax.text(
                    longitudes[i], latitudes[i],
                    f"Relative_{relative}",
                    fontsize=8, ha='right', color='darkblue'
                )

            # Add summary metrics in the graph
            total_time = f"{result['total_time']:.2f} hours"
            total_cost = f"{result['total_cost']:.2f} USD"
            ax.text(
                0.95, 0.95,
                f"Total Time: {total_time}\nTotal Cost: {total_cost}",
                transform=ax.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
            )

            # Set axis titles and layout
            ax.set_title("Route Visualization")
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")
            ax.legend(loc="upper left")

            # Add the graph to the Tkinter frame
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

            logging.info("Graph successfully rendered.")
        except Exception as e:
            logging.error(f"Error rendering graph: {e}")
            messagebox.showerror("Error", "Failed to render the graph. Check logs for details.")


    def update_notation_summary(self, mode_colors):
        """Update the notation summary below the graph."""
        try:
            # Clear any existing notations
            for widget in self.output_frame.winfo_children():
                widget.destroy()

            # Add a label for notation summary
            summary_label = ttk.Label(self.output_frame, text="Legend: Transport Modes", font=("Arial", 10, "bold"))
            summary_label.pack(pady=5)

            # Add color and label for each transport mode
            for mode, color in mode_colors.items():
                mode_label = ttk.Label(
                    self.output_frame,
                    text=f"{mode.capitalize()}: ",
                    font=("Arial", 10),
                    foreground=color
                )
                mode_label.pack(anchor="w")

            # Add a note for relatives
            relative_label = ttk.Label(
                self.output_frame,
                text="Relatives: Black Dots",
                font=("Arial", 10),
                foreground="black"
            )
            relative_label.pack(anchor="w")
        except Exception as e:
            logging.error(f"Error updating notation summary: {e}")


    def display_segments(self, result):

        """Display detailed segment information in a table."""
        tree = ttk.Treeview(self.output_frame, columns=("Start", "End", "Mode", "Distance"))
        tree.heading("#0", text="Segment")
        tree.heading("Start", text="Start")
        tree.heading("End", text="End")
        tree.heading("Mode", text="Mode")
        tree.heading("Distance", text="Distance (km)")

        tree.column("#0", width=50, anchor="center")
        tree.column("Start", width=100, anchor="center")
        tree.column("End", width=100, anchor="center")
        tree.column("Mode", width=100, anchor="center")
        tree.column("Distance", width=100, anchor="center")

        for i in range(len(result['order']) - 1):
            start = self.relatives[result['order'][i]]['relative']
            end = self.relatives[result['order'][i + 1]]['relative']
            mode = result['transport_modes'][i]
            distance = f"{self.optimizer._compute_distance(self.relatives[result['order'][i]], self.relatives[result['order'][i + 1]]):.2f}"
            tree.insert("", "end", text=str(i + 1), values=(start, end, mode, distance))

        tree.pack(fill="both", expand=True)

    
    

    def on_resize(self, event):
        """Callback to dynamically adjust graph proportions when resized."""
        try:
            if hasattr(self, "last_result"):  # Check if there is a previous result to replot
                #clear only graph widgets
                for widget in self.graph_frame.winfo_children():
                    widget.destroy()
                
                #Replot the graph
                self.plot_graph(self.last_result)  # Replot the graph
        except Exception as e:
                logging.error(f"Error during graph resize: {e}")
                messagebox.showerror("Error", "Failed to resize the graph. Check logs for details.")
    
    

    def save_graph(self):
        """Save the current graph as a PNG file."""
        try:
            if not hasattr(self, 'last_result') or not self.last_result:
                raise ValueError("No graph data available. Run the optimizer first.")

            result = self.last_result

            # Prepare data for plotting
            order = result.get('order', [])
            transport_modes = result.get('transport_modes', [])
            if len(order) - 1 != len(transport_modes):
                logging.error(
                    f"Data mismatch in save_graph: order length is {len(order)}, "
                    f"but transport_modes length is {len(transport_modes)}."
                )
                raise ValueError("Data mismatch in graph. Cannot save.")

            latitudes = [self.relatives[i]['latitude'] for i in order]
            longitudes = [self.relatives[i]['longitude'] for i in order]

            # Add first point to close the loop
            latitudes.append(latitudes[0])
            longitudes.append(longitudes[0])

            # Create the Matplotlib figure
            fig = Figure(figsize=(8, 6), dpi=100)
            ax = fig.add_subplot(111)

            # Define transport mode colors
            mode_colors = {
                'walking': 'green',
                'bicycle': 'yellow',
                'bus': 'blue',
                'train': 'red'
            }

            # Plot edges with transport mode-specific colors
            for i in range(len(order) - 1):
                mode = transport_modes[i]
                color = mode_colors.get(mode, 'gray')  # Default to gray if mode is unknown
                ax.plot(
                    [longitudes[i], longitudes[i + 1]],
                    [latitudes[i], latitudes[i + 1]],
                    color=color,
                    linestyle='-',
                    linewidth=2
                )

            # Plot relatives' nodes as black points
            ax.scatter(longitudes, latitudes, color="black", s=50, label="Relatives")

            # Annotate nodes with names
            for i, relative in enumerate(order):
                ax.text(
                    longitudes[i], latitudes[i],
                    f"Relative_{relative}",
                    fontsize=8, ha='right', color='darkblue'
                )

            # Add summary metrics in the graph
            total_time = f"{result['total_time']:.2f} hours"
            total_cost = f"{result['total_cost']:.2f} USD"
            ax.text(
                0.95, 0.95,
                f"Total Time: {total_time}\nTotal Cost: {total_cost}",
                transform=ax.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
            )

            # Set axis titles and layout
            ax.set_title("Route Visualization")
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")
            ax.legend(loc="upper left")

            # Open a file dialog to let the user select the save path
            file_path = asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
                title="Save Graph As"
            )
            if not file_path:
                return  # User canceled the save dialog

            # Save the graph to the selected path
            fig.savefig(file_path)
            messagebox.showinfo("Success", f"Graph saved successfully at {file_path}")
            logging.info(f"Graph successfully saved at {file_path}")
            
        except Exception as e:
            logging.error(f"Error saving graph: {e}")
            messagebox.showerror("Error", f"Failed to save graph: {e}")



if __name__ == "__main__":
    app = ttk.Window(themename="darkly")  # Using ttkbootstrap theme
    RouteOptimizerApp(app)
    app.mainloop()
