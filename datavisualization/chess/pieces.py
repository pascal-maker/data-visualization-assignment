from abc import ABC#importing abstract base class
import functools


def print_board(func):#this is a decorator
    @functools.wraps(func)#wrapper for the print_board decorator
    def wrapper(self, *args, **kwargs):#this is a wrapper function
        result = func(self, *args, **kwargs)#calling the function
        if self.board is not None:#checking if the board is not empty
            self.board.print_board()#printing the board 
        return result#returning the result
    return wrapper#returning the wrapper


def save_board(func):#this is a decorator
    @functools.wraps(func)#wrapper for the save_board decorator
    def wrapper(self, *args, **kwargs):#this is a wrapper function
        result = func(self, *args, **kwargs)#calling the function
        if self.board is not None:#checking if the board is not empty
            self.board.save_board_state()#saving the board state
        return result#returning the result
    return wrapper#returning the wrapper


class BaseChessPiece(ABC, dict):#class to represent a chess piece
    def __init__(self, color: str, name: str, symbol: str, identifier: int):#constructor for the class
        self.color = color#setting the color of the piece
        self.name = name#setting the name of the piece
        self.symbol = symbol#setting the symbol of the piece
        self.identifier = identifier#setting the identifier of the piece
        self.position = 'None'#setting the position of the piece
        self.is_alive = True#setting the is_alive attribute of the piece
        self.board = None#setting the board attribute of the piece
        dict.__init__(self, color=color, name=name, symbol=symbol,#dictionary to store the piece
                      identifier=identifier, position='None', is_alive=True)#dictionary to store the piece

    @print_board
    @save_board
    def move(self, movement: str):#function to move the piece
        """Execute the move on the board. Called by subclasses via super().move(movement)."""
        if self.board is None:#checking if the board is not empty
            print(movement)#printing the movement
            return  #returning the movement

        if movement == self.position:#checking if the movement is the same as the current position
            print("Movement blocked: out of bounds or invalid move")#printing the error message
            return  #returning the movement

        new_location = self.board.get_piece(movement)#getting the piece at the new location

        if new_location is not None:#checking if the new location is not empty
            if new_location.color == self.color:#checking if the new location is occupied by a friendly piece
                print(f"Cannot move to {movement}: occupied by a friendly piece")#printing the error message
                return  #returning the movement
            self.board.kill_piece(movement)#killing the piece at the new location

        self.board.squares[self.position] = None#removing the piece from the old position
        self.position = movement#setting the new position
        self['position'] = movement#setting the new position
        self.board.squares[self.position] = self#setting the new position
        print(f"{self} moved to {movement}")#printing the movement

    def die(self):#function to kill the piece
        self.is_alive = False#setting the is_alive attribute to False
        self['is_alive'] = False#setting the is_alive attribute to False

    def set_initial_position(self, position: str):#function to set the initial position
        self.position = position#setting the initial position
        self['position'] = position#setting the initial position

    def define_board(self, board):#function to define the board
        self.board = board#setting the board

    def __str__(self):#function to represent the piece as a string
        return f"{self.color} {self.name} {self.identifier}"#printing the piece as a string

    def __repr__(self):#function to represent the piece as a string
        return f"{self.color} {self.name} {self.identifier}"#printing the piece as a string


class Pawn(BaseChessPiece):#class to represent a pawn
    def __init__(self, color: str, identifier: int):#constructor for the class
        super().__init__(color, 'Pawn', '-', identifier)#calling the constructor of the parent class

    def move(self):#function to move the pawn
        from board_movements import BoardMovements#importing the board_movements module
        movement = BoardMovements.forward(self.position, self.color, 1)#moving the pawn forward
        super().move(movement)#calling the move function of the parent class


class Rook(BaseChessPiece):#class to represent a rook
    def __init__(self, color: str, identifier: int):#constructor for the class
        super().__init__(color, 'Rook', 'R', identifier)#calling the constructor of the parent class

    def move(self, direction: str = 'Forward', squares: int = 1):#function to move the rook
        from board_movements import BoardMovements#importing the board_movements module
        directions = {
            'Forward':  BoardMovements.forward,#forward movement
            'Backward': BoardMovements.backward,#backward movement
            'Left':     BoardMovements.left,#left movement
            'Right':    BoardMovements.right,#right movement
        }
        if direction in directions:#checking if the direction is valid
            movement = directions[direction](self.position, self.color, squares)#moving the rook
            super().move(movement)#calling the move function of the parent class
        else:
            print(f"Invalid direction for Rook: {direction}")#printing the error message


class Bishop(BaseChessPiece):#class to represent a bishop
    def __init__(self, color: str, identifier: int):#constructor for the class
        super().__init__(color, 'Bishop', 'B', identifier)#calling the constructor of the parent class

    def move(self, direction: str = 'ForwardRight', squares: int = 1):#function to move the bishop
        from board_movements import BoardMovements#importing the board_movements module
        directions = {
            'ForwardLeft':   BoardMovements.forward_left,#forward left movement
            'ForwardRight':  BoardMovements.forward_right,#forward right movement
            'BackwardLeft':  BoardMovements.backward_left,#backward left movement
            'BackwardRight': BoardMovements.backward_right,#backward right movement
        }
        if direction in directions:#checking if the direction is valid
            movement = directions[direction](self.position, self.color, squares)#moving the bishop
            super().move(movement)#calling the move function of the parent class
        else:
            print(f"Invalid direction for Bishop: {direction}")#printing the error message


class Knight(BaseChessPiece):#class to represent a knight
    def __init__(self, color: str, identifier: int):#constructor for the class
        super().__init__(color, 'Knight', 'N', identifier)#calling the constructor of the parent class

    def move(self, direction: str = 'ForwardLeft'):#function to move the knight
        col_idx = ord(self.position[0]) - ord('a')#getting the column index of the knight
        row = int(self.position[1])#getting the row index of the knight

        # L-shaped moves: (col_offset, row_offset)
        knight_moves = {
            'ForwardLeft':   (col_idx - 1, row + 2),#forward left movement
            'ForwardRight':  (col_idx + 1, row + 2),#forward right movement
            'BackwardLeft':  (col_idx - 1, row - 2),#backward left movement
            'BackwardRight': (col_idx + 1, row - 2),#backward right movement
            'LeftForward':   (col_idx - 2, row + 1),#left forward movement
            'LeftBackward':  (col_idx - 2, row - 1),#left backward movement
            'RightForward':  (col_idx + 2, row + 1),#right forward movement
            'RightBackward': (col_idx + 2, row - 1),#right backward movement
        }

        if direction not in knight_moves:#checking if the direction is valid
            print(f"Invalid direction for Knight: {direction}")#printing the error message
            return

        new_col_idx, new_row = knight_moves[direction]#getting the new column index and row index
        if new_col_idx < 0 or new_col_idx > 7 or new_row < 1 or new_row > 8:#checking if the new position is within the board boundaries
            print("Knight movement blocked: out of bounds")#printing the error message
            return

        movement = f"{chr(ord('a') + new_col_idx)}{new_row}"#setting the new position
        super().move(movement)#calling the move function of the parent class


class Queen(BaseChessPiece):#class to represent a queen
    def __init__(self, color: str, identifier: int):#constructor for the class
        super().__init__(color, 'Queen', 'Q', identifier)#calling the constructor of the parent class

    def move(self, direction: str = 'Forward', squares: int = 1):#function to move the queen
        from board_movements import BoardMovements#importing the board_movements module
        directions = {
            'Forward':       BoardMovements.forward,#forward movement
            'Backward':      BoardMovements.backward,#backward movement
            'Left':          BoardMovements.left,#left movement
            'Right':         BoardMovements.right,#right movement
            'ForwardLeft':   BoardMovements.forward_left,#forward left movement
            'ForwardRight':  BoardMovements.forward_right,#forward right movement
            'BackwardLeft':  BoardMovements.backward_left,#backward left movement
            'BackwardRight': BoardMovements.backward_right,#backward right movement
        }
        if direction in directions:#checking if the direction is valid
            movement = directions[direction](self.position, self.color, squares)#moving the queen
            super().move(movement)#calling the move function of the parent class
        else:
            print(f"Invalid direction for Queen: {direction}")#printing the error message


class King(BaseChessPiece):#class to represent a king
    def __init__(self, color: str, identifier: int):#constructor for the class
        super().__init__(color, 'King', 'K', identifier)#calling the constructor of the parent class

    def move(self, direction: str = 'Forward'):#function to move the king
        from board_movements import BoardMovements#importing the board_movements module
        directions = {
            'Forward':       BoardMovements.forward,#forward movement
            'Backward':      BoardMovements.backward,#backward movement
            'Left':          BoardMovements.left,#left movement
            'Right':         BoardMovements.right,#right movement
            'ForwardLeft':   BoardMovements.forward_left,#forward left movement
            'ForwardRight':  BoardMovements.forward_right,#forward right movement
            'BackwardLeft':  BoardMovements.backward_left,#backward left movement
            'BackwardRight': BoardMovements.backward_right,#backward right movement
        }
        if direction in directions:#checking if the direction is valid
            # King always moves exactly 1 square
            movement = directions[direction](self.position, self.color, 1)#moving the king
            super().move(movement)#calling the move function of the parent class
        else:
            print(f"Invalid direction for King: {direction}")#printing the error message
