import numpy as np
from random import random

sigmoid = lambda x: 1 / (1 + np.exp(-x))

class Ajan:
	def __init__(self, tip):
		self.params = np.random.random((10,9))*2 - 1
		self.bias = np.random.random(9)*2-1
		self.tip = tip
		self.score = 0
	
	def answer(self, grid):
		grid = np.array(list(map(int,list(grid))))/2
		if self.tip == 2:
			grid = np.where(grid==0.5,2,grid)/2
		input = np.append(grid, self.tip)
		ans = sigmoid( np.dot( input.T, self.params) + self.bias ).reshape(3,3) - grid.reshape(3,3)*10
		print(np.amax(ans))
		print(ans)
		ans = np.where(ans<0.5,0,ans)
		#ans = np.argmax(ans,axis=0)
		i = np.where(ans == np.amax(ans))[1][0]
		j = np.where(ans == np.amax(ans))[0][0]
		#grid = "".join(map(lambda x:str(int(x)),list(grid.flatten())))
		#i = np.round(np.polyval(self.params[:5], base(grid,3))-np.polyval(self.params[:5], 0) + np.sin(self.params[10])+ np.cos(self.params[11]))
		#j = np.round(np.polyval(self.params[-5:], base(grid,3))-np.polyval(self.params[:-5], 0)+ np.sin(self.params[-10])+ np.cos(self.params[-11]))

		
		ret = np.zeros((3,3))
		#print(self.tip,"\t",i,j)
		try:
			ret[int(np.abs(j)),int(np.abs(i))] = self.tip
			#print("".join(map(lambda x:str(int(x)),list(ret.flatten()))))
			return "".join(map(lambda x:str(int(x)),list(ret.flatten())))
		except:
			return "000000000"
			
	def plot(self,pyp):
		pyp.plot(np.arange(19682),[self.answer(baseN(i,3)) for i in np.arange(19682)])
		
	def new(self,mrate):
		ajan = Ajan(self.tip)
		ajan.params = self.params + (0.5 - np.random.random((10,9)))*mrate
		ajan.bias = self.bias + (0.5 - np.random.random(9))*mrate
		return ajan