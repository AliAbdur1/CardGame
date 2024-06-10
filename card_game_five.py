import pygame
import sys
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 3
CARD_WIDTH = 100
CARD_HEIGHT = 150
BOARD_ORIGIN_X = (WINDOW_WIDTH - (GRID_SIZE * CARD_WIDTH)) // 2
BOARD_ORIGIN_Y = (WINDOW_HEIGHT - (GRID_SIZE * CARD_HEIGHT)) // 2
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)

# Set up display
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Triple Triad')
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
def initialize_board():
    global board, red_cards, blue_cards, dragging_card, current_team, player_team
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    red_cards = [Card('red') for _ in range(5)]
    blue_cards = [Card('blue') for _ in range(5)]
    for i, card in enumerate(red_cards):
        card.rect.topleft = (BOARD_ORIGIN_X - CARD_WIDTH * 1.5, BOARD_ORIGIN_Y + i * (CARD_HEIGHT // 2))
    for i, card in enumerate(blue_cards):
        card.rect.topleft = (BOARD_ORIGIN_X + GRID_SIZE * CARD_WIDTH + CARD_WIDTH // 2, BOARD_ORIGIN_Y + i * (CARD_HEIGHT // 2))
    dragging_card = None
    current_team = random.choice(['red', 'blue'])
    player_team = None

initialize_board()

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
    red_count, blue_count = 0, 0
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col]:
                x = BOARD_ORIGIN_X + col * CARD_WIDTH
                y = BOARD_ORIGIN_Y + row * CARD_HEIGHT
                board[row][col].rect.topleft = (x, y)
                board[row][col].draw(DISPLAYSURF)
                if board[row][col].team == 'red':
                    red_count += 1
                else:
                    blue_count += 1

    for card in red_cards:
        card.draw(DISPLAYSURF)
    for card in blue_cards:
        card.draw(DISPLAYSURF)

    # Draw the score indicators
    font = pygame.font.Font(None, 36)
    red_score_text = font.render(f'Red: {red_count}', True, RED)
    blue_score_text = font.render(f'Blue: {blue_count}', True, BLUE)
    DISPLAYSURF.blit(red_score_text, (BOARD_ORIGIN_X - CARD_WIDTH * 1.5, BOARD_ORIGIN_Y - 50))
    DISPLAYSURF.blit(blue_score_text, (BOARD_ORIGIN_X + GRID_SIZE * CARD_WIDTH + CARD_WIDTH // 2, BOARD_ORIGIN_Y - 50))

# Function to place a card on the board
def place_card(row, col, card):
    board[row][col] = card
    directions = [(-1, 0, 0, 1), (1, 0, 1, 0), (0, -1, 2, 3), (0, 1, 3, 2)]
    for dr, dc, s1, s2 in directions:
        r, c = row + dr, col + dc
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c]:
            if card.sides[s1] > board[r][c].sides[s2]:
                board[r][c].animate_color_change(card.team)

# Function to display the title screen
def show_title_screen():
    DISPLAYSURF.fill(GREY)
    font = pygame.font.Font(None, 74)
    text = font.render('AENOCH', True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    DISPLAYSURF.blit(text, text_rect)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                waiting = False

# Function to display the team selection screen
def show_team_selection_screen():
    DISPLAYSURF.fill(GREY)
    font = pygame.font.Font(None, 50)
    red_text = font.render('Red Team', True, RED)
    blue_text = font.render('Blue Team', True, BLUE)
    red_rect = red_text.get_rect(center=(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2))
    blue_rect = blue_text.get_rect(center=(3 * WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2))
    DISPLAYSURF.blit(red_text, red_rect)
    DISPLAYSURF.blit(blue_text, blue_rect)
    pygame.display.update()
    global player_team
    choosing = True
    while choosing:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if red_rect.collidepoint(event.pos):
                    player_team = 'red'
                    choosing = False
                elif blue_rect.collidepoint(event.pos):
                    player_team = 'blue'
                    choosing = False

# turn indicator
def display_current_player():
    font = pygame.font.Font(None, 36)
    current_player_text = font.render(f"Current Turn: {'Red' if current_team == 'red' else 'Blue'}", True, BLACK)
    DISPLAYSURF.blit(current_player_text, (BOARD_ORIGIN_X, WINDOW_HEIGHT - 50))
# turn indicator ^^

# Function to display the game over screen
def show_game_over_screen(winner):
    DISPLAYSURF.fill(GREY)
    font = pygame.font.Font(None, 74)
    text = font.render(f'{winner} Wins!', True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    DISPLAYSURF.blit(text, text_rect)

    font = pygame.font.Font(None, 50)
    new_game_text = font.render('New Game', True, GREEN)
    new_game_rect = new_game_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
    DISPLAYSURF.blit(new_game_text, new_game_rect)

    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if new_game_rect.collidepoint(event.pos):
                    initialize_board()
                    show_team_selection_screen()
                    waiting = False

# new addition vv
def is_board_full():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] is None:
                return False
    return True
# new addition ^^

# Main game loop
show_title_screen()
show_team_selection_screen()

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
    display_current_player()

    # Check for game over
    if is_board_full():
        red_count = sum(card.team == 'red' for row in board for card in row if card)
        blue_count = sum(card.team == 'blue' for row in board for card in row if card)
        if red_count > blue_count:
            winner = 'Red Team'
        elif blue_count > red_count:
            winner = 'Blue Team'
        else:
            winner = 'Draw'
        show_game_over_screen(winner)
    
    pygame.display.update()
    FPS_CLOCK.tick(FPS)
