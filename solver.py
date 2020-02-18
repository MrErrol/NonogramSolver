from time import time
from sys import argv
from argparse import ArgumentParser

from lib.nonogram import Nonogram
from lib.solver import solver

def getOptions(args=argv[1:]):
    parser = ArgumentParser(description="Parses command.")
    parser.add_argument("-i", "--input", help="Input file with nonogram.")
    parser.add_argument("-l", "--live", dest='interactive', default=False, action='store_true', help="Live plotting mode.")
    parser.add_argument("-d", "--depth", dest='searching_depth', type=int, default=2, action='store', help="Searching depth for assumption making.")
    options = parser.parse_args(args)
    return options

options = getOptions()

nono = Nonogram(options.input, presolved=False)

if options.interactive:
    nono.plot(interactive=options.interactive)
    
t0 = time()

cycle = solver(nono, searching_depth=options.searching_depth, interactive=options.interactive)

if not nono.undetermind:
    print("Solved Nonogram in cycle: " + str(cycle) + ".")

t1 = time()

print("Solved in : "+str(t1-t0)+'s')

if not options.interactive:
    nono.plot()
else:
    nono.end_iplot()
