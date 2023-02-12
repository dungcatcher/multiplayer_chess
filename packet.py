class Packet:
    def __init__(self, packet_type, description, data):
        self.type = packet_type  # Initial or update
        self.description = description
        self.data = data
