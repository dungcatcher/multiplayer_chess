import pygame


def get_image_at(image, rect):
    surface = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
    surface.blit(image, (0, 0), rect)
    return surface


piece_images = {}


def load_piece_images():
    orig_chess_sprites = pygame.image.load('../Assets/chess_sprites.png').convert_alpha()
    chess_sprites = pygame.transform.smoothscale(orig_chess_sprites, (360, 120))

    piece_letters = ['q', 'k', 'r', 'n', 'b', 'p']
    colours = ['b', 'w']

    for x, letter in enumerate(piece_letters):
        for y, colour in enumerate(colours):
            piece_image = get_image_at(chess_sprites, pygame.Rect(x * 60, y * 60, 60, 60))
            piece_images[colour + letter] = piece_image


class GraphicalPiece:
    def __init__(self, piece_id, pos, board_rect):
        self.image = piece_images[piece_id]
        self.pos = pos
        self.rect = self.image.get_rect(center=(board_rect.left + 60 * pos[0] + 30, board_rect.top + 60 * pos[1] + 30))

    def draw(self, window):
        window.blit(self.image, self.rect)
