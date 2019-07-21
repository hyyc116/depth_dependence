#coding:utf-8

'''
1. 三个indictor 画图 level, depth, dependence


'''

from basic_config import *


plt.rc('legend',**{'fontsize':12})
markers = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']

def count_list(clist):
    level_counter = Counter(clist)
    size = len(clist)
    # logging.info('plot {:} distribution ...'.format(name))
    ## level的cdf
    cdf_xs = []
    cdf_ys = []

    cdf_num = 0
    for level in sorted(level_counter.keys()):
        cdf_xs.append(level)
        cdf_ys.append(cdf_num/float(size))
        cdf_num+=level_counter[level]


    return cdf_xs,cdf_ys

def load_data(path):
    logging.info('loading data ...')
    data_file = open(path)
    data_file.readline()

    data = []
    for line in data_file:
        line = line.strip().split(';')
        data.append(line)

    logging.info('data loaded ...')
    # print len(data)
    # print data[:10]
    # print len(zip(*data))
    return data

def fig3():

    # data = load_data('all_00-17_noclusters.csv')

    data = load_data('all_00_17_everything.csv')


    uts,levels,depths,dependences,pub_years,fields = zip(*data)

    levels = [float(level) for level in levels]

    depths = [float(depth) for depth in depths]

    dependences = [float(dependence) for dependence in dependences]

    # plot_dis_within_one(levels,depths,dependences)

    level_xs,level_ys = count_list(levels)
    depth_xs, depth_ys = count_list(depths)
    dependence_xs, dependence_ys = count_list(dependences)
    plt.figure()
    fig,axes = plt.subplots(3,1,figsize=(6,12))
    ax1 = axes[0]
    l1, = ax1.plot(level_xs,level_ys,label='level')
    ax1.set_ylabel('cumulative probability')
    ax1.set_xlabel('level\n(a)')
    ax1.set_xscale('log')
    # plot_field_dis(levels,fields,'level',True,ax=ax1)

    # ax1.set_ylim(0,20)

    ax2 = axes[1]

    ax2.plot(depth_xs,depth_ys,label='depth')
    ax2.set_xlabel('depth\n(b)')
    ax2.set_ylabel('cumulative probability')
    ax2.set_xlim(-0.5,16)
    # plot_field_dis(depths,fields,'level',  False,ax=ax2)



    ax3=axes[2]
    ax3.plot(dependence_xs,dependence_ys,label='dependence')
    ax3.set_xlabel('dependence\n(c)')
    ax3.set_ylabel('cumulative probability')
    ax3.set_xlim(-0.5,16)
    # plot_field_dis(levels,fields,'level',True,ax=ax1)
    # plot_field_dis(dependences,fields,'dependence',False,ax=ax3)


    fig.tight_layout()

    plt.savefig('fig/fig3.jpg',dpi=300)

def bin_levels(level):

    if level<200:
        return 0
    elif level<500:
        return 1
    elif level < 1000:
        return 2
    elif level < 2000:
        return 3
    else:
        return 4

def plot_box_relations(bin_levels,depths,l1,l2,labels,xlog=False,ax=None):

    level_depths = defaultdict(list)
    for i,bin_level in enumerate(bin_levels):
        depth = depths[i]
        level_depths[bin_level].append(depth)

    # plt.figure(figsize=(7,4))
    for bin_level in sorted(level_depths.keys()):

        # print l1,l2, bin_level, len(level_depths[bin_level])

        b_depths = level_depths[bin_level]

        xs,ys = cdf_list(b_depths)

        print bin_level,labels
        ax.plot(xs,ys,label='{:}:{:}'.format(l1,labels[bin_level]))




    # plt.figure(figsize=(10,5))

    # plt.boxplot(data)
    # plt.xticks(xs,labels)
    # plt.xlabel(l1)
    # plt.ylabel(l2)

    if xlog:
        ax.set_xscale('log')

    ax.set_ylabel('cumulative probability')
    ax.set_xlabel(l2)
    ax.legend()

def cdf_list(alist):
    acounter = Counter(alist)

    total = len(alist)

    acc_num = 0

    xs = []
    ys = []
    for a in sorted(acounter.keys()):
        xs.append(a)
        ys.append(acc_num/float(total))
        acc_num+=acounter[a]


    return xs,ys

def bin_dependence(dependence):
    if dependence <2:
        return 0
    elif dependence < 5:
        return 1
    elif dependence < 10:
        return 2
    # elif dependence < 20:
    #     return 3
    else:
        return 3


def fig4():

    data = load_data('all_00_17_everything.csv')

    uts,levels,depths,dependences,pub_years,fields = zip(*data)

    levels = [int(level) for level in levels]

    depths = [float(depth) for depth in depths]

    dependences = [float(dependence) for dependence in dependences]

    fig,axes = plt.subplots(3,1,figsize=(5,10))
    level_labels = ['[0.1k-0.2k)','[0.2k-0.5k)','[0.5k-1k)','[1k-2k)','2k+']
    depth_labels = ['[0-2)','[2-5)','[5-10)','10+']
    plot_box_relations([bin_levels(level) for level in levels],depths,'level','depth\n(a)',level_labels,ax=axes[0])
    axes[0].set_xlim(-0.5,16)
    plot_box_relations([bin_levels(level) for level in levels],dependences,'level','dependence\n(b)',level_labels,ax=axes[1])
    axes[1].set_xlim(-0.5,16)
    plot_box_relations([bin_dependence(depth) for depth in  depths],dependences,'depth','dependence\n(c)',depth_labels,ax=axes[2])
    axes[2].set_xlim(-0.5,16)


    plt.tight_layout()
    plt.savefig('fig/fig4.jpg',dpi=300)

def plot_field_dis(attrs,fields,name,log=True,ax=None):

    logging.info('plot field distribution ...')
    print name,len(attrs)
    field_nums = Counter(fields)
    field_attrs = defaultdict(list)

    for i,attr in enumerate(attrs):
        field = fields[i]

        field_attrs[field].append(attr)

    field_dict = {}

    field_dict['1'] = 'SSH'
    field_dict['2'] = 'BHS'
    field_dict['3'] = 'PSE'
    field_dict['4'] = 'LES'
    field_dict['5'] = 'MCS'

    field_xys = {}
    # for field in field_attrs.keys():
    for field in ['2','4','5','3','1']:

        # print field



        attrs = sorted(field_attrs[field])
        num = len(attrs)


        print field_dict[field],field_nums[field],np.mean(attrs),np.median(attrs),np.min(attrs),num

        attr_counter = Counter(attrs)
        xs = []
        ys = []
        has = 0
        for attr in sorted(attr_counter.keys()):
            xs.append(attr)
            ys.append(has/float(num))
            has+=attr_counter[attr]

            if name=='level' and attr==200:
                print has,has/float(num)

        field_xys[str(field)] = [xs,ys]



    # plt.figure(figsize=(7,4))
    # for field in np.arange(1,6):
    for field in ['2','4','5','3','1']:

        xs,ys = field_xys[str(field)]
        ax.plot(xs,ys,label=field_dict[str(field)])

    if log:
        ax.set_xscale('log')

    if name=='level':
        name = name+'\n(a)'
    elif name =='depth':
        name = name+'\n(b)'
    elif name=='dependence':
        name = name+'\n(c)'
    ax.set_xlabel(name)
    ax.set_ylabel('cumulative probability')

    # ax.set_xlim(-0.5,16)

    ax.legend(loc=4)

    # plt.legend()
    # plt.tight_layout()

    # plt.savefig('fig/field_{:}_dis.png'.format(name),dpi=400)

    # logging.info('Done')



def fig5():
    data = load_data('all_00_17_everything.csv')
    uts,levels,depths,dependences,pub_years,fields = zip(*data)

    levels = [int(level) for level in levels]

    depths = [float(depth) for depth in depths]

    dependences = [float(dependence) for dependence in dependences]

    fig,axes = plt.subplots(3,1,figsize=(5,10))
    plot_field_dis(levels,fields,'level',True,ax=axes[0])
    plot_field_dis(depths,fields,'depth',False,ax=axes[1])
    axes[1].set_xlim(-0.5,16)

    plot_field_dis(dependences,fields,'dependence',False,ax=axes[2])
    axes[2].set_xlim(-0.5,16)

    plt.tight_layout()
    plt.savefig('fig/fig5.jpg',dpi=300)



if __name__ == '__main__':
    # fig3()

    fig4()

    # fig5()
