__author__ = 'feiyicheng'

from Tkinter import *
from tkFileDialog import askopenfilename, askopenfile
import tkMessageBox as box
from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image
from PIL import ImageTk
import testSimilarity
import webbrowser


## global variables
mol = None
BLANK_IMG = Image.new( 'RGB', (500, 300), color='purple')

class MyFrame(Frame):
	def __init__(self):
		Frame.__init__( self )
		self.padding = "3 3 12 12"
		# self.master.title( "Example" )
		# self.grid( column=0, row=0, sticky=(N, W, E, S) )
		self.pack()
		self.columnconfigure(0,weight=1)
		self.rowconfigure(0, weight=1)
		self.canvas = Canvas( self, width=500, height=300 )
		# self.canvas.grid(row=2, column=1)
		self.canvas.pack()
		self.photo = ImageTk.PhotoImage(BLANK_IMG)
		self.image_on_canvas = self.canvas.create_image(250, 150, image=self.photo)
		self.label  = Label(self, text="choose a molfile to find similar molecules(.mol suffix supported only currently)").pack()
		self.loadFileButton = Button( self, text="Browse", command=self.load_file,width = 30).pack()#.grid(column=1,row=1,sticky=(N, ))
		self.submitButton = Button(self, text="Submit", command = self.submit, width = 40).pack()#.grid( column=1, row=3, sticky=(S, ) )

	def submit(self):
		global mol
		if mol is None:
			box.showwarning("warning",'self.mol is None!')
		else:
			sims = testSimilarity.showSimilarMols(mol)
			self._show_PubChemInfo(sims)
		return

	def load_file(self):
		global mol
		file_opt = {}
		file_opt['filetypes'] = [('all files','.*'), ('mol files', '.mol'),('sdf files','.sdf')]
		file = askopenfile(**file_opt)

		if file:
			molblock = file.read( )
			try:
				if file.name.endswith('.sdf'):
					# mol = Chem.MolFromPDBBlock(molblock)
					mol = Chem.SDMolSupplier(molblock)[0]
					# box.INFO('info',"load "+ fname.name + " successfully")
					# print(molblock)
					self._change_image(Draw.MolToImage( mol ))
				elif file.name.endswith('.mol'):
					mol = Chem.MolFromMolBlock(molblock)
					box.showinfo('info', "load " + file.name + " successfully" )
					# print(molblock)
					# Draw.MolToImage( mol ).show( )
					self._change_image(Draw.MolToImage(mol))
				else:
					print("Sorry..file type not supported yet ")
				return
				# self.canvas.itemconfig(d.image_on_canvas, image = Draw.MolToImage(mol))
			except Exception, e:
				print(e.message)

		else:
			print("file not chosen")
			return

	def _show_image(self):
		pass

	def _change_image(self, pilImg):
		self.photo = ImageTk.PhotoImage( pilImg )
		self.canvas.itemconfig( self.image_on_canvas, image= self.photo)

	def _show_PubChemInfo(self, sims):
		## get urls
		IDs = [id for (_, id, _, _, _) in sims]
		urls = ["https://pubchem.ncbi.nlm.nih.gov/compound/"+id for id in IDs]

		### construct entrys to show on GUI
		top = Toplevel()
		for i in range(len(sims)):
			label1 = Label( top, text=IDs[i]).grid(row = i+1)
			urlButton = Button(top, text="open",command=lambda: webbrowser.open(urls[i]) ).grid(row=i+1, column=1)
			ent1 = Entry( top ,width=50)
			var1 = StringVar( )
			var1.set(urls[i] )
			ent1.config( textvariable=var1 )
			ent1.grid(row = i+1,column =2)

		return


if __name__=="__main__":
	MyFrame().mainloop()
	# MmFrame.mainloop()