import os
from pieces import Pawn
from board import Board

# Clear old board state file before each run so generator output is fresh
if os.path.exists('board.txt'):
    os.remove('board.txt')

# --- 1. Basic piece creation (no board) ---
print("=== Basic piece test ===")# printing the basic piece test
pawn = Pawn('BLACK', 1)#creating a black pawn
print(f"Created: {pawn}")#printing the black pawn

# --- 2. Full board setup ---
print("\n=== Initial board ===")#printing the initial board
board = Board()#creating a board
board.print_board()#printing the board

# --- 3. Move BLACK Pawn 1 forward ---
print("\n=== BLACK Pawn 1 moves forward ===")#printing the black pawn move
black_pawn = board.find_piece('-', 1, 'BLACK')[0][1]#finding the black pawn
black_pawn.move()#moving the black pawn

# --- 4. Move WHITE Pawn 1 forward (moves toward lower rows) ---
print("\n=== WHITE Pawn 1 moves forward ===")#printing the white pawn move
white_pawn = board.find_piece('-', 1, 'WHITE')[0][1]#finding the white pawn
white_pawn.move()#moving the white pawn

# --- 5. Move BLACK Knight 1 ---
print("\n=== BLACK Knight 1 moves ForwardLeft ===")#printing the black knight move
black_knight = board.find_piece('N', 1, 'BLACK')[0][1]#finding the black knight
black_knight.move('ForwardLeft')#moving the black knight

# --- 6. Replay saved states via generator ---
print("\n=== Replaying saved board states ===")#printing the saved board states
for i, state in enumerate(Board.load_board_states()):#looping through the saved board states
    pieces_on_board = sum(1 for v in state.values() if v is not None)#counting the number of pieces on the board
    print(f"State {i + 1}: {pieces_on_board} pieces on board")#printing the number of pieces on the board
