class Move:
    def __init__(self, start, end, flags=None):
        if flags is None:
            self.flags = []
        self.start = start
        self.end = end
