import numpy as np
import scipy as sp
import networkx
from networkx.algorithms import isomorphism
from matplotlib import pyplot
from collections import Counter
from StringIO import StringIO


def input_chem_content(content, input_flag):
	filechem = StringIO( content )
	count_row = 0
	count_find = 0
	bond_flag = 0
	i_temp = 0
	alpha_flag = 0
	atom_num = 0
	G = networkx.Graph( );
	while True:
		list = filechem.readline( );
		count_row = count_row + 1
		buf = list.split( )
		if count_row==4:
			atom_num = int( buf[0] )
			break
	for i in range( 1, atom_num + 1 ):
		G.add_node( i )
	Chem_Matrix = np.identity( atom_num )
	for i in filechem.readlines( ):
		alpha_flag = 0
		for j in i.split( ):
			if j.isalpha( )==True:
				alpha_flag = 1
		count_find = count_find + 1
		if i.split( )[0]=='M':
			break
		# print(i)
		if alpha_flag==0:
			bond_flag = 1
			i_temp = count_find
		if bond_flag==1:
			# print(count_find)
			# print(i_temp)
			if count_find==i_temp:
				Chem_Matrix[int( i.split( )[0] ) - 1, int( i.split( )[1] ) - 1] = int( i.split( )[2] )
				Chem_Matrix[int( i.split( )[1] ) - 1, int( i.split( )[0] ) - 1] = int( i.split( )[2] )
				G.add_weighted_edges_from( [(int( i.split( )[0] ), int( i.split( )[1] ), int( i.split( )[2] ))] )
				G.add_weighted_edges_from( [(int( i.split( )[1] ), int( i.split( )[0] ), int( i.split( )[2] ))] )
				i_temp = i_temp + 1
	if input_flag=='g1':
		g1 = G
		# print(G.get_edge_data( 1, 2 ))
		return g1
	if input_flag=='g2':
		g2 = G
		# print(G.get_edge_data( 1, 2 ))
		return g2


def input_chem(filestring, input_flag):
	filechem = open( filestring, 'r' )
	count_row = 0
	count_find = 0
	bond_flag = 0
	i_temp = 0
	alpha_flag = 0
	atom_num = 0
	G = networkx.Graph( );
	while True:
		list = filechem.readline( );
		count_row = count_row + 1
		buf = list.split( )
		if count_row==4:
			atom_num = int( buf[0] )
			break
	for i in range( 1, atom_num + 1 ):
		G.add_node( i )
	Chem_Matrix = np.identity( atom_num )
	for i in filechem.readlines( ):
		alpha_flag = 0
		for j in i.split( ):
			if j.isalpha( )==True:
				alpha_flag = 1
		count_find = count_find + 1
		if i.split( )[0]=='M':
			break
		print(i)
		if alpha_flag==0:
			bond_flag = 1
			i_temp = count_find
		if bond_flag==1:
			print(count_find)
			print(i_temp)
			if count_find==i_temp:
				Chem_Matrix[int( i.split( )[0] ) - 1, int( i.split( )[1] ) - 1] = int( i.split( )[2] )
				Chem_Matrix[int( i.split( )[1] ) - 1, int( i.split( )[0] ) - 1] = int( i.split( )[2] )
				G.add_weighted_edges_from( [(int( i.split( )[0] ), int( i.split( )[1] ), int( i.split( )[2] ))] )
				G.add_weighted_edges_from( [(int( i.split( )[1] ), int( i.split( )[0] ), int( i.split( )[2] ))] )
				i_temp = i_temp + 1
	if input_flag=='g1':
		g1 = G
		print(G.get_edge_data( 1, 2 ))
		return g1
	if input_flag=='g2':
		g2 = G
		print(G.get_edge_data( 1, 2 ))
		return g2


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
	gm = isomorphism.GraphMatcher( g1, g2, edge_match=lambda e1, e2: e1['weight']==e2['weight'] )


	# if g2 is not MCS return error
	if not gm.subgraph_is_isomorphic( ):
		raise NotIsomorphismException( "g2 should be a subgraph of g1" )


	# Oops! the gm.mapping dict will generate only if the above method has executed


	# get the reaction center
	answers = []
	for mapping in gm.subgraph_isomorphisms_iter( ):
		map2to1 = {v: k for (k, v) in mapping.items( )}

		for (key1, key2) in mapping.iteritems( ):
			neighbor1 = g1.neighbors( key1 )
			neighbor2 = g2.neighbors( key2 )
			neighbor2to1 = map( lambda key: map2to1[key], neighbor2 )
			if not Counter( neighbor1 )==Counter( neighbor2to1 ):
				answers.append( (key1, key2) )
				break

	return answers


if __name__=='__main__':
	# construct Graph 1
	g1 = input_chem( '1.sdf', 'g1' )
	# construct Graph 2

	g2 = input_chem( 'out.sdf', 'g2' )

	# Match the two graph
	gm = isomorphism.GraphMatcher( g1, g2 )
	networkx.draw_networkx( g1 )
	pyplot.show( )
	networkx.draw_networkx( g2 )
	pyplot.show( )

	# get iterator of all possible subgraphs
	# subgs =  gm.subgraph_isomorphisms_iter()
	#networkx.draw_networkx(g1)
	# pyplot.show()
	print(getReactionCenter( g1, g2 ))
