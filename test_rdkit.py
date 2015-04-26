__author__ = 'feiyicheng'

from rdkit import Chem
from rdkit.Chem import rdFMCS
from rdkit import DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols

if __name__ == '__main__':
	supp = Chem.SDMolSupplier("/Users/feiyicheng/Desktop/ADS/Develop/1.sdf")
	mols = [m for m in supp]
	# print("numMOl:" + str(len(mols)))
	# mcs = rdFMCS.FindMCS(mols)
	# print("")
	fingers = [FingerprintMols.FingerprintMol(x) for x in mols]
	print("similarity:\n" + str(DataStructs.FingerprintSimilarity(fingers[0],fingers[1])))


