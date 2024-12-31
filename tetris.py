import sys

# Define the Tetris shapes in their fixed orientations.
# For simplicity, we define each shape as a list of (x, y) offsets,
# with y=0 as the *bottom* row of the shape. This is important
# so that our "drop until collision" logic can work from row=0 upward.

SHAPES = {
    'I': [(0, 0), (1, 0), (2, 0), (3, 0)],  # 4 wide, 1 tall
    'Q': [(0, 0), (1, 0), (0, 1), (1, 1)],  # 2x2 square
    'S': [(1, 0), (2, 0), (0, 1), (1, 1)],  # "S" shape, 3 wide, 2 tall
    'Z': [(0, 0), (1, 0), (1, 1), (2, 1)],  # "Z" shape, 3 wide, 2 tall
    'T': [(0, 0), (1, 0), (2, 0), (1, 1)],  # "T" shape, 3 wide, 2 tall
    'L': [(0, 0), (1, 0), (2, 0), (0, 1)],  # "L" shape, 3 wide, 2 tall
    'J': [(0, 0), (1, 0), (2, 0), (2, 1)],  # "J" shape, 3 wide, 2 tall
}

NUM_ROWS = 100
NUM_COLS = 10


def can_place(grid, shape, bottom_row, left_col):
    """
    Return True if the piece with given shape can be placed
    such that the bottom-left corner of its bounding box is
    at (bottom_row, left_col) in the grid, without collision
    and without going out of bounds.
    """
    for (dx, dy) in shape:
        # The square is at grid position (row, col) = (bottom_row + dy, left_col + dx).
        row = bottom_row + dy
        col = left_col + dx
        # Check vertical bounds
        if row < 0 or row >= NUM_ROWS:
            return False
        # Check horizontal bounds
        if col < 0 or col >= NUM_COLS:
            return False
        # Check collision with existing blocks
        if grid[row][col]:
            return False
    return True

def print_grid(grid):
    for row in grid:
        print(''.join(['#' if cell else '.' for cell in row]))
    print()

def place_piece(grid, shape, bottom_row, left_col):
    """
    Place the piece onto the grid at the given bottom_row, left_col
    by marking those cells as occupied (True).
    """
    for (dx, dy) in shape:
        row = bottom_row + dy
        col = left_col + dx
        grid[row][col] = True


def clear_full_rows(grid):
    """
    Remove any fully filled rows from the grid and shift everything
    above them downward. The shape of each row remains intact; we
    simply drop rows as a whole.
    """
    new_grid = []
    for row in range(NUM_ROWS):
        if not all(grid[row]):  # keep any row that's not completely filled
            new_grid.append(grid[row])

    # Count how many rows have been removed
    removed_count = NUM_ROWS - len(new_grid)

    # Add empty rows on top to keep grid size the same (100 rows)
    for _ in range(removed_count):
        new_grid.insert(0, [False] * NUM_COLS)

    # The new_grid now has the bottom rows first, top rows last
    return new_grid


def get_stack_height(grid):
    """
    Return the height of the stack.
    """
    height = 0
    for row in reversed(range(NUM_ROWS)):
        if any(grid[row]):
            height += 1
    return height


def process_line(line):
    """
    Given one line from the input (e.g. 'I0,I4,Q8'), parse each piece
    and its left-column. Then drop them into an empty grid. Finally,
    return the resulting stack height.
    """
    # Initialize a 100 x 10 grid of False (empty)
    grid = [[False] * NUM_COLS for _ in range(NUM_ROWS)]

    # Each item in line is 'Letter<col>' (e.g. 'Q0', 'I4')
    pieces = line.split(',')
    piece_count = 0
    for item in pieces:
        piece_count += 1
        shape_letter = item[0]
        left_str = item[1:]
        left = int(left_str)  # the left-most column for the piece

        shape = SHAPES[shape_letter]

        # We simulate "dropping" the piece from row=0 upwards until collision.
        # We'll track the row where the *bottom* of the shape ends up.
        # the shape bottom starts with the shape fitting into the grid i.e.
        # the bottom_row is the max y value of the shape
        bottom_row = max([shape_point[1] - 1 for shape_point in shape])
        while True:
            if can_place(grid, shape, bottom_row + 1, left):
                bottom_row += 1
            else:
                # We can't go any further down safely
                break

        # Place the piece at the final bottom_row
        place_piece(grid, shape, bottom_row, left)

        # Clear any fully filled rows
        # breakpoint()
        # if shape_letter == 'Q' and piece_count >= 149:
        #     breakpoint()
        grid = clear_full_rows(grid)
        # breakpoint()

    # After placing all pieces in this line, compute the resulting height
    return get_stack_height(grid)


def main():
    """
    Read lines from stdin, process each, and print the stack height result.
    """
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        height = process_line(line)
        print(height)


if __name__ == '__main__':
    main()