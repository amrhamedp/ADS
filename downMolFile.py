__author__ = 'feiyicheng'

import urllib2
import pymongo
from multiprocessing.dummy import Pool as ThreadPool
from rdkit import Chem
from StringIO import StringIO
import os.path

DIR = "/Users/feiyicheng/Desktop/ADS/molfiles/"
conn = pymongo.Connection( )
db = conn.adsdata

COUNT = 0

def urlMolFile(id):
	return "http://www.genome.jp/dbget-bin/www_bget?-f+m+compound+" + id

def downloadTo(url, dir, filename):
	global COUNT
	COUNT += 1

	if os.path.exists(dir+filename):
		print("file "+dir+filename+" already exists")
		return True

	file = open(dir+filename, 'w')
	if not file:
		print("cannot download " + url)
		return False
	else:
		try:
			file.write(urllib2.urlopen(url).read())
		except Exception ,e:
			print("error when writing to: " + dir + filename)
			print(e.message + '\n')
			return False
	file.close()
	# print(filename +"   downloaded successfully")
	print("count: "+ str(COUNT))
	return True

def downloadMolFileTo(url):
	downloadTo(url,DIR, url.split('+')[-1] + ".mol")


def getUrlsCompound():
	results = []
	for cpd in db.compound.find():
		id = cpd['ENTRY'].split()[0]
		url = urlMolFile(id)
		results.append(url)
	return results

if __name__ == "__main__":
	urls  = getUrlsCompound()
	print(len(urls))
	print(len(set(urls)))

	# pool = ThreadPool(4)
	# results = pool.map(downloadMolFileTo, urls)
	#
	# pool.close()
	# pool.join()




