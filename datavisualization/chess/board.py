import json#importing json module
from pieces import Rook, Knight, Bishop, Queen, King, Pawn#importing all the pieces from the pieces module


class Board: #class to represent the board
    def __init__(self): #constructor of the class
        # Dict comprehension: all 64 squares initialised to None
        self.squares = {
            f"{chr(col)}{row}": None #assigning None to each square
            for col in range(ord('a'), ord('i')) #iterating through columns
            for row in range(1, 9) #iterating through rows
        }
        self.setup_board()#setting up the board

        # Give every piece its starting position and a reference to this board
        for square, piece in self.squares.items(): #iterating through all the squares
            if piece is not None:
                piece.set_initial_position(square)#setting the initial position of the piece
                piece.define_board(self)#defining the board for the piece

    def setup_board(self): #setting up the board
        # --- BLACK major pieces on row 1 ---
        self.squares['a1'] = Rook('BLACK', 1)#placing black rook on a1
        self.squares['b1'] = Knight('BLACK', 1)#placing black knight on b1
        self.squares['c1'] = Bishop('BLACK', 1)#placing black bishop on c1
        self.squares['d1'] = Queen('BLACK', 1)#placing black queen on d1
        self.squares['e1'] = King('BLACK', 1)#placing black king on e1
        self.squares['f1'] = Bishop('BLACK', 2)#placing black bishop on f1
        self.squares['g1'] = Knight('BLACK', 2)#placing black knight on g1
        self.squares['h1'] = Rook('BLACK', 2)#placing black rook on h1

        # Black pawns on row 2 — dict comprehension
        black_pawns = {
            f"{chr(col)}2": Pawn('BLACK', col - ord('a') + 1)#placing black pawns on row 2
            for col in range(ord('a'), ord('i'))#iterating through columns
        }
        self.squares.update(black_pawns)#updating the squares with black pawns

        # --- WHITE major pieces on row 8 ---
        self.squares['a8'] = Rook('WHITE', 1)#placing white rook on a8
        self.squares['b8'] = Knight('WHITE', 1)#placing white knight on b8
        self.squares['c8'] = Bishop('WHITE', 1)#placing white bishop on c8
        self.squares['d8'] = Queen('WHITE', 1)#placing white queen on d8
        self.squares['e8'] = King('WHITE', 1)#placing white king on e8
        self.squares['f8'] = Bishop('WHITE', 2)#placing white bishop on f8
        self.squares['g8'] = Knight('WHITE', 2)#placing white knight on g8
        self.squares['h8'] = Rook('WHITE', 2)#placing white rook on h8

        # White pawns on row 7 — dict comprehension
        white_pawns = {
            f"{chr(col)}7": Pawn('WHITE', col - ord('a') + 1)#placing white pawns on row 7
            for col in range(ord('a'), ord('i'))#iterating through columns
        }
        self.squares.update(white_pawns)#updating the squares with white pawns

    def print_board(self):#function to print the board
        """Print the board row by row using list comprehensions."""
        rows = [
            [self.squares[f"{chr(col)}{row}"] for col in range(ord('a'), ord('i'))] #iterating through columns
            for row in range(1, 9)#iterating through rows
        ]
        for row in rows:#iterating through rows
            print(row)#printing each row

    def find_piece(self, symbol: str, identifier: int, color: str):#finding a piece on the board
        """Return all (square, piece) pairs matching the given symbol, identifier and color."""
        return [
            (square, piece)#returning the square and the piece
            for square, piece in self.squares.items()#iterating through all the squares
            if piece is not None#checking if the square is not empty
            and piece.symbol == symbol#checking if the symbol matches
            and piece.identifier == identifier#checking if the identifier matches
            and piece.color == color#checking if the color matches
        ]

    def get_piece(self, square: str):#function to get a piece
        """Return the piece on a specific square."""#returning the piece on a specific square
        return self.squares[square]#returning the piece on the square

    def is_square_empty(self, square: str) -> bool:#checking if the square is empty
        """Return True if the square is empty."""#returning true if the square is empty
        return self.get_piece(square) is None#returning false if the square is not empty

    def kill_piece(self, square: str):#function to kill a piece
        """Call die() on the piece at the given square and clear the square."""#calling die() on the piece and clearing the square
        piece = self.squares[square]#getting the piece on the square
        if piece is not None:#checking if the square is not empty
            piece.die()#calling die() on the piece
            self.squares[square] = None#clearing the square

    def save_board_state(self):#function to save the board state
        """Append the current§ board state as a JSON line to board.txt."""#saving the board state as a JSON line to board.txt
        with open('board.txt', 'a') as file:#opening board.txt in append mode
            file.write(json.dumps(self.squares) + '\n')#writing the board state as a JSON line to board.txt

    @staticmethod
    def load_board_states():#function to load the board states
        """Generator that yields one saved board state at a time from board.txt."""#loading the board states from board.txt
        with open('board.txt', 'r') as file:#opening board.txt in read mode
            for line in file:#iterating through the lines
                line = line.strip()#removing whitespace from the line
                if line:#checking if the line is not empty
                    yield json.loads(line)#loading the board state from the line
