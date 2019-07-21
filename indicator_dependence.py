#coding:utf-8

'''
1. 三个indictor 画图 level, depth, dependence


'''

from basic_config import *
plt.rc('legend',**{'fontsize':12})
markers = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']
def load_data():
	logging.info('loading data ...')
	data_file = open('depth_dependence.csv')
	data_file.readline()

	data = []
	for line in data_file:
		line = line.strip().split(',')
		data.append(line)

	logging.info('data loaded ...')
	return zip(*data)


def distributiion_three_indicators(data):
	uts,levels,depths,dependences,pub_years,fields = data

	levels = [int(level) for level in levels]

	depths = [float(depth) for depth in depths]

	dependences = [float(dependence) for dependence in dependences]

	plot_dis_within_one(levels,depths,dependences)

	# plot_dis(levels,'level',True)

	# plot_dis(depths,'depth',False)

	# plot_dis(dependences,'dependence',False)
	fig,axes = plt.subplots(4,1,figsize=(5,14))
	plot_field_dis(levels,fields,'level',True,ax=axes[0],ax4=axes[3])
	plot_field_dis(depths,fields,'depth',False,ax=axes[1],ax4=axes[3])
	plot_field_dis(dependences,fields,'dependence',False,ax=axes[2],ax4=axes[3])
	plt.tight_layout()
	plt.savefig('field_dis.jpg',dpi=300)
	# plot_correlation(levels,depths,'level','depth',True)
	# plot_correlation(levels,dependences,'level','dependence',True)
	# plot_correlation(dependences,depths,'dependence','depth',False)

	fig,axes = plt.subplots(3,1,figsize=(5,10))
	level_labels = ['[0.1k-0.2k)','[0.2k-0.5k)','[0.5k-1k)','[1k-2k)','[2k-5k)','5k+']
	depth_labels = ['[0-2)','[2-5)','[5-10)','[10-20)','20+']
	plot_box_relations([bin_levels(level) for level in levels],depths,'level','depth\n(a)',level_labels,ax=axes[0])
	plot_box_relations([bin_levels(level) for level in levels],dependences,'level','dependence\n(b)',level_labels,ax=axes[1])

	plot_box_relations([bin_dependence(dependence) for dependence in  dependences],depths,'dependence','depth\n(c)',depth_labels,ax=axes[2])

	plt.tight_layout()
	plt.savefig('relation.jpg',dpi=300)

	# plot_box_relations([bin_dependence(dependence) for dependence in  dependences],levels,'dependence','level\n(d)',depth_labels,xlog=True)

	# plot_box_relations([bin_depth(depth) for depth in  depths],dependences,'depth','dependence\n(e)',depth_labels)
	# plot_box_relations([bin_depth(depth) for depth in  depths],levels,'depth','level\n(f)',depth_labels,xlog=True)


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

	ax.set_ylabel('cumulative percentage')
	ax.set_xlabel(l2)
	ax.legend()

	# plt.tight_layout()

	# plt.savefig('fig/cdf_{:}_{:}.png'.format(l1,l2),dpi=200)


def cdf_list(alist):
	acounter = Counter(alist)

	total = len(alist)

	acc_num = 0

	xs = []
	ys = []
	for a in sorted(acounter.keys()):
		acc_num+=acounter[a]
		xs.append(a)
		ys.append(acc_num/float(total))

	return xs,ys






def bin_levels(level):

	if level<200:
		return 0
	elif level<500:
		return 1
	elif level < 1000:
		return 2
	elif level < 2000:
		return 3
	elif level <5000:
		return 4

	else:
		return 5

	# elif level < 10000:
	# 	return 5
	# elif level < 20000:
	# 	return 6
	# elif level < 50000:
	# 	return 7

	# elif level < 100000:
	# 	return 8

def bin_depth(depth):

	if depth <2:
		return 0
	elif depth < 5:
		return 1
	elif depth < 10:
		return 2
	elif depth < 20:
		return 3
	elif depth < 50:
		return 4

def bin_dependence(dependence):
	if dependence <2:
		return 0
	elif dependence < 5:
		return 1
	elif dependence < 10:
		return 2
	elif dependence < 20:
		return 3
	elif dependence < 50:
		return 4


def plot_correlation(levels,depths,l1,l2,log=True):

	plt.figure()

	plt.plot(levels,depths,'o',fillstyle='none')
	plt.xlabel(l1)
	plt.ylabel(l2)

	if log:
		plt.xscale('log')

	plt.tight_layout()

	plt.savefig('fig/{:}_{:}.png'.format(l1,l2),dpi=200)


def plot_field_dis(attrs,fields,name,log=True,ax=None,ax4=None):

	logging.info('plot field distribution ...')
	print name
	field_attrs = defaultdict(list)

	for i,attr in enumerate(attrs):
		field = fields[i]

		field_attrs[field].append(attr)


	# format
	# plt.figure()

	field_xys = {}
	for field in field_attrs.keys():

		attrs = field_attrs[field]



		n,bins,patches = ax4.hist(attrs,bins=1000)

		print len(n),len(bins),len(patches)
		print field
		field_xys[str(field)] = [bins[:-1],n]

	field_dict = {}

	field_dict['1'] = 'Social sciences and humanities'
	field_dict['2'] = 'Biomedical and health sciences'
	field_dict['3'] = 'Physical sciences and engineering'
	field_dict['4'] = 'Life and earth sciences'
	field_dict['5'] = 'Mathematics and computer science'

	# plt.figure(figsize=(7,4))
	for field in np.arange(1,6):
		xs,ys = field_xys[str(field)]
		now = 0
		cdf_ys = []
		total = np.sum(ys)
		for y in ys:
			now+=y
			cdf_ys.append(now/float(total))

		ax.plot(xs,cdf_ys,label=field_dict[str(field)])
		# print xs,cdf_ys
	# plt.yscale('log')
	if log:
		ax.set_xscale('log')

	if name=='level':
		name = name+'\n(a)'
	elif name =='depth':
		name = name+'\n(b)'
	elif name=='dependence':
		name = name+'\n(c)'
	ax.set_xlabel(name)
	ax.set_ylabel('cumulative distribution')

	# plt.legend()
	# plt.tight_layout()

	# plt.savefig('fig/field_{:}_dis.png'.format(name),dpi=400)

	# logging.info('Done')



def plot_dis(levels,name,log=True):
	level_counter = Counter(levels)
	size = len(levels)
	logging.info('plot {:} distribution ...'.format(name))
	## level的cdf
	cdf_xs = []
	cdf_ys = []
	pdf_ys = []

	cdf_num = 0
	for level in sorted(level_counter.keys()):
		cdf_xs.append(level)
		cdf_num+=level_counter[level]
		cdf_ys.append(cdf_num)

		pdf_ys.append(level_counter[level])


	fig,axes = plt.subplots(1,2,figsize=(10,5))
	ax1 = axes[0]
	ax1.plot(cdf_xs,list(np.array(cdf_ys)/float(size)))
	ax1.set_xlabel(name)
	if log:
		ax1.set_xscale('log')
	# plt.yscale('log')
	ax1.set_ylabel('$P(x<={:})$'.format(name))
	ax1.set_title('CDF')

	ax2 = axes[1]
	ax2.plot(cdf_xs,pdf_ys)
	# ax2.hist(levels,bins=100,log=True)
	ax2.set_xlabel(name)
	ax2.set_ylabel('number of papers')

	if log:
		ax2.set_xscale('log')

	ax2.set_yscale('log')
	ax2.set_title('PDF')


	plt.tight_layout()
	plt.savefig('fig/{:}_dis.png'.format(name),dpi=200)
	logging.info('done')

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
		cdf_num+=level_counter[level]
		cdf_ys.append(cdf_num/float(size))

	return cdf_xs,cdf_ys

def plot_dis_within_one(levels,depths,dependences):

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

	ax2 = axes[1]

	ax2.plot(depth_xs,depth_ys,label='depth')
	ax2.set_xlabel('depth\n(b)')
	ax2.set_ylabel('cumulative probability')

	ax3=axes[2]
	ax3.plot(dependence_xs,dependence_ys,label='dependence')
	ax3.set_xlabel('dependence\n(c)')
	ax3.set_ylabel('cumulative probability')

	fig.tight_layout()

	plt.savefig('fig/three_attr_dis.png',dpi=200)



if __name__ == '__main__':
	data = load_data()
	distributiion_three_indicators(data)









