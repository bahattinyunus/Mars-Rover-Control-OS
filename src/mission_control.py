"""
Mission Control Orchestrator for Mars-Rover-Control-OS.
Initializes all sub-systems and manages the main mission loop.
"""

import time
import sys
import os

# Ensure src is in search path
sys.path.append(os.path.dirname(__file__))

from control.drive_node import DriveNode
from navigation.path_planner import PathPlanner
from perception.sensor_fusion import SensorFusion
from comms.telemetry_node import TelemetryNode
from diagnostics import SystemDiagnostics

class MissionControl:
    def __init__(self):
        print("🚀 INITIALIZING MARS ROVER CONTROL OS...")
        
        # Mock Config
        self.config = {
            "wheel_radius": 0.15,
            "track_width": 0.75,
            "kp": 1.5, "ki": 0.1, "kd": 0.05
        }

        # Sub-system Initialization
        self.diagnostics = SystemDiagnostics()
        self.fusion = SensorFusion()
        self.drive = DriveNode(self.config)
        self.planner = PathPlanner()
        self.comms = TelemetryNode(rover_id="ARES_01")

        self.running = True

    def run_mission_loop(self):
        """
        Main lifecycle loop of the rover OS.
        Sense -> Plan -> Act -> Report
        """
        print("✅ MISSION CONTROL ONLINE. ENTERING MAIN LOOP.")
        
        try:
            while self.running:
                # 1. Sense (Simulated measurement)
                dt = 0.1 # 10Hz loop
                self.fusion.predict(dt)
                
                # 2. Plan
                # current_pose = self.fusion.get_estimate()["pose"]
                # target_v, target_w = self.planner.compute_local_velocity(current_pose, None)

                # 3. Act (Mock control commands)
                # self.drive.process_command(target_v, target_w)

                # 4. Diagnostics & Report
                self.diagnostics.update_metrics(battery=98.5, cpu=12.4, mem=45.2, latency=0.5)
                
                if self.diagnostics.is_safe_mode:
                    print("⚠️ ALERT: MISSION CONTROL IN SAFE MODE. LIMITING ACTUATION.")
                
                summary = self.diagnostics.get_summary()
                packet = self.comms.format_packet(state="NAVIGATING", sensors=summary)
                self.comms.send_telemetry(packet)

                time.sleep(dt)
                
                # For demo purposes, we'll break after one iteration
                print("--- Cycle Complete ---")
                break

        except KeyboardInterrupt:
            print("🛑 SHUTDOWN COMMAND RECEIVED.")
            self.running = False

if __name__ == "__main__":
    mc = MissionControl()
    mc.run_mission_loop()
