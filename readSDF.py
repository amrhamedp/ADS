__author__ = 'feiyicheng'

import networkx as nx
from StringIO import StringIO

def concat(stringlist):
	result = ""
	for str in stringlist:
		result += str
	return result


def graphFromSDF(filechem):
	# filechem is a file object
	for i in range(3) :
		filechem.readline() #skip the first 3 lines
	metadata = filechem.readline( ).strip( ).split( )
	numAtom = int(metadata[0])
	numBond = int(metadata[1])

	g = nx.Graph( ) # restore the topology
	graph = {}  # restore the metadata
	for i in range(numAtom):
		atomline = filechem.readline()
		atomdata = atomline.strip( ).split( )
		graph[i+1] = {'index':i+1, 'atomtype':atomdata[3], 'x':atomdata[0],'y':atomdata[1]}

	for i in range(numBond):
		bondline = filechem.readline()
		bonddata = bondline.strip().split()
		graph[int(bonddata[0])][int(bonddata[1])] = {'index':i+1, 'bondtype':bonddata[2]}
		graph[int( bonddata[1] )][int(bonddata[0])] = graph[int( bonddata[0] )][int(bonddata[1])]
		# print(graph[int( bonddata[0])])
		if graph[int(bonddata[0])]['atomtype'] != "H" and graph[int( bonddata[1] )]['atomtype']!="H":
			g.add_weighted_edges_from([ (int(bonddata[0]),int(bonddata[1]), int(bonddata[2]) )] )

	# check no. of lines
	if not filechem.readline().split()[0] == "M":
		raise Exception("counting errer!")
	return (g, graph)


def graphsFromSDF(filechem):
	# path = ""
	# filechem = open(path)
	content  = concat(filechem.readlines())
	slices = content.split("$$$$\n")
	# print(len(slices))
	results = []
	for slice in slices:
		if slice == '':
			continue
		fakefile = StringIO(slice)
		results.append(graphFromSDF(fakefile))
	return results

if __name__ == '__main__':
	molecules = graphsFromSDF(open("/Users/feiyicheng/Desktop/ADS/Develop/test2.sdf"))
