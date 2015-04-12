__author__ = 'feiyicheng'

from main import *

if __name__ == '__main__':
	hehe = KEGG_lib.KEGG_raw2obj(KEGG.getItemContent('ec:1.1.1.342'))
	print(str('ALL_REAC' in hehe.keys()))
