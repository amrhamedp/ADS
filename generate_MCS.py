__author__ = 'feiyicheng'

from fmcs import fmcsWithPath
from test_chem_code import input_chem_content
from isomorphism import getReactionCenter
from matplotlib import  pyplot
import networkx as nx
from StringIO import StringIO
from readSDF import *

def reactionCenter(filename):
	# in this method, g2 do not need to be subgraph of g1
	mcs = fmcsWithPath(filename=filename)
	# print(mcs['content1'])
	# print(mcs['content2'])
	# print(mcs['contentmcs'])

	# g1 = input_chem_content(mcs['content1'], 'g1')
	g1 = graphFromSDF(StringIO(mcs['content1']))[0]
	print g1.node
	# nx.draw_networkx(g1)
	# pyplot.show( )

	# g2 = input_chem_content( mcs['content2'], 'g2' )
	g2 = graphFromSDF( StringIO( mcs['content2'] ) )[0]
	print g2.node
	# nx.draw_networkx( g2)
	# pyplot.show( )

	# gmcs = input_chem_content(mcs['contentmcs'], 'g2')
	gmcs = graphFromSDF( StringIO( mcs['contentmcs'] ) )[0]
	nx.draw_networkx(gmcs)
	pyplot.show()

	print getReactionCenter(g1, gmcs)


if __name__ =='__main__':
	reactionCenter('/Users/feiyicheng/Desktop/ADS/Develop/test2.sdf')