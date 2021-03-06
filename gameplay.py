from players import HumanPlayer, RandomComputerPlayer, GeniusComputerPlayer


class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # we will use a single list to rep 3x3 board
        self.current_winner = None  # keep track of winner


    def print_board(self):
        for row in [self.board[i*3:(i + 1) * 3] for i in range(3)]:  # using list comprehension to split the board into
            # 0-2, 3-5, 6-8 and  looking at each element (row) of [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2 etc (tells us what number corresponds to what box)
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')


    def available_moves(self):
        # Using list comprehension
        return [i for i, spot in enumerate(self.board) if spot == ' ']  # where i, spot is a tuple and we are
        # appending the list with the i position of the tuple

        # # Not using list comprehension
        # moves = []
        # for (x, spot) in enumerate(self.board):
        #     # ['x', ' ', 'o'] --> [(0, 'x'), (1, ' '), (2, 'o')]
        #     if spot == ' ':
        #         moves.append(x)
        #
        # return moves

    def empty_squares(self):
        return ' ' in self.board  # this will return  a boolean: Either True or False


    def num_empty_squares(self):
        return self.board.count(' ')


    def make_move(self, square, letter):
        # if the move is valid, then make the move then return true. If not valid, return false
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):  # We require the self because it will return a boolean value
                self.current_winner = letter
            return True
        return False


    def winner(self, square, letter):
        row_index = square//3
        row = self.board[row_index*3:(row_index + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        # Check column
        column_index = square % 3
        column = [self.board[column_index + i * 3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # Check diagonals
        # We can check this by looking to see if the square is an even number (0, 2, 4, 6) since these are the only
        # possible moves to win a diagonal
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # left to right diagonal
            if all([spot == letter for spot in diagonal1]):
                return True

            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        # if all of these checks fail, we return false
        return False


def play(game, x_player, o_player, print_game=True):
    """Returns the winner of the game or returns None for a tie"""
    if print_game:
        game.print_board_nums()

    letter = 'X'

    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)  # o_player will be the self parameter and game will be the second one
        else:
            square = x_player.get_move(game)

        # Now let's make a move
        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square}')
                game.print_board()
                print('')  # just an empty line

            if game.current_winner:
                if print_game:
                    print(letter + ' wins')
                return letter
            # after we make a move, we need to alternate letters
            if letter == 'X':
                letter = 'O'
            else:
                letter = 'X'

    if print_game:
        print('It\'s a tie')

if __name__ == '__main__':
    x_player = HumanPlayer('X')
    # o_player = GeniusComputerPlayer('O')
    o_player = RandomComputerPlayer('O')
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)


