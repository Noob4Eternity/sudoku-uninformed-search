import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import copy
import time
from letters_transform import to_letters, to_numbers, check_if_letters
from BFS_Sudoku import Problem, Node
# Assuming all the helper functions and classes are defined above (`Problem`, `Node`, etc.)

def draw_board(board, initial_board, ax, title='Sudoku Solver'):
    """
    Function to draw the current state of the Sudoku board using matplotlib.
    Original digits are black, and solver-entered digits are blue.
    """
    # Create a grid
    ax.clear()
    ax.set_title(title, fontsize=14)
    ax.set_xticks(np.arange(-0.5, 9, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 9, 1), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=2)

    # Set the background color for each cell
    cmap = ListedColormap(["white", "lightgrey"])
    background = [[1 if ((i // 3) + (j // 3)) % 2 == 0 else 0 for j in range(9)] for i in range(9)]
    ax.imshow(background, cmap=cmap)

    # Populate the board
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                color = 'black' if initial_board[i][j] != 0 else 'blue'
                ax.text(j, i, str(board[i][j]), va='center', ha='center', fontsize=14, weight='bold', color=color)

    # Hide axes
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    plt.pause(0.1)

def DFS_visualize(problem, initial_board, ax):
    """
    Modified DFS function to visualize the solving process using matplotlib.
    """
    # Create initial node of problem tree holding the original board
    start = Node(problem.initial)
    if problem.check_legal(start.state):
        draw_board(start.state, initial_board, ax, title="Solved!")
        return start.state

    stack = []
    stack.append(start)  # Places the root node on the stack

    while stack:
        node = stack.pop()  # Pops the last node, tests legality, then expands the same popped node
        draw_board(node.state, initial_board, ax, title="Solving...")  # Draw the current board state

        if problem.check_legal(node.state):
            draw_board(node.state, initial_board, ax, title="Solved!")  # Draw the final solved board
            return node.state

        stack.extend(node.expand(problem))
    
    draw_board(node.state, initial_board, ax, title="No Solution Found")
    return None

def H_Solve_Visualizer(board):
    print("\nSolving with DFS and heuristics...")
    letters = False
    if check_if_letters(board):  # Checks if the board contains letters instead of numbers
        board = to_numbers(board)  # Transforms letter puzzles to numeric puzzles
        letters = True

    # Create a copy of the initial board to distinguish original vs. solver-entered digits
    initial_board = copy.deepcopy(board)

    # Set up the visualizer
    fig, ax = plt.subplots()
    draw_board(board, initial_board, ax, title="Initial Board")

    start_time = time.time()
    problem = Problem(board)
    solution = DFS_visualize(problem, initial_board, ax)

    elapsed_time = time.time() - start_time

    if solution:
        if letters:
            solution = to_letters(solution)  # Transforms back numeric puzzles to original letter puzzle type
        print("Found solution:")
        for row in solution:
            print(row)
    else:
        print("No possible solutions")

    print("Elapsed time: " + str(elapsed_time) + " seconds")
    plt.show()

# Example Sudoku board to solve
example_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Solve and visualize
H_Solve_Visualizer(example_board)
