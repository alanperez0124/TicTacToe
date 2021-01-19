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




