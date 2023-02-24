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

        self.clients = []
        self.queueing = []
        self.games = {}
        self.game_id_players = {}  # game_id: [players]

        connection_thread = Thread(target=self.handle_connections, daemon=True)
        connection_thread.start()

    def get_response(self, socket):
        response = socket.recv(4096)
        response_object = pickle.loads(response)
        return response_object

    def update(self):
        while True:
            if len(self.queueing) >= 2:  # Match making
                white_player = self.queueing[0]
                opponent = self.queueing[1]

                new_game_id = self.gen_game_id()
                new_game = Game()
                self.games[new_game_id] = new_game

                self.game_id_players[new_game_id] = [white_player, opponent]
                reference_queuer_data = {
                    "colour": "w",
                    "game_id": new_game_id,
                    "game": pickle.dumps(new_game)
                }
                reference_queuer_packet = Packet('initial', None, reference_queuer_data)
                white_player.sendall(pickle.dumps(reference_queuer_packet))

                opponent_queuer_data = {
                    "colour": "b",
                    "game_id": new_game_id,
                    "game": pickle.dumps(new_game)
                }
                opponent_queuer_packet = Packet('initial', None, opponent_queuer_data)
                opponent.sendall(pickle.dumps(opponent_queuer_packet))

                self.queueing.remove(white_player)
                self.queueing.remove(opponent)

    def handle_connections(self):
        self.socket.listen()
        while True:
            conn, addr = self.socket.accept()
            print(f'{addr} has connected!')
            client_thread = Thread(target=self.client_handler, args=(conn, addr), daemon=True)
            client_thread.start()

    def gen_game_id(self):
        while True:
            new_game_id = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=6))
            if new_game_id not in self.games.keys():
                return new_game_id

    def client_handler(self, client_socket, addr):
        self.clients.append(client_socket)
        self.queueing.append(client_socket)

        while True:
            response = self.get_response(client_socket)
            if not response:
                break
            else:
                if response.type == 'update':
                    if response.description == 'move':
                        game_id = response.data['game_id']
                        move = response.data['move']
                        self.games[game_id].board.make_move(move)

                        update_data = {
                            'move': move,
                            'game': self.games[game_id]
                        }
                        update_packet = Packet('update', 'move', update_data)
                        for player in self.game_id_players[game_id]:
                            player.sendall(pickle.dumps(update_packet))
