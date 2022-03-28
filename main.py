import numpy as np


class SudokuBoard:
    def __init__(self, end_value):
        self.end_value = end_value
        self.potential_vals = np.empty(shape=(9, 9), dtype=list)
        
        
    def valid_value(self, target_row, target_col, value):
        if value == 0:
            return True 
        #Check for row and column:
        for i in range(9):
            if self.end_value[i][target_col] == value and i != target_row or self.end_value[target_row][i] == value and i != target_col:
                return False 
        #Find the start of a 3x3 block:
        block_row, block_col = target_row - (target_row % 3), target_col - (target_col % 3)
        
        #Check each element in the block:
        for row in range(3):
            for col in range(3):
                if value == self.end_value[block_row + row][block_col + col] and block_row + row != target_row and block_col + col != target_col:
                    return False  
        return True

    
    def constraints(self):
        for (row, col), current_value in np.ndenumerate(self.end_value):
            self.potential_vals[row][col] = []
            if current_value == 0:
                for value in range(1, 10):
                    if self.valid_value(row, col, value) == True:
                        self.potential_vals[row][col].append(value)
        return None 
    
    
    def solvable(self):
        for row, col in np.ndindex(9, 9):
            if self.end_value[row][col] == 0 and len(self.potential_vals[row][col]) < 1:
                return False
        return True

    
    def valid_board(self):
        for (row, col), value in np.ndenumerate(self.end_value):  
            if self.valid_value(row, col, value) != True:  
                return False
        return True


    def goal(self):
        if 0 not in self.end_value:
            return True

    def one_poss_val(self):
        poss_val_list = [] 
        for row in range(9):
            for col in range(9):
                if len(self.potential_vals[row][col]) == 1 and self.end_value[row][col] == 0:
                    poss_val_list.append((row, col)) 
        return poss_val_list

    
    def new_constraints(self, target_row, target_col, value):
        for i in range(9):
            if value in self.potential_vals[target_row][i]: 
                self.potential_vals[target_row][i].remove(value)
            if value in self.potential_vals[i][target_col]:  
                self.potential_vals[i][target_col].remove(value)
        #Update the block:
        block_row, block_col = target_row - (target_row % 3), target_col - (target_col % 3)
        
        for row in range(3):
            for col in range(3):
                if value in self.potential_vals[block_row + row][block_col + col]: 
                    self.potential_vals[block_row + row][block_col + col].remove(value)
        return None

    
    def copy_board(self):
        new_board = SudokuBoard(np.ndarray.copy(self.end_value))  
        for (row, col), values in np.ndenumerate(self.potential_vals):
            new_board.potential_vals[row][col] = values[:]  
        return new_board  

    
    def gen_next_board(self, row, col, value):
        new_board = self.copy_board() 
        
        #Update the board configs:
        new_board.end_value[row][col] = value
        new_board.potential_vals[row][col] = []  

        new_board.new_constraints(row, col, value)  
        poss_val_list = new_board.one_poss_val()  
        while poss_val_list:
            row, col = poss_val_list.pop() 

            new_board.end_value[row][col] = new_board.potential_vals[row][col][0]  
            new_board.potential_vals[row][col] = []  
            new_board.new_constraints(row, col, new_board.end_value[row][col])  

            poss_val_list = new_board.one_poss_val() 
        return new_board  

    


def minimum_value(sudoku_board):
    position_choices = {}  
    for key in range(10):  
        position_choices[key] = []

    for (row, col), end_value in np.ndenumerate(sudoku_board.end_value):
        if end_value == 0:  
            position_choices[len(sudoku_board.potential_vals[row][col])].append((row, col)) 

    #Find the position with minimum possible moves
    for i in range(10):
        if position_choices[i]:
            return position_choices[i]  

        
def degree(sudoku_board, row, col):
    degree_number = 0 
    for i in range(9):
        #Search column
        if sudoku_board.end_value[row][i] == 0: 
            degree_number += 1
        #Search row
        if sudoku_board.end_value[i][col] == 0: 
            degree_number += 1

    #Find start of a 3x3 block:
    block_row, block_col = row - (row % 3), col - (col % 3)

    #Check each element in the block:
    for row_i in range(3):
        for col_i in range(3):
            if sudoku_board.end_value[row_i + block_row][col_i + block_col]: 
                degree_number += 1
    return degree_number 


def new_cell(sudoku_board):
    min_value_positions = minimum_value(sudoku_board)  
    if len(min_value_positions) == 1:  
        return min_value_positions[0][0], min_value_positions[0][1] 
    target_row, target_col, max_degree = -1, -1, 0 
    
    for position in min_value_positions: 
        current_degree = degree(sudoku_board, position[0], position[1])  
        if max_degree < current_degree:
            max_degree = current_degree  
            target_row, target_col = position  
    return target_row, target_col  


def depth_first_search(sudoku_board):
    row, col = new_cell(sudoku_board)  
    values = sudoku_board.potential_vals[row][col]
    for value in values:  
        new_board = sudoku_board.gen_next_board(row, col, value)  
        if new_board.goal():
            return new_board  
        if new_board.solvable():
            searched_board = depth_first_search(new_board)
            if searched_board != None and searched_board.goal():
                return searched_board  
    return None


def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.
    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.
    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    solved = SudokuBoard(sudoku)
    if solved.valid_board() != True:  
        return np.full(shape=(9, 9), fill_value=-1, dtype=int) 
    if solved.goal() == True:  
        return solved.end_value  
    
    solved.constraints()  
    solved = depth_first_search(solved) 

    if solved == None:
        return np.full(shape=(9, 9), fill_value=-1, dtype=int) 
    return solved.end_value 