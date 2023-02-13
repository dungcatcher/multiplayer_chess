from move import Move


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


def gen_piece_moves(board, pos):
    if board.position[pos[1]][pos[0]][1] == 'p':
        return gen_pawn_moves(board, pos)
    elif board.position[pos[1]][pos[0]][1] == 'n':
        return gen_knight_moves(board, pos)
    elif board.position[pos[1]][pos[0]][1] == 'b':
        return gen_bishop_moves(board, pos)
    elif board.position[pos[1]][pos[0]][1] == 'r':
        return gen_rook_moves(board, pos)
    elif board.position[pos[1]][pos[0]][1] == 'q':
        return gen_queen_moves(board, pos)
    elif board.position[pos[1]][pos[0]][1] == 'k':
        return gen_king_moves(board, pos)


