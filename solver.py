from nonogram import Nonogram
import methods
#from visualizers.simple_visualizer import just_plot_it
from copy import copy
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

from time import time
t0 = time()

# Simple beggining, gives nice block limits initialization and usually even fills some cells
for i in range(2):
    for row in range(nono.nRows):
        sth_changed, nono.rowBlockOrigins[row] = methods.push_block_Origins(nono.rowHints[row], nono.rowBlockOrigins[row], index=0)
        sth_changed, nono.rowBlockEndings[row] = methods.push_block_Endings(nono.rowHints[row], nono.rowBlockEndings[row], index=0)
        methods.fill_row(nono, row, interactive=interactive)
    nono.transpose()

cycle = 0 
# main loop
while nono.undetermind:
    # Check if anything improved
    if nono.rowsChanged == set() and nono.colsChanged == set():
        # Calling advanced, more costly function
        methods.analyze_multi_block_relations(nono)

    # Check if anything improved
    if nono.rowsChanged == set() and nono.colsChanged == set():
        # Calling advanced, even more costly function
        if not methods.search_for_assumptions(nono, searching_depth=searching_depth):
            print("Failed to solve Nonogram.")
            print("Cycle : " + str(cycle))
            break
    
    rowsChanged = copy(nono.rowsChanged)
    colsChanged = copy(nono.colsChanged)
    nono.rowsChanged = set()
    nono.colsChanged = set()
    
    # Loop over Nonogram dimensions (rows and columns)
    for i in range(2):
        # Loop over Nonogram rows (columns if transposed)
        for row in rowsChanged:
            sth_changed_1, origins = methods.deduce_new_block_origins(nono.rows[row], nono.rowHints[row], nono.rowBlockOrigins[row])
            sth_changed_2, endings = methods.deduce_new_block_endings(nono.rows[row], nono.rowHints[row], nono.rowBlockEndings[row])
            if sth_changed_1:
                nono.rowBlockOrigins[row] = origins
                nono.rowsChanged.add(row)
            if sth_changed_2:
                nono.rowBlockEndings[row] = endings
                nono.rowsChanged.add(row)
            if sth_changed_1 or sth_changed_2:
                methods.fill_row(nono, row, interactive=interactive)
        nono.transpose()
        rowsChanged, colsChanged = colsChanged, rowsChanged
        
    cycle += 1

if not nono.undetermind:
    print("Solved Nonogram in cycle: " + str(cycle) + ".")

t1 = time()

print("Solved in : "+str(t1-t0)+'s')

if not interactive:
    nono.plot()
else:
    nono.end_iplot()
