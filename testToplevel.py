__author__ = 'feiyicheng'

from Tkinter import *
from tkFileDialog import askopenfilename, askopenfile
import tkMessageBox as box
from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image
from PIL import ImageTk



class MmFrame(Frame):
	def __init__(self):
		Frame.__init__( self )
		self.padding = "3 3 12 12"
		self.pack()
		self.columnconfigure( 0, weight=1 )
		self.rowconfigure( 0, weight=1 )
		self.button = Button(self, Text = "fdsafd", width = 30, command=self._popup()).pack()


	def _popup(self):
		toplevel  = Toplevel()
		ent1 = Entry(self,state = 'readonly')
		var1 = StringVar()
		var1.set("fasdfdsf")
		ent1.config( textvariable=var1, relief='flat' )




if __name__ == '__main__':
	MmFrame.mainloop()