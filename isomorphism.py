__author__ = 'feiyicheng'

import networkx
from networkx.algorithms import isomorphism
from matplotlib import pyplot
from collections import Counter

class NotIsomorphismException( Exception ):
	def __init__(self, msg):
		self.message = msg


def getReactionCenter(g1, g2):
	"""
	Input: keys are integers
		g1: The reactant(OR product)
		g2: MCS(maximum common substructure) between reactant and product(main)
	Output:
		[(n1, n2),(n1',n2')], representing all possibles of the keys of the reaction center in g1 and g2
	"""
	if type( g1 )!=networkx.classes.Graph or type( g1 )!=type( g2 ):
		raise TypeError( "g1 and g2 should be an instance of Graph" )

	# Matcher of g1 and g2
	gm = isomorphism.GraphMatcher( g1, g2, edge_match=lambda e1,e2: e1['weight']==e2['weight'])


	# if g2 is not MCS return error
	if not gm.subgraph_is_isomorphic():
		raise NotIsomorphismException( "g2 should be a subgraph of g1" )


	# Oops! the gm.mapping dict will generate only if the above method has been executed


	# get the reaction center
	answers = []
	for mapping in gm.subgraph_isomorphisms_iter():
		# generate dict from g2 to g1 (since g2 is substructure so that map a key in g2 into g1 will always succeed)
		map2to1 = {v: k for (k, v) in mapping.items( )}

		for (key1, key2) in mapping.iteritems( ):
			neighbor1 = g1.neighbors( key1 )
			neighbor2 = g2.neighbors( key2 )
			neighbor2to1 = map(lambda key : map2to1[key] , neighbor2)
			if not Counter(neighbor1) == Counter(neighbor2to1):
				answers.append((key1, key2))
				break

	return list(set(answers))



if __name__ == '__main__':
	# construct Graph 1
	g1_nodes = [1,2,3,4,5,6]
	g1_edges = [
		(1,2),
		(1,3),
		(1,4),
		(3,4),
		(3,5),
		(1,6),
		(4,6),
	]
	g1 = networkx.Graph()
	g1.add_nodes_from(g1_nodes)
	g1.add_edges_from(g1_edges, weight=3)

	# construct Graph 2
	g2_nodes = [1,2,3,4,5]
	g2_edges = [
		(1,2),
		(2,4),
		(2,3),
		(2,5),
		(4,5),
		(3,5),
	]
	g2 = networkx.Graph( )
	g2.add_nodes_from( g2_nodes )
	g2.add_edges_from( g2_edges ,weight=3)

	# Match the two graph
	gm = isomorphism.GraphMatcher(g1,g2)

	# networkx.draw_networkx(g1)
	# networkx.draw_networkx( g2 )
	# pyplot.show()

	# get iterator of all possible subgraphs
	# subgs =  gm.subgraph_isomorphisms_iter()
	# networkx.draw_networkx(g1)
	# pyplot.show()
	print(g2[1][2]['weight'])
	print(getReactionCenter(g1,g2))


