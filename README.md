# Graph Search Algorithms

## Input legend:-

0: empty cell
1: cell occupied by lizard
2: cell occupied by tree

### Problem statement: 
Place p lizards on an nxn board with certain cells occupied by trees.

Lizards in cell (i,j) can attack other lizards in the same column, row and diagonal unless there is a tree in the path.

## Inputs:

### Depth First Search
DFS

10 (n)

25 (p)

0002000200

0200020002

0002000200

0200020002

0002000200

0200020002

0002000200

0200020002

0002000200

0200020002

### Breadth First Search
BFS

6

5

000000

022220

020020

020020

022220

000000

### Simulated Annealing
SA

10

6

2222222222

0220000000

0220000000

0220022200

0220000000

0220000000

0220022222

0220022222

0000000000

0000000000

## Outputs:
OK

Output board with lizards

OR

FAIL (if p lizards cannot be placed on this board)
