#!/usr/bin/env python3

from random import randint
import time
import subprocess

def random_picture(n):
    picture = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            picture[i][j] = randint(0, 1)
    return picture

def get_blocks(row):
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
        
def make_experiment(range, output_file):
    for size in range:
        generate_input_file(random_picture(size), f"./experiments/inputs/{size}.txt")
    
    with open(output_file, "w") as file:
        for size in range:  
            print(f"processing {size}x{size} matrix experiment...")
            start_time = time.time()
            
            subprocess.run(['./nonogram.py', f'-i./experiments/inputs/{size}.txt'], stdout=subprocess.PIPE)
            
            spent_time = time.time() - start_time
            file.write(f"{size} {spent_time}\n")
    
    
    

if __name__ == "__main__":
    
    make_experiment(range(5, 65, 5), "./experiments/experiment_results.txt")
