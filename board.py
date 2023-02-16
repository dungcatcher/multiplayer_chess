from movegen import gen_piece_moves


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
        self.all_moves = self.gen_all_moves(self.turn)

    def gen_all_moves(self, colour):
        moves = []

        for x in range(8):
            for y in range(8):
                if self.position[y][x] is not None:
                    if self.position[y][x][0] == colour:
                        piece_moves = gen_piece_moves(self, (x, y))
                        for move in piece_moves:
                            print(move.start, move.end)
                        moves += piece_moves

        return moves

    def fetch_moves_from_square(self, pos):
        moves = []

        for move in self.all_moves:
            if move.start == pos:
                moves.append(move)

        return moves
