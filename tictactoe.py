"""
Tic Tac Toe Game Logic

Initial source code based on CS50AI project course: https://cs50.harvard.edu/ai/2020/projects/0/tictactoe/
Game logic completed by Ishmam Ahmed Chowdhury: https://github.com/Ishmam156
"""

import copy
import math

# Defining globals to keep track of game
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Stores all the possible values of the board in variables
    total_places = sum(1 for i in board for j in i)
    empty_places = sum(1 for i in board for j in i if j == None)
    x_moves = sum(1 for i in board for j in i if j == "X")
    o_moves = sum(1 for i in board for j in i if j == "O")

    # Check if start of the game
    if empty_places == total_places:
        return X
    # If X has more moves in the board than O
    elif x_moves > o_moves:
        return O
    # In all other cases, X plays
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Loop through the board and check all places which are EMPTY and add them to a single set
    return set(
        (i, j)
        for i, val1 in enumerate(board)
        for j, val2 in enumerate(val1)
        if val2 == EMPTY
    )


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Make deep copy of board
    new_board = copy.deepcopy(board)
    # Check whose turn it is
    turn = player(new_board)

    # Check if the action is a valid one
    if new_board[action[0]][action[1]] is None:
        # Make movie
        new_board[action[0]][action[1]] = turn
    else:
        raise ValueError("Not a valid action")

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # No winner at start
    winner = None

    for idx, _ in enumerate(board):
        # Single diagonal check
        if idx == 0:
            if (
                board[idx][idx] == board[idx + 1][idx + 1]
                and board[idx + 1][idx + 1] == board[idx + 2][idx + 2]
            ):
                winner = board[idx][idx]

        # Reverse diagonal check
        elif idx == 2:
            if (
                board[0][idx] == board[1][idx - 1]
                and board[1][idx - 1] == board[idx][idx - 2]
            ):
                winner = board[0][idx]

        # Horizontal Check
        if board[idx][0] == board[idx][1] and board[idx][1] == board[idx][2]:
            winner = board[idx][0]

        # Vertical Check
        elif board[0][idx] == board[1][idx] and board[1][idx] == board[2][idx]:
            winner = board[0][idx]

        # Check if there is winner
        if winner:
            return X if winner == "X" else O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Get status
    empty_places = sum(1 for i in board for j in i if j == None)
    won = winner(board)

    # Check if won or board full
    if won or not empty_places:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # Get winner
    won = winner(board)

    # Check for X and O
    if won == X:
        return 1
    elif won == O:
        return -1
    else:
        return 0


def max_value(board):
    """
    Returns highest possible score.
    """

    # Check if board is terminal
    if terminal(board):
        return utility(board)

    # Extreme value as a starting point
    v = -math.inf

    # Loop through the board
    for action in actions(board):
        # Get the value of the board
        value = min_value(result(board, action))
        score = max(v, value)

        # Check if score is higher than v
        if score > v:
            v = score
            # If already reached highest score, break out
            if v == 1:
                return v

    return v


def min_value(board):
    """
    Returns lowest possible score.
    """

    # Check if board is terminal
    if terminal(board):
        return utility(board)

    # Extreme value as a starting point
    v = math.inf

    # Loop through the board
    for action in actions(board):
        # Get the value of the board
        value = max_value(result(board, action))
        score = min(v, value)

        # Check if score is lower than v
        if score < v:
            v = score
            # If already reached lowest score, break out
            if v == -1:
                return v

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Check if terminal board
    if terminal(board):
        return None

    # Check whose turn it is
    turn = player(board)

    if turn == X:
        # Keep track of score and move
        best_move = {}
        # Loop through moves
        for moves in actions(board):
            # Store the score and action
            move = min_value(result(board, moves))
            best_move[move] = moves

            # If already found optimum move
            if max(best_move) == 1:
                return best_move[max(best_move)]

        return best_move[max(best_move)]

    else:
        # Keep track of score and move
        best_move = {}
        # Loop through moves
        for moves in actions(board):
            # Store the score and action
            move = max_value(result(board, moves))
            best_move[move] = moves

            # If already found optimum move
            if min(best_move) == -1:
                return best_move[min(best_move)]

        return best_move[min(best_move)]