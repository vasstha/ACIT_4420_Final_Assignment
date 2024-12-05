import matplotlib.pyplot as plt

def plot_route(route, relatives, transport_modes):
    """
    Plots the optimized route with color-coded edges and transport mode notations.
    """
    latitudes = [relatives[i]['latitude'] for i in route]
    longitudes = [relatives[i]['longitude'] for i in route]
    latitudes.append(latitudes[0])  # To complete the loop
    longitudes.append(longitudes[0])
    
    transport_mode_colors = {
        'walking': 'blue',
        'bicycle': 'green',
        'bus': 'orange',
        'train': 'red'
    }
    
    plt.figure(figsize=(10, 6))
    ax = plt.gca()

    # Plot the route
    for i in range(len(route)):
        start_lat, start_lon = latitudes[i], longitudes[i]
        end_lat, end_lon = latitudes[i + 1], longitudes[i + 1]
        mode = transport_modes[i]
        color = transport_mode_colors[mode]

        # Draw the segment with the appropriate color
        ax.plot(
            [start_lon, end_lon],
            [start_lat, end_lat],
            color=color,
            label=mode if i == 0 else "",  # Add legend only once per mode
            linewidth=2
        )
        # Annotate the mode
        mid_lat = (start_lat + end_lat) / 2
        mid_lon = (start_lon + end_lon) / 2
        ax.text(mid_lon, mid_lat, mode, fontsize=8, color=color, ha="center")

    # Plot the nodes
    for i, rel in enumerate(route):
        ax.scatter(longitudes[i], latitudes[i], color="black", s=50)
        ax.text(longitudes[i], latitudes[i], f"R{i + 1}", fontsize=10, color="black", ha="center")

    plt.title("Optimized Route with Transport Modes")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.legend(loc="upper left", title="Transport Modes")
    plt.show()
