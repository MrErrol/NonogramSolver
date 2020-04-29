from time import time
from sys import argv
from argparse import ArgumentParser

from lib.nonogram import Nonogram
from lib.solver import solver
from utils.tools import compare_nonograms


def find_and_print_hint(options):
    """
    Function initializes new (possibly presolved) nonogram and prints hint
    for the next cell to be filled.
    """
    new_nono = Nonogram(options.input)
    new_nono.mode_data.set_verbosity(options.verbosity)
    solver(new_nono, searching_depth=options.searching_depth)


def get_options(args):
    """
    Function parses command line arguments.
    """
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
                        dest='verbosity',
                        default=-1, const=0,
                        action='store', nargs='?', type=int,
                        help="Hinter mode. May be provided with verbosity (0-1).",
                       )
    parser.add_argument("-c", "--check",
                        dest='presolved_datafile', default=None,
                        help="File with presolved cells. Turns on verification mode. \
                        Checks whether mistake has been made. Does not plot the solution.",
                       )
    parser.add_argument("-d", "--depth",
                        dest='searching_depth', type=int, default=2, action='store',
                        help="Searching depth for assumption making.",
                       )
    read_options = parser.parse_args(args)
    return read_options

if __name__ == '__main__':
    OPTIONS = get_options(argv[1:])


    # Prevents setting interactive plot for check and hinter modes
    if OPTIONS.wait_time > -1e-9 and (OPTIONS.presolved_datafile or OPTIONS.verbosity >= 0):
        print("Can't use live mode with hint mode or check mode.")
        quit()

    # Creating empty datafile for special case of hint mode giving just first move
    if OPTIONS.verbosity >= 0 and not OPTIONS.presolved_datafile:
        print("You haven't provided me any presolved cells!")
        print("Have this for a good start:")
        find_and_print_hint(OPTIONS)
        quit()


    NONOGRAM = Nonogram(OPTIONS.input, presolved=None, wait=OPTIONS.wait_time)


    if OPTIONS.wait_time > -1e-9:
        NONOGRAM.plot(interactive=True)


    TIME_BEFORE_SOLVING = time()

    CYCLE = solver(NONOGRAM, searching_depth=OPTIONS.searching_depth)

    TIME_AFTER_SOLVING = time()


    if OPTIONS.presolved_datafile:
        USER_NONOGRAM = Nonogram(OPTIONS.input, presolved=OPTIONS.presolved_datafile)
        compare_nonograms(NONOGRAM, USER_NONOGRAM, verbose=OPTIONS.verbosity)

        if OPTIONS.verbosity >= 0:
            find_and_print_hint(OPTIONS)

        quit()

    if not NONOGRAM.meta_data.progress_tracker.get_number_of_undetermind_cells():
        print("Solved Nonogram in cycle: " + str(CYCLE) + ".")

    print("Solving took : " + str(TIME_AFTER_SOLVING - TIME_BEFORE_SOLVING) + 's')

    if OPTIONS.wait_time > -1e-9:
        NONOGRAM.end_iplot()
    else:
        NONOGRAM.plot()
