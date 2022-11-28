import sys
import copy
import random
from text_to_speech import *
import emoji


INF = sys.maxsize
BLANK = "_"
X = "X"
O = "O"
EMPTY_GRID = [[BLANK, BLANK, BLANK], [BLANK, BLANK, BLANK], [BLANK, BLANK, BLANK]]


class TicTacToe:
    def __init__(self):
        self.init_state = copy.deepcopy(EMPTY_GRID)
        self.player = "X"

    def terminal_test(self, state):
        if not (BLANK in state[0] or BLANK in state[1] or BLANK in state[2]):
            return True
        winner = self.winner(state)
        return winner == X or winner == O

    def winner(self, state):
        for row in [0, 1, 2]:
            if (
                state[row][0] != BLANK
                and state[row][0] == state[row][1]
                and state[row][0] == state[row][2]
            ):
                return state[row][0]

        for col in [0, 1, 2]:
            if (
                state[0][col] != BLANK
                and state[0][col] == state[1][col]
                and state[0][col] == state[2][col]
            ):
                return state[0][col]

        if (
            state[0][0] != BLANK
            and state[0][0] == state[1][1]
            and state[0][0] == state[2][2]
        ):
            return state[0][0]

        if (
            state[2][0] != BLANK
            and state[2][0] == state[1][1]
            and state[2][0] == state[0][2]
        ):
            return state[2][0]

        return None

    def utility(self, state):
        winner = self.winner(state)
        if winner == X:
            return 1
        elif winner == O:
            return -1
        else:
            return 0

    def actions(self, state):
        moves = []
        for row in [0, 1, 2]:
            for col in [0, 1, 2]:
                if state[row][col] == BLANK:
                    moves.append((row, col))
        return moves

    def result(self, state, action, player):
        res_state = copy.deepcopy(state)
        res_state[action[0]][action[1]] = player
        return res_state


n_levels = 0
n_states = 0
n_terminal_states = 0
states = dict()
terminal_states = set()


def minimax_decision(game, state):
    """
    It returns the best action for the current player to take, given the current state of the game

    :param game: the game object
    :param state: the current state of the game
    :return: The best action to take.
    """
    global n_levels, n_states, n_terminal_states, states, terminal_states
    n_levels = n_states = n_terminal_states = 0
    states = dict()
    terminal_states = set()
    best_actions = []  # used when more than one best action exists

    value = -INF
    actions = game.actions(state)
    for i in range(len(actions)):
        result_state = game.result(state, actions[i], X)
        statestr = grid_to_str(result_state)
        if statestr in states:
            next_state_value = states[statestr]
        else:
            n_states += 1
            next_state_value = min_value(game, result_state, 1)
            states[statestr] = next_state_value
        if next_state_value > value:
            value = next_state_value
            best_actions.clear()
            best_actions.append(actions[i])
        elif next_state_value == value:
            best_actions.append(actions[i])

    if len(best_actions) == 1:
        best_action = best_actions[0]
    else:
        best_action = random.choice(best_actions)
    return best_action


def max_value(game, state, level):
    """
    The function returns the maximum value of the game for the player X, given the current state of
    the game

    :param game: the game object
    :param state: the current state of the game
    :param level: the current level of the tree
    :return: The maximum value of the next state.
    """
    global n_levels, n_states, n_terminal_states, states
    n_levels = max(n_levels, level)
    if game.terminal_test(state):
        util = game.utility(state)
        n_terminal_states += 1
        terminal_states.add(grid_to_str(state))
        return util
    value = -INF
    actions = game.actions(state)
    for action in actions:
        next_state = game.result(state, action, X)
        statestr = grid_to_str(next_state)
        if statestr in states:
            next_state_value = states[statestr]
        else:
            n_states += 1
            next_state_value = min_value(game, next_state, level + 1)
            states[grid_to_str(next_state)] = next_state_value
        value = max(value, next_state_value)
    return value


def min_value(game, state, level):
    """
    It returns the minimum value of the game for the given state, assuming that the opponent plays
    optimally

    :param game: the game object
    :param state: the current state of the game
    :param level: the current level of the tree
    :return: The minimum value of the next state.
    """
    global n_levels, n_states, n_terminal_states, states
    n_levels = max(n_levels, level)
    if game.terminal_test(state):
        util = game.utility(state)
        n_terminal_states += 1
        terminal_states.add(grid_to_str(state))
        return util
    value = INF
    actions = game.actions(state)
    for action in actions:
        next_state = game.result(state, action, O)
        statestr = grid_to_str(next_state)
        if statestr in states:
            next_state_value = states[statestr]
        else:
            n_states += 1
            next_state_value = max_value(game, next_state, level + 1)
            states[grid_to_str(next_state)] = next_state_value
        value = min(value, next_state_value)
    return value


def print_grid(title, grid):
    """
    It prints the title, then it prints the grid

    :param title: The title of the grid
    :param grid: a list of lists of strings
    """
    print(title)
    for row in [0, 1, 2]:
        for col in [0, 1, 2]:
            print(grid[row][col], end=" ")
        print()


def grid_to_str(grid):
    """
    It takes a list of lists of strings and returns a single string

    :param grid: a 3x3 list of lists of strings
    :return: The grid in string form.
    """
    return "".join(grid[0]) + "".join(grid[1]) + "".join(grid[2])


def play_game():
    game = TicTacToe()
    grid = copy.deepcopy(EMPTY_GRID)

    try:

        moves = {
            1: [0, 0],
            2: [0, 1],
            3: [0, 2],
            4: [1, 0],
            5: [1, 1],
            6: [1, 2],
            7: [2, 0],
            8: [2, 1],
            9: [2, 2],
        }

        win_statements = [
            "Congrats! Good win!",
            "You are awesome at this game!",
            "You are the champion!",
            "You ought to be pleased with yourself!",
            "Congratulations! You are stunning!",
            "You win!",
        ]
        lose_statements = [
            "You lose:(, Sometimes a loss is the best thing that can happen. It teaches you what you should have done next time.",
            "Oh no, you lose.",
            "Better luck next time buddy.",
            "Come back stronger next time.",
        ]
        SpeakText(
            "Greetings and welcome to Tic Tac Toe Deluxe. What is your gamer name?\n>>> "
        )
        username = getMove()
        welcomeMessage = "Nice to meet you " + username
        SpeakText(welcomeMessage)
        player = "O"

        SpeakText("Game is about to start now. You have the first move")
        print_grid("Current grid:", grid)

        while not game.terminal_test(grid):
            if player == O:
                print("Current player is", username)

                SpeakText(
                    "Squares are labelled 1 to 9. Say the square you would like to play in next"
                )
                try:
                    ans = getMove()
                except:
                    SpeakText("Please say a number between 1 and 9")
                    ans = getMove()

                if ans == "eat":
                    ans = 8
                elif ans.isdigit():
                    ans = int(ans)
                rowCol = moves[ans]
                row, col = int(rowCol[0]), int(rowCol[1])
                if grid[row][col] == BLANK:
                    if player == X:
                        grid[row][col] = emoji.emojize(":alien:", variant = "emoji_type")
                    if player == O:
                        grid[row][col] = emoji.emojize(":collision:",  variant = "emoji_type")

                    if player == X:
                        player = O
                    else:
                        player = X
                    print_grid("Current grid:", grid)
            else:
                print("Current player is", player, "(Computer)")
                row, col = minimax_decision(game, grid)
                SpeakText(f"Computer played in ({findMoveSquare(row, col, moves)})")

                if grid[row][col] == BLANK:
                    if player == X:
                        grid[row][col] = emoji.emojize(":alien:",  variant = "emoji_type")
                    if player == O:
                        grid[row][col] = emoji.emojize(":collision:",  variant = "emoji_type")
                    # grid[row][col] = player
                    if player == X:
                        player = O
                    else:
                        player = X
                    print_grid("Current grid:", grid)

        winner = game.winner(grid)

        if winner == X:
            statement = random.choice(lose_statements)
            SpeakText(statement)
        elif winner == O:
            statement = random.choice(win_statements)
            SpeakText(statement)
        else:
            SpeakText("It was a draw")
    except:
        SpeakText("An unexpected error seems to have occurred. Let's try this again")
        play_game()


def findMoveSquare(row, col, moveDict):
    """
    It takes a row and column number and a dictionary of squares and their row and column numbers and
    returns the square number that corresponds to the row and column number

    :param row: the row of the square you want to move to
    :param col: the column of the square you want to move to
    :param moveDict: a dictionary that maps the square number to the row and column of the square
    :return: A set of the square numbers that have the row and column values passed in.
    """
    rowCol = [row, col]
    squareNum = {index for index in moveDict if moveDict[index] == rowCol}
    return squareNum


if __name__ == "__main__":
    # play_game()
    print(emoji.emojize(" collistion :collision:"))