import tkinter as tk
import time
import logging
from evolutionary_optimizer import EvolutionaryOptimizer
from route_visualizer import RouteVisualizer
from relatives_data import relatives, transport_modes
from gui_main import RouteOptimizerApp


def run_cli():
    """Run the program in CLI mode."""
    print("Welcome to the Route Optimizer CLI!")
    logging.basicConfig(filename="cli_execution_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

    try:
        # Get user inputs
        criteria = input("Enter optimization criteria (time/cost/transfers): ").strip().lower()
        if criteria not in ["time", "cost", "transfers"]:
            raise ValueError("Invalid criteria. Choose from 'time', 'cost', or 'transfers'.")

        population_size = int(input("Enter population size (e.g., 50): "))
        generations = int(input("Enter number of generations (e.g., 200): "))

        # Start timing
        start_time = time.time()

        # Initialize the optimizer
        optimizer = EvolutionaryOptimizer(
            relatives=relatives,
            transport_modes=transport_modes,
            population_size=population_size,
            generations=generations,
            criteria=criteria
        )

        # Run the optimizer
        result = optimizer.optimize()

        # End timing
        elapsed_time = time.time() - start_time

        # Display results
        print("\n--- Optimal Route ---")
        print("Optimal Route Order:", result['order'])
        print(f"Total Time: {result['total_time']:.2f} hrs")
        print(f"Total Cost: {result['total_cost']:.2f}")
        print("Transport Modes:", result['transport_modes'])
        print(f"Execution Time: {elapsed_time:.2f} seconds")

        # Log the execution details
        logging.info(
            f"Criteria: {criteria}, Population Size: {population_size}, Generations: {generations}, "
            f"Execution Time: {elapsed_time:.2f} seconds, Optimal Route: {result['order']}, "
            f"Total Time: {result['total_time']:.2f}, Total Cost: {result['total_cost']:.2f}"
        )

        # Visualize route
        visualizer = RouteVisualizer(route=result, relatives=relatives)
        visualizer.plot_route()

    except ValueError as e:
        print(f"Input Error: {e}")
        logging.error(f"Input Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logging.error(f"Unexpected Error: {e}")


def run_gui():
    """Run the program in GUI mode."""
    try:
        root = tk.Tk()
        app = RouteOptimizerApp(root)
        root.mainloop()
    except Exception as e:
        print(f"An unexpected error occurred in GUI mode: {e}")
        logging.error(f"Unexpected Error in GUI mode: {e}")


if __name__ == "__main__":
    print("Select Mode:")
    print("1. CLI (Command Line Interface)")
    print("2. GUI (Graphical User Interface)")

    mode = input("Enter the number corresponding to your choice: ").strip()

    if mode == "1":
        run_cli()
    elif mode == "2":
        run_gui()
    else:
        print("Invalid choice. Exiting the program.")
