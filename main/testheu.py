import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import copy
import time

# Check if the board is correctly filled
def check_legal(state):
    exp_sum = 45  # Sum for a row, column, or quadrant in 9x9 Sudoku

    # Check rows and columns
    for row in range(9):
        if (len(state[row]) != 9) or (sum(state[row]) != exp_sum):
            return False
        column_sum = 0
        for column in range(9):
            column_sum += state[column][row]
        if column_sum != exp_sum:
            return False

    # Check quadrants
    for column in range(0, 9, 3):
        for row in range(0, 9, 3):
            block_sum = 0
            for block_row in range(3):
                for block_column in range(3):
                    block_sum += state[row + block_row][column + block_column]
            if block_sum != exp_sum:
                return False

    return True

# Return set of valid numbers that do not appear in used
def filter_values(values, used):
    return [number for number in values if number not in used]

# Return empty spot on grid with most constraints (least amount of options)
def get_spot(board):
    target_option_len = 9
    spot_row, spot_col = None, None

    for row in range(9):
        for column in range(9):
            if board[row][column] == 0:
                options = filter_row(board, row)
                options = filter_col(options, board, column)
                options = filter_quad(options, board, row, column)
                if len(options) < target_option_len:
                    target_option_len = len(options)
                    spot_row, spot_col = row, column

    return spot_row, spot_col

# Filter valid values based on row
def filter_row(state, row):
    number_set = range(1, 10)
    in_row = [number for number in state[row] if number != 0]
    options = filter_values(number_set, in_row)
    return options

# Filter valid values based on column
def filter_col(options, state, column):
    in_column = [state[row][column] for row in range(9) if state[row][column] != 0]
    options = filter_values(options, in_column)
    return options

# Filter valid values based on quadrant
def filter_quad(options, state, row, column):
    in_block = []
    row_start = (row // 3) * 3
    column_start = (column // 3) * 3

    for block_row in range(3):
        for block_column in range(3):
            in_block.append(state[row_start + block_row][column_start + block_column])
    
    options = filter_values(options, in_block)
    return options

# Generate possible actions (states) for the next move
def generate_actions(state):
    row, column = get_spot(state)

    if row is None or column is None:
        return []

    # Get valid values for the selected spot
    options = filter_row(state, row)
    options = filter_col(options, state, column)
    options = filter_quad(options, state, row, column)

    # Generate new states for each valid option
    new_states = []
    for number in options:
        new_state = copy.deepcopy(state)
        new_state[row][column] = number
        new_states.append(new_state)

    return new_states

# Function to draw the current state of the Sudoku board
def draw_board(board, initial_board, ax, title='Sudoku Solver'):
    ax.clear()
    ax.set_title(title, fontsize=14)
    ax.set_xticks(np.arange(-0.5, 9, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 9, 1), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=2)

    cmap = ListedColormap(["white", "lightgrey"])
    background = [[1 if ((i // 3) + (j // 3)) % 2 == 0 else 0 for j in range(9)] for i in range(9)]
    ax.imshow(background, cmap=cmap)

    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                color = 'black' if initial_board[i][j] != 0 else 'blue'
                ax.text(j, i, str(board[i][j]), va='center', ha='center', fontsize=14, weight='bold', color=color)

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    plt.pause(0.1)

# Modified DFS function to visualize the solving process
def DFS_visualize(initial_board, ax):
    board = copy.deepcopy(initial_board)
    if check_legal(board):
        draw_board(board, initial_board, ax, title="Solved!")
        return board

    stack = [board]

    while stack:
        current = stack.pop()
        draw_board(current, initial_board, ax, title="Solving...")

        if check_legal(current):
            draw_board(current, initial_board, ax, title="Solved!")
            return current

        stack.extend(generate_actions(current))

    draw_board(current, initial_board, ax, title="No Solution Found")
    return None

# Solve and visualize the Sudoku board
def H_Solve_Visualizer(board):
    print("\nSolving with DFS and heuristics...")

    initial_board = copy.deepcopy(board)
    fig, ax = plt.subplots()
    draw_board(board, initial_board, ax, title="Initial Board")

    start_time = time.time()
    solution = DFS_visualize(initial_board, ax)
    elapsed_time = time.time() - start_time

    if solution:
        print("Found solution:")
        for row in solution:
            print(row)
    else:
        print("No possible solutions")

    print("Elapsed time: " + str(elapsed_time) + " seconds")
    plt.show()

# Example Sudoku board to solve
example_board = [[0, 3, 0, 0, 0, 1, 5, 0, 0],
                 [0, 0, 0, 5, 0, 0, 0, 8, 4],
                 [0, 0, 5, 0, 0, 7, 0, 6, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 8, 0, 2, 0, 0, 0, 7, 0],
                 [0, 0, 0, 8, 5, 0, 0, 0, 9],
                 [0, 0, 3, 0, 9, 4, 0, 0, 7],
                 [0, 0, 4, 0, 0, 0, 0, 0, 8],
                 [5, 0, 6, 0, 1, 0, 0, 0, 0]]

# Solve and visualize
H_Solve_Visualizer(example_board)
