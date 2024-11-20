# Nonogram-Solver

Nonogram je hra, ve které musíte rekonstruovat obdélníkový obrázek (každá buňka je buď nakreslená nebo prázdná), mající rozměry vyplněných bloků v každém řádku a sloupci. Tento projekt byl vytvořen pro řešení Nonogramu pomocí SAT-solveru. K řešení byl použit SAT-solver [Glucose](https://github.com/audemard/glucose).

## Popis Nonogramu

Hra Nonogram obvykle vypadá jako pole N x M, kde je vedle každého řádku a sloupce napsána sada čísel --- velikosti vyplněných bloků v odpovídajícím řádku/sloupci. Například sade (1, 3, 2) může odpovídat řetězec ..#..###.##. (prázdné buňky označíme tečkou a vyplněné buňky mřížkou). Všimněte si, že pořadí čísel v řádcích a sloupcích je důležité. Nonogram můžete vyzkoušet na tomto [odkazu](https://www.goobix.com/games/nonograms/).

Pro náš program je nutné zadat vstupní data v následujícím formátu:

```
N M                             // velikosti polí
                                // prázdný řetězec (pro čitelnost)
r[1,1] r[1,2] ... r[1, R_1]     // velikosti bloků v prvním řádku
r[2,1] r[2,2] ... r[2, R_2]     //       ...         druhém řádku
              ...
r[N,1] r[N,2] ... r[N, R_N]   
                                // prázdný řetězec znovu

s[1,1] s[1,2] ... s[1, S_1]     // velikosti bloků v prvním sloupci
s[2,1] s[2,2] ... s[2, S_2]     //       ...         druhém sloupci
              ...
s[M,1] s[M,2] ... s[M, S_M]  

```

Bude například následující obrázek

```
...#.
...##
##.##
#.#.#
###..
```

mít takový vstup

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

## Uživatelska dokumentaci

Ke spuštění programu použijte následující skript:

```
nonogram.py [-h] [-i INPUT] [-f FORMULA] [-o OUTPUT] [-s SOLVER]
```
Možné argumenty:

```
-h, --help            show this help message and exit
-i, --input INPUT     path of an input file | default = input.txt
-f, --formula FORMULA
                    output file for a cnf formula (in DIMACS format) | default = formula.cnf
-o, --output OUTPUT   path of an output file for a picture | if not setted - into std out
-s, --solver SOLVER   path to a sat-solver file | default = glucose
```