import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import copy
import time
from letters_transform import to_letters, to_numbers, check_if_letters
class Node:
    
    def __init__(self, state):
        self.state = state

    def expand(self, problem):
        # Return list of valid states
        return [Node(state) for state in problem.actions(self.state)]

class Problem(object):

    def __init__(self, initial):
        self.initial = initial
        self.size = len(initial) # Size of grid
        self.height = int(self.size/3) # Size of a quadrant

    def check_legal(self, state):
        # Maximum sum of row, column or quadrant
        exp_sum = sum(range(1, self.size+1))

        # Returns false if expected sum of row or column are invalid
        for row in range(self.size):
            if (len(state[row]) != self.size) or (sum(state[row]) != exp_sum):
                return False
            column_sum = 0
            for column in range(self.size):
                column_sum += state[column][row]
            if (column_sum != exp_sum):
                return False

        # Returns false if expected sum of a quadrant is invalid
        for column in range(0,self.size,3):
            for row in range(0,self.size,self.height):
                block_sum = 0
                for block_row in range(0,self.height):
                    for block_column in range(0,3):
                        block_sum += state[row + block_row][column + block_column]

                if (block_sum != exp_sum):
                    return False
        return True

    # Return set of valid numbers from values that do not appear in used
    def filter_values(self, values, used):
        return [number for number in values if number not in used]

    # Return empty spot on grid with most constraints (least amount of options)
    def get_spot(self, board, state):
        target_option_len = board
        row = 0
        while row < board:
            column = 0
            while column < board:
                if state[row][column] == 0:
                    options = self.filter_row(state, row)
                    options = self.filter_col(options, state, column)
                    options = self.filter_quad(options, state, row, column)
                    if len(options) < target_option_len:
                        target_option_len = len(options)
                        options = []
                        spotrow = row
                        spotcol = column
                column = column + 1
            row = row + 1                
        return spotrow, spotcol

    # Filter valid values based on row
    def filter_row(self, state, row):
        number_set = range(1, self.size+1) # Defines set of valid numbers that can be placed on board
        in_row = [number for number in state[row] if (number != 0)]
        options = self.filter_values(number_set, in_row)
        return options

    # Filter valid values based on column
    def filter_col(self, options, state, column):
        in_column = []
        for column_index in range(self.size):
            if state[column_index][column] != 0:
                in_column.append(state[column_index][column])
        options = self.filter_values(options, in_column)
        return options

    # Filter valid values based on quadrant
    def filter_quad(self, options, state, row, column):
        in_block = [] # List of valid values in spot's quadrant
        row_start = int(row/self.height)*self.height
        column_start = int(column/3)*3
        
        for block_row in range(0, self.height):
            for block_column in range(0,3):
                in_block.append(state[row_start + block_row][column_start + block_column])
        options = self.filter_values(options, in_block)
        return options    

    def actions(self, state):
        row,column = self.get_spot(self.size, state) # Get first empty spot on board

        # Remove a square's invalid values
        options = self.filter_row(state, row)
        options = self.filter_col(options, state, column)
        options = self.filter_quad(options, state, row, column)

        # Return a state for each valid option (yields multiple states)
        for number in options:
            new_state = copy.deepcopy(state) # Norvig used only shallow copy to copy states; deepcopy works like a perfect clone of the original
            new_state[row][column] = number
            yield new_state


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
example_board =[[0,3,0,0,0,1,5,0,0], # very hard
      [0,0,0,5,0,0,0,8,4],
      [0,0,5,0,0,7,0,6,0],
      [0,0,0,0,0,0,0,0,0],
      [0,8,0,2,0,0,0,7,0],
      [0,0,0,8,5,0,0,0,9],
      [0,0,3,0,9,4,0,0,7],
      [0,0,4,0,0,0,0,0,8],
      [5,0,6,0,1,0,0,0,0]]


# Solve and visualize
H_Solve_Visualizer(example_board)
