# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint propagation is used based on the rules defined for Sudoku plus we iterate through all the units and check for the existence of same value in multiple boxes in each units. If there is same value within the unit, then compare the length of the values with the number of boxes found with that value. If both the lengths are same, then remove the digits of this value from the values of other boxes of that particular unit. Ex: If the value of a box is 'XY' where n=2, then naked twins will try to find the value 'XY' in other boxes within that unit and if found then the value 'XY'  will be in n=2 boxes within that units. Then we eliminate the digits X&Y from values of the other boxes in the unit. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Originally we apply constraint to eliminate value from all peers peers(Row Unit, Column Unit and 3x3 square unit) in case of diagonal sudoku problem in addition to this we eliminate the value(single digit) from the values of all its peers along major diagonal if the box is a part of the major diagonals.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.