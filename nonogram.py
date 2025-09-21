#!/usr/bin/env python3

import argparse 
import subprocess

def load_input(input_file):
    # loads the input from input_file
    # creates global variable N and M for the field sizes
    # returns two arrays which are arrays of row and column blocks
    
    try:
        with open(input_file) as file:
            global M
            global N
            lines = []
            for line in file:
                lines.append(line.split())
            N = int(lines[0][0])
            M = int(lines[0][1])
            
            rows = []
            columns = []
            for i in range(2, N + 2):
                rows.append([*map(int, lines[i])])
                
            for i in range(N + 3, N + M + 3):
                columns.append([*map(int, lines[i])])
    except:
        print("Provided file does not exist...")
        exit()
        
    return (rows, columns)
        

def field_variable(i, j):
    # returns number of variable in CNF corresponding to (i, j)-th cell in a field
    return 1 + i * M + j

def row_block_variable(i, j, k):
    # returns the number of variable corresponding to k-th block of i-th row, that begins in column j
    return 1 + N * M + i * M * M + j * M + k

def column_block_variable(i, j, k):
    # returns the number of variable corresponding to k-th block of j-th column, that begins in row i 
    return 1 + N * M + N * M * M + i * N * M + j * N + k

def create_cnf(rows, columns):
    #creates a CNF formule and returns it
    #the formule is returned in DIMACS format as an array of clauses
    
    clauses = []
    
    # if block variable is equal to 1 then all the corresponding field cells needs to be filled
    for row in range(N):
        for column in range(M):
            for block in range(len(rows[row])):
                block_len = rows[row][block]
                if column + block_len > M:
                    clauses.append([-row_block_variable(row, column, block)])
                    continue
                for i in range(block_len):
                    clauses.append([-row_block_variable(row, column, block), field_variable(row, column + i)])
                    
    for row in range(N):
        for column in range(M):
            for block in range(len(columns[column])):
                block_len = columns[column][block]
                if row + block_len > N:
                    clauses.append([-column_block_variable(row, column, block)])
                    continue
                for i in range(block_len):
                    clauses.append([-column_block_variable(row, column, block), field_variable(row + i, column)])
    
    # each block begins in one cell
    for row in range(N):
        for block in range(len(rows[row])):
            for column_1 in range(M):
                for column_2 in range(M):
                    if column_1 == column_2:
                        continue
                    clauses.append([-row_block_variable(row, column_1, block), -row_block_variable(row, column_2, block)])
    
    for column in range(M):
        for block in range(len(columns[column])):
            for row_1 in range(N):
                for row_2 in range(N):
                    if row_1 == row_2:
                        continue
                    clauses.append([-column_block_variable(row_1, column, block), -column_block_variable(row_2, column, block)])
    
    # first block exists
    for row in range(N):
        clause = []
        for column in range(M):
            clause.append(row_block_variable(row, column, 0))
        clauses.append(clause)
    
    for column in range(M):
        clause = []
        for row in range(N):
            clause.append(column_block_variable(row, column, 0))
        clauses.append(clause)
        
    # if i-th block exists, then (i + 1)-th also exists and begins in allowed cell
    for row in range(N):
        for column in range(M):
            for block in range(1, len(rows[row])):
                clause = [-row_block_variable(row, column, block - 1)]
                block_len = rows[row][block - 1]
                for next_column in range(column + block_len + 1, M):
                    clause.append(row_block_variable(row, next_column, block))
                clauses.append(clause)
                
    for column in range(M):
        for row in range(N):
            for block in range(1, len(columns[column])):
                clause = [-column_block_variable(row, column, block - 1)]
                block_len = columns[column][block - 1]
                for next_row in range(row + block_len + 1, N):
                    clause.append(column_block_variable(next_row, column, block))
                clauses.append(clause)
                
    # if field cell is filled then exists some row block and some column block, that contains this cell
    for row in range(N):
        for column in range(M):
            clause = [-field_variable(row, column)]
            for block in range(len(rows[row])):
                block_len = rows[row][block]
                for block_column in range(max(0, column - block_len + 1), column + 1):
                    clause.append(row_block_variable(row, block_column, block))
            clauses.append(clause)
                    
    for row in range(N):
        for column in range(M):
            clause = [-field_variable(row, column)]
            for block in range(len(columns[column])):
                block_len = columns[column][block]
                for block_row in range(max(0, row - block_len + 1), row + 1):
                    clause.append(column_block_variable(block_row, column, block))
            clauses.append(clause)
    
    return clauses

                                        
def store_cnf(cnf, output_file):
    # stores a cnf formule to a corresponding file 
    with open(output_file, "w") as file:
        file.write(f"p cnf {str(N * M + N * M * M + N * N * M)} {str(len(cnf))}\n")
        for clause in cnf:
            for var in clause:
                file.write(f"{var} ")
            file.write("0\n")

def process_cnf(cnf_file, solver_file):
    # runs a solver on a given cnf file
    return subprocess.run(['./' + solver_file, '-model', cnf_file], stdout=subprocess.PIPE)

def output_results(result, output_file = ""):
    # gets results from a solver and decodes it to a readable format
    # stores the result to a output_file or write it to std out
    for line in result.stdout.decode('utf-8').split('\n'):
        if len(line) < 1000:
            print(line)                
        
        
    if (result.returncode == 20):
        if output_file != "":
            with open(output_file, "w") as file:
                file.write("unsolvable")
        else:
            print("unsolvable")
        return

    model = []
    for line in result.stdout.decode('utf-8').split('\n'):
        if line.startswith("v"):
            vars = line.split(" ")
            vars.remove("v")
            model.extend(int(v) for v in vars)      
            
    model = model[: N * M]
    
    picture = [['.' for _ in range(M)] for _ in range(N)]
    for row in range(N):
        for column in range(M):
            if model[field_variable(row, column) - 1] > 0:
                picture[row][column] = '#'
        
    if output_file != "":
        with open(output_file, "w") as file:
            for row in picture:
                for i in row:
                    file.write(i)
                file.write("\n")  
    else:
        for row in picture:
            for i in row:
                print(i, end = "")
            print()    
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Script that finds a solution for a nonogram or tells that no such exist.")
    
    parser.add_argument("-i", "--input", default = "input.txt", help = "path of an input file | default = input.txt", type = str)
    parser.add_argument("-f", "--formula", default = "formula.cnf", help = "output file for a cnf formula (in DIMACS format) | default = formula.cnf", type = str)
    parser.add_argument("-o", "--output", default = "", help = "path of an output file for a picture | if not setted - into std out", type = str)
    parser.add_argument("-s", "--solver", default = "glucose-syrup", help = "path to a sat-solver file | default = glucose-syrup", type = str)
 

    args = parser.parse_args()
    
    rows, columns = load_input(args.input)
    
    cnf = create_cnf(rows, columns)
    
    store_cnf(cnf, args.formula)
    
    result = process_cnf(args.formula, args.solver)
    output_results(result, args.output)