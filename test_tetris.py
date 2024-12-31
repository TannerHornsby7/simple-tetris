import pytest
from tetris import process_line

def test_single_q0():
    # Example given: "Q0" should result in a height of 2 (since Q is 2 high)
    line = "Q0"
    assert process_line(line) == 2

def test_example_1():
    # Example 1: "I0,I4,Q8" => final height = 1 after the bottom row clears
    # Explanation from the prompt:
    #  - The I's fill horizontally at row 0,
    #  - The Q at column 8 also sits at bottom,
    #  - Once the row is completely filled, it is removed,
    #  => final stack = height 1
    line = "I0,I4,Q8"
    assert process_line(line) == 1

def test_example_2():
    # Example 2: "T1,Z3,I4" => no rows are filled, final height = 4
    # T and Z are 2 units tall, the I is 1 unit tall (but might stack above others).
    # The prompt says the final is 4.
    line = "T1,Z3,I4"
    assert process_line(line) == 4

def test_example_3():
    # Example 3 from the prompt:
    # "Q0,I2,I6,I0,I6,I6,Q2,Q4" => final output is 3
    line = "Q0,I2,I6,I0,I6,I6,Q2,Q4"
    assert process_line(line) == 3

def test_multiple_squares():
    # If we drop multiple Q squares in various columns without filling a row,
    # let’s just verify the stack height logic. For instance:
    # "Q0,Q2,Q4" - none of these 2x2 squares overlap or fill a 10-wide row,
    # so they should stack up to 2 in height.
    line = "Q0,Q2,Q4"
    assert process_line(line) == 2
    
def test_fill_grid():
    # extend the first example to fill the grid and then clear it
    line = "I0,I4," * 99 + "I0"
    assert process_line(line) == 100

def test_fill_grid_and_clear():
    # extend the first example to fill the grid and then clear it
    line = "I0,I4," * 100
    line += "Q8," * 49 + "Q8"
    assert process_line(line) == 0