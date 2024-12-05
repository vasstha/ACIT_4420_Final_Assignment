from itertools import permutations
import logging
from modules.route_calculator import calculate_route_time, calculate_route_cost, precompute_distance_matrix, select_best_transport_mode

def find_optimal_route(relatives, transport_modes, criteria='time'):
    """
    Finds the optimal route based on the selected criteria.
    """
    distance_matrix = precompute_distance_matrix(relatives)  # Assuming this function is defined
    n = len(relatives)
    best_route = None
    best_value = float('inf')
    best_modes = []

    for route in permutations(range(n)):
        total_cost = 0
        total_time = 0
        transfers = 0
        current_modes = []
        previous_mode = None

        for i in range(len(route) - 1):
            start = route[i]
            end = route[i + 1]
            distance = distance_matrix[start][end]
            mode = select_best_transport_mode(distance)  # Assuming this function is defined
            current_modes.append(mode)

            if criteria == 'time':
                total_time += distance / transport_modes[mode]['speed']
                if previous_mode and mode != previous_mode:
                    total_time += transport_modes[mode]['transfer_time_min'] / 60
            elif criteria == 'cost':
                total_cost += distance * transport_modes[mode]['cost_per_km']
            elif criteria == 'transfers':
                if previous_mode and mode != previous_mode:
                    transfers += 1

            previous_mode = mode

        # Add the return leg to complete the loop
        start = route[-1]
        end = route[0]
        distance = distance_matrix[start][end]
        mode = select_best_transport_mode(distance)
        current_modes.append(mode)

        if criteria == 'time':
            total_time += distance / transport_modes[mode]['speed']
            if previous_mode and mode != previous_mode:
                total_time += transport_modes[mode]['transfer_time_min'] / 60
        elif criteria == 'cost':
            total_cost += distance * transport_modes[mode]['cost_per_km']
        elif criteria == 'transfers':
            if previous_mode and mode != previous_mode:
                transfers += 1
                logging.info(f"Route: {route}, Mode Changes: {transfers}")

        # Evaluate based on the criteria
        if criteria == 'time' and total_time < best_value:
            best_value = total_time
            best_route = route
            best_modes = current_modes
        elif criteria == 'cost' and total_cost < best_value:
            best_value = total_cost
            best_route = route
            best_modes = current_modes
        elif criteria == 'transfers' and transfers < best_value:
            best_value = transfers
            best_route = route
            best_modes = current_modes

    return best_route, best_value, best_modes

