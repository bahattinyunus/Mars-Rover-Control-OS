"""
Telemetry Node for Mars-Rover-Control-OS.
Handles outgoing status data to Earth.
"""

import json
import time

class TelemetryNode:
    def __init__(self, rover_id="ROVER_01"):
        self.rover_id = rover_id

    def format_packet(self, state, sensors):
        """
        Formats internal state and sensor data into a telemetry packet.
        """
        packet = {
            "timestamp": time.time(),
            "rover_id": self.rover_id,
            "state": state,
            "sensors": sensors
        }
        return json.dumps(packet)

    def send_telemetry(self, packet):
        """
        Sends the telemetry packet via the communication interface.
        """
        # Placeholder for actual transmission logic
        print(f"Sending Telemetry: {packet[:100]}...")
