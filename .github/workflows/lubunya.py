from tkinter import Tk, Canvas, Scale, HORIZONTAL,Button
from math import sin,cos,atan,pi
with open("naca0012.txt") as dosya:
    points = dosya.readlines()[3:]
    points = [i[1:-1].split(' ') for i in points]
    print(points)
noktalar = []
angle = pi/6
for i in points:
    if len(i) == 2:
        print(i)
        noktalar.append(list(map(float, i)))
print(noktalar)
newnoktalar = []
for i in noktalar:
    aci = atan(i[1]/(i[0]+0.000000000001))
    newnoktalar.append([i[0]/(cos(aci)+0.00000000000001)*cos(angle),i[1]/(sin(aci)+0.00000000000001)*sin(angle)])
print(newnoktalar)

def save():
    print("naca0012-IBO{}.txt".format(int(angle*180/pi)))
    with open("naca0012-IBO{}.txt".format(int(angle*180/pi)),"w") as dosya:
        dosya.writelines("Naca0012-IBO{}\n".format(int(angle*180/pi)))
        dosya.writelines("      66.       66.\n")
        dosya.writelines("\n")
        for i in newnoktalar:
            dosya.writelines("{} {}".format(i[0],i[1])+"\n")

tk = Tk()
tk.wm_minsize(640,480)
tk.wm_maxsize(640,480)
sc = Scale(tk, from_=0, to=360, orient=HORIZONTAL)
sc.set(30)
sc.pack()
save = Button(tk,text="SAVE",command=save)
save.pack()
can = Canvas(tk,width=640,height=480)
can.pack()

def loop():
    global newnoktalar,angle
    can.delete("all")
    #can.create_oval(103+5,103+5,97-5,97-5)
    newnoktalar = [[0.0,0.0] for i in range(len(noktalar))]
    angle=sc.get()*pi/180
    for i in noktalar[106:]+noktalar[40:66]:#noktalar[99:]+noktalar[33:66]:
        aci = atan((i[1]) / (i[0]-2/3 + 0.000000000001))
        #print(aci)
        L = ((i[0]-2/3)**2 + (i[1])**2)**0.5
        newnoktalar[noktalar.index(i)] = [L* cos(angle-aci)+2/3, L* sin(angle-aci)]
    newnoktalar[0:40] = noktalar[66:106]
    newnoktalar[66:106] = noktalar[0:40]
    #can.create_line(2/3*400+100,500,2/3*400+100,-500)
    for i in newnoktalar:#noktalar[106:]+noktalar[40:66]:
        can.create_oval(i[0]*400+3+100,i[1]*400+3+100,i[0]*400-3+100,i[1]*400-3+100)
    for i in range(len(newnoktalar)):
        try:
            if (((newnoktalar[i][0]-newnoktalar[i+1][0])**2 + (newnoktalar[i][1]-newnoktalar[i+1][1])**2)**0.5) > 0.2:
                continue
            can.create_line(newnoktalar[i][0]*400+100,newnoktalar[i][1]*400+100,newnoktalar[i+1][0]*400+100,newnoktalar[i+1][1]*400+100)
        except:
            pass
    tk.after(100, loop)
tk.after(100,loop)
tk.mainloop()
