from move import Move
import copy


def gen_absolute_moves(board, pos, vectors):
    colour = board.position[pos[1]][pos[0]][0]
    moves = []

    for vector in vectors:
        test_square = (pos[0] + vector[0], pos[1] + vector[1])
        if 0 <= test_square[0] <= 7 and 0 <= test_square[1] <= 7:
            if board.position[test_square[1]][test_square[0]] is None:
                moves.append(Move(pos, test_square))
            elif board.position[test_square[1]][test_square[0]][0] != colour:
                moves.append(Move(pos, test_square, flags=["capture"]))

    return moves


def gen_sliding_moves(board, pos, vectors):
    colour = board.position[pos[1]][pos[0]][0]
    moves = []

    for vector in vectors:
        test_square = pos
        while True:
            test_square = (test_square[0] + vector[0], test_square[1] + vector[1])
            if 0 <= test_square[0] <= 7 and 0 <= test_square[1] <= 7:
                if board.position[test_square[1]][test_square[0]] is None:
                    moves.append(Move(pos, test_square))
                else:
                    if board.position[test_square[1]][test_square[0]][0] != colour:
                        moves.append(Move(pos, test_square, flags=["capture"]))
                    break
            else:
                break

    return moves


def check_piece_attackers(board, moves, piece):
    for move in moves:
        if 'capture' in move.flags:
            if board.position[move.end[1]][move.end[0]][1] == piece:
                return True

    return False


def in_check(board, colour):
    king_pos = board.w_king_pos if colour == 'w' else board.b_king_pos

    piece_moves = {
        'n': gen_knight_moves(board, king_pos),
        'b': gen_bishop_moves(board, king_pos),
        'r': gen_rook_moves(board, king_pos),
        'q': gen_queen_moves(board, king_pos),
        'k': gen_king_moves(board, king_pos)
    }

    for piece, moves in piece_moves.items():
        if check_piece_attackers(board, moves, piece):
            return True

    return False


def gen_pawn_moves(board, pos):
    colour = board.position[pos[1]][pos[0]][0]
    moves = []

    direction = -1 if colour == 'w' else 1

    if (colour == 'w' and pos[1] == 1) or (colour == 'b' and pos[1] == 6):  # Promotions
        pass
    else:
        test_square = (pos[0], pos[1] + direction)
        if board.position[test_square[1]][test_square[0]] is None:
            moves.append(Move(pos, test_square))
            if (colour == 'w' and pos[1] == 6) or (colour == 'b' and pos[1] == 1):  # Double push
                new_test_square = (pos[0], pos[1] + 2 * direction)
                if board.position[new_test_square[1]][new_test_square[0]] is None:
                    moves.append(Move(pos, new_test_square, flags=['double push']))

    capture_vectors = [(-1, direction), (1, direction)]
    for vector in capture_vectors:
        test_square = (pos[0] + vector[0], pos[1] + vector[1])
        if 0 <= test_square[0] <= 7 and 0 <= test_square[1] <= 7:
            if board.position[test_square[1]][test_square[0]]:
                if board.position[test_square[1]][test_square[0]][0] != colour:
                    moves.append(Move(pos, test_square, flags=["capture"]))

    return moves


def gen_knight_moves(board, pos):
    vectors = [(-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1)]
    moves = gen_absolute_moves(board, pos, vectors)
    return moves


def gen_bishop_moves(board, pos):
    vectors = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    moves = gen_sliding_moves(board, pos, vectors)
    return moves


def gen_rook_moves(board, pos):
    vectors = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    moves = gen_sliding_moves(board, pos, vectors)
    return moves


def gen_queen_moves(board, pos):
    return gen_bishop_moves(board, pos) + gen_rook_moves(board, pos)


def gen_king_moves(board, pos):
    vectors = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]
    moves = gen_absolute_moves(board, pos, vectors)
    return moves


def gen_piece_moves(board, pos, filter_illegal=True):
    moves = []

    if board.position[pos[1]][pos[0]][1] == 'p':
        moves = gen_pawn_moves(board, pos)
    elif board.position[pos[1]][pos[0]][1] == 'n':
        moves = gen_knight_moves(board, pos)
    elif board.position[pos[1]][pos[0]][1] == 'b':
        moves = gen_bishop_moves(board, pos)
    elif board.position[pos[1]][pos[0]][1] == 'r':
        moves = gen_rook_moves(board, pos)
    elif board.position[pos[1]][pos[0]][1] == 'q':
        moves = gen_queen_moves(board, pos)
    elif board.position[pos[1]][pos[0]][1] == 'k':
        moves = gen_king_moves(board, pos)

    if filter_illegal:
        colour = board.position[pos[1]][pos[0]][0]

        new_moves = []
        for move in moves:
            new_board = copy.deepcopy(board)
            new_board.make_move(move, gen_new_moves=False)
            if not in_check(new_board, colour):
                new_moves.append(move)

        return new_moves
    else:
        return moves
