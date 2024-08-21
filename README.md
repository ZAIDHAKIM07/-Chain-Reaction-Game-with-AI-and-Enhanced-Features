Chain Reaction Game with AI and Enhanced Features
Overview
This project is a Python implementation of the classic "Chain Reaction" game, enhanced with AI capabilities and additional features like "Undo Last Move" and "Restart Game." The game allows two players (either human or AI) to take turns placing gems on a grid. The objective is to cause chain reactions by overloading cells with gems until one player dominates the entire board.

Features
AI Opponents: Play against AI with varying levels of difficulty.
Undo Last Move: Allows players to undo their last move, providing more flexibility and strategy.
Restart Game: Reset the game at any time to start fresh.
Overflow Mechanism: Cells can overflow to adjacent cells, changing the game's dynamics and creating exciting chain reactions.
Setup Instructions
Prerequisites
Ensure you have the following installed:

Python 3.10 or later
pygame library (for graphical user interface)
You can install the pygame library using pip:

bash
Copy code
pip install pygame
Cloning the Repository
First, clone the repository to your local machine:

bash
Copy code
git clone https://github.com/ZAIDHAKIM07/-Chain-Reaction-Game-with-AI-and-Enhanced-Features.git
cd Chain-Reaction-Game-with-AI-and-Enhanced-Features
Running the Game
Navigate to the directory containing the game files:

bash
Copy code
cd 2D-GAME
Run the game using Python:

bash
Copy code
python game.py
How to Play
Starting the Game
Upon starting the game, you can choose whether each player will be human or AI using the dropdown menus.
Click "Start Game" to begin.
Making Moves
Players take turns placing gems on the board. You can place a gem in any empty cell or a cell that already contains one of your gems.
If a cell exceeds its capacity (equal to the number of adjacent cells), it will overflow, spreading its gems to neighboring cells and potentially causing further overflows.
Undo Last Move
If a human player wishes to undo their last move, they can press the "Undo Last Move" button to revert to the previous game state.
Restart Game
At any point, you can press the "Restart Game" button to reset the board and start a new game.
Winning the Game
The game continues until one player controls all the cells on the board. The player who achieves this first is declared the winner.
Game Mechanics
Overflow Mechanism: When a cell reaches its capacity, it overflows, sending one gem to each adjacent cell. The color of the gems changes to the player who caused the overflow.

AI Implementation: The AI uses a game tree with a minimax algorithm to decide its moves, evaluating potential future states to determine the most optimal move.

Contributing
If you would like to contribute to this project, feel free to fork the repository and submit a pull request with your enhancements or bug fixes.

License
This project is licensed under the MIT License. See the LICENSE file for more details.
