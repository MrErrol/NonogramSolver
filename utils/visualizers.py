from time import sleep
from matplotlib import pyplot as plt


def end_iplot():
    "Ends interactive plot."
    plt.ioff()
    plt.show()


def update_plot(data, fig, image, wait):
    "Updates interactive plot."
    image.set_data(data)
    fig.canvas.draw()
    fig.canvas.flush_events()
    sleep(wait)


def call_imshow(data):
    "Calls pyplot.imshow with bunch of parameters."
    plt.axis('off')
    return plt.imshow(data,
                      cmap='binary', origin='upper',
                      vmin=-1, vmax=1,
                      extent=(0.5, 0.5 + len(data[0]), 0.5, 0.5 + len(data)),
                     )


def plot(data, interactive=False):
    """
    Initializes plot and plots the data provided.
    Works both for interactive and static plots.
    """
    if interactive:
        plt.ion()
        fig = plt.figure()
        fig.canvas.draw()
        image = call_imshow(data)
    else:
        fig = plt.figure()
        image = call_imshow(data)
        plt.show()
    return fig, image
