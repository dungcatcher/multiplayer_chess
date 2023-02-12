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
        pass


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
                    moves.append(Move(pos, test_square, flags=['double push']))

    capture_vectors = [(-1, direction), (1, direction)]
    for vector in capture_vectors:
        test_square = (pos[0] + vector[0], pos[1] + vector[1])
        if 0 <= test_square[0] <= 7 and 0 <= test_square[1] <= 7:
            if board.position[test_square[1]][test_square[0]][0] != colour:
                moves.append(Move(pos, test_square, flags=["capture"]))

    return moves


def gen_knight_moves(board, pos):
    vectors = [(-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1)]
    moves = gen_absolute_moves(board, pos, vectors)
    return moves


def gen_piece_moves(board, pos):
    if board.position[pos[1]][pos[0]][1] == 'p':
        gen_pawn_moves(board, pos)
    elif board.position[pos[1]][pos[0]][1] == 'n':
        gen_knight_moves(board, pos)
    elif board.position[pos[1]][pos[0]][1] == 'b':
        gen_knight_moves(board, pos)