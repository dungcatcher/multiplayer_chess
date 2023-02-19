import pygame
import socket
import pickle
from threading import Thread
from graphical_piece import load_piece_images, piece_images, GraphicalPiece
from packet import Packet

pygame.init()

HOST = "localhost"
PORT = 1194


class GameClient:
    def __init__(self):
        self.window = pygame.display.set_mode((960, 540))
        self.clock = pygame.time.Clock()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.colour = None
        self.game_id = None
        self.game = None

        self.orig_chessboard_img = pygame.image.load('../Assets/chessboard.png').convert_alpha()
        self.chessboard_img = pygame.transform.smoothscale(self.orig_chessboard_img, (480, 480))
        self.board_rect = self.chessboard_img.get_rect(center=(self.window.get_width() / 2, self.window.get_height() / 2))

        self.pieces = []
        load_piece_images()

        self.left_click = False

        self.selected_piece = None

        connection_thread = Thread(target=self.connect_with_server, daemon=True)
        connection_thread.start()

    def make_move(self, move):
        for piece in self.pieces:
            if piece.pos == move.start:
                if 'capture' in move.flags:
                    for captured in self.pieces:
                        if captured.pos == move.end:
                            self.pieces.remove(captured)
                piece.update_move(move, self.board_rect)

    def load_pieces(self):
        flipped = True if self.colour == 'b' else False
        for x in range(8):
            for y in range(8):
                if self.game.board.position[y][x] is not None:
                    piece_id = self.game.board.position[y][x]
                    new_piece = GraphicalPiece(piece_id, (x, y), self.board_rect, flipped)
                    new_piece.moves = self.game.board.fetch_moves_from_square((x, y))
                    self.pieces.append(new_piece)

    def update(self):
        while True:
            self.draw()

            mouse_x, mouse_y = pygame.mouse.get_pos()

            self.left_click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.left_click = True

            if self.game is not None:
                if self.left_click:
                    if self.selected_piece:
                        for move in self.selected_piece.moves:
                            if not self.selected_piece.flipped:
                                square_rect = pygame.Rect(self.board_rect.left + move.end[0] * 60,
                                                          self.board_rect.top + move.end[1] * 60, 60, 60)
                            else:
                                square_rect = pygame.Rect(self.board_rect.left + (7 - move.end[0]) * 60,
                                                          self.board_rect.top + (7 - move.end[1]) * 60, 60, 60)
                            if square_rect.collidepoint((mouse_x, mouse_y)):
                                self.selected_piece = None
                                move_data = {
                                    'game_id': self.game_id,
                                    'move': move
                                }
                                move_packet = Packet('update', 'move', move_data)
                                self.socket.sendall(pickle.dumps(move_packet))
                                break

                    for piece in self.pieces:
                        if piece.piece_id[0] == self.colour and self.colour == self.game.board.turn:
                            if piece.rect.collidepoint((mouse_x, mouse_y)):
                                self.selected_piece = piece

            pygame.display.update()

    def draw(self):
        self.window.fill((20, 20, 20))

        if self.game is not None:
            self.window.blit(self.chessboard_img, self.board_rect)

            if self.selected_piece is not None:
                for move in self.selected_piece.moves:
                    surf = pygame.Surface((60, 60), pygame.SRCALPHA, 32)
                    pygame.draw.circle(surf, (0, 0, 0, 128), (30, 30), 15)
                    if not self.selected_piece.flipped:
                        circle_rect = surf.get_rect(topleft=(self.board_rect.left + move.end[0] * 60, self.board_rect.top + move.end[1] * 60))
                    else:
                        circle_rect = surf.get_rect(topleft=(self.board_rect.left + (7 - move.end[0]) * 60, self.board_rect.top + (7 - move.end[1]) * 60))
                    self.window.blit(surf, circle_rect)

            for piece in self.pieces:
                piece.draw(self.window)

    def get_response(self):
        response = self.socket.recv(4096)
        response_object = pickle.loads(response)
        return response_object

    def connect_with_server(self):
        self.socket.connect((HOST, PORT))

        while True:
            response = self.get_response()
            if not response:
                break
            else:
                if response.type == 'initial':
                    self.colour = response.data['colour']
                    self.game_id = response.data['game_id']
                    self.game = pickle.loads(response.data['game'])

                    self.load_pieces()
                elif response.type == 'update':
                    if response.description == 'move':
                        print(response.data['game'])
                        self.game = response.data['game']
                        self.make_move(response.data['move'])

                        for piece in self.pieces:
                            piece.moves = self.game.board.fetch_moves_from_square(piece.pos)
