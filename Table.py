class ox:
	def __init__(self, i, j, type):
		self.type=type
		self.x=(2*i+1)*640/3/2
		self.y=(2*j+1)*640/3/2

	def draw(self, can):
		if self.type == 1:
			can.create_line(self.x-90,self.y-90,self.x+90,self.y+90,width=8)
			can.create_line(self.x+90,self.y-90,self.x-90,self.y+90,width=8)
		else:
			can.create_oval(self.x-90,self.y-90,self.x+90,self.y+90,width=8)

class Grid:
	def __init__(self, grid = "000000000"):
		self.grid = grid;
		self.objs = []
		self.done = False

	def replay(self):
		self.grid = "000000000"
		self.objs = []
		self.done = False

	def addToGrid(self, code):
		if self.done or len(code) != 9:
			return 0
		for i in range(len(code)):
			if self.grid[i] == "0" and code[i] != "0":
				self.grid = list(self.grid)
				self.grid[i] = code[i]
				self.grid = "".join(self.grid)
				self.updateGrid()
				return 1

		return 0

	def updateGrid(self):
		if self.done:
			return 0
		for i in range(3):
			for j in range(3):
				if self.grid[i+3*j] != "0":
					self.objs.append(ox(i,j,int(self.grid[i+3*j])))

	def checkEnd(self):
		if self.done:
			return 0
		for i in range(3):
			if self.grid[3*i:3*i+3].count("1") == 3:
				#print("Wins X")
				self.done = True
				return 1

			elif self.grid[3*i:3*i+3].count("2") == 3:
				#print("Wins O")
				self.done = True
				return 2

		for i in range(3):
			if self.grid[i::3].count("1") == 3:
				#print("Wins X")
				self.done = True
				return 1

			elif self.grid[i::3].count("2") == 3:
				#print("Wins O")
				self.done = True
				return 2

		if (self.grid[0]+self.grid[4]+self.grid[-1]).count("1") == 3 or (self.grid[2]+self.grid[4]+self.grid[-3]).count("1") == 3:
			#print("Wins X")
			self.done = True
			return 1

		elif (self.grid[0]+self.grid[4]+self.grid[-1]).count("2") == 3 or (self.grid[2]+self.grid[4]+self.grid[-3]).count("2") == 3:
			#print("Wins O")
			self.done = True
			return 2

		return 0

	def updateCanva(self,canva):
		canva.delete("all")
		_=[i.draw(canva) for i in self.objs]

		canva.create_line(640/3,0,640/3,640		,width=5)
		canva.create_line(2*640/3,0,2*640/3,640	,width=5)
		canva.create_line(0,640/3,640,640/3		,width=5)
		canva.create_line(0,2*640/3,640,2*640/3	,width=5)
	