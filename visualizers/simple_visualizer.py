from pylab import figure, grid, imshow, show

def just_plot_it(nonogram):
    figure(1, dpi=100)
    if not nonogram.transposed:
        imshow([row[:-1] for row in nonogram.rows], cmap='binary', origin='upper', \
               extent=( 0.5 , 0.5 + nonogram.nRows, 0.5 , 0.5 + nonogram.nCols ))
    else:
        imshow([row[:-1] for row in nonogram.cols], cmap='binary', \
               extent=( 0.5 , 0.5 + nonogram.nCols, 0.5 , 0.5 + nonogram.nRows ))
    grid(False)
    show()