from time import time
from sys import argv
from argparse import ArgumentParser

from lib.nonogram import Nonogram
from lib.solver import solver
from utils.tools import compare_nonograms

def getOptions(args):
    parser = ArgumentParser(description="Parses command.")
    parser.add_argument("input",
                        help="Input file with nonogram.",
                       )
    parser.add_argument("-l", "--live",
                        dest='wait_time',
                        default=-1.0, const=0.0,
                        action='store', nargs='?', type=float,
                        help="Live plotting mode. May be provided with time \
                        (in seconds) to wait after each plot update.",
                       )
    parser.add_argument("--hint",
                        dest='hinter', default=False, action='store_true',
                        help="Hinter mode.",
                       )
    parser.add_argument("-v", "--verbosity",
                        dest='verbosity', type=int, default=1, action='store',
                        help="Sets verbosity for hinter mode. (0-1)",
                       )
    parser.add_argument("-c", "--check",
                        dest='presolved_datafile',
                        help="File with presolved cells. Turns on verification mode. \
                        Checks whether mistake has been made. Does not plot the solution.",
                       )
    parser.add_argument("-d", "--depth",
                        dest='searching_depth', type=int, default=2, action='store',
                        help="Searching depth for assumption making.",
                       )
    read_options = parser.parse_args(args)
    return read_options

options = getOptions(argv[1:])

nono = Nonogram(options.input, presolved=None, wait=options.wait_time)


if options.wait_time > -1e-9:
    nono.plot(interactive=True)

if options.hinter:
    nono.fill_cell = nono.show_hint
    nono.mode_data.set_verbosity(options.verbosity)


timeBeforeSolving = time()

cycle = solver(nono,
               searching_depth=options.searching_depth
              )

timeAfterSolving = time()


if options.presolved_datafile:
    user_nono = Nonogram(options.input, presolved=options.presolved_datafile)
    compare_nonograms(nono, user_nono, verbose=options.verbosity)
    quit()

if not nono.meta_data.progress_tracker.get_number_of_undetermind_cells():
    print("Solved Nonogram in cycle: " + str(cycle) + ".")

print("Solved in : " + str(timeAfterSolving - timeBeforeSolving) + 's')

if options.wait_time > -1e-9:
    nono.end_iplot()
else:
    nono.plot()
