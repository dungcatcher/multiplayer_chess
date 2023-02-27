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

        self.w_king_pos = (4, 7)
        self.b_king_pos = (4, 0)

        self.all_moves = self.gen_all_moves(self.turn)

    def gen_all_moves(self, colour):
        moves = []

        for x in range(8):
            for y in range(8):
                if self.position[y][x] is not None:
                    if self.position[y][x][0] == colour:
                        piece_moves = gen_piece_moves(self, (x, y))
                        moves += piece_moves

        return moves

    def fetch_moves_from_square(self, pos):
        moves = []

        for move in self.all_moves:
            if move.start == pos:
                moves.append(move)

        return moves

    def make_move(self, move, gen_new_moves=True):
        piece_id = self.position[move.start[1]][move.start[0]]
        self.position[move.end[1]][move.end[0]] = piece_id
        self.position[move.start[1]][move.start[0]] = None

        if piece_id[1] == 'wk':
            self.w_king_pos = move.end
        elif piece_id[1] == 'bk':
            self.b_king_pos = move.end

        self.turn = 'b' if self.turn == 'w' else 'w'
        if gen_new_moves:
            self.all_moves = self.gen_all_moves(self.turn)
