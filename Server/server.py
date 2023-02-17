import socket
from threading import Thread
from packet import Packet
from game import Game
import pickle
import random
import string

HOST = "localhost"
PORT = 1194


class GameServer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        print('Server has started, waiting for clients...')

        self.clients = set()
        self.games = {}
        self.game_id_players = {}  # game_id: [players]

        connection_thread = Thread(target=self.handle_connections, daemon=True)
        connection_thread.start()

    def update(self):
        while True:
            pass

    def handle_connections(self):
        self.socket.listen()
        while True:
            conn, addr = self.socket.accept()
            print(f'{addr} has connected!')
            client_thread = Thread(target=self.client_handler, args=(conn, addr), daemon=True)
            client_thread.start()

    def gen_game_id(self):
        while True:
            new_game_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if new_game_id not in self.games.keys():
                return new_game_id

    def client_handler(self, client_socket, addr):
        self.clients.add(client_socket)
        client_assigned_game = None

        if self.games:
            for game_id, game in self.games.items():  # Search for games waiting for an opponent
                if game.status == 'waiting':
                    client_assigned_game = game_id
                    game.status = 'playing'
        else:
            new_game_id = self.gen_game_id()
            new_game = Game()
            self.games[new_game_id] = new_game
            client_assigned_game = new_game_id

        # Initial data
        if len(self.clients) == 1:
            colour = "white"
        else:
            colour = "black"

        initial_data = {
            "colour": colour,
            "game_id": client_assigned_game,
            "game": pickle.dumps(self.games[client_assigned_game])
        }

        if client_assigned_game not in self.game_id_players:
            self.game_id_players[client_assigned_game] = [client_socket]
        else:
            self.game_id_players[client_assigned_game].append(client_socket)

        initial_data_packet = Packet('initial', None, initial_data)
        serialized_data_packet = pickle.dumps(initial_data_packet)

        for client in self.game_id_players[client_assigned_game]:
            client.sendall(serialized_data_packet)
