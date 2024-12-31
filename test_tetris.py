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

def test_fill_one_row():
    # A quick test to fill a single row with two I pieces (each 4 wide) and
    # one Q square (2 wide) => 4+4+2 = 10 wide exactly.
    # This should fill row 0 completely and clear it, ending up with height = 0.
    line = "I0,I4,Q8"
    # This is basically the same as example_1; we expect height=1 per example_1
    # But let's confirm it remains consistent with the official example.
    assert process_line(line) == 1