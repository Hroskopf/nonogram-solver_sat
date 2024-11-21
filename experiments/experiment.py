#!/usr/bin/env python3

from random import randint
import time
import subprocess

def random_picture(n):
    # generates a random picture
    picture = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            picture[i][j] = randint(0, 1)
    return picture

def get_blocks(row):
    # returns an array of blocks for given row
    blocks = []
    row.append(0)
    cnt = 0
    for i in row:
        if i == 1:
            cnt += 1
        else:
            if cnt > 0:
                blocks.append(cnt)
                cnt = 0
    return blocks

def generate_input_file(picture, file_name):
    # generates a file with decoded picture
    n = len(picture)
    with open(file_name, "w") as file:
        file.write(f"{n} {n}\n\n")
        for row in picture:
            blocks = get_blocks(row)
            for block in blocks:
                file.write(f"{block} ")
            file.write("\n")
        file.write("\n")
        for column_num in range(n):
            column = []
            for row_num in range(n):
                column.append(picture[row_num][column_num])
            blocks = get_blocks(column)
            for block in blocks:
                file.write(f"{block} ")
            file.write("\n")
        
def make_experiment(input_files, output_file):
    # provides an experiment on given input_file
    # mesures time needed to procces given image and outputs it as a row to a output_file
    with open(output_file, "w") as file:
        for input_file in input_files:  
            print(f"processing {input_file} experiment...")
            start_time = time.time()
            
            subprocess.run(['./nonogram.py', f'-i{input_file}'], stdout=subprocess.PIPE)
            
            spent_time = time.time() - start_time
            print(spent_time)
            file.write(f"{input_file} {round(spent_time, 3)}\n")
    
    
    
    

if __name__ == "__main__":
    
    input_files = []
    
    for size in range(3, 49, 3):
        file_name = f"experiments/inputs/{size}.txt"
        generate_input_file(random_picture(size), file_name)
        input_files.append(file_name)
    
    make_experiment(input_files, "experiments/experiment_results.txt")
