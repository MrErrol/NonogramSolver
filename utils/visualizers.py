from matplotlib import pyplot as plt


def end_iplot():
    plt.ioff()
    plt.show()


def update_plot(data, fig, im):
    im.set_data(data)
    fig.canvas.draw()
    fig.canvas.flush_events()


def call_imshow(data):
    plt.axis('off')
    return plt.imshow(data,
                      cmap='binary', origin='upper',
                      vmin=-1, vmax=1,
                      extent=( 0.5 , 0.5 + len(data[0]), 0.5 , 0.5 + len(data) ),
                      )


def plot(data, interactive=False):
    if interactive:
        plt.ion()
        fig = plt.figure()
        fig.canvas.draw()
        im = call_imshow(data)
    else:
        fig = plt.figure()
        im = call_imshow(data)
        plt.show()
    return fig, im
