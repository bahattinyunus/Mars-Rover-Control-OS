"""
Diagnostics module for Mars-Rover-Control-OS.
Monitors system health and manages state transitions to Safe Mode.
"""

import time

class SystemDiagnostics:
    def __init__(self):
        self.health_status = {
            "battery": 100.0,
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
            "comm_latency": 0.0,
            "modules": {
                "control": "OK",
                "navigation": "OK",
                "perception": "OK",
                "comms": "OK"
            }
        }
        self.is_safe_mode = False

    def update_metrics(self, battery, cpu, mem, latency):
        """
        Updates the internal health metrics.
        """
        self.health_status["battery"] = battery
        self.health_status["cpu_usage"] = cpu
        self.health_status["memory_usage"] = mem
        self.health_status["comm_latency"] = latency
        
        self._check_safety_thresholds()

    def update_module_status(self, module_name, status):
        """
        Updates the heartbeat status of a specific module.
        """
        if module_name in self.health_status["modules"]:
            self.health_status["modules"][module_name] = status
        self._check_safety_thresholds()

    def _check_safety_thresholds(self):
        """
        Internal logic to trigger Safe Mode based on README specifications.
        """
        # README: Battery < 15% -> Safe Mode
        if self.health_status["battery"] < 15.0:
            self._trigger_safe_mode("CRITICAL_BATTERY")

        # README: Comm Latency > 1200s -> Safe Mode
        if self.health_status["comm_latency"] > 1200.0:
            self._trigger_safe_mode("COMM_TIMEOUT")

        # Module failure
        for mod, status in self.health_status["modules"].items():
            if status == "CRITICAL_ERROR":
                self._trigger_safe_mode(f"MODULE_FAILURE_{mod}")

    def _trigger_safe_mode(self, reason):
        if not self.is_safe_mode:
            print(f"DIAGNOSTICS: !!! TRIGGERING SAFE MODE !!! Reason: {reason}")
            self.is_safe_mode = True

    def get_summary(self):
        return {
            "safe_mode_active": self.is_safe_mode,
            "metrics": self.health_status
        }
