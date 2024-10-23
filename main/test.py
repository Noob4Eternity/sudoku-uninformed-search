import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from queue import Queue
import copy
import time

class Problem(object):

    def __init__(self, initial):
        self.initial = initial
        self.size = len(initial)  # Size of a grid
        self.height = int(self.size / 3)  # Size of a quadrant

    def filter_values(self, values, used):
        """Return set of valid numbers from values that do not appear in used."""
        return [number for number in values if number not in used]

    def get_spot(self, board, state):
        """Return first empty spot on grid (marked with 0)."""
        for row in range(board):
            for column in range(board):
                if state[row][column] == 0:
                    return row, column   

    def actions(self, state):
        """Generate valid moves based on Sudoku rules."""
        number_set = range(1, self.size + 1)
        in_column = []
        in_block = []

        row, column = self.get_spot(self.size, state)

        # Filter valid values based on row
        in_row = [number for number in state[row] if number != 0]
        options = self.filter_values(number_set, in_row)

        # Filter valid values based on column
        for column_index in range(self.size):
            if state[column_index][column] != 0:
                in_column.append(state[column_index][column])
        options = self.filter_values(options, in_column)

        # Filter valid values based on quadrant
        row_start = int(row / self.height) * self.height
        column_start = int(column / 3) * 3
        
        for block_row in range(self.height):
            for block_column in range(3):
                in_block.append(state[row_start + block_row][column_start + block_column])
        options = self.filter_values(options, in_block)

        for number in options:
            yield number, row, column

    def result(self, state, action):
        """Returns updated board after adding new valid value."""
        play, row, column = action
        new_state = copy.deepcopy(state)
        new_state[row][column] = play
        return new_state

    def check_legal(self, state):
        """Use sums of each row, column, and quadrant to determine validity of board state."""
        total = sum(range(1, self.size + 1))

        # Check rows and columns
        for row in range(self.size):
            if len(state[row]) != self.size or sum(state[row]) != total:
                return False

            column_total = 0
            for column in range(self.size):
                column_total += state[column][row]

            if column_total != total:
                return False

        # Check quadrants
        for column in range(0, self.size, 3):
            for row in range(0, self.size, self.height):
                block_total = 0
                for block_row in range(self.height):
                    for block_column in range(3):
                        block_total += state[row + block_row][column + block_column]

                if block_total != total:
                    return False

        return True

class Node:

    def __init__(self, state, action=None):
        self.state = state
        self.action = action

    def expand(self, problem):
        """Use each action to create a new board state."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """Return node with new board state."""
        next_state = problem.result(self.state, action)
        return Node(next_state, action)

def draw_board(board, initial_board, ax, title='Sudoku Solver'):
    """Function to draw the current state of the Sudoku board using matplotlib."""
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

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    plt.pause(0.1)

def BFS_visualize(problem, initial_board, ax):
    """Modified BFS function to visualize the solving process using matplotlib."""
    node = Node(problem.initial)
    if problem.check_legal(node.state):
        draw_board(node.state, initial_board, ax, title="Solved!")
        return node

    frontier = Queue()
    frontier.put(node)

    while frontier.qsize() != 0:
        node = frontier.get()
        draw_board(node.state, initial_board, ax, title="Solving...")

        for child in node.expand(problem):
            if problem.check_legal(child.state):
                draw_board(child.state, initial_board, ax, title="Solved!")
                return child

            frontier.put(child)

    draw_board(node.state, initial_board, ax, title="No Solution Found")
    return None

def BFS_solve_visualizer(board):
    print("\nSolving with BFS and Visualizer...")
    initial_board = copy.deepcopy(board)
    fig, ax = plt.subplots()
    draw_board(board, initial_board, ax, title="Initial Board")

    start_time = time.time()
    problem = Problem(board)
    solution = BFS_visualize(problem, initial_board, ax)
    elapsed_time = time.time() - start_time

    if solution:
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

BFS_solve_visualizer(example_board)
