class BoardMovements:
    """
    Static movement helpers for chess pieces.
    All methods return the new position string, or the original position
    if the move is blocked (out of bounds).

    Direction convention:
    - BLACK starts on rows 1-2, WHITE starts on rows 7-8.
    - 'Forward' for BLACK increments the row; for WHITE it decrements.
    - 'Left' / 'Right' are from an absolute board perspective (a←h).
    """

    @staticmethod
    def forward(position: str, color: str, squares: int = 1) -> str:# this is a comment
        column = position[0]#getting the column
        row = int(position[1])#getting the row
        new_row = row + squares if color == 'BLACK' else row - squares#calculating the new row
        if new_row < 1 or new_row > 8:#checking if the new row is within the board
            print("Movement blocked: out of bounds")#printing that the movement is blocked
            return position#returning the original position
        return f"{column}{new_row}"#returning the new position

    @staticmethod
    def backward(position: str, color: str, squares: int = 1) -> str:# this is a comment
        column = position[0]#getting the column
        row = int(position[1])#getting the row
        new_row = row - squares if color == 'BLACK' else row + squares#calculating the new row
        if new_row < 1 or new_row > 8:#checking if the new row is within the board
            print("Movement blocked: out of bounds")#printing that the movement is blocked
            return position#returning the original position
        return f"{column}{new_row}"#returning the new position

    @staticmethod
    def left(position: str, color: str, squares: int = 1) -> str:# this is a comment
        column = position[0]#getting the column
        row = int(position[1])#getting the row
        new_column = chr(ord(column) - squares)#calculating the new column
        if new_column == '`' or new_column < 'a' or new_column > 'h':#checking if the new column is within the board
            print("Movement blocked: out of bounds")#printing that the movement is blocked
            return position#returning the original position
        return f"{new_column}{row}"#returning the new position

    @staticmethod
    def right(position: str, color: str, squares: int = 1) -> str:# this is a comment
        column = position[0]#getting the column
        row = int(position[1])#getting the row
        new_column = chr(ord(column) + squares)#calculating the new column
        if new_column == 'i' or new_column < 'a' or new_column > 'h':#checking if the new column is within the board
            print("Movement blocked: out of bounds")#printing that the movement is blocked
            return position#returning the original position
        return f"{new_column}{row}"#returning the new position

    @staticmethod
    def forward_left(position: str, color: str, squares: int = 1) -> str: # this is a comment
        new_pos = BoardMovements.forward(position, color, squares)#calculating the new position
        if new_pos == position:#checking if the new position is the same as the original position
            return position#returning the original position
        result = BoardMovements.left(new_pos, color, squares)#calculating the new position
        return position if result == new_pos else result#returning the new position or the original position

    @staticmethod
    def forward_right(position: str, color: str, squares: int = 1) -> str: # this is a comment
        new_pos = BoardMovements.forward(position, color, squares)#calculating the new position
        if new_pos == position:#checking if the new position is the same as the original position
            return position#returning the original position
        result = BoardMovements.right(new_pos, color, squares)#calculating the new position
        return position if result == new_pos else result#returning the new position or the original position

    @staticmethod
    def backward_left(position: str, color: str, squares: int = 1) -> str: # this is a comment
        new_pos = BoardMovements.backward(position, color, squares)#calculating the new position
        if new_pos == position:#checking if the new position is the same as the original position
            return position#returning the original position
        result = BoardMovements.left(new_pos, color, squares)#calculating the new position
        return position if result == new_pos else result#returning the new position or the original position

    @staticmethod
    def backward_right(position: str, color: str, squares: int = 1) -> str:# this is a comment
        new_pos = BoardMovements.backward(position, color, squares)#calculating the new position
        if new_pos == position:#checking if the new position is the same as the original position

            return position#returning the original position
        result = BoardMovements.right(new_pos, color, squares)#calculating the new position
        return position if result == new_pos else result#returning the new position or the original position
