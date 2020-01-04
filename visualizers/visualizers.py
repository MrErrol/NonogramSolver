from matplotlib import pyplot as plt

def end_iplot():
    plt.ioff()
    plt.show()

def update_plot(data, fig, im):
    im.set_data(data)
    fig.canvas.draw()
    fig.canvas.flush_events()

def plot(data, interactive=False):
    if interactive:
        plt.ion()
        fig = plt.figure()
        fig.canvas.draw()
        im = plt.imshow(data, cmap='binary', origin='upper', vmin=-1, vmax=1, \
                        extent=( 0.5 , 0.5 + len(data), 0.5 , 0.5 + len(data[0]) ) )
    else:
        fig = plt.figure()
        im = plt.imshow(data, cmap='binary', origin='upper', vmin=-1, vmax=1, \
                        extent=( 0.5 , 0.5 + len(data), 0.5 , 0.5 + len(data[0]) ) )
        plt.show()
    return fig, im