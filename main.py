__author__ = 'feiyicheng'

import urllib2
import re
import pymongo
from multiprocessing.dummy import Pool as ThreadPool

TOTAL = 0
COUNT = 0


class KEGG:
	@staticmethod
	def getUrlofList(list):
		return "http://rest.kegg.jp/list/" + list

	@staticmethod
	def getUrlofItem(code):
		# print code
		return("http://rest.kegg.jp/get/" +code)

	@staticmethod
	def getList(listname):
		return urllib2.urlopen(KEGG.getUrlofList(list=listname)).read()

	@staticmethod
	def getItemContent(code):
		return urllib2.urlopen(KEGG.getUrlofItem(code)).read()


class KEGG_lib:
	@staticmethod
	def KEGG_raw2obj(content):
		lines = content.split('\n')
		obj = {}
		current_name = ""
		for line in lines:
			# the key only appears in the first 12 words
			maybe_name = line[0:11]
			data = line[12:].strip()
			if maybe_name.strip():  # if not blank
				current_name = maybe_name.strip()
			if not current_name in obj.keys():
				obj[current_name] = data
			else: # add to the existing result
				if type(obj[current_name]) != list:
					obj[current_name] = [obj[current_name]]
				obj[current_name].append(data)
		# TODO:  addtype
		return obj





def spider():
	# initialize the count
	COUNT = 0


	# connect the local mongodb
	conn = pymongo.Connection( )
	db = conn.adsdata

	logfile = open("./runtime.log", "a")

	enzyme_content = KEGG.getList('enzyme')
	enzyme_lines = enzyme_content.split('\n')

	TOTAL= len(enzyme_lines)

	enzyme_ids = map(lambda line:line[0:11].strip(), enzyme_lines)

	## multithread inserting
	pool = ThreadPool(10)
	try:
		pool.map(lambda id:insertEnzymeTreeWith(id, db), enzyme_ids )
	except Exception,e:
		print("Error: " + e.message)

	pool.close()
	pool.join()

	""" loop implementation/ single thread
	for line in enzyme_lines:
		enzyme_id = line[0:11].strip()
		print "enzyme_id:"
		print enzyme_id
		try:
			insertEnzymeTreeWith(enzyme_id, db)
		except Exception ,e:
			logfile.write(e.message + '\n')
			print("%d / %d error"%(count, total) + '\n' + e.message)
		count += 1
		print("%d / %d completed" %(count, total))
	"""

	conn.close()


def insertEnzymeTreeWith(enzyme_id, db):
	enzyme_obj = KEGG_lib.KEGG_raw2obj( KEGG.getItemContent( enzyme_id ) )
	if 'ALL_REAC' not in enzyme_obj.keys():
		return
	if type(enzyme_obj['ALL_REAC']) != list:
		enzyme_obj['ALL_REAC'] = [enzyme_obj['ALL_REAC']]
	enzyme_obj['ALL_REAC'] = map( lambda s: re.findall( "R\d{5}", s ), enzyme_obj['ALL_REAC'] )
	enzyme_obj['ALL_REAC'] = [item for l in enzyme_obj['ALL_REAC'] for item in l]
	reaction_ids = enzyme_obj['ALL_REAC']
	print "reaction_ids: "
	print reaction_ids
	reaction_ins = list( )
	for reaction_id in reaction_ids:
		reaction_obj = KEGG_lib.KEGG_raw2obj( KEGG.getItemContent( reaction_id ) )
		# reaction_objs.append(reaction_obj)
		(reactant_ids, outcome_ids) = getReactantsAndOutcomes( reaction_obj )
		reactant_objs = [KEGG_lib.KEGG_raw2obj( KEGG.getItemContent( "cpd:" + id ) ) for id in reactant_ids]
		outcome_objs = [KEGG_lib.KEGG_raw2obj( KEGG.getItemContent( "cpd:" + id ) ) for id in outcome_ids]
		reactant_ins = [db.compound.insert( reactant ) for reactant in reactant_objs]
		outcome_ins = [db.compound.insert( outcome ) for outcome in outcome_objs]
		reaction_obj['REF_REACTANT'] = reactant_ins
		reaction_obj['REF_OUTCOME'] = outcome_ins
		reaction_in = db.reaction.insert( reaction_obj )
		reaction_ins.append( reaction_in )
	enzyme_obj['REF_REACTION'] = reaction_ins
	enzyme_in = db.enzyme.insert( enzyme_obj )
	COUNT += 1
	print("%d / %d completed"%(COUNT, TOTAL))



def getReactantsAndOutcomes(reaction_obj):
	equation = reaction_obj['EQUATION']
	# print "equation: "
	# print equation
	reactants_str = equation.split('<=>')[0]
	outcomes_str= equation.split( '<=>' )[1]
	reactants = re.findall( "C\d{5}", reactants_str)
	outcomes = re.findall("C\d{5}", outcomes_str)
	return((reactants,outcomes))





if __name__ == '__main__':
	# print KEGG_Enzyme.getItemContent("ec:1.1.1.10")
	# obj_10 = KEGG_lib.KEGG_raw2obj( KEGG.getItemContent( "ec:1.1.1.10" ))
	# print obj_10['GENES']
	spider()