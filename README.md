# Nonogram-Solver

[Nonogram](https://en.wikipedia.org/wiki/Nonogram) is a popular logic game in which ypu must reconstruct a picture by the sizes of blocks in each row/column. This program is used for solving the puzzle using the [Glucose](https://github.com/audemard/glucose) SAT-solver.

## What is Nonogram

The game Nonogram usually looks like an N x M grid, where next to each row and column there is a list of numbers — the sizes of the filled blocks in the corresponding row/column. For example, the list (1, 3, 2) may correspond to the string ..#..###.##. (we mark empty cells with a dot and filled cells with a hash). Notice that the order of numbers in rows and columns is important. Your task is to recreate image from given lists. You can try out a Nonogram at this [link](https://www.goobix.com/games/nonograms/).

## User's documantation

### Installation

For using the program you need to have a installed SAT-solver. If you don't have one, you can run `./setup.sh` script. It will create a `glucose-syrup` executable, which our program will use.

### Input data representation

You need to prepare the input data in the next format

```
N M                             // sizes of the image
                                // empty line (for better-looking)
r[1,1] r[1,2] ... r[1, R_1]     // sizes of the blocks in first row
r[2,1] r[2,2] ... r[2, R_2]     //       ...              second row
              ...               //       ...
r[N,1] r[N,2] ... r[N, R_N]     
                                // again the empty line

s[1,1] s[1,2] ... s[1, S_1]     // sizes of blocks in first column
s[2,1] s[2,2] ... s[2, S_2]     //       ...          second column
              ...               //       ...
s[M,1] s[M,2] ... s[M, S_M]  

```

So for example, the next picture:

```
...#.
...##
##.##
#.#.#
###..
```

will be decoded like this:

```
5 5

1
2
2 2
1 1 1
3

3
1 1
2
3
3
```

### How to run the program

For running the program you need to run next script:

```
nonogram.py [-h] [-i INPUT] [-f FORMULA] [-o OUTPUT] [-s SOLVER]
```

With the next possible parameters:

```
-h, --help            show this help message and exit
-i, --input INPUT     path of an input file | default = input.txt
-f, --formula FORMULA
                    output file for a cnf formula (in DIMACS format) | default = formula.cnf
-o, --output OUTPUT   path of an output file for a picture | if not setted - into std out
-s, --solver SOLVER   path to a sat-solver file | default = glucose
```

### Input examples

You can find the next example inputs in `sample_inputs` directory:

```
5x5-sat.in          -> small satisfiable input
5x5-unsat.in        -> small non-satisfiable input
15x15-sat.in        -> bigger satisfiable
big-sat.in          -> 29 x 21 satisfiable
very-big-sat.in     -> 50 x 25 satisfiable
extra-big-sat.in    -> 100 x 90 satisfiable
```

## SAT formulas

For the information about SAT formulas decoding read the czech docs.