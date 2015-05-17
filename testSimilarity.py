__author__ = 'feiyicheng'

import pymongo
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols
from rdkit.Chem import Draw
from os import system

conn = pymongo.Connection( )
db = conn.adsdata
DIR = "/Users/feiyicheng/Desktop/ADS/molfiles/"
from multiprocessing.dummy import Pool as ThreadPool

class highest10(list):
	def __init__(self):
		list.__init__(self)
		self.minIndex = 0
		self.min = 10

	def update(self, tp):
		if len(self) == 0:
			self.append(tp)
			self.minIndex = 0
			self.min = tp[1]
			return

		if len(self) < 10:
			if tp[1] < self.min:
				self.min = tp[1]
				self.minIndex = len(self)
			self.append( tp )
			return

		else:
			if tp[1] > self.min:
				self[self.minIndex] = tp
			tempmin = 10
			for i in xrange(10):
				if self[i][1] < tempmin:
					self.minIndex = i
					tempmin = self[i][1]
				self.min = tempmin



def mostSimilarmols(mol):
	# mol should be rdkit mol object
	results10 = highest10()

	for cpd in db.compound.find():
		# print(cpd['molfile'])
		if cpd['molfile'] == '':
			# some compounds do not have mol file(from kegg)
			continue

		moltmp = Chem.MolFromMolBlock(cpd['molfile'])
		if moltmp == None:
			continue
		fpIn = FingerprintMols.FingerprintMol(mol)
		fpTmp = FingerprintMols.FingerprintMol(moltmp)
		sml = DataStructs.FingerprintSimilarity(fpIn, fpTmp)
		results10.update(((moltmp, cpd),sml))

	return [ (tmp,cpd,sml) for ((tmp,cpd),sml) in results10]


def showSimilarMols(mol):

	# (mol obj, mongo obj, similarity(float))
	results = mostSimilarmols( mol )

	# (mol obj,
	# KEGG _id\\string,
	# name\\list,
	# formula \\
	# similarity\\float)
	sims = [(mol, scp['id'], reduce(lambda x,y: "", scp['NAME'],""),scp['FORMULA'],s) for (mol, scp, s) in results]


	sims = sorted( list( set( sims ) ), key=lambda tp: tp[4], reverse=True )
	mols = [mol for (mol,_,_,_,_) in sims]
	print("hehe")
	# atoms = mols[0].GetAtoms()
	# for atom in atoms:
	# 	print(atom)
	weights = [reduce(lambda x,y:x + y.GetMass(), mol.GetAtoms() ,0) for mol in mols]
	IDs = [id for (_,id,_,_,_) in sims]
	formulas  = [formula for (_,_,_,formula,_) in sims]

	legends = [
		"ID: " + IDs[i] + " "
	+ "formula: " + formulas[i] + "\n"
	+ "weight: " + str(weights[i])
	# +	"NAME: " + names[i] + "\n"
		for i in range(len(sims))
	]
	print(sims)
	# for mol in mols:
	# 	Draw.MolToImage(mol).show()
	img = Draw.MolsToGridImage(mols, molsPerRow=3, legends=legends,subImgSize=(400,400))
	img.show()

	return sims




if __name__ == "__main__":
	mol = Chem.MolFromMolFile("/Users/feiyicheng/Desktop/ADS/molfiles/C00010.mol")
	# fg1 = FingerprintMols.FingerprintMol(mol)
	# print(DataStructs.FingerprintSimilarity(fg1,fg1))
	results = mostSimilarmols(mol)
	sims = [(s,scp['id']) for ((_,scp),s) in results]
	print(sims)
	sims = sorted(list(set(sims)), key=lambda tp:tp[0],reverse=True)
	print(sims)
	system("open "+ "/Users/feiyicheng/Desktop/ADS/molfiles/C00259.mol")
	for sim in sims:
		# image = Draw.MolToImage()
		system("open " + DIR+str(sim[1]) + ".mol")

