def create_plot(x, y, name):
    data = {
        'x': x,
        'y': y,
        'mode': 'lines',
        'type': 'scatter',
        'name': name,
    }

    return data


def all_plots(N, tab, const_p):
    plots = []
    x = [i*const_p/60 for i in range(N)]
    for i in range(len(tab)):
        plots.append([create_plot(x, tab[i][1], tab[i][0] ), create_plot(x, tab[i][3], tab[i][2])])


    return plots
