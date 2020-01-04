from nonogram import Nonogram
import methods
#from visualizers.simple_visualizer import just_plot_it
from copy import copy
from sys import argv

if len(argv) == 1:
    print("Usage: solver.py nonogram_filename")
    quit()
else:
    nono = Nonogram(argv[1])

try:
    interactive = argv[2]
    nono.plot(interactive=interactive)
except:
    interactive = False

# Simple beggining, gives nice block limits initialization and usually even fills some cells
for i in range(2):
    for row in range(nono.nRows):
        sth_changed, nono.rowBlockOrigins[row] = methods.push_block_Origins(nono.rowHints[row], nono.rowBlockOrigins[row], index=0)
        sth_changed, nono.rowBlockEndings[row] = methods.push_block_Endings(nono.rowHints[row], nono.rowBlockEndings[row], index=0)
        methods.fill_row(nono, row, interactive=interactive)
    nono.transpose()

cycle = 0 
while nono.undetermind:
    # Check if anything improved
    if nono.rowsChanged == set() and nono.colsChanged == set():
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

if not interactive:
    nono.plot()
else:
    nono.end_iplot()