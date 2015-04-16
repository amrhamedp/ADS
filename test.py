__author__ = 'feiyicheng'

from test_chem_code import  input_chem
from MCS import MCSs
from isomorphism import getReactionCenter
import networkx
from matplotlib import pyplot
from fmcs import fmcs

if __name__ == '__main__':
	# g1 = input_chem("/Users/feiyicheng/Desktop/1.txt",input_flag='g1')
	# g2 = input_chem( "/Users/feiyicheng/Desktop/2.txt", input_flag='g2' )
	#
	# # networkx.draw_networkx( g1 )
	# # pyplot.show()
	# # networkx.draw_networkx( g2 )
	# # pyplot.show( )
	#
	# mcs = MCSs(g1, g2)
	# print(mcs)

	mcs = fmcs()
