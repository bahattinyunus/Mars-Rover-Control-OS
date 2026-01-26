"""
Simulator Interface for Mars-Rover-Control-OS.
Bridge for Gazebo or custom simulator.
"""

class SimulatorInterface:
    def __init__(self, simulator_url="localhost:11345"):
        self.simulator_url = simulator_url

    def spawn_rover(self, initial_pose):
        """
        Spawns the rover model in the simulation environment.
        """
        print(f"Spawning rover at {initial_pose} in simulator at {self.simulator_url}")

    def sync_clock(self):
        """
        Syncs the OS clock with the simulation world clock.
        """
        pass
