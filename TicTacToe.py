import math
import random


class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter

    # we want all players to get their next move given a game
    def get_move(self, game):
        pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)  # this makes the child class inherit all the methods and properties from its parent
        # Player.__init__(self, letter)  is an alternative


    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, apple):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0 - 8):')
            # we are going to check if this is a valid input
            try:
                val = int(square)
                if val not in apple.available_moves():  # apple.available_moves() is a list of available positions
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid Square. Try again')

        return val



class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())  # randomly choose one
        else:
            # get the square based off the minimax algorithm
            square = self.minimax(game, self.letter)['position']

        return square

    def minimax(self, state, player):
        # we call it state and not game because at every iteration of minimax, we pass in a representation(a screenshot)
        # of that game
        max_player = self.letter  # us
        other_player = 'O' if player == 'X' else 'X'

        # First, we want to check if the previous move is a winner
        # this is our base case
        if state.current_winner == other_player:
            # we should return position and score because we need to keep track of the score for minimax to work
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}

        elif not state.empty_squares():  # no empty squares
            return {'position': None, 'score': 0}

        # Initializing some Dictionaries
        if player == max_player:
            best = {'osition': None, 'score': -math.inf}  # each score should maximize (be larger)
        else:
            best = {'position': None, 'score': math.inf}  # each score should minimize

        for possible_move in state.available_moves():
            # step 1: make a move, try that spot
            state.make_move(possible_move, player)
            # step 2: recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player)  # now, we alternate players

            # step 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # otherwise this will get messed up from the recursion part

            # step 4: Update the dictionaries if necessary
            if player == max_player:  # we are trying to maximize the max_player
                if sim_score['score'] > best['score']:
                    best = sim_score  # replace best
            else:  # but minimize the other player
                if sim_score['score'] < best['score']:
                    best = sim_score  # replace best

        return best


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
    o_player = GeniusComputerPlayer('O')
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)

