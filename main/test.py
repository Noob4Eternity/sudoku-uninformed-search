import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from queue import Queue
import copy
import time
from BFS_Sudoku import Problem, Node, check_if_letters, to_numbers, to_letters
# Assuming all functions from the previous code (`Problem`, `Node`, etc.) are imported or defined above

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


def BFS_visualize(problem, initial_board, ax):
    """
    Modified BFS function to visualize the solving process using matplotlib.
    """
    # Create initial node of problem tree holding original board
    node = Node(problem.initial)
    # Check if original board is correct and immediately return if valid
    if problem.check_legal(node.state):
        draw_board(node.state, initial_board, ax, title="Solved!")
        return node

    frontier = Queue()
    frontier.put(node)

    # Loop until all nodes are explored or solution found
    while (frontier.qsize() != 0):

        node = frontier.get()
        draw_board(node.state, initial_board, ax, title="Solving...")  # Draw the current board state

        for child in node.expand(problem):
            if problem.check_legal(child.state):
                draw_board(child.state, initial_board, ax, title="Solved!")  # Draw the final solved board
                return child

            frontier.put(child)

    draw_board(node.state, initial_board, ax, title="No Solution Found")
    return None

def BFS_solve_visualizer(board):
    print("\nSolving with BFS and Visualizer...")
    
    # Check if the board contains letters instead of numbers
    letters = False
    if check_if_letters(board): 
        board = to_numbers(board)  # Transform letter puzzles to numeric puzzles
        letters = True

    # Create a copy of the initial board to distinguish original vs. solver-entered digits
    initial_board = copy.deepcopy(board)

    # Set up the visualizer
    fig, ax = plt.subplots()
    draw_board(board, initial_board, ax, title="Initial Board")

    start_time = time.time()

    problem = Problem(board)
    solution = BFS_visualize(problem, initial_board, ax)

    elapsed_time = time.time() - start_time

    if solution:
        if letters:
            solution.state = to_letters(solution.state)  # Convert back to letters if needed
        print("Found solution:")
        for row in solution.state:
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
BFS_solve_visualizer(example_board)
