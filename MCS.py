__author__ = 'feiyicheng'

from networkx.algorithms import isomorphism
import networkx
from itertools import chain, combinations
from matplotlib import pyplot
from test_chem_code import input_chem

##First generate all subgraphs of G2 using:

def powerset(iterable):
	s = list( iterable )
	return chain.from_iterable( combinations( s, r ) for r in range( len( s ) + 1 ) )


def all_subgraphs(graph):
	a = [i+1 for i in range( len( graph.nodes( ) ) )]
	a.reverse( )
	for vertices in powerset( a ):
		yield graph.subgraph( vertices )


def MCSs(G1, G2):
	## (reversed list, to start with longest subgraphs first and then we can break, when one is found)
	subgraphs = all_subgraphs( G2 )

	# max length and MCS
	MCS = None
	max_len = 0

	for sg2 in reversed( list( subgraphs ) ):
		print(len(sg2.nodes()))
		if len( sg2.nodes( ) ) < max_len: continue
		GM = isomorphism.GraphMatcher( G1, sg2 )
		if GM.subgraph_is_isomorphic( ):
			for mapping in GM.subgraph_isomorphisms_iter( ):
				if len(mapping) > max_len:
					MCS = mapping
					max_len = len(mapping)

	return MCS


if __name__ == '__main__':
	g1 = input_chem("")




	"""
	### test the algorithm
	# construct Graph 1
	g1_nodes = [1, 2, 3, 4, 5, 6]
	g1_edges = [
		(1, 2),
		(1, 3),
		(1, 4),
		(3, 4),
		(3, 5),
		(1, 6),
		(4, 6),
	]
	g1 = networkx.Graph( )
	g1.add_nodes_from( g1_nodes )
	g1.add_edges_from( g1_edges )

	# construct Graph 2
	g2_nodes = [1, 2, 3, 4, 5]
	g2_edges = [
		(1, 2),
		(2, 4),
		(2, 3),
		(2, 5),
		(4, 5),
		(3, 5),
	]
	g2 = networkx.Graph( )
	g2.add_nodes_from( g2_nodes )
	g2.add_edges_from( g2_edges )

	# networkx.draw_networkx(g1)
	# pyplot.show()
	# networkx.draw_networkx(g2)
	# pyplot.show()

	mcs = MCSs(g1,g2)
	print(mcs)
	# networkx.draw_networkx( mcs)
	# pyplot.show()
	"""