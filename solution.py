__author__ = 'Vikash Khanna'
__email__  = 'vcashk@gmail.com'
# AI_Nanodegree_Term1_Project1

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def identify_all_units():
    # possible unit types are : Row Units, Column Units and 3x3 Square Units
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    return row_units + column_units + square_units

def cross(A, B):
    """
    Cross product of elements in A and elements in B.
    Returns:
        the cross product of two input elements
    """
    return [x+y for x in A for y in B]


# all boxes in sudoku 
boxes = cross(rows, cols)

# boxes for the diagonal units
diag_units_lr = [unit[0] for unit in [cross(r,c) for r,c in zip(rows,cols)]]
diag_units_rl = [unit[0] for unit in [cross(r,c) for r,c in zip(rows,reversed(cols))]]

# dict of peers for all the boxes 
allunits = identify_all_units()
units = dict((s, [u for u in allunits if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def naked_twins(values):
    """
    Eliminate values using the naked twins strategy. 
    Go through all the units and check for the existence of same value of multiple boxes in each units. 

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in allunits:
        for box in unit:
            box_value = values[box]
            dplaces = [box for box in unit if values[box]==box_value]
            if(len(dplaces) >1 and len(dplaces)==len(box_value)):
                other_boxes = [box for box in unit if values[box]!=box_value]
                for other_box in other_boxes:
                    for digit in box_value:
                        assign_value(values, other_box, values[other_box].replace(digit,''))
    return values

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    
    In addtion to the normal elimination rules, for diagonal sudoku if the box is a part of the Major Diagonals, then also eliminate 
    the value(single digit) from the values of all its peers along that diagonal.
    Args: 
        values(dict): A sudoku grid in dictionary form.

    Returns: 
        The resulting sudoku grid in dictionary form.
    """
    processed_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in processed_values:
        digit = values[box]
        for peer in peers[box]:
            #values[peer] = values[peer].replace(digit,'')
            assign_value(values, peer, values[peer].replace(digit,''))
        
        diag_unit = True if box in diag_units_lr else False
        if diag_unit:
            for peer in diag_units_lr:
                if len(values[peer])>1:
                    #values[peer] = values[peer].replace(digit,'')
                    assign_value(values, peer, values[peer].replace(digit,''))

        diag_unit = True if box in diag_units_rl else False
        if diag_unit:
            for peer in diag_units_rl:
                if len(values[peer])>1:
                    #values[peer] = values[peer].replace(digit,'')
                    assign_value(values, peer, values[peer].replace(digit,''))
    
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Args: 
        values(dict): A sudoku grid in dictionary form.

    Returns: 
        The resulting sudoku grid in dictionary form.
    """
    for unit in allunits:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """
    Iterate over eliminate() and only_choice() return False if box with no value
    return the sudoku if solved else return the sudoku.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Recursive DFS and constraint propagation used to create a search tree
    This serach will be recursively called until
    the sudoku is resolved
    """
    # reduce grid using initial function
    values = reduce_puzzle(values)
    if values is False:
        return False 
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## this is  =solved
    # Choose one of the unfilled squares 
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # solve recursively
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = max(len(values[s]) for s in boxes)+1
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.

    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for char in grid:
        if char in digits:
            chars.append(char)
        if char == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def initial_grid_values(grid):
    return dict(zip(boxes, grid))

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    processed_values = search(values)
    return processed_values

def initial_state(grid):
    values = initial_grid_values(grid)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    print('Initial State of Sudoku:')
    print('===================')
    display(initial_state(diag_sudoku_grid))
    print('===================')
    print('                     ')
    print('Final State of Sudoku:')
    print('===================')
    display(solve(diag_sudoku_grid))
    print('===================')

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
