import pygame
import socket
import pickle
from threading import Thread
from graphical_piece import load_piece_images, piece_images, GraphicalPiece

pygame.init()

HOST = "10.0.0.105"
PORT = 65431


class GameClient:
    def __init__(self):
        self.window = pygame.display.set_mode((960, 540))
        self.clock = pygame.time.Clock()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.colour = None
        self.game_id = None
        self.board = None

        self.orig_chessboard_img = pygame.image.load('../Assets/chessboard.png').convert_alpha()
        self.chessboard_img = pygame.transform.smoothscale(self.orig_chessboard_img, (480, 480))
        self.board_rect = self.chessboard_img.get_rect(center=(self.window.get_width() / 2, self.window.get_height() / 2))

        self.pieces = []
        load_piece_images()

        connection_thread = Thread(target=self.connect_with_server, daemon=True)
        connection_thread.start()

    def load_pieces(self):
        for x in range(8):
            for y in range(8):
                if self.board.position[y][x] is not None:
                    piece_id = self.board.position[y][x]
                    new_piece = GraphicalPiece(piece_id, (x, y), self.board_rect)
                    self.pieces.append(new_piece)

    def update(self):
        while True:
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.update()

    def draw(self):
        self.window.fill((20, 20, 20))

        if self.board is not None:
            self.window.blit(self.chessboard_img, self.board_rect)

            for piece in self.pieces:
                piece.draw(self.window)

    def get_response(self):
        response = self.socket.recv(4096)
        response_object = pickle.loads(response)
        return response_object

    def connect_with_server(self):
        self.socket.connect((HOST, PORT))
        response = self.get_response()
        if response.type == 'initial':
            self.colour = response.data['colour']
            self.game_id = response.data['game_id']
            self.board = pickle.loads(response.data['board'])
            
            self.load_pieces()

        while True:
            response = self.get_response()
            if not response:
                break
            else:
                print(response)
