# This is the route_visualizer.py script.
import matplotlib.pyplot as plt
import networkx as nx

class RouteVisualizer:
    def __init__(self, route, relatives):
        """
        Initialize RouteVisualizer.
        
        Args:
            route (dict): Optimized route details, including transport modes.
            relatives (list): List of relative location data.
        """
        self.route = route
        self.relatives = relatives

    def plot_route(self):
        """
        Visualize the optimized route using networkx and matplotlib.
        """
        # Create a directed graph
        G = nx.DiGraph()

        # Add nodes (relatives' locations)
        for i, relative in enumerate(self.relatives):
            G.add_node(
                i, 
                pos=(relative['longitude'], relative['latitude']), 
                label=relative['relative']
            )

        # Add edges with colors based on transport modes
        route_order = self.route['order']
        transport_modes = self.route['transport_modes']
        edge_colors = []
        edge_labels = {}

        for i in range(len(route_order) - 1):
            start = route_order[i]
            end = route_order[i + 1]
            mode = transport_modes[i]

            # Assign color based on transport mode
            if mode == 'walking':
                color = 'red'
            elif mode == 'bicycle':
                color = 'yellow'
            elif mode == 'bus':
                color = 'blue'
            elif mode == 'train':
                color = 'green'
            else:
                color = 'gray'

            G.add_edge(start, end)
            edge_colors.append(color)
            edge_labels[(start, end)] = mode.capitalize()  # Mode label

        # Add the final edge back to the starting point
        start = route_order[-1]
        end = route_order[0]
        mode = transport_modes[-1]
        if mode == 'walking':
            color = 'red'
        elif mode == 'bicycle':
            color = 'yellow'
        elif mode == 'bus':
            color = 'blue'
        elif mode == 'train':
            color = 'green'
        else:
            color = 'gray'

        G.add_edge(start, end)
        edge_colors.append(color)
        edge_labels[(start, end)] = mode.capitalize()

        # Get node positions
        pos = nx.get_node_attributes(G, 'pos')

        # Plot the graph
        plt.figure(figsize=(14, 10))
        nx.draw(
            G, 
            pos, 
            with_labels=False, 
            node_size=700, 
            node_color='lightblue', 
            edge_color=edge_colors, 
            arrows=True
        )

        # Add node labels
        labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_labels(G, pos, labels, font_size=10)

        # Add edge labels
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        # Add title and legend
        plt.title("Tarjan's Optimized Route with Transport Modes")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.legend(
            handles=[
                plt.Line2D([0], [0], color='red', lw=2, label='Walking'),
                plt.Line2D([0], [0], color='yellow', lw=2, label='Bicycle'),
                plt.Line2D([0], [0], color='blue', lw=2, label='Bus'),
                plt.Line2D([0], [0], color='green', lw=2, label='Train')
            ], 
            loc='upper left'
        )

        plt.grid(True)
        plt.show()