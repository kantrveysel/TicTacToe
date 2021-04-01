from tkinter import Tk, Canvas
from time import sleep
from Agent import Ajan
from Table import Grid,ox
import numpy as np
import pickle
from random import shuffle

### SETUP
root = Tk()
canva = Canvas(root, width = 640, height = 640, bg="white")
canva.pack()
game = Grid()
pop = 81
ajansx = [Ajan(1) for _ in range(pop)]
ajanso = [Ajan(2) for _ in range(pop)]

theAjan = Ajan(1)
dotrain = False
if not dotrain:
	best = pickle.load(open("best.x","rb"))
	theAjan.params = best["params"]
	theAjan.bias = best["bias"]
	if theAjan.tip == 1:
		game.addToGrid(theAjan.answer(game.grid))

### GRID
#game.addToGrid("100000000")
ajx,ajo,turn  = 0,0,1
selected = []
all = []

def loop():
	if dotrain:
		global ajx,ajo,turn,selected,ajansx,ajanso,minscore,pop,all
		end = game.checkEnd()
		#print(ajx,ajo)
		if end:
			game.updateCanva(canva)
			if end == 1:
				ajansx[ajx].score +=1
				ajanso[ajo].score -=1
				turn = 1
			elif end == 2:
				ajanso[ajo].score +=1
				ajansx[ajx].score -=1
				turn = 1
		try:
			if turn == 1:
				if game.addToGrid(ajansx[ajx].answer(game.grid)) != 0:
					turn = 2
					ajansx[ajx].score += 1
				else:
					game.replay()
					#ajanso[ajo].score -= 1
					ajx +=1
					ajo +=1
					turn=1
			else:
				if game.addToGrid(ajanso[ajo].answer(game.grid)) != 0:
					turn = 1
					ajanso[ajo].score += 1
				else:
					game.replay()
					#ajansx[ajx].score -= 1
					ajx +=1
					ajo +=1
					turn =1
		except:
			ajx = 0
			ajo = 0
			all=[]
			_=[all.append(i) for i in ajansx if i.score >1]
			_=[all.append(i) for i in ajanso if i.score >1]
			all.sort(key = lambda i:i.score, reverse=True)
			ajansx.sort(key = lambda i:i.score, reverse=True)
			ajanso.sort(key = lambda i:i.score, reverse=True)
			selected = [ajansx[0],ajanso[0]]
			
			#print(np.array([i.score for i in all]).mean(),all[0].score)
			u = 0
			while len(selected) < pop:
				try:
					selected.append(ajansx[u].new(.3))
					selected.append(ajanso[u].new(.3))
					u+=1
				except:
					u=0
			ajansx = []
			ajanso = []
			
			### DISTRIBUTE SELECTED AGENT
			shuffle(selected)
			for i in selected[:pop]:
				i.tip = 1
				i.score=0
				ajansx.append(i)

			for i in selected[pop:]:
				i.tip = 2
				i.score=0
				ajanso.append(i)
				
			game.replay()
	else:
		game.updateGrid()
		if game.checkEnd():
			game.replay()
			if theAjan.tip == 1:
				game.addToGrid(theAjan.answer(game.grid))
			
		game.updateCanva(canva)
	
	#game.updateCanva(canva)
	root.after(1 if dotrain else 100, loop)

def click(e):
	if not dotrain:
		code = list("000000000")
		code[int(np.floor(3*e.x/640) + 3*np.floor(3*e.y/640))] = "2" if theAjan.tip == 1 else "1"
		code = "".join(code)
		game.addToGrid(code)
		print(game.grid)
		print(theAjan.answer(game.grid),end="\n\n")
		game.addToGrid(theAjan.answer(game.grid))
	else:
		game.updateCanva(canva)

def up():
	game.updateCanva(canva)
	root.after(150, up)
	
up()
root.bind("<Button-1>",click)
root.after(50, loop)
root.mainloop()

print("END")
pickle.dump({"params":all[0].params , "bias":all[0].bias},open("best.x","wb"))
