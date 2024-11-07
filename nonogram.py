#!/usr/bin/env python3

import argparse 

def load_input(input_file):
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
        
    return (rows, columns)
        

def field_variable(i, j):
    return 1 + i * M + j

def row_block_variable(i, j, k):
    return 1 + N * M + i * M * M + j * M + k

def column_block_variable(i, j, k):
    return 1 + N * M + N * M * M + i * N * M + j * N + k

def create_cnf(rows, columns):
    
    clauses = []
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
    with open(output_file, "w") as file:
        file.write(f"p cnf {str(N * M + N * M * M + N * N * M)} {str(len(cnf))}\n")
        for clause in cnf:
            for var in clause:
                file.write(f"{var} ")
            file.write("0\n")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Script that finds a solution for a nonogram or tells that no such exist.")
    
    parser.add_argument("-i", "--input", default = "sample_inputs/3x3-sat.in", help = "path of an input file", type = str)
    parser.add_argument("-f", "--formula", default = "formula.cnf", help = "path of a file for a cnf formula (in DIMACS format)", type = str)
    parser.add_argument("-o", "--output", default = "output.txt", help = "path of an output file", type = str)

    args = parser.parse_args()
    
    rows, columns = load_input(args.input)
    
    cnf = create_cnf(rows, columns)
    
    
    store_cnf(cnf, args.formula)
    
    