"""
Command Parser for Mars-Rover-Control-OS.
Handles complex packet reassembly and CRC16 validation for DTN protocols.
"""

import json
import zlib

class CommandParser:
    def __init__(self):
        self.packet_buffer = {} # keyed by sequence_id
        self.MAX_BUFFER_SIZE = 100

    def parse_packet(self, raw_data):
        """
        Parses a single packet. Logic handles fragmentation.
        Expected format: {'seq': int, 'total': int, 'payload': str, 'crc': int}
        """
        try:
            packet = json.loads(raw_data)
        except json.JSONDecodeError:
            return None

        if not self.validate_crc(packet):
            print("Packet integrity compromised. Discarding.")
            return None

        seq_id = packet.get('seq')
        total = packet.get('total')
        
        self.packet_buffer[seq_id] = packet['payload']
        
        if len(self.packet_buffer) == total:
            return self._reassemble_and_parse()
        return None

    def validate_crc(self, packet):
        """
        Validates the payload using CRC16 (simulated via zlib.crc32).
        """
        payload = packet.get('payload', '')
        provided_crc = packet.get('crc', 0)
        actual_crc = zlib.crc32(payload.encode())
        return provided_crc == actual_crc

    def _reassemble_and_parse(self):
        """
        Reassembles fragments in order and parses the full command.
        """
        sorted_keys = sorted(self.packet_buffer.keys())
        full_command_str = "".join([self.packet_buffer[k] for k in sorted_keys])
        self.packet_buffer.clear() # Reset buffer
        
        try:
            return json.loads(full_command_str)
        except json.JSONDecodeError:
            return None
            
    def clear_buffer(self):
        self.packet_buffer.clear()
