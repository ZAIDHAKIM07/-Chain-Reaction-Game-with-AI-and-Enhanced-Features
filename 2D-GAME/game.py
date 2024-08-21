#   Author: Catherine Leung
#   This is the game that you will code the bots to play.  You can also play against your bot
#   To run the game you will need pygames installed.  See: https://pypi.org/project/pygame/
#   Once you have pygames, you can run the game by using the command:
#   python game.py
#   
#   the gem images used are from opengameart.org by qubodup
#   https://opengameart.org/content/rotating-crystal-animation-8-step,
#   https://creativecommons.org/licenses/by/3.0/

import pygame
import sys
import math

from a1_partd import overflow
from a1_partc import Queue
from player1 import PlayerOne
from player2 import PlayerTwo

# Function to create a deep copy of the board
def copy_board(board):
    """
    Create a deep copy of the game board.

    Parameters:
    board (list of list of int): The game board to copy.

    Returns:
    list of list of int: A deep copy of the board.
    """
    current_board = []
    for row in board:
        current_board.append(row.copy())
    return current_board

# Button class to manage UI buttons
class Button:
    def __init__(self, x, y, width, height, text):
        """
        Initialize a Button object.

        Parameters:
        x (int): The x-coordinate of the button.
        y (int): The y-coordinate of the button.
        width (int): The width of the button.
        height (int): The height of the button.
        text (str): The text to display on the button.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.color = (0, 0, 0)
        self.bg_color = (200, 200, 200)

    def draw(self, window):
        """
        Draw the button on the given window.

        Parameters:
        window (pygame.Surface): The window to draw the button on.
        """
        pygame.draw.rect(window, self.bg_color, self.rect)
        pygame.draw.rect(window, self.color, self.rect, 2)
        text_surf = self.font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        window.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """
        Check if the button was clicked.

        Parameters:
        event (pygame.event.Event): The event to check.

        Returns:
        bool: True if the button was clicked, False otherwise.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Dropdown:
    def __init__(self, x, y, width, height, options):
        """
        Initialize a Dropdown object.

        Parameters:
        x (int): The x-coordinate of the dropdown.
        y (int): The y-coordinate of the dropdown.
        width (int): The width of the dropdown.
        height (int): The height of the dropdown.
        options (list of str): The list of options for the dropdown.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.current_option = 0

    def draw(self, window):
        """
        Draw the dropdown on the given window.

        Parameters:
        window (pygame.Surface): The window to draw the dropdown on.
        """
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height), 2)
        font = pygame.font.Font(None, 36)
        text = font.render(self.options[self.current_option], 1, BLACK)
        window.blit(text, (self.x + 5, self.y + 5))

    def handle_event(self, event):
        """
        Handle events for the dropdown (e.g., selecting an option).

        Parameters:
        event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
                self.current_option = (self.current_option + 1) % len(self.options)

    def get_choice(self):
        """
        Get the currently selected option index.

        Returns:
        int: The index of the currently selected option.
        """
        return self.current_option

class Board:
    def __init__(self, width, height, p1_sprites, p2_sprites):
        """
        Initialize the game board.

        Parameters:
        width (int): The width of the board.
        height (int): The height of the board.
        p1_sprites (list of pygame.Surface): The list of sprites for player 1.
        p2_sprites (list of pygame.Surface): The list of sprites for player 2.
        """
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.p1_sprites = p1_sprites
        self.p2_sprites = p2_sprites
        self.board[0][0] = 1
        self.board[self.height - 1][self.width - 1] = -1
        self.turn = 0
        self.history = []  # Stack to keep track of game states

    def get_board(self):
        """
        Get the current state of the game board.

        Returns:
        list of list of int: The current state of the board.
        """
        current_board = []
        for i in range(self.height):
            current_board.append(self.board[i].copy())
        return current_board

    def valid_move(self, row, col, player):
        """
        Check if a move is valid.

        Parameters:
        row (int): The row of the move.
        col (int): The column of the move.
        player (int): The player making the move (1 or -1).

        Returns:
        bool: True if the move is valid, False otherwise.
        """
        if 0 <= row < self.height and 0 <= col < self.width:
            if self.board[row][col] == 0 or self.board[row][col] / abs(self.board[row][col]) == player:
                return True
        return False

    def add_piece(self, row, col, player):
        """
        Add a piece to the board at the specified location.

        Parameters:
        row (int): The row where the piece is added.
        col (int): The column where the piece is added.
        player (int): The player making the move (1 or -1).

        Returns:
        bool: True if the piece was successfully added, False otherwise.
        """
        self.history.append(copy_board(self.board))  # Save the current state before making a move
        if self.valid_move(row, col, player):
            self.board[row][col] += player
            self.turn += 1
            return True
        return False

    def undo(self):
        """
        Undo the last move made on the board.
        """
        if self.history:
            self.board = self.history.pop()

    def check_win(self):
        """
        Check if there is a winner.

        Returns:
        int: 1 if player 1 wins, -1 if player 2 wins, 0 if no winner yet.
        """
        if self.turn > 0:
            num_p1 = 0
            num_p2 = 0
            for i in range(self.height):
                for j in range(self.width):
                    if self.board[i][j] > 0:
                        if num_p2 > 0:
                            return 0
                        num_p1 += 1
                    elif self.board[i][j] < 0:
                        if num_p1 > 0:
                            return 0
                        num_p2 += 1
            if num_p1 == 0:
                return -1
            if num_p2 == 0:
                return 1
        return 0

    def do_overflow(self, q):
        """
        Handle overflow on the board.

        Parameters:
        q (Queue): The queue used to manage overflow states.

        Returns:
        int: The number of overflow steps taken.
        """
        oldboard = copy_board(self.board)
        numsteps = overflow(self.board, q)
        if numsteps != 0:
            self.set(oldboard)
        return numsteps

    def set(self, newboard):
        """
        Set the board to a new state.

        Parameters:
        newboard (list of list of int): The new state of the board.
        """
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col] = newboard[row][col]

    def draw(self, window, frame):
        """
        Draw the board and its pieces on the window.

        Parameters:
        window (pygame.Surface): The window to draw the board on.
        frame (int): The current frame of the animation.
        """
        for row in range(GRID_SIZE[0]):
            for col in range(GRID_SIZE[1]):
                rect = pygame.Rect(col * CELL_SIZE + X_OFFSET, row * CELL_SIZE + Y_OFFSET, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(window, BLACK, rect, 1)
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] != 0:
                    rpos = row * CELL_SIZE + Y_OFFSET
                    cpos = col * CELL_SIZE + X_OFFSET
                    sprite = p1_sprites if self.board[row][col] > 0 else p2_sprites
                    if abs(self.board[row][col]) == 1:
                        cpos += CELL_SIZE // 2 - 16
                        rpos += CELL_SIZE // 2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 2:
                        cpos += CELL_SIZE // 2 - 32
                        rpos += CELL_SIZE // 2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 3:
                        cpos += CELL_SIZE // 2 - 16
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos = col * CELL_SIZE + X_OFFSET + CELL_SIZE // 2 - 32
                        rpos += CELL_SIZE // 2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 4:
                        cpos += CELL_SIZE // 2 - 32
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos += CELL_SIZE // 2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos -= CELL_SIZE // 2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))


# Constants
GRID_SIZE = (5, 6)
CELL_SIZE = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X_OFFSET = 0
Y_OFFSET = 100
FULL_DELAY = 5

# Load sprites for players
p1spritesheet = pygame.image.load('blue.png')
p2spritesheet = pygame.image.load('pink.png')
p1_sprites = []
p2_sprites = []

# Player IDs
player_id = [1, -1]

# Extract sprites from the spritesheet
for i in range(8):
    curr_sprite = pygame.Rect(32 * i, 0, 32, 32)
    p1_sprites.append(p1spritesheet.subsurface(curr_sprite))
    p2_sprites.append(p2spritesheet.subsurface(curr_sprite))

frame = 0

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((1200, 800))

pygame.font.init()
font = pygame.font.Font(None, 36)
bigfont = pygame.font.Font(None, 108)

# Create the game board and UI elements
player1_dropdown = Dropdown(900, 50, 200, 50, ['Human', 'AI'])
player2_dropdown = Dropdown(900, 110, 200, 50, ['Human', 'AI'])
undo_button = Button(900, 250, 200, 50, 'Undo Last Move')
restart_button = Button(900, 310, 200, 50, 'Restart Game')

status = ["", ""]
current_player = 0
board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)

running = True
overflow_boards = Queue()
overflowing = False
numsteps = 0
has_winner = False
bots = [PlayerOne(), PlayerTwo()]
grid_col = -1
grid_row = -1
choice = [None, None]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            # Handle dropdowns to switch between Human and AI
            player1_dropdown.handle_event(event)
            player2_dropdown.handle_event(event)

            # Handle undo and restart buttons
            if undo_button.is_clicked(event):
                if choice[current_player] == 0:  # Only allow human players to undo
                    board.undo()
                    current_player = (current_player + 1) % 2  # Revert to the previous player

            if restart_button.is_clicked(event):
                board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)  # Reset the board
                current_player = 0  # Reset to player 1's turn
                has_winner = False  # Reset the winner status

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y - Y_OFFSET
                col = x - X_OFFSET
                grid_row, grid_col = row // CELL_SIZE, col // CELL_SIZE

    # Update choices after handling events
    choice[0] = player1_dropdown.get_choice()
    choice[1] = player2_dropdown.get_choice()

    # Check for a winner
    win = board.check_win()
    if win != 0:
        winner = 1 if win == 1 else 2
        has_winner = True

    if not has_winner:
        if overflowing:
            status[0] = "Overflowing"
            if not overflow_boards.is_empty():
                if repeat_step == FULL_DELAY:
                    next_board = overflow_boards.dequeue()
                    board.set(next_board)
                    repeat_step = 0
                else:
                    repeat_step += 1
            else:
                overflowing = False
                current_player = (current_player + 1) % 2

        else:
            status[0] = "Player " + str(current_player + 1) + "'s turn"
            make_move = False
            if choice[current_player] == 1:
                (grid_row, grid_col) = bots[current_player].get_play(board.get_board())
                status[1] = "Bot chose row {}, col {}".format(grid_row, grid_col)
                if not board.valid_move(grid_row, grid_col, player_id[current_player]):
                    has_winner = True
                    winner = ((current_player + 1) % 2) + 1
                else:
                    make_move = True
            else:
                if board.valid_move(grid_row, grid_col, player_id[current_player]):
                    make_move = True

            if make_move:
                board.add_piece(grid_row, grid_col, player_id[current_player])
                numsteps = board.do_overflow(overflow_boards)
                if numsteps != 0:
                    overflowing = True
                    repeat_step = 0
                else:
                    current_player = (current_player + 1) % 2
                grid_row = -1
                grid_col = -1

    # Drawing the game elements
    window.fill(WHITE)
    board.draw(window, frame)
    window.blit(p1_sprites[math.floor(frame)], (850, 60))
    window.blit(p2_sprites[math.floor(frame)], (850, 120))
    frame = (frame + 0.5) % 8

    player1_dropdown.draw(window)
    player2_dropdown.draw(window)
    undo_button.draw(window)
    restart_button.draw(window)

    if not has_winner:
        text = font.render(status[0], True, BLACK)
        window.blit(text, (X_OFFSET, 750))
        text = font.render(status[1], True, BLACK)
        window.blit(text, (X_OFFSET, 700))
    else:
        text = bigfont.render("Player " + str(winner) + " wins!", True, BLACK)
        window.blit(text, (300, 250))

    pygame.display.update()
    pygame.time.delay(100)

pygame.quit()
sys.exit()
