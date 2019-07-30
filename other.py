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


    absolute_depths = np.array(depths)*np.array(levels)
    absolute_dependences = np.array(dependences)*np.array(levels)

    # plot_dis_within_one(levels,depths,dependences)

    level_xs,level_ys = count_list(levels)
    ab_depth_xs, ab_depth_ys = count_list(absolute_depths)
    depth_xs, depth_ys = count_list(depths)
    ab_dependence_xs, ab_dependence_ys = count_list(absolute_dependences)
    dependence_xs, dependence_ys = count_list(dependences)

    # plt.figure()
    fig,axes = plt.subplots(5,1,figsize=(4,15))
    ax1 = axes[0]
    l1, = ax1.plot(level_xs,level_ys,label='level')
    ax1.set_ylabel('cumulative probability')
    ax1.set_xlabel('level\n(a)')
    ax1.set_xscale('log')
    # plot_field_dis(levels,fields,'level',True,ax=ax1)

    # ax1.set_ylim(0,20)

    ax2 = axes[1]

    ax2.plot(ab_depth_xs,ab_depth_ys,label='depth')
    ax2.set_xlabel('absolute depth\n(b)')
    ax2.set_ylabel('cumulative probability')
    ax2.set_xscale('log')
    # ax2.set_xlim(-0.5,16)

    ax3 = axes[2]

    ax3.plot(depth_xs,depth_ys,label='depth')
    ax3.set_xlabel('relvative depth\n(c)')
    ax3.set_ylabel('cumulative probability')
    ax3.set_xlim(-0.5,16)
    # plot_field_dis(depths,fields,'level',  False,ax=ax2)


    ax4=axes[3]
    ax4.plot(ab_dependence_xs,ab_dependence_ys,label='dependence')
    ax4.set_xlabel('absolute dependence\n(d)')
    ax4.set_ylabel('cumulative probability')
    ax4.set_xscale('log')
    # ax4.set_xlim(-0.5,16)


    ax5=axes[4]
    ax5.plot(dependence_xs,dependence_ys,label='dependence')
    ax5.set_xlabel('relative dependence\n(e)')
    ax5.set_ylabel('cumulative probability')
    # ax5.set_xlim(-0.5,16)
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


def bin_abs_depth(depth):

    if depth<10:
        return 0
    elif depth<100:
        return 1
    elif depth <1000:
        return 2
    elif depth <10000:
        return 3
    else:
        return 4

def fig4():

    data = load_data('all_00_17_everything.csv')

    uts,levels,depths,dependences,pub_years,fields = zip(*data)

    levels = [int(level) for level in levels]

    depths = [float(depth) for depth in depths]

    dependences = [float(dependence) for dependence in dependences]

    absolute_depths = np.array(depths)*np.array(levels)
    absolute_dependences = np.array(dependences)*np.array(levels)

    fig,axes = plt.subplots(3,2,figsize=(10,12))
    level_labels = ['[0.1k-0.2k)','[0.2k-0.5k)','[0.5k-1k)','[1k-2k)','2k+']
    depth_labels = ['[0-2)','[2-5)','[5-10)','10+']
    abs_depth_labels = ['[$10^0$,$10^1$)','[$10^1$,$10^2$)','[$10^2$,$10^3$)','[$10^3$,$10^4$)','$10^4$+']
    plot_box_relations([bin_levels(level) for level in levels],absolute_depths,'level','absolute depth\n(a)',level_labels,ax=axes[0,0])
    axes[0,0].set_xscale('log')

    plot_box_relations([bin_levels(level) for level in levels],depths,'level','relative depth\n(b)',level_labels,ax=axes[0,1])
    axes[0,1].set_xlim(-0.5,16)

    plot_box_relations([bin_levels(level) for level in levels],absolute_dependences,'level','absolute dependence\n(c)',level_labels,ax=axes[1,0])
    axes[1,0].set_xscale('log')

    plot_box_relations([bin_levels(level) for level in levels],dependences,'level','relative dependence\n(d)',level_labels,ax=axes[1,1])
    axes[1,1].set_xlim(-0.5,16)

    plot_box_relations([bin_dependence(depth) for depth in  depths],dependences,'relative depth','relative dependence\n(e)',depth_labels,ax=axes[2,0])
    axes[2,0].set_xlim(-0.5,16)


    plot_box_relations([bin_abs_depth(depth) for depth in  absolute_depths],absolute_dependences,'abs depth','absolute dependence\n(f)',abs_depth_labels,ax=axes[2,1])
    axes[2,1].set_xscale('log')


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


    absolute_depths = np.array(depths)*np.array(levels)
    absolute_dependences = np.array(dependences)*np.array(levels)

    fig,axes = plt.subplots(5,1,figsize=(4,15))
    plot_field_dis(levels,fields,'level\n(a)',True,ax=axes[0])
    plot_field_dis(absolute_depths,fields,'absolute depth\n(b)',False,ax=axes[1])
    axes[1].set_xscale('log')
    plot_field_dis(depths,fields,'relative depth\n(c)',False,ax=axes[2])
    axes[2].set_xlim(-0.5,16)

    plot_field_dis(absolute_dependences,fields,'absolute dependence\n(d)',False,ax=axes[3])
    axes[3].set_xscale('log')
    plot_field_dis(dependences,fields,'relative dependence\n(e)',False,ax=axes[4])
    axes[4].set_xlim(-0.5,16)

    plt.tight_layout()
    plt.savefig('fig/fig5.jpg',dpi=300)


def tab_1_2():

    data = load_data('all_00_17_everything.csv')

    uts,levels,depths,dependences,pub_years,fields = zip(*data)

    levels = [int(level) for level in levels]

    depths = [float(depth) for depth in depths]

    dependences = [float(dependence) for dependence in dependences]

    absolute_depths = np.array(depths)*np.array(levels)
    absolute_dependences = np.array(dependences)*np.array(levels)


    labels = ['level','absolute depth','relative depth','absolute dependence','relative dependence']

    datas = [levels,absolute_depths,depths,absolute_dependences,dependences]

    lines = ['| |'+'|'.join(labels)+'|']
    lines.append('|'+"|".join([':---:']*(len(labels)+1))+'|')

    tab2 = ['| |'+'|'.join(labels)+'|']
    tab2.append('|'+"|".join([':---:']*(len(labels)+1))+'|')

    for i,data1 in enumerate(datas):
        line = []
        line2 = []
        for j,data2 in enumerate(datas):

            if j<i:
                line.append(' ')
                line2.append(' ')
                continue


            # print labels[i],';',labels[j],';',pearsonr(data1,data2)

            line.append('{:.2f}'.format(pearsonr(data1,data2)[0]))
            line2.append('{:.2f}'.format(spearmanr(data1,data2)[0]))

        lines.append(labels[i]+'|'+'|'.join(line)+"|")
        tab2.append(labels[i]+'|'+'|'.join(line2)+"|")

    print('\n'.join(lines))

    f = open('README.md','w')

    f.write('#### TABLE 1\n')

    f.write('\n'.join(lines)+'\n')

    f.write('#### TABLE 2\n')

    f.write('\n'.join(tab2)+'\n')

    f.close()

def tab_3():

    data = load_data('all_00_17_everything.csv')
    uts,levels,depths,dependences,pub_years,fields = zip(*data)

    levels = [int(level) for level in levels]

    depths = [float(depth) for depth in depths]

    dependences = [float(dependence) for dependence in dependences]


    absolute_depths = np.array(depths)*np.array(levels)
    absolute_dependences = np.array(dependences)*np.array(levels)

    field_dict = {}

    field_dict['1'] = 'SSH'
    field_dict['2'] = 'BHS'
    field_dict['3'] = 'PSE'
    field_dict['4'] = 'LES'
    field_dict['5'] = 'MCS'

    sorted_fields =  ['2','4','5','3','1']

    field_attr_list = defaultdict(lambda:defaultdict(list))

    for i,field in enumerate(fields):

        level = levels[i]
        depth = depths[i]
        abs_depth = depths[i]

        dependence = dependences[i]
        abs_dependence = absolute_dependences[i]

        field_attr_list[field]['level'].append(level)
        field_attr_list[field]['depth'].append(depth)

        field_attr_list[field]['dependence'].append(dependence)

        field_attr_list[field]['abs_depth'].append(abs_depth)

        field_attr_list[field]['abs_dependence'].append(abs_dependence)


    # lines = ['| |'+'|'.join(['No. of Pub','Mean Level','Mean Level','Mean Level','Mean Level','Mean Level','Mean Level','Mean Level','Mean Level','Mean Level','Mean Level','Mean Level','Mean Level','Mean Level','Mean Level','Mean Level'])]

    datas = []
    datas.append([' ','No. of Pub','Mean Level','Median Level','Max. Level','Mean absolute depth','Median absolute depth','Max. absolute depth','Mean relative depth','Median relative depth','Max. relative depth','Mean absolute dependence','Median absolute dependence','Max. absolute dependence','Mean relvative dependence','Median relvative dependence','Max. relvative dependence'])
    for field in sorted_fields:

        field_name = field_dict[field]

        levels = field_attr_list[field]['level']
        depths = field_attr_list[field]['depth']
        dependences = field_attr_list[field]['dependence']

        abs_depths = field_attr_list[field]['abs_depth']
        abs_dependences = field_attr_list[field]['abs_dependence']

        num = len(levels)
        print num

        mean_level,median_level,max_level = np.mean(levels),np.median(levels),np.max(levels)
        mean_depth,median_depth,max_depth = np.mean(depths),np.median(depths),np.max(depths)
        mean_dependence,median_dependence,max_dependence = np.mean(dependences),np.median(dependences),np.max(dependences)

        mean_abs_depth,median_abs_depth,max_abs_depth = np.mean(abs_depths),np.median(abs_depths),np.max(abs_depths)
        mean_abs_dependence,median_abs_dependence,max_abs_dependence = np.mean(abs_dependences),np.median(abs_dependences),np.max(abs_dependences)

        datas.append([field_name,num,mean_level,median_level,max_level,mean_abs_depth,median_abs_depth,max_abs_depth,mean_depth,median_depth,max_depth,mean_abs_dependence,median_abs_dependence,max_abs_dependence,mean_dependence,median_dependence,max_dependence])


    data = np.array(datas).transpose()

    # print data

    lines = ['|'+'|'.join(data[0])+'|']

    lines.append('|'+'|'.join([':---:']*len(data[0]))+"|")

    for line in data[1:]:

        lines.append('|'+line[0]+'|'+'|'.join(['{:.2f}'.format(float(l)) for l in line[1:]])+'|')

    # print lines

    f = open('README.md','a')

    f.write('#### TABLE 3\n')

    f.write('\n'.join(lines)+'\n')

    f.close()



if __name__ == '__main__':
    # fig3()

    # fig4()

    # fig5()

    tab_1_2()

    tab_3()
