from geopy.distance import geodesic
import numpy as np


def precompute_distance_matrix(relatives):
    """
    Precomputes a distance matrix for all pairs of relatives.
    """
    n = len(relatives)
    distance_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i][j] = geodesic(
                    (relatives[i]['latitude'], relatives[i]['longitude']),
                    (relatives[j]['latitude'], relatives[j]['longitude'])
                ).kilometers
    return distance_matrix


def calculate_distance(point1, point2):
    return geodesic((point1['latitude'], point1['longitude']),
                    (point2['latitude'], point2['longitude'])).kilometers


def calculate_route_cost(route, relatives, transport_modes):
    total_cost = 0
    for i in range(len(route) - 1):
        start = relatives[route[i]]
        end = relatives[route[i + 1]]
        distance = calculate_distance(start, end)
        mode = select_best_transport_mode(distance)
        total_cost += distance * transport_modes[mode]['cost_per_km']
    return total_cost


def calculate_route_time(route, relatives, transport_modes):
    total_time = 0
    previous_mode = None
    for i in range(len(route) - 1):
        start = relatives[route[i]]
        end = relatives[route[i + 1]]
        distance = calculate_distance(start, end)
        mode = select_best_transport_mode(distance)
        total_time += distance / transport_modes[mode]['speed']
        if previous_mode and previous_mode != mode:
            total_time += transport_modes[mode]['transfer_time_min'] / 60
        previous_mode = mode
    return total_time

def select_best_transport_mode(distance):
    if distance < 1:
        return 'walking'
    elif distance < 3:
        return 'bicycle'
    elif distance < 15:
        return 'bus'
    else:
        return 'train'
