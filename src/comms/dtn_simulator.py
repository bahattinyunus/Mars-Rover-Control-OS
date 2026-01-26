"""
DTN Simulator for Mars-Rover-Control-OS.
Simulates latency and packet loss typical in Deep Space Networks.
"""

import random
import time

class DtnSimulator:
    def __init__(self, latency_min=300, latency_max=1200, loss_rate=0.05):
        self.latency_min = latency_min # seconds (e.g., Earth-Mars round trip)
        self.latency_max = latency_max
        self.loss_rate = loss_rate

    def simulate_transmission(self, data):
        """
        Simulates the transmission of data through a high-latency, lossy link.
        """
        if random.random() < self.loss_rate:
            print("Packet lost in interplanetary space!")
            return None
        
        latency = random.uniform(self.latency_min, self.latency_max)
        # In a real simulation, we'd use a queue and time.sleep would be avoided in favor of async
        print(f"Data will arrive in {latency:.2f} seconds.")
        return data
