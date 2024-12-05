
# **TarjanPlanner**

TarjanPlanner is a route optimization program designed to find the most efficient routes between multiple locations using evolutionary algorithms. The program supports multiple optimization criteria such as minimizing travel time, cost, or number of transfers. It features both a Command-Line Interface (CLI) and a Graphical User Interface (GUI), making it user-friendly for different types of users. TarjanPlanner also provides visualizations of the optimized routes and detailed summaries, ensuring an intuitive experience.

---

## **Features**
- **Multiple Optimization Criteria:** Optimize routes by time, cost, or transfers.
- **Dual Interface Options:** Choose between CLI and GUI modes for convenience.
- **Visualized Routes:** View optimized routes as graphs with transport modes and metrics.
- **Customizable Parameters:** Adjust population size and number of generations for optimization.
- **Save and Export Results:** Save route graphs and summaries for future reference.

---

## **Installation Requirements**

To use TarjanPlanner, ensure you have the following installed:

1. **Python** (Version 3.8 or later)
2. **Required Libraries:** Install dependencies using the command:
   ```bash
   pip install -r requirements.txt
   ```
   Ensure the following packages are included:
   - `logging`
   - `time`
   - `tkinter`
   - `matplotlib`
   - `networkx`
   - `geopy`
   - `pandas`
   - `datetime`
   - `ttkbootstrap`

---

## **How to Run**

1. Clone the repository:
   ```bash
   git clone <repository-link>
   cd <repository-name>
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the program:
   - **For CLI mode:**
     ```bash
     python main.py
     ```
     Choose `1` when prompted to run in CLI mode.
   - **For GUI mode:**
     ```bash
     python main.py
     ```
     Choose `2` when prompted to run in GUI mode.

---

## **File Structure**
- **`main.py`**: Entry point of the program, manages CLI and GUI modes.
- **`evolutionary_optimizer.py`**: Core module implementing the evolutionary algorithm for route optimization.
- **`route_visualizer.py`**: Handles visualization of the optimized routes using `matplotlib` and `networkx`.
- **`gui_main.py`**: Provides the GUI functionality with interactive elements for route optimization.
- **`requirements.txt`**: Contains a list of required Python packages.
- **Sample Data Files**: Includes default `locations.json` and `mode_of_transport.json` for testing.

---

## **Example Usage**
- **CLI Mode Example:**
  ```
  Select Mode:
  1. CLI (Command Line Interface)
  2. GUI (Graphical User Interface)
  Enter the number corresponding to your choice: 1
  ```
  Enter optimization criteria (time, cost, or transfers), population size, and the number of generations as prompted.

- **GUI Mode Example:**
  After selecting GUI mode, adjust parameters such as optimization criteria, population size, and generations, then click "Run Optimizer" to visualize the optimal route.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contributing**

Contributions are welcome! Feel free to fork the repository and submit pull requests. Please ensure your contributions follow the existing coding style and are thoroughly tested.

---

## **Contact**

For questions, issues, or suggestions, please contact:

- **Name:** [Your Full Name]  
- **Email:** [Your Email Address]  
- **GitHub:** [Your GitHub Profile Link]  
- **LinkedIn:** [Your LinkedIn Profile Link] (optional)

---

## **Future Improvements**
- Add real-time data integration (e.g., traffic updates).
- Improve transport mode prediction with machine learning models.
- Enhance GUI with more customization options.

---

## **Acknowledgments**
Special thanks to [Any Mentors, Team Members, or Specific Contributors] for their guidance and support in developing this project.

---

## **FAQs**
### What Python version is required?
Python 3.8 or later is recommended.

### How can I test the program?
Use the provided sample data files (`locations.json` and `mode_of_transport.json`) for testing.

### Who can I contact for support?
You can contact me at the email address provided above.
