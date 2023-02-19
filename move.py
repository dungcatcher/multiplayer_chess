class Move:
    def __init__(self, start, end, flags=None):
        if flags is None:
            self.flags = []
        else:
            self.flags = flags
        self.start = start
        self.end = end
