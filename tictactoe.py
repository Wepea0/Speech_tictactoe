import sys
import copy
import random
from TextToSpeech_Test1 import *


INF = sys.maxsize


class Game:
    def __init__(self, init_state):
        self.init_state = init_state

    def __str__(self):
        return "Init_state=" + str(self.init_state)

    # placeholder, to be overridden in derived class
    def terminal_test(self, state):
        return True

    # placeholder, to be overriden in derived class
    def utility(self, state):
        return 0

    # placeholder, to be overriden in derived class
    def actions(self, state):
        moves = []
        return moves

    # placeholder, to be overriden in derived class
    def result(self, state, action):
        return state


BLANK = "_"
X = "X"
O = "O"
EMPTY_GRID = [[BLANK, BLANK, BLANK], [BLANK, BLANK, BLANK], [BLANK, BLANK, BLANK]]


class TicTacToe(Game):
    def __init__(self):
        super().__init__(copy.deepcopy(EMPTY_GRID))
        self.player = "X"

    def terminal_test(self, state):
        # if there is no empty space then it's a terminal state
        if not (BLANK in state[0] or BLANK in state[1] or BLANK in state[2]):
            return True

        # otherwise, if there's a winner, it's a terminal state
        winner = self.winner(state)
        return winner == X or winner == O

    def winner(self, state):
        # check each row for a winning configuration
        for row in [0, 1, 2]:
            if (
                state[row][0] != BLANK
                and state[row][0] == state[row][1]
                and state[row][0] == state[row][2]
            ):
                return state[row][0]

        # check each column for a winner configuration
        for col in [0, 1, 2]:
            if (
                state[0][col] != BLANK
                and state[0][col] == state[1][col]
                and state[0][col] == state[2][col]
            ):
                return state[0][col]

        # check the top left to bottom right diagonal
        if (
            state[0][0] != BLANK
            and state[0][0] == state[1][1]
            and state[0][0] == state[2][2]
        ):
            return state[0][0]

        # check the bottom left to top right diagonal
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
    global n_levels, n_states, n_terminal_states, states
    n_levels = max(n_levels, level)
    if game.terminal_test(state):
        util = game.utility(state)
        # print_grid("Reached terminal state with utility "+str(util)+":",state)
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
    global n_levels, n_states, n_terminal_states, states
    n_levels = max(n_levels, level)
    if game.terminal_test(state):
        util = game.utility(state)
        # print_grid("Reached terminal state with utility "+str(util)+":",state)
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


def read_grid(prompt, grid):
    print(prompt)
    for row in range(3):
        vals = input()
        grid[row] = vals.split()


def print_grid(title, grid):
    print(title)
    for row in [0, 1, 2]:
        for col in [0, 1, 2]:
            print(grid[row][col], end=" ")
        print()


def grid_to_str(grid):
    return "".join(grid[0]) + "".join(grid[1]) + "".join(grid[2])


def test_terminal():
    game = TicTacToe()
    test_again = "Y"
    grid = copy.deepcopy(EMPTY_GRID)
    while test_again == "Y" or test_again == "y":
        read_grid("Enter a grid:", grid)
        print("Thanks. You entered", grid)
        print("String version: ", grid_to_str(grid))
        print("Terminal?", game.terminal_test(grid))
        print("Winner?", game.winner(grid))
        print("Utility?", game.utility(grid))
        test_again = input("Test again? (Y/N)")
    print("Bye!")


def test_move():
    game = TicTacToe()
    grid = copy.deepcopy(EMPTY_GRID)

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
    print("Heree")
    SpeakText("Greetings and welcome to Tic Tac Toe Deluxe. What is your name?\n>>> ")
    username = getMove()
    welcomeMessage = "Nice to meet you " + username
    SpeakText(welcomeMessage)
    SpeakText(
        "What difficulty would you like. Say 'Easy' for a warmup game and 'Normal' for a real test"
    )
    difficulty = getMove()

    while difficulty != "easy" and difficulty != "normal":
        SpeakText(
            "Incorrect choice! What difficulty would you like. Say 'Easy' for a warmup game and 'Normal' for a real test "
        )
        difficulty = getMove()
    SpeakText("Enter 1 to have the first turn and 2 to have the second turn\n>>> ")

    user_turn = int(getMove())
    while user_turn != 1 and user_turn != 2:

        SpeakText(
            "Incorrect input. Enter 1 to have the first turn and 2 to have the second turn"
        )
        user_turn = int(getMove())
    player = "O" if user_turn == 1 else "X"

    SpeakText("Game is about to start now...")
    print_grid("Current grid:", grid)

    while not game.terminal_test(grid):
        if player == O:
            print("Current player is", username)

            # print("Enter the row and col to play: ")

            SpeakText(
                "Squares are labelled 1 to 9. Say the square you would like to play in next"
            )
            ans = getMove()
            if ans == "eat":
                ans = 8
            elif ans.isdigit():
                ans = int(ans)
            rowCol = moves[ans]
            row, col = int(rowCol[0]), int(rowCol[1])
            print("You entered ", row, col)
            if grid[row][col] == BLANK:
                grid[row][col] = player
                if player == X:
                    player = O
                else:
                    player = X
                print_grid("Current grid:", grid)
            # else:
            #     SpeakText("Incorrect input. Squares are labelled 1 to 9. Say the square you would like to play in next")
            #     ans = getMove()
            #     while(ans not in moves and grid[moves[ans][0]][moves[ans][1]] != BLANK):
            #         SpeakText("Incorrect input. Squares are labelled 1 to 9. Say the square you would like to play in next")
            #         ans = int(getMove())
            #     rowCol = moves[ans]
            #     row, col = int(rowCol[0]), int(rowCol[1])
            #     grid[row][col] = player
            #     if player == X:
            #         player = O
            #     else:
            #         player = X
            #     print_grid("Current grid:", grid)

        else:
            print("Current player is", player, "(Computer)")

            # setting a 50% chance of 'dumb' decision
            if difficulty == "Easy".lower():
                prob = random.randint(1, 10)
                if prob > 5:
                    row, col = random.choice(game.actions(grid))
                else:
                    row, col = minimax_decision(game, grid)
            else:
                row, col = minimax_decision(game, grid)

            # acceptedMove  = findMoveSquare(row, col, moves)

            SpeakText(f"Computer played in ({findMoveSquare(row, col, moves)})")
            if grid[row][col] == BLANK:
                grid[row][col] = player
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
        SpeakText("It was a draw -_-")
        SpeakText("Say 'Yes' to play again and 'No' to quit")
    play_again = getMove()
    if play_again.lower() == "yes":
        SpeakText("Yess! Let's run this back")
        test_move()
    else:
        SpeakText("Sad to see you go :(")


def test_minimax():
    game = TicTacToe()
    test_again = "Y"
    grid = copy.deepcopy(EMPTY_GRID)
    while test_again == "Y" or test_again == "y":
        read_grid("Enter a grid for which it is X's turn", grid)
        print("Thanks. You entered", grid)
        action = minimax_decision(game, grid)
        print("\nThe best move for X is", action)
        print(
            "The game tree had",
            n_levels,
            "levels,",
            n_states,
            "states altogether, ",
            len(states),
            "unique states.",
            "It reached",
            n_terminal_states,
            "terminal states of which",
            len(terminal_states),
            "were unique.",
        )
        test_again = input("Another test? (Y/N)")


# Find the number of the square that corresponds to the row, column of
# the move that has just been played
def findMoveSquare(row, col, moveDict):
    rowCol = [row, col]
    squareNum = [list(moveDict.values()).index(rowCol)]
    return squareNum


if __name__ == "__main__":
    # test_terminal()
    test_move()
    # test_minimax()
