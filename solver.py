from lib.nonogram import Nonogram
from lib.solver import solver
from time import time
from sys import argv

try:
    nono = Nonogram(argv[1])
except:
    print("Usage: solver.py nonogram_file [interactive]")
    quit()
    
try:
    interactive = argv[2]
    nono.plot(interactive=interactive)
except:
    interactive = False
    
try:
    searching_depth = argv[3]
except:
    searching_depth = 2


t0 = time()

cycle = solver(nono, searching_depth=searching_depth, interactive=interactive)

if not nono.undetermind:
    print("Solved Nonogram in cycle: " + str(cycle) + ".")

t1 = time()

print("Solved in : "+str(t1-t0)+'s')

if not interactive:
    nono.plot()
else:
    nono.end_iplot()
