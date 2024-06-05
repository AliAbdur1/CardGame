import pygame
import sys
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800  # Increased to fit team card areas
WINDOW_HEIGHT = 600  # Adjust height to fit the whole board properly
GRID_SIZE = 3
CARD_WIDTH = 70  # Card width for rectangle shape
CARD_HEIGHT = 100  # Card height for rectangle shape
BOARD_ORIGIN_X = (WINDOW_WIDTH - (GRID_SIZE * CARD_WIDTH)) // 2
BOARD_ORIGIN_Y = (WINDOW_HEIGHT - (GRID_SIZE * CARD_HEIGHT)) // 2
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)

# Set up display
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Card Game')
FPS_CLOCK = pygame.time.Clock()

# Card class
class Card:
    def __init__(self, team):
        self.team = team
        self.sides = [random.randint(1, 9) for _ in range(4)]  # top, bottom, left, right
        self.color = RED if team == 'red' else BLUE
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 24)
        # Draw the numbers on the card
        nums = [(self.rect.x + CARD_WIDTH // 2, self.rect.y + 5), 
                (self.rect.x + CARD_WIDTH // 2, self.rect.y + CARD_HEIGHT - 25), 
                (self.rect.x + 5, self.rect.y + CARD_HEIGHT // 2), 
                (self.rect.x + CARD_WIDTH - 25, self.rect.y + CARD_HEIGHT // 2)]
        for num, pos in zip(self.sides, nums):
            text = font.render(str(num), True, WHITE)
            text_rect = text.get_rect(center=pos)
            surface.blit(text, text_rect)

    def animate_color_change(self, new_team):
        old_color = self.color
        new_color = RED if new_team == 'red' else BLUE
        for i in range(30):  # Simple transition animation
            ratio = i / 29
            self.color = (
                int(old_color[0] * (1 - ratio) + new_color[0] * ratio),
                int(old_color[1] * (1 - ratio) + new_color[1] * ratio),
                int(old_color[2] * (1 - ratio) + new_color[2] * ratio)
            )
            draw_board()
            pygame.display.update()
            FPS_CLOCK.tick(FPS)
        self.team = new_team
        self.color = new_color

# Initialize board
board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_team = 'red'

# Generate cards for each team
red_cards = [Card('red') for _ in range(5)]
blue_cards = [Card('blue') for _ in range(5)]
for i, card in enumerate(red_cards):
    card.rect.topleft = (BOARD_ORIGIN_X - CARD_WIDTH * 1.5, BOARD_ORIGIN_Y + i * (CARD_HEIGHT // 2))
for i, card in enumerate(blue_cards):
    card.rect.topleft = (BOARD_ORIGIN_X + GRID_SIZE * CARD_WIDTH + CARD_WIDTH // 2, BOARD_ORIGIN_Y + i * (CARD_HEIGHT // 2))

dragging_card = None
drag_offset_x = 0
drag_offset_y = 0

# Function to draw the grid
def draw_grid():
    for x in range(GRID_SIZE + 1):
        pygame.draw.line(DISPLAYSURF, BLACK, 
                         (BOARD_ORIGIN_X + x * CARD_WIDTH, BOARD_ORIGIN_Y), 
                         (BOARD_ORIGIN_X + x * CARD_WIDTH, BOARD_ORIGIN_Y + GRID_SIZE * CARD_HEIGHT))
    for y in range(GRID_SIZE + 1):
        pygame.draw.line(DISPLAYSURF, BLACK, 
                         (BOARD_ORIGIN_X, BOARD_ORIGIN_Y + y * CARD_HEIGHT), 
                         (BOARD_ORIGIN_X + GRID_SIZE * CARD_WIDTH, BOARD_ORIGIN_Y + y * CARD_HEIGHT))

# Function to draw the board
def draw_board():
    DISPLAYSURF.fill(GREY)
    draw_grid()
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col]:
                x = BOARD_ORIGIN_X + col * CARD_WIDTH
                y = BOARD_ORIGIN_Y + row * CARD_HEIGHT
                board[row][col].rect.topleft = (x, y)
                board[row][col].draw(DISPLAYSURF)

    for card in red_cards:
        card.draw(DISPLAYSURF)
    for card in blue_cards:
        card.draw(DISPLAYSURF)

# Function to place a card on the board
def place_card(row, col, card):
    board[row][col] = card
    # Check and flip adjacent cards based on new x, -x, y, -y logic
    directions = [(-1, 0, 0, 1), (1, 0, 1, 0), (0, -1, 2, 3), (0, 1, 3, 2)]
    for dr, dc, s1, s2 in directions:
        r, c = row + dr, col + dc
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c]:
            if card.sides[s1] > board[r][c].sides[s2]:
                board[r][c].animate_color_change(card.team)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if current_team == 'red':
                for card in red_cards:
                    if card.rect.collidepoint(event.pos):
                        dragging_card = card
                        drag_offset_x = card.rect.x - mouse_x
                        drag_offset_y = card.rect.y - mouse_y
                        break
            else:
                for card in blue_cards:
                    if card.rect.collidepoint(event.pos):
                        dragging_card = card
                        drag_offset_x = card.rect.x - mouse_x
                        drag_offset_y = card.rect.y - mouse_y
                        break
        elif event.type == MOUSEBUTTONUP:
            if dragging_card:
                mouse_x, mouse_y = event.pos
                row = (mouse_y - BOARD_ORIGIN_Y) // CARD_HEIGHT
                col = (mouse_x - BOARD_ORIGIN_X) // CARD_WIDTH
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and board[row][col] is None:
                    place_card(row, col, dragging_card)
                    if dragging_card in red_cards:
                        red_cards.remove(dragging_card)
                    if dragging_card in blue_cards:
                        blue_cards.remove(dragging_card)
                    current_team = 'blue' if current_team == 'red' else 'red'
                dragging_card = None
        elif event.type == MOUSEMOTION:
            if dragging_card:
                mouse_x, mouse_y = event.pos
                dragging_card.rect.topleft = (mouse_x + drag_offset_x, mouse_y + drag_offset_y)
    
    draw_board()
    pygame.display.update()
    FPS_CLOCK.tick(FPS)
