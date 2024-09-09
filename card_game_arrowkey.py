import os
import pygame
import sys
import random
from pygame.locals import *

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)
# Initialize Pygame
pygame.init()
pygame.mixer.init()

current_volume = 0.5
pygame.mixer.music.set_volume(current_volume)
# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000
GRID_SIZE = 3
CARD_WIDTH = 160
CARD_HEIGHT = 225
BOARD_ORIGIN_X = (WINDOW_WIDTH - (GRID_SIZE * CARD_WIDTH)) // 2
BOARD_ORIGIN_Y = (WINDOW_HEIGHT - (GRID_SIZE * CARD_HEIGHT)) // 2
FPS = 30

# music btn rects v
#play & other btn imgs v
play_image = pygame.image.load('images/icons/play_btn.png')
play_image = pygame.transform.scale(play_image, (50, 50))
pause_image = pygame.image.load('images/icons/pause_btn.png')
pause_image = pygame.transform.scale(pause_image, (50, 50))
vol_up_img = pygame.image.load('images/icons/vol_up.png')
vol_up_img = pygame.transform.scale(vol_up_img, (50, 50))
vol_dn_img = pygame.image.load('images/icons/vol_dn.png')
vol_dn_img = pygame.transform.scale(vol_dn_img, (50, 50))
#play & other btn imgs ^

pause_button_rect = pygame.Rect(50, 50, 50, 50)  # Example for pause button
play_button_rect = pygame.Rect(120, 50, 50, 50)  # Example for play button
volume_up_rect = pygame.Rect(200, 50, 50, 50)    # Example for volume up button
volume_down_rect = pygame.Rect(280, 50, 50, 50)
# music btn rects ^

# Colors
TYPE_ON_CARDS = (247, 220, 210)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# RED = (255, 0, 0)
RED = (172, 19, 45) # pygame will accept HEX code for colors but this creates issue for color change animation function
YELLOW = (255, 255, 0)
BLUE = (19, 114, 172)
GREY = (200, 200, 200)
GREEN = (42, 197, 81)

# music v
pygame.mixer.music.load('music/9convert.com - Hades II  The Silver Sisters.mp3')  # Adjust to your file path
pygame.mixer.music.play(-1)  # Loop indefinitely
pygame.mixer.music.set_volume(0.5)
# music ^

# Set up display
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Triple Triad')
FPS_CLOCK = pygame.time.Clock()

# image import v
BORDER_IMAGE_PATH = "images/card/card_boarder_image.png"  # Replace with the path to your image file
BACKGROUND_forBoard_IMG_PATH = "images/backgrounds/depositphotos_1750670-stock-photo-zodiac-disc-gold.jpg" # path to bg
BACKGROUND_forTitle_and_GO_PATH = 'images/backgrounds/wheel-zodiac-signs-14292638.webp'
BACK_OF_A_CARD_path = 'images/card/back_of_card.jpg'

BOCard_Image = pygame.image.load(BACK_OF_A_CARD_path)
BOCard_Image = pygame.transform.scale(BOCard_Image, (CARD_WIDTH, CARD_HEIGHT))

BORDER_IMAGE = pygame.image.load(BORDER_IMAGE_PATH)
BORDER_IMAGE = pygame.transform.scale(BORDER_IMAGE, (CARD_WIDTH + 7, CARD_HEIGHT + 7))  # Adjust the size if necessary

BG_baord_IMAGE = pygame.image.load(BACKGROUND_forBoard_IMG_PATH) # loads in bg
BG_board_IMAGE = pygame.transform.scale(BG_baord_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT)) # scales bg to display size

BG_Title_GO_IMAGE = pygame.image.load(BACKGROUND_forTitle_and_GO_PATH)
BG_Title_GO_IMAGE = pygame.transform.scale(BG_Title_GO_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))
# image import ^

# Define the selection modes
DECK_SELECTION = 0
GRID_SELECTION = 1

# Start in deck selection mode
selection_mode = DECK_SELECTION

selected_card_index = 0
grid_row, grid_col = 0, 0



def fade_out(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill(BLACK)
    for alpha in range(0, 175):
        fade.set_alpha(alpha)
        # show_title_screen() # may need to change
        DISPLAYSURF.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(3)
        
    
def fade_in(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill(BLACK)
    for alpha in range(174, -1, -1):  # Start from 174 down to 0
        fade.set_alpha(alpha)
        DISPLAYSURF.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(3)
        


# new cards stuff v

TOTAL_CARDS = [
    [1, 2, 3, 4], [4, 3, 2, 1], [5, 5, 5, 5], [6, 6, 6, 6],
    [2, 3, 4, 5], [5, 4, 3, 2], [7, 7, 7, 7], [8, 8, 8, 8],
    [3, 4, 5, 6], [6, 5, 4, 3], [9, 9, 9, 9], [1, 1, 1, 1],
    [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4], [5, 5, 5, 5],
    [6, 6, 6, 6], [7, 7, 8, 7], [8, 8, 8, 8], [9, 9, 7, 9],
    [1, 2, 3, 4], [4, 3, 2, 1], [5, 6, 7, 8], [8, 7, 6, 5],
    [1, 1, 1, 9], [9, 1, 1, 1], [2, 2, 2, 8], [8, 2, 2, 2],
    [3, 3, 3, 7], [7, 3, 3, 3]
]

# Load images
def load_images():
    image_dict = {
        1: pygame.image.load('images/card/33774.png'),
        2: pygame.image.load('images/card/lion_hunter.png'),
        3: pygame.image.load('images/card/IMG_0946.png'),
        4: pygame.image.load('images/card/314293.png'),
        5: pygame.image.load('images/card/green_bat.png'),
        6: pygame.image.load('images/card/animal-monkey-silhouette-png.png'),
        7: pygame.image.load('images/card/IMG_0945.png'),
        8: pygame.image.load('images/card/314293.png'),
        9: pygame.image.load('images/card/33774.png'),
        10: pygame.image.load('images/card/green_bat.png'),
        11: pygame.image.load('images/card/IMG_0946.png'),
        12: pygame.image.load('images/card/314293.png'),
        13: pygame.image.load('images/card/green_bat.png'),
        14: pygame.image.load('images/card/green_bat.png'),
        15: pygame.image.load('images/card/green_bat.png'),
        16: pygame.image.load('images/card/314293.png'),
        17: pygame.image.load('images/card/IMG_0949.png'),
        18: pygame.image.load('images/card/animal-monkey-silhouette-png.png'),
        19: pygame.image.load('images/card/simple-bird-flying-silhouette-08e636.webp'),
        20: pygame.image.load('images/card/314293.png'),
        21: pygame.image.load('images/card/green_bat.png'),
        22: pygame.image.load('images/card/lion_hunter.png'),
        23: pygame.image.load('images/card/IMG_0946.png'),
        24: pygame.image.load('images/card/314293.png'),
        25: pygame.image.load('images/card/IMG_0949.png'),
        26: pygame.image.load('images/card/lion_hunter.png'),
        27: pygame.image.load('images/card/IMG_0946.png'),
        28: pygame.image.load('images/card/314293.png'),
        29: pygame.image.load('images/card/33774.png'),
        30: pygame.image.load('images/card/green_bat.png'),
        # Add paths for all necessary images
    }
    for key in image_dict:
        image_dict[key] = pygame.transform.scale(image_dict[key], (CARD_WIDTH, CARD_HEIGHT))
    return image_dict

images = load_images()


class Card:
    def __init__(self, team, sides, image):
        self.team = team
        self.sides = sides  # top, bottom, left, right
        self.color = RED if team == 'red' else BLUE
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)
        self.border_image = BORDER_IMAGE
        self.image = image

    def draw(self, surface):
        # Draw border image
        border_rect = self.border_image.get_rect(topleft=(self.rect.x - 3, self.rect.y - 3))  # Adjust offset to center the border
        surface.blit(self.border_image, border_rect)

        # Draw card
        pygame.draw.rect(surface, self.color, self.rect)

        if self.image:
            image_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, image_rect)

        font = pygame.font.Font('fonts/old_celtiberian/Old Celtiberians.otf', 25) # was None
        nums = [(self.rect.x + CARD_WIDTH // 2, self.rect.y + 5),
                (self.rect.x + CARD_WIDTH // 2, self.rect.y + CARD_HEIGHT - 25),
                (self.rect.x + 5, self.rect.y + CARD_HEIGHT // 2),
                (self.rect.x + CARD_WIDTH - 25, self.rect.y + CARD_HEIGHT // 2)]
        for num, pos in zip(self.sides, nums):
            text = font.render(str(num), True, TYPE_ON_CARDS)
            text_rect = text.get_rect(center=pos)
            surface.blit(text, text_rect)

    def animate_color_change(self, new_team):
        old_color = self.color
        new_color = RED if new_team == 'red' else BLUE
        for i in range(24):
            ratio = i / 23
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

#zigzag start
def initialize_board():
    global board, red_cards, blue_cards, dragging_card, current_team, player_team
    random.shuffle(TOTAL_CARDS)
    red_cards_data = TOTAL_CARDS[:5]
    blue_cards_data = TOTAL_CARDS[5:10]
    
    red_cards = [Card('red', sides, images[sides[0]]) for sides in red_cards_data]
    blue_cards = [Card('blue', sides, images[sides[0]]) for sides in blue_cards_data]
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    # red_cards = [Card('red') for _ in range(5)]
    # blue_cards = [Card('blue') for _ in range(5)]

    # Zigzag pattern for red cards
    for i, card in enumerate(red_cards):
        x_offset = -CARD_WIDTH * 1.5 + (i % 2) * -60  # Adjust the x offset to create the zigzag
        y_offset = BOARD_ORIGIN_Y + i * (CARD_HEIGHT // 2) * 1.1
        card.rect.topleft = (BOARD_ORIGIN_X + x_offset, y_offset)

    # Zigzag pattern for blue cards
    for i, card in enumerate(blue_cards):
        x_offset = GRID_SIZE * CARD_WIDTH + CARD_WIDTH // 2 + (i % 2) * 60  # Adjust the x offset to create the zigzag
        y_offset = BOARD_ORIGIN_Y + i * (CARD_HEIGHT // 2) * 1.1
        card.rect.topleft = (BOARD_ORIGIN_X + x_offset, y_offset)

    dragging_card = None
    current_team = random.choice(['red', 'blue'])
    player_team = None
#zig zag end

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
    DISPLAYSURF.blit(BG_board_IMAGE, (0,0))
    # music buttons V
    DISPLAYSURF.blit(pause_image, pause_button_rect.topleft)  # Pause button
    DISPLAYSURF.blit(play_image, play_button_rect.topleft)    # Play button
    DISPLAYSURF.blit(vol_up_img, volume_up_rect.topleft) # Volume up button
    DISPLAYSURF.blit(vol_dn_img, volume_down_rect.topleft) # Volume down button
    # music buttons ^
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

    # Draw the mode indicators
    font = pygame.font.Font(None, 25)
    same_mode_text = font.render(f'Same Mode: {"ON" if same_mode_enabled else "OFF"}', True, BLACK)
    plus_mode_text = font.render(f'Plus Mode: {"ON" if plus_mode_enabled else "OFF"}', True, BLACK)
    DISPLAYSURF.blit(same_mode_text, (10, 900)) # sets position of the same mode rect on dsiplay
    DISPLAYSURF.blit(plus_mode_text, (10, 930)) # sets position of the plus mode rect on dsiplay
    

# Function to place a card on the board
def place_card(row, col, card):
    # Place the card on the board at the specified row and column
    board[row][col] = card
    
    # Directions list to check for adjacent cards
    # Format: (row offset, column offset, side index of placed card, side index of adjacent card)
    directions = [(-1, 0, 0, 1),  # Upwards (top side of the placed card)
                  (1, 0, 1, 0),   # Downwards (bottom side of the placed card)
                  (0, -1, 2, 3),  # Left (left side of the placed card)
                  (0, 1, 3, 2)]   # Right (right side of the placed card)
    
    # Loop through each direction to check adjacent cards
    for dr, dc, s1, s2 in directions:
        # Calculate the position of the adjacent card
        r, c = row + dr, col + dc
        
        # Check if the adjacent position is within bounds and has a card
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c]:
            # If the side of the placed card is stronger than the adjacent card's side
            if card.sides[s1] > board[r][c].sides[s2]:
                # Flip the adjacent card to the team of the placed card
                board[r][c].animate_color_change(card.team)
    
    # "Same" rule check
    if same_mode_enabled:
        # List to keep track of adjacent cards with the same value
        same_adjacent = []
        
        # Loop through each direction to check adjacent cards for the "Same" rule
        for dr, dc, s1, s2 in directions:
            # Calculate the position of the adjacent card
            r, c = row + dr, col + dc
            
            # Check if the adjacent position is within bounds and has a card
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c]:
                # If the side of the placed card is equal to the adjacent card's side
                if card.sides[s1] == board[r][c].sides[s2]:
                    # Add the adjacent card to the same_adjacent list
                    same_adjacent.append((r, c))
        
        # If there are two or more adjacent cards with the same value
        if len(same_adjacent) >= 2:
            # Flip all the adjacent cards with the same value to the team of the placed card
            for r, c in same_adjacent:
                board[r][c].animate_color_change(card.team)
    
    # "Plus" rule check
    if plus_mode_enabled:
        # List to keep track of adjacent cards satisfying the "Plus" rule
        plus_adjacent = []
        
        # Loop through each pair of directions to check for the "Plus" rule
        for i, (dr1, dc1, s1a, s2a) in enumerate(directions):
            # Calculate the position of the first adjacent card
            r1, c1 = row + dr1, col + dc1
            
            for j, (dr2, dc2, s1b, s2b) in enumerate(directions):
                # Ensure that the two directions are different
                if i != j:
                    # Calculate the position of the second adjacent card
                    r2, c2 = row + dr2, col + dc2
                    
                    # Check if both adjacent positions are within bounds and have cards
                    if (0 <= r1 < GRID_SIZE and 0 <= c1 < GRID_SIZE and 
                        0 <= r2 < GRID_SIZE and 0 <= c2 < GRID_SIZE and 
                        board[r1][c1] and board[r2][c2]):
                        
                        # If the sum of the sides of the placed card and the first adjacent card
                        # equals the sum of the sides of the placed card and the second adjacent card
                        if card.sides[s1a] + board[r1][c1].sides[s2a] == card.sides[s1b] + board[r2][c2].sides[s2b]:
                            # Add both adjacent cards to the plus_adjacent list
                            plus_adjacent.append((r1, c1))
                            plus_adjacent.append((r2, c2))
        
        # If the "Plus" rule condition is met
        if plus_adjacent:
            # Flip all the adjacent cards that satisfy the "Plus" rule to the team of the placed card
            for r, c in plus_adjacent:
                board[r][c].animate_color_change(card.team)


# Function to display the title screen
def show_title_screen():
    DISPLAYSURF.blit(BG_Title_GO_IMAGE, (0,0))
    font = pygame.font.Font('fonts/stencil_gothic/Gothic Stencil - Dker.ttf', 74)
    text = font.render('Triple Triad', True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    DISPLAYSURF.blit(text, text_rect)

    font = pygame.font.Font('fonts/adon/Adon Black.otf', 50)
    text = font.render('Press any key to start', True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
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

    fade_out(WINDOW_WIDTH, WINDOW_HEIGHT)
    

    

# Function to display the team selection screen with "Same" and "Plus" mode options
def show_team_selection_screen():
    
    DISPLAYSURF.blit(BG_Title_GO_IMAGE, (0, 0))
    font = pygame.font.Font('fonts/adon/Adon Black.otf', 40)
    red_text = font.render('Red Team', True, RED)
    blue_text = font.render('Blue Team', True, BLUE)
    red_rect = red_text.get_rect(center=(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2))
    blue_rect = blue_text.get_rect(center=(3 * WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2))
    same_mode_text = font.render('Same Mode: OFF', True, BLACK)
    same_mode_rect = same_mode_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
    plus_mode_text = font.render('Plus Mode: OFF', True, BLACK)
    plus_mode_rect = plus_mode_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150))
    DISPLAYSURF.blit(red_text, red_rect)
    DISPLAYSURF.blit(blue_text, blue_rect)
    DISPLAYSURF.blit(same_mode_text, same_mode_rect)
    DISPLAYSURF.blit(plus_mode_text, plus_mode_rect)
    pygame.display.update()
    
    global player_team, same_mode_enabled, plus_mode_enabled
    choosing = True
    same_mode_enabled = False
    plus_mode_enabled = False
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
                elif same_mode_rect.collidepoint(event.pos):
                    same_mode_enabled = not same_mode_enabled
                    same_mode_text = font.render(f'Same Mode: {"ON" if same_mode_enabled else "OFF"}', True, BLACK)
                elif plus_mode_rect.collidepoint(event.pos):
                    plus_mode_enabled = not plus_mode_enabled
                    plus_mode_text = font.render(f'Plus Mode: {"ON" if plus_mode_enabled else "OFF"}', True, BLACK)
                    
                DISPLAYSURF.blit(BG_Title_GO_IMAGE, (0, 0))
                DISPLAYSURF.blit(red_text, red_rect)
                DISPLAYSURF.blit(blue_text, blue_rect)
                DISPLAYSURF.blit(same_mode_text, same_mode_rect)
                DISPLAYSURF.blit(plus_mode_text, plus_mode_rect)
                pygame.display.update()

    fade_out(WINDOW_WIDTH, WINDOW_HEIGHT)

# Turn indicator
def display_current_player():
    font = pygame.font.Font('fonts/aesthico/Aesthico(Demo)-Regular.ttf', 20)
    current_player_text = font.render(f"Current Turn: {'Red' if current_team == 'red' else 'Blue'}", True, BLACK)
    DISPLAYSURF.blit(current_player_text, (BOARD_ORIGIN_X, WINDOW_HEIGHT - 50))

# Function to display the game over screen
def show_game_over_screen(winner):
    DISPLAYSURF.fill(GREY)
    font = pygame.font.Font('fonts/aesthico/Aesthico(Demo)-Regular.ttf', 60)
    text = font.render(f'{winner} Wins!', True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    DISPLAYSURF.blit(text, text_rect)

    font = pygame.font.Font('fonts/adon/Adon Black.otf', 50)
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
                    fade_out(WINDOW_WIDTH, WINDOW_HEIGHT) # proper place for fade out in game over screen
                    initialize_board()
                    show_team_selection_screen()
                    waiting = False

    

# Check if the board is full
def is_board_full():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] is None:
                return False
    return True

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

            # Handle pause/play/volume controls for music...
            if pause_button_rect.collidepoint(mouse_x, mouse_y):
                pygame.mixer.music.pause()
            elif play_button_rect.collidepoint(mouse_x, mouse_y):
                pygame.mixer.music.unpause()
            elif volume_up_rect.collidepoint(mouse_x, mouse_y):
                current_volume = min(1.0, current_volume + 0.1)
                pygame.mixer.music.set_volume(current_volume)
            elif volume_down_rect.collidepoint(mouse_x, mouse_y):
                current_volume = max(0.0, current_volume - 0.1)
                pygame.mixer.music.set_volume(current_volume)

            # Handle card dragging if no music button is clicked
            else:
                if current_team == 'red':
                    for card in red_cards:
                        if card.rect.collidepoint(event.pos):
                            dragging_card = card
                            # Define drag offsets when the card is clicked
                            drag_offset_x = card.rect.x - mouse_x
                            drag_offset_y = card.rect.y - mouse_y
                            break
                else:
                    for card in blue_cards:
                        if card.rect.collidepoint(event.pos):
                            dragging_card = card
                            # Define drag offsets when the card is clicked
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
                # Update the position of the card based on the drag offsets
                dragging_card.rect.topleft = (mouse_x + drag_offset_x, mouse_y + drag_offset_y)

        # Handle arrow key navigation
        elif event.type == KEYDOWN:
            # Determine the deck based on the current team
            deck = red_cards if current_team == 'red' else blue_cards

            if selection_mode == DECK_SELECTION:
                # Navigate through the deck with arrow keys
                if event.key == pygame.K_UP or event.key == pygame.K_LEFT:  # Move up/left in the deck
                    selected_card_index = (selected_card_index - 1) % len(deck)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:  # Move down/right in the deck
                    selected_card_index = (selected_card_index + 1) % len(deck)

                # When Enter or Space is pressed, select the card and switch to grid selection mode
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    selected_card = deck[selected_card_index]
                    selection_mode = GRID_SELECTION  # Switch to grid selection

            elif selection_mode == GRID_SELECTION:
                # Navigate through the grid with arrow keys
                if event.key == pygame.K_UP:  # Move up on the grid
                    grid_row = max(0, grid_row - 1)
                elif event.key == pygame.K_DOWN:  # Move down on the grid
                    grid_row = min(GRID_SIZE - 1, grid_row + 1)
                elif event.key == pygame.K_LEFT:  # Move left on the grid
                    grid_col = max(0, grid_col - 1)
                elif event.key == pygame.K_RIGHT:  # Move right on the grid
                    grid_col = min(GRID_SIZE - 1, grid_col + 1)

                # Place the selected card using Enter or Space, then switch back to deck selection mode
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if board[grid_row][grid_col] is None:
                        place_card(grid_row, grid_col, selected_card)
                        deck.remove(selected_card)
                        current_team = 'blue' if current_team == 'red' else 'red'
                        selected_card_index = 0  # Reset selected index
                        selection_mode = DECK_SELECTION  # Switch back to deck selection mode

    # ---- Drawing Section ----
    DISPLAYSURF.fill(BLACK)  # Clear the screen with a background color (BLACK)

    # Draw the game board first
    draw_board()

    if selection_mode == GRID_SELECTION:
        # Highlight the current grid cell for card placement
        pygame.draw.rect(DISPLAYSURF, YELLOW, 
                         (BOARD_ORIGIN_X + grid_col * CARD_WIDTH, BOARD_ORIGIN_Y + grid_row * CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT), 3)

    # Draw the deck of cards for the current player (either red or blue team)
    for card in red_cards:
        card.draw(DISPLAYSURF)  # Draw all red team cards
    for card in blue_cards:
        card.draw(DISPLAYSURF)  # Draw all red team cards

    if selection_mode == DECK_SELECTION:
        # Highlight the currently selected card in the deck
        selected_card = red_cards[selected_card_index] if current_team == 'red' else blue_cards[selected_card_index]
        pygame.draw.rect(DISPLAYSURF, YELLOW, selected_card.rect.inflate(10, 10), 3)  # Draw yellow border around selected card


    # Draw the current player
    display_current_player()

    # Check for game over
    if is_board_full():
        pygame.display.update()
        pygame.time.delay(1000)  # 2-second delay
        fade_out(WINDOW_WIDTH, WINDOW_HEIGHT)

        red_count = sum(card.team == 'red' for row in board for card in row if card)
        blue_count = sum(card.team == 'blue' for row in board for card in row if card)
        if red_count > blue_count:
            winner = 'Red Team'
        elif blue_count > red_count:
            winner = 'Blue Team'
        else:
            winner = 'Draw'
        show_game_over_screen(winner)

    # Refresh the display
    pygame.display.update()
    FPS_CLOCK.tick(FPS)
