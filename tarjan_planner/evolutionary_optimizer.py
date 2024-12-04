# This is the evolutionary_optimizer.py script.

import random
from geopy.distance import geodesic
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

class EvolutionaryOptimizer:
    def __init__(self, relatives, transport_modes, population_size=50, generations=200, mutation_rate=0.1, criteria='time', log_file_path="execution_log.csv"):
        self.relatives = relatives
        self.transport_modes = transport_modes
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.criteria = criteria
        self.log_file_path = log_file_path

    def _compute_distance(self, relative1, relative2):
        return geodesic(
            (relative1['latitude'], relative1['longitude']),
            (relative2['latitude'], relative2['longitude'])
        ).kilometers

    def _select_best_transport_mode(self, distance):
        if distance < 1:
            return 'walking'
        elif distance < 3:
            return 'bicycle'
        elif distance < 15:
            return 'bus'
        else:
            return 'train'

    def _evaluate_fitness(self, route):
        total_distance = 0
        total_time = 0
        total_cost = 0
        transport_modes = []

        for i in range(len(route) - 1):
            start = self.relatives[route[i]]
            end = self.relatives[route[i + 1]]
            distance = self._compute_distance(start, end)
            total_distance += distance

            best_mode = self._select_best_transport_mode(distance)
            transport_modes.append(best_mode)

            mode_details = self.transport_modes[best_mode]
            total_time += distance / mode_details['speed']
            total_cost += distance * mode_details['cost_per_km']

        start = self.relatives[route[-1]]
        end = self.relatives[route[0]]
        distance = self._compute_distance(start, end)
        total_distance += distance
        best_mode = self._select_best_transport_mode(distance)
        transport_modes.append(best_mode)
        mode_details = self.transport_modes[best_mode]
        total_time += distance / mode_details['speed']
        total_cost += distance * mode_details['cost_per_km']

        if self.criteria == 'time':
            fitness = 1 / total_time
        elif self.criteria == 'cost':
            fitness = 1 / total_cost
        else:
            fitness = 1 / len(transport_modes)

        return fitness, total_time, total_cost, transport_modes

    def _evaluate_population(self, population):
        """
        Evaluate the fitness of a population in parallel using ThreadPoolExecutor.
        """
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(self._evaluate_fitness, population))
        return results
    
    def optimize(self):
        """
        Perform optimization using an evolutionary algorithm with parallelized fitness evaluation.
        """
        population = self._initialize_population()
        best_individual = None
        best_fitness = -float('inf')
        best_route_info = None

        for generation in range(self.generations):
            # Parallel evaluation of population fitness
            fitness_results = self._evaluate_population(population)
            fitness_values = [result[0] for result in fitness_results]

            # Find the best individual in this generation
            for i, fitness in enumerate(fitness_values):
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_individual = population[i]
                    best_route_info = fitness_results[i]

            # Selection (Roulette Wheel Selection)
            selected = random.choices(
                population=population, weights=fitness_values, k=self.population_size
            )

            # Crossover and mutation to create the next population
            next_population = []
            for i in range(0, len(selected), 2):
                parent1, parent2 = selected[i], selected[(i + 1) % len(selected)]
                child = self._crossover(parent1, parent2)
                self._mutate(child)
                next_population.append(child)

            # Update the population
            population = next_population

        # Return the best individual and its details
        return {
            'order': best_individual,
            'fitness': best_fitness,
            'total_time': best_route_info[1],
            'total_cost': best_route_info[2],
            'transport_modes': best_route_info[3]
        }

    def _initialize_population(self):
        return [random.sample(range(len(self.relatives)), len(self.relatives)) for _ in range(self.population_size)]

    def _crossover(self, parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        child = [None] * size
        child[start:end] = parent1[start:end]

        pointer = 0
        for gene in parent2:
            if gene not in child:
                while child[pointer] is not None:
                    pointer += 1
                child[pointer] = gene
        return child

    def _mutate(self, individual):
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(len(individual)), 2)
            individual[i], individual[j] = individual[j], individual[i]
