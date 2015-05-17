__author__ = 'feiyicheng'

import pymongo

conn = pymongo.Connection( )
db = conn.adsdata
DIR = "/Users/feiyicheng/Desktop/ADS/molfiles/"
from multiprocessing.dummy import Pool as ThreadPool

def insertMol(cpd):
	id = cpd['ENTRY'].split( )[0]
	file  = open( DIR + id + '.mol', 'r' )
	content = file.read()
	cpd['molfile'] = content
	db.compound.save(cpd)

	file.close()


if __name__ == "__main__":
	print(type(db.compound.find()))
	cpds = list(db.compound.find())

	pool = ThreadPool(4)
	map(insertMol, cpds)

	pool.close()
	pool.join()
