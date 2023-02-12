class Move:
    def __init__(self, start, pos, flags=None):
        if flags is None:
            self.flags = []
        self.start = start
        self.pos = pos
