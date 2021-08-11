# bot.py
import os
import time
import tictactoe as ttt
import keep_alive
import random

from discord.ext import commands

# Get Discord BOT Token from enivornment variables
TOKEN = os.environ["DISCORD_TOKEN"]

# Setting global variables
user = None
board = ttt.initial_state()
game_over = ttt.terminal(board)
player = ttt.player(board)

# Starts a new fresh game
def restart():
    global user
    global board
    user = None
    board = ttt.initial_state()


# Informs current game status
def game_status():
    game_over = ttt.terminal(board)
    player = ttt.player(board)
    return (game_over, player)


# Helper function to show X/O/Cell Number
def get_value(value, index):
    if value:
        return value
    else:
        return index


# Helper dictionary to convert user input to board cell
INPUT_TO_RESULT = {
    "1": [0, 0],
    "2": [0, 1],
    "3": [0, 2],
    "4": [1, 0],
    "5": [1, 1],
    "6": [1, 2],
    "7": [2, 0],
    "8": [2, 1],
    "9": [2, 2],
}

# Helper function to print current board
def print_board():
    val1 = (
        " "
        + str(get_value(board[0][0], 1))
        + " \t|\t "
        + str(get_value(board[0][1], 2))
        + " \t|\t "
        + str(get_value(board[0][2], 3))
        + "  \t"
    )
    val2 = "\n--------------------"
    val3 = (
        " "
        + str(get_value(board[1][0], 4))
        + " \t|\t "
        + str(get_value(board[1][1], 5))
        + " \t|\t "
        + str(get_value(board[1][2], 6))
        + "  \t"
    )
    val4 = "\n--------------------"
    val5 = (
        " "
        + str(get_value(board[2][0], 7))
        + " \t|\t "
        + str(get_value(board[2][1], 8))
        + " \t|\t "
        + str(get_value(board[2][2], 9))
        + "  \t"
    )
    return "\n".join([val1, val2, val3, val4, val5])


# Helper function to print fresh board
def fresh_board():
    val1 = " " + str(1) + " \t|\t " + str(2) + " \t|\t " + str(3) + "  \t"
    val2 = "\n--------------------"
    val3 = " " + str(4) + " \t|\t " + str(5) + " \t|\t " + str(6) + "  \t"
    val4 = "\n--------------------"
    val5 = " " + str(7) + " \t|\t " + str(8) + " \t|\t " + str(9) + "  \t"
    return "\n".join([val1, val2, val3, val4, val5])


# Helper function to play AI's move
def ai_turn():
    global board

    # Corner moves as for a first move, this is usually the best move
    corner_moves = [[0, 0], [0, 2], [2, 0], [2, 2]]
    # Check if board is currently empty or not
    all_moves = [val is None for sublist in board for val in sublist]

    # If board empty, select from corner_moves
    if sum(all_moves) == len(all_moves):
        move = corner_moves[random.randint(0, 3)]
        board = ttt.result(board, move)
    # Select from minimax algorithm
    else:
        move = ttt.minimax(board)
        board = ttt.result(board, move)


# Helper function to check if game is finished or not and send appropiate message
def finished():
    global board
    game_over = ttt.terminal(board)
    if game_over:
        winner = ttt.winner(board)
        if winner is None:
            result = f"Game Over: `Tie.`"
        else:
            if winner == user:
                person = "You"
            else:
                person = "AI"
            result = f"Game Over: Winner is `{person}!`"
        return result
    return False


# Prefix command that must be provided and the bot will be listening too
bot = commands.Bot(command_prefix="!ttt ")

# Starts the game and if user is defined, it will restart the game
@bot.command(name="start", help="Starts a new Tic Tac Toe Game!")
async def start(ctx):

    if user is not None:
        restart()

    await ctx.send("`Tic Tac Toe!`")
    await ctx.send("Ready to play against a `super AI?`")
    await ctx.send(
        "Use the `!ttt play` command followed by either `X` or `O` to get started!"
    )
    await ctx.send("Use the `!ttt rules` command to go through the game rules.")


# Shows the main game rules
@bot.command(name="rules", help="Learn the game rules")
async def rules(ctx):

    await ctx.send("You will be playing against the AI in a `3 x 3` game!")
    await ctx.send(fresh_board())
    await ctx.send(
        "Input where you want to place yourself by using `!ttt select (1 - 9)`"
    )
    await ctx.send("For example: `!ttt select 1`")
    await ctx.send(
        "First to either have 3 of themselves in a straight line or diagonally `wins!`"
    )


# Select X/O to play
@bot.command(name="play", help="Select which character to play with")
async def play(ctx, character=None):
    # Get game status
    game_over, _ = game_status()
    # If game currently over, ask user to start again
    if game_over:
        return await ctx.send(
            "Current game is over! Type `!ttt start` and get ready for the next round!"
        )
    # If input not provided, send error message
    if character == None:
        return await ctx.send("You must select either `'X'` or `'O'`!")
    global user
    # Check if user has provided X, x, O, o
    if user is None:
        if character in ["X", "x"]:
            user = ttt.X
            await ctx.send("You've selected `X` and will go `first!`")
            await rules(ctx)
        elif character in ["O", "o"]:
            # If user has selected O, then AI will go first
            user = ttt.O
            await ctx.send("You've selected `O` and will go `second!`")
            await ctx.send("`Ai is thinking...`")
            time.sleep(0.5)
            ai_turn()
            await ctx.send(print_board())
            await ctx.send("Your turn `now!`")
        else:
            await ctx.send("You must select either `'X'` or `'O'!`")
    # If user is already selected and still this command was provided, send error
    else:
        await ctx.send(f"You are already playing as `{user}`")


# Select which cell to play
@bot.command(name="select", help="Select cell to play")
async def select(ctx, cell_number=None):
    global board
    # If cell number not provided, send error
    if cell_number == None:
        return await ctx.send(f"You must select a place between `(1 - 9)!`")
    game_over, player = game_status()
    # If game over, ask user to start again as no point in allowing board selection
    if game_over:
        return await ctx.send(
            "Current game is over! Type `!ttt start` and get ready for the next round!"
        )
    if user == player and not game_over:
        # Check for correct cell number
        if cell_number not in [str(i) for i in range(1, 10)]:
            await ctx.send(f"You must select a place between `(1 - 9)!`")
        else:
            await ctx.send(f"You've selected: `{cell_number}`")
            # Check if current cell number is empty
            try:
                result = INPUT_TO_RESULT[cell_number]
                board = ttt.result(board, (result[0], result[1]))
                await ctx.send(print_board())
                # Check if game is finished with this move
                response = finished()
                if response:
                    return await ctx.send(response)
                # Make AI play
                await ctx.send("`Ai is thinking...`")
                time.sleep(0.5)
                ai_turn()
                await ctx.send(print_board())
                # Check if game is finished with this move
                response = finished()
                if response:
                    return await ctx.send(response)
                await ctx.send("Your turn `again!`")
            except ValueError:
                # If not able to place the piece, send error
                await ctx.send("There is `already` a piece there!")
    else:
        # If game has not started, user variable will be None
        if user is None:
            await ctx.send(f"Game has not started yet!")
            await ctx.send(
                f"Use the `!ttt play` command followed by either `X` or `O` to get started!"
            )
        # Game has started but it's currently AI's turn
        else:
            await ctx.send(f"It's `not` your turn!")


# Show current board status
@bot.command(name="board", help="Print the current board")
async def current_board(ctx):
    await ctx.send(print_board())


# Run server and run the bot
keep_alive.keep_alive()
bot.run(TOKEN)