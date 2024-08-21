# Main Author: [MOHAMMED ZAID SHABBIR KHAN HAKIM]
# Main Reviewer: [Reviewer's Name]

# This function duplicates and returns the board.
# It is useful for making non-destructive changes to the board state.
def copy_board(board):
    """
    Create a deep copy of the current board state.
    
    Parameters:
    board (list of list of int): The current game board represented as a 2D list.
    
    Returns:
    list of list of int: A deep copy of the board.
    """
    current_board = []
    height = len(board)
    for i in range(height):
        current_board.append(board[i].copy())
    return current_board

# This function evaluates the current board from the perspective of the player.
def evaluate_board(board, player):
    """
    Evaluate the board and return a score from the player's perspective.
    
    Parameters:
    board (list of list of int): The current game board represented as a 2D list.
    player (int): The player for whom the evaluation is being performed (1 or -1).
    
    Returns:
    float: A positive score if the board is favorable to the player, 
           negative if unfavorable, or infinity if it's a winning/losing board.
    """
    score = 0
    for row in board:
        for cell in row:
            if cell == player:
                score += 1
            elif cell == -player:
                score -= 1

    if all(cell == player for row in board for cell in row if cell != 0):
        return float('inf')
    elif all(cell == -player for row in board for cell in row if cell != 0):
        return float('-inf')
    return score

# This class represents the game tree used for determining the best move.
class GameTree:
    class Node:
        def __init__(self, board, depth, player, tree_height=4):
            """
            Initialize a Node in the game tree.
            
            Parameters:
            board (list of list of int): The current board state.
            depth (int): The depth of this node in the game tree.
            player (int): The player whose move is being simulated (1 or -1).
            tree_height (int): The maximum height of the game tree.
            """
            self.board = board
            self.depth = depth
            self.player = player
            self.children = []
            self.score = None

            if depth < tree_height:
                self.expand_children(tree_height)

        def expand_children(self, tree_height):
            """
            Expand the current node by generating all possible moves.
            
            Parameters:
            tree_height (int): The maximum height of the game tree.
            """
            moves = possible_moves(self.board, self.player)
            for move in moves:
                new_board = make_move(self.board, move, self.player)
                child = GameTree.Node(new_board, self.depth + 1, -self.player, tree_height)
                self.children.append(child)

            if not self.children:
                self.score = evaluate_board(self.board, self.player)

    def __init__(self, board, player, tree_height=4):
        """
        Initialize the GameTree with a root node and build the tree.
        
        Parameters:
        board (list of list of int): The initial board state.
        player (int): The player for whom the tree is being built (1 or -1).
        tree_height (int): The maximum height of the game tree.
        """
        self.root = self.Node(board, 0, player, tree_height)
        self.player = player
        self.minimax(self.root, player)

    def minimax(self, node, player):
        """
        Perform the minimax algorithm to evaluate the best move.
        
        Parameters:
        node (Node): The current node being evaluated.
        player (int): The player for whom the move is being evaluated.
        
        Returns:
        float: The evaluated score for this node.
        """
        if node.score is not None:
            return node.score

        if player == self.player:
            max_eval = -float('inf')
            for child in node.children:
                eval = self.minimax(child, -player)
                max_eval = max(max_eval, eval)
            node.score = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for child in node.children:
                eval = self.minimax(child, -player)
                min_eval = min(min_eval, eval)
            node.score = min_eval
            return min_eval

    def get_move(self):
        """
        Get the best move based on the current game tree.
        
        Returns:
        tuple: The row and column of the best move determined by the minimax algorithm.
        """
        best_score = float('inf')
        best_move = None

        for child in self.root.children:
            score = self.minimax(child, False)
            if score < best_score:
                best_score = score
                best_move = extract_move(self.root.board, child.board)
        return best_move

# Function to apply a move to the board and handle any overflow.
def make_move(board, move, player):
    """
    Make a move on the board and apply overflow rules.
    
    Parameters:
    board (list of list of int): The current game board.
    move (tuple): The row and column where the move is to be made.
    player (int): The player making the move (1 or -1).
    
    Returns:
    list of list of int: The updated board after making the move.
    """
    new_board = copy_board(board)
    i, j = move
    new_board[i][j] += player
    overflow(new_board, i, j, player)
    return new_board

# Function to handle overflow mechanics on the board.
def overflow(board, i, j, player):
    """
    Handle the overflow of pieces on the board after a move.
    
    Parameters:
    board (list of list of int): The current game board.
    i (int): The row of the piece to check for overflow.
    j (int): The column of the piece to check for overflow.
    player (int): The player whose piece is overflowing (1 or -1).
    """
    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    overflow_count = 4

    for x, y in neighbors:
        if x < 0 or x >= len(board) or y < 0 or y >= len(board[0]) or board[x][y] != player:
            overflow_count -= 1

    if abs(board[i][j]) >= overflow_count:
        board[i][j] = 0
        for x, y in neighbors:
            if 0 <= x < len(board) and 0 <= y < len(board[0]):
                board[x][y] += player
                if abs(board[x][y]) >= 4:
                    overflow(board, x, y, player)

# Function to determine all possible valid moves for a player.
def possible_moves(board, player):
    """
    Get a list of all possible valid moves for the player.
    
    Parameters:
    board (list of list of int): The current game board.
    player (int): The player for whom to generate the moves (1 or -1).
    
    Returns:
    list of tuple: A list of valid moves (row, column) on the board.
    """
    moves = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == 0 or board[i][j] == player]
    return moves

# Function to extract the move made by comparing the original and new boards.
def extract_move(original_board, new_board):
    """
    Extract the move made by comparing the original board and the new board.
    
    Parameters:
    original_board (list of list of int): The original board before the move.
    new_board (list of list of int): The board after the move.
    
    Returns:
    tuple: The row and column where the move was made.
    """
    for i in range(len(original_board)):
        for j in range(len(original_board[0])):
            if original_board[i][j] != new_board[i][j]:
                return (i, j)
    return None
