class Board:
    def __init__(self):
        self.position = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp" for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            ["wp" for _ in range(8)],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
        ]
        self.turn = "w"
