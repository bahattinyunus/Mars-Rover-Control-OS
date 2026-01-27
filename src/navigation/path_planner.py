"""
Path Planner for Mars-Rover-Control-OS.
Implementation of Hybrid A* logic for Martian terrain navigation.
"""

import math
import heapq

class PathPlanner:
    def __init__(self, planning_mode="hybrid_a_star"):
        self.planning_mode = planning_mode
        self.RESOLUTION = 0.5
        self.HEURISTIC_WEIGHT = 1.0

    def compute_global_path(self, start, goal, occupancy_grid):
        """
        Computes a global path from start (x, y, theta) to goal (x, y, theta).
        Using Hybrid A* search.
        """
        # start/goal format: [x, y, theta]
        open_set = []
        # Priority queue entry: (f_score, state)
        heapq.heappush(open_set, (0, tuple(start)))
        
        came_from = {}
        g_score = {tuple(start): 0}
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if self._is_at_goal(current, goal):
                return self._reconstruct_path(came_from, current)
            
            for next_state in self._get_neighbors(current):
                # Simulated cost calculation based on terrain and distance
                tenative_g = g_score[current] + self._calculate_cost(current, next_state)
                
                if next_state not in g_score or tenative_g < g_score[next_state]:
                    came_from[next_state] = current
                    g_score[next_state] = tenative_g
                    f_score = tenative_g + self.HEURISTIC_WEIGHT * self._heuristic(next_state, goal)
                    heapq.heappush(open_set, (f_score, next_state))
                    
        return [] # Path not found

    def _get_neighbors(self, state):
        """
        Generates kinematically feasible neighbors (forward, backward, steering).
        """
        x, y, theta = state
        neighbors = []
        steer_angles = [-0.5, 0, 0.5] # rad
        step_size = 1.0 # meters
        
        for steer in steer_angles:
            new_theta = theta + steer
            new_x = x + step_size * math.cos(new_theta)
            new_y = y + step_size * math.sin(new_theta)
            neighbors.append((round(new_x, 2), round(new_y, 2), round(new_theta, 2)))
        return neighbors

    def _heuristic(self, state, goal):
        # Euclidean + Heading alignment heuristic
        dist = math.sqrt((state[0]-goal[0])**2 + (state[1]-goal[1])**2)
        angle_diff = abs(state[2] - goal[2])
        return dist + 0.5 * angle_diff

    def _calculate_cost(self, current, next_state):
        return 1.0 # Basic unit cost per step

    def _is_at_goal(self, state, goal):
        return math.sqrt((state[0]-goal[0])**2 + (state[1]-goal[1])**2) < 0.5

    def _reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]
