from tkinter import *
depth = 0
max_depth = 100

def display_grid(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                entry_boxes[i][j].delete(0, END)
                entry_boxes[i][j].insert(0, str(grid[i][j]))
                entry_boxes[i][j].config(justify=CENTER)
            else:
                entry_boxes[i][j].delete(0, END)
                entry_boxes[i][j].config(justify=CENTER)

def load_grid_from_ui():
    grid = []
    entry_index = 0
    for i in range(9):
        row = []
        for j in range(9):
            value = entry_boxes[i][j].get()
            if value.isdigit():
                row.append(int(value))
            else:
                row.append(0)
                entry_index +=1
        grid.append(row)
    return grid

def check_sudoku():
    input_grid = load_grid_from_ui()

    if not is_valid_sudoku(input_grid):
        result_label.config(text="Invalid Sudoku")
        clear_completed_grid()
        completed_frame.grid_forget()  # Hide the completed Sudoku grid frame

    elif solve_sudoku(input_grid, depth, max_depth):
        display_completed_grid(input_grid)
        result_label.config(text="Solved Sudoku")
        completed_frame.grid(row=5, columnspan=9)
    else:
        result_label.config(text="No solution exists.")
        clear_completed_grid()
        completed_frame.grid_forget()
def clear_completed_grid():
    for i in range(9):
        for j in range(9):
            completed_boxes[i][j].delete(0, END)
def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None


def is_valid_sudoku(grid):
    # Check rows
    for row in grid:
        if not is_valid_set(row):
            return False

    # Check columns
    for col in range(9):
        column = [grid[row][col] for row in range(9)]
        if not is_valid_set(column):
            return False

    # Check boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = [grid[row][col] for row in range(box_row, box_row + 3) for col in range(box_col, box_col + 3)]
            if not is_valid_set(box):
                return False

    return True

def is_valid_set(nums):
    # Check if a list of numbers has no duplicates (0 is considered an empty cell)
    seen = set()
    for num in nums:
        if num != 0 and num in seen:
            return False
        seen.add(num)
    return True
def is_valid_move(grid, num, row, col):
    return (
        is_valid_in_row(grid, num, row) and
        is_valid_in_column(grid, num, col) and
        is_valid_in_box(grid, num, row, col)
    )

def is_valid_in_row(grid, num, row):
    return num not in grid[row]

def is_valid_in_column(grid, num, col):
    return all(grid[i][col] != num for i in range(9))

def is_valid_in_box(grid, num, row, col):
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False
    return True

def solve_sudoku(grid, depth, max_depth):
    if depth > max_depth:
        return False
    else:
        empty_cell = find_empty_cell(grid)
        if not empty_cell:
            return True

        row, col = empty_cell

        for num in range(1, 10):
            if is_valid_move(grid, num, row, col):
                grid[row][col] = num
                if solve_sudoku(grid, depth + 1, max_depth):
                    return True
                grid[row][col] = 0

        return False
def display_completed_grid(grid):
    for box_row in range(3):
        for box_col in range(3):
            for i in range(3):
                for j in range(3):
                    row = box_row * 3 + i
                    col = box_col * 3 + j

                    completed_boxes[row][col].config(state='normal')  # Temporarily make it editable
                    completed_boxes[row][col].delete(0, END)
                    completed_boxes[row][col].insert(0, str(grid[row][col]))
                    completed_boxes[row][col].config(justify=CENTER)
                    completed_boxes[row][col].config(state='readonly')  # Make it read-only again



root = Tk()
root.title("Sudoku Solver GUI")

Text = Label(root, text='Fill out the known boxes and hit the "Solve Sudoku" button for the soloution')
Text.grid(row=0, columnspan=9)

frame = Frame(root, padx=10, pady=10)
frame.grid(row=1, columnspan=9)

entry_boxes = [[None for _ in range(9)] for _ in range(9)]

for i in range(3):
    for j in range(3):
        grouped_frame = Frame(frame, padx=0, pady=0, bd=1, relief="sunken")
        grouped_frame.grid(row=i, column=j)  # Create a 3x3 grid of grouped_frame

        row_entries = []  # Initialize row_entries here
        for a in range(3):
            for b in range(3):
                grouped_frame = Frame(frame, padx=0, pady=0, bd=1, relief="sunken")
                grouped_frame.grid(row=i, column=j)  # Create a 3x3 grid of grouped_frame


                for a in range(3):
                    for b in range(3):
                        entry_frame = Frame(grouped_frame, padx=0, pady=0, bd=0)
                        entry_frame.grid(row=a, column=b)  # Create a 3x3 grid of entry_frame

                        entry = Entry(entry_frame, width=3)
                        entry.grid(row=a, column=b)  # Place Entry widgets in a 3x3 grid within each entry_frame

                        # Calculate the actual row and column in the 9x9 grid
                        actual_row = 3 * i + a
                        actual_col = 3 * j + b

                        # Store the entry in the correct position in entry_boxes
                        entry_boxes[actual_row][actual_col] = entry

# Create a button to check the Sudoku
check_button = Button(root, text="Solve Sudoku", command=check_sudoku)
check_button.grid(row=2, columnspan=9, pady=10)

result_label = Label(root, text="")
result_label.grid(row=3, columnspan=9)

# Create Entry widgets to display the completed Sudoku grid


completed_frame = Frame(root, padx=10, pady=10)
completed_frame.grid(row=5, columnspan=9)
completed_frame.grid_forget()  # Hide the completed Sudoku grid frame initially

completed_boxes = []
for box_row in range(3):
    for box_col in range(3):
        box_frame = Frame(completed_frame, padx=0, pady=0, bd=1, relief="sunken")
        box_frame.grid(row=box_row, column=box_col)

        for i in range(3):
            for j in range(3):
                row = box_row * 3 + i
                col = box_col * 3 + j

                entry_frame = Frame(box_frame, padx=0, pady=0, bd=0)
                entry_frame.grid(row=i, column=j)

                entry = Entry(entry_frame, width=3, state="readonly")
                entry.grid(row=0, column=0)  # Place Entry widget in the entry_frame

                # Store the entry in the correct position in completed_boxes
                if len(completed_boxes) <= row:
                    completed_boxes.append([])
                completed_boxes[row].append(entry)

root.mainloop()
