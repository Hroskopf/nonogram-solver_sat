#!/usr/bin/env python3

import argparse 

def load_input(input_file):
    with open(input_file) as file:
        lines = []
        for line in file:
            lines.append(line.split())
        n = int(lines[0][0])
        m = int(lines[0][1])
        
        rows = []
        columns = []
        for i in range(2, n + 2):
            rows.append([*map(int, lines[i])])
            
        for i in range(n + 3, n + m + 3):
            columns.append([*map(int, lines[i])])
        
    return (rows, columns)
        
    
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Script that finds a solution for a nonogram or tells that no such exist.")
    
    parser.add_argument("-i", "--input", default = "input.in", help = "path of an input file", type = str)
    parser.add_argument("-f", "--formula", default = "formula.cnf", help = "path of a file for a cnf formula (in DIMACS format)", type = str)
    parser.add_argument("-o", "--output", default = "output.txt", help = "path of an output file", type = str)

    args = parser.parse_args()
    
    rows, columns = load_input(args.input)
    
    print(rows)
    print(columns)
    
    