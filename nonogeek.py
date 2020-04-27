from time import time
from sys import argv
from argparse import ArgumentParser

from lib.nonogram import Nonogram
from lib.solver import solver
from utils.tools import compare_nonograms

def getOptions(args=argv[1:]):
    parser = ArgumentParser(description="Parses command.")
    parser.add_argument("input",
                        help="Input file with nonogram.",
                       )
    parser.add_argument("-l", "--live",
                        dest='interactive', default=False, action='store_true',
                        help="Live plotting mode.",
                       )
    parser.add_argument('-w', '--wait',
                        dest='wait', default=0.0, action='store', type=float,
                        help="Additional waiting time after each plot update in \
                        live plotting mode. Given in sec.",
                       )
    parser.add_argument("--hint",
                        dest='hinter', default=False, action='store_true',
                        help="Hinter mode.",
                       )
    parser.add_argument("-v", "--verbose",
                        dest='verbose', type=int, default=1, action='store',
                        help="Sets verbosity for hinter mode. (0-1)",
                       )
    parser.add_argument("-c", "--check",
                        dest='just_check',
                        help="File with presolved cells. Turns on verification mode. \
                        Checks whether mistake has been made. Does not plot the solution.",
                       )
    parser.add_argument("-d", "--depth",
                        dest='searching_depth', type=int, default=2, action='store',
                        help="Searching depth for assumption making.",
                       )
    options = parser.parse_args(args)
    return options

options = getOptions()

nono = Nonogram(options.input, presolved=None, wait=options.wait)

if options.interactive:
    nono.plot(interactive=options.interactive)

if options.hinter:
    nono.fill_cell = nono.show_hint
    nono.verbose = options.verbose


timeBeforeSolving = time()

cycle = solver(nono,
               searching_depth=options.searching_depth
              )

timeAfterSolving = time()


if options.just_check:
    user_nono = Nonogram(options.input, presolved=options.just_check)
    compare_nonograms(nono, user_nono, verbose=options.verbose)
    quit()

if not nono.meta_data.progress_tracker.get_number_of_undetermind_cells():
    print("Solved Nonogram in cycle: " + str(cycle) + ".")

print("Solved in : " + str(timeAfterSolving - timeBeforeSolving) + 's')

if not options.interactive:
    nono.plot()
else:
    nono.end_iplot()
