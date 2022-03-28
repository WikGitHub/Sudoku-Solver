# AI Sudoku
The sudoku_solver, solves sudoku boards, examples of a constraint satisfaction problem, employing constraint propagation, as well as depth-first search and heuristics to solve the puzzles.

## Constraint propagation
Constraint satisfaction problems involve a set of variables which each can be assigned different values under some set of constraints. For sudoku, the set of variables would be the individual cells on the sudoku grid, the domain for the variables are the numbers 1-9 and the constraints state that each number appears exactly once per the grid’s rows, columns and 3x3 blocks. To find a solution, a complete and consistent assignment of the domain values to the variables must be made under the constraints.

## Search algorithm
Within the sudoku-solver is an implementation of a depth-first search algorithm. This backtracking algorithm is useful because it allows the sudoku-solver to explore for an assignment of a number to a cell and see if the resulting state is consistent (valid under the constraints). If so, this is iteratively repeated until the assignment is complete and a solution has been found. In the case that an assignment is inconsistent with the constraints, the sudoku-solver is able to backtrack to a previous state which did follow the constraints and explore another assignment. In doing this, a search tree is formed, where the sudoku-solver starts at the root and explores as far as possible down each of the nodes before it backtracks or finds the solution (Norvig, 2010). 

## Heuristics
To improve search efficiency, heuristics for choosing which variable to fill next were implemented. The most constraining variable heuristic picks the variable with the smallest set of possible values. Here, it would select the cell with the smallest set of remaining possible numbers initialised to it as the first to begin exploring. By doing this, the heuristic picks the cells most likely to reach an inconsistent assignment sooner, hence increasing the efficiency and speed of pruning. This is because failed assignments are done earlier in the search rather than later, saving time.

As mentioned above, it may be possible that more than one cell has the same number of values, hence a degree heuristic is used too to split the decision. Here, it assigns a value to the variable involved in the largest number of constraints on other unassigned variables, meaning the cell which will affect the highest number of empty cells is chosen.
Using both of these two dynamic variable ordering heuristics, the search has increased efficiency compared to static variable ordering since, instead of always selecting cells for assignment in a certain order, the updated information from the search is used to inform the selection.


## Implementation
Below is a brief explanation of the choices made for the implementation of the algorithmic approach.

### Functions 
The main function is the sudoku_solver function. This accepts the initial grid and performs checks for constraint satisfaction and whether the sudoku is solved. If not, a 9x9 array of -1s is returned, and if solved, the same solved array is returned. The domain for each variable is set at the start using the constraints function, which sets the possible numbers for each cell. Following from this, when performing updates to the domain, a copy is used.

After initialising the possible numbers for each cell, the depth-first search is performed by calling the function of the same name. This recursive function uses the heuristics for variable ordering and fills the grid using constraint propagation while exploring. It evaluates the outcomes of the assignments, backtracking if necessary, until either an inconsistent assignment is made or a solution is found. As part of the degree heuristic, functions to deal with finding the cell which will affect most other cells, and calculate the size of the effect it will have, were created.

As mentioned before, a copy of the sudoku grid object is made and numbers are assigned to certain cells (gen_next_board). A function updates all possible numbers for remaining empty cells which would be affected by the assignment, narrowing down the domains for each cell variable. 

To simplify the search, after the update, a function finds empty cells with only one remaining possible number in their domain and returns their positions so that they are updated too. The resultant sudoku grid object is passed to the depth-first search again to be evaluated.

### Data structures
Chosen data structures of note for the implementation included lists, dictionaries and multidimensional numpy arrays. These allowed easy management of key data such as possible numbers to assign to cells, and cell positions. As the input was a 9x9 numpy array, keeping the updated state of the grid as a numpy array meant there was no need for conversion while solving the puzzle. Also, this provided inbuilt functions to more easily iterate over, and alter, the data within.

# References 
Norvig, P., 2010. Solving Every Sudoku Puzzle. [online] Norvig.com. Available at: <http://www.norvig.com/sudoku.html>