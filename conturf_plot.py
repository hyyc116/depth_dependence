#coding:utf-8

from basic_config import *

from matplotlib import ticker, cm
import matplotlib.gridspec as gridspec

def test_grid():

    fig = plt.figure(tight_layout=True,figsize=(25,15))
    gs = gridspec.GridSpec(2, 3)

    ax = fig.add_subplot(gs[:, :2])
    ax.plot(np.arange(0, 1e6, 1000))
    ax.set_ylabel('YLabel0')
    ax.set_xlabel('XLabel0')

    for i in range(2):
        ax = fig.add_subplot(gs[i, 2])
        ax.plot(np.arange(1., 0., -0.1) * 2000., np.arange(1., 0., -0.1))
        ax.set_ylabel('YLabel1 %d' % i)
        ax.set_xlabel('XLabel1 %d' % i)
        if i == 0:
            for tick in ax.get_xticklabels():
                tick.set_rotation(55)
    fig.align_labels()  # same as fig.align_xlabels(); fig.align_ylabels()

    plt.savefig('test_layout.jpg',dpi=200)

def load_data(path):
    logging.info('loading data ...')
    data_file = open(path)
    data_file.readline()

    data = []
    for line in data_file:
        line = line.strip().split(',')
        data.append(line)

    logging.info('data loaded ...')
    # print len(data)
    # print data[:10]
    # print len(zip(*data))
    return data


def plot_conturf():

    data = load_data('scim_new_20190618.CSV')


    uts,levels,depths,dependences,pub_years= zip(*data)


    x = np.array([int(l) for l in levels])
    y = np.array([float(d) for d in depths])
    y2 = np.array([float(d) for d in dependences])

    def z(x,y):

        return x*y

    ## 全局
    x_range = np.linspace(np.min(x),np.max(x)+100,10000)
    y_range = np.linspace(np.min(y),np.max(y)+1,1000)

    X, Y = np.meshgrid(x_range, y_range)
    z1 = z(X,Y)

    fig = plt.figure(tight_layout=True,figsize=(10,6))
    gs = gridspec.GridSpec(2, 3)
    ax = fig.add_subplot(gs[:, :2])
    cs = ax.contourf(X, Y, z1, cmap=cm.RdBu_r,alpha=0.9)

    ax.set_xlabel('level\n(a)')

    ax.set_ylabel('relative depth')

    ax.plot(x,y,'ko',alpha=0.8)
    cbar = fig.colorbar(cs,ax=ax)

    ## log
    ax = fig.add_subplot(gs[0, 2])
    cs = ax.contourf(X, Y, z1, cmap=cm.RdBu_r,alpha=0.9)
    ax.plot(x,y,'ko',alpha=0.8)
    ax.set_xscale('log')
    cbar = fig.colorbar(cs,ax=ax)
    ax.set_xlabel('level\n(b)')

    ax.set_ylabel('relative depth')


    ## log
    x_range = np.linspace(np.min(x),510,10000)
    y_range = np.linspace(np.min(y),np.max(y)+1,1000)

    X, Y = np.meshgrid(x_range, y_range)
    z1 = z(X,Y)
    ax = fig.add_subplot(gs[1, 2])
    cs = ax.contourf(X, Y, z1, cmap=cm.RdBu_r,alpha=0.9)
    ax.plot(x,y,'ko',alpha=0.8)
    ax.set_xlim(0,510)
    cbar = fig.colorbar(cs,ax=ax)
    ax.set_xlabel('level\n(c)')

    ax.set_ylabel('relative depth')

    plt.savefig('conturf_depth.jpg',dpi=400)


    ## 全局
    x_range = np.linspace(np.min(x),np.max(x)+100,10000)
    y_range = np.linspace(np.min(y2),np.max(y2)+1,1000)

    X, Y = np.meshgrid(x_range, y_range)
    z1 = z(X,Y)

    fig = plt.figure(tight_layout=True,figsize=(10,6))
    gs = gridspec.GridSpec(2, 3)
    ax = fig.add_subplot(gs[:, :2])
    cs = ax.contourf(X, Y, z1, cmap=cm.RdBu_r,alpha=0.9)

    ax.set_xlabel('level\n(a)')

    ax.set_ylabel('relative dependence')

    ax.plot(x,y2,'ko',alpha=0.8)
    cbar = fig.colorbar(cs,ax=ax)

    ## log
    ax = fig.add_subplot(gs[0, 2])
    cs = ax.contourf(X, Y, z1, cmap=cm.RdBu_r,alpha=0.9)
    ax.plot(x,y2,'ko',alpha=0.8)
    ax.set_xscale('log')
    cbar = fig.colorbar(cs,ax=ax)
    ax.set_xlabel('level\n(b)')

    ax.set_ylabel('relative dependence')


    ## log
    x_range = np.linspace(np.min(x),510,10000)
    y_range = np.linspace(np.min(y2),10+1,1000)

    X, Y = np.meshgrid(x_range, y_range)
    z1 = z(X,Y)
    ax = fig.add_subplot(gs[1, 2])
    cs = ax.contourf(X, Y, z1, cmap=cm.RdBu_r,alpha=0.9)
    ax.plot(x,y2,'ko',alpha=0.8)
    ax.set_xlim(0,510)
    ax.set_ylim(0,11)
    cbar = fig.colorbar(cs,ax=ax)
    ax.set_xlabel('level\n(c)')

    ax.set_ylabel('relative dependence')

    plt.savefig('conturf_dependence.jpg',dpi=400)

if __name__ == '__main__':
    plot_conturf()

    # test_grid()
