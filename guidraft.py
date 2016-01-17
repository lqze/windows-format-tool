from tkinter import *

root = Tk()
root.title("Auto BlackBox disk Formatter")

frame = Frame(root,width=300,height=400)
frame.pack()

w1 = Label(frame, text="Select Disk Volume")
w1.pack()
w1.place(relx=0.1, rely=0.05, anchor=NW)

var1 = StringVar()
var1.set('DefaultDIskHere')
choices1 = ['DefaultDiskHere', 'B', 'C', 'D','E', 'F']
option1 = OptionMenu(frame, var1, *choices1)
option1.pack()
option1.configure(width=32)
option1.place(relx=0.1, rely=0.10, anchor=NW)

w12 = Label(frame, text="(H:\)\t\t\t32GB FAT")
w12.pack()
w12.place(relx=0.1, rely=0.18, anchor=NW)

w2 = Label(frame, text="Select Firmware")
w2.pack()
w2.place(relx=0.1, rely=0.25, anchor=NW)

var2 = StringVar()
var2.set('Dropdown 2')
choices2 = ['Dropdown 2', 'green', 'blue', 'yellow','white', 'magenta']
option2 = OptionMenu(frame,var2, *choices2)
option2.pack()
option2.configure(width=32)
option2.place(relx=0.1, rely=0.3, anchor=NW)


CheckVar1 = IntVar()
C1 = Checkbutton(frame, text = "Quick Format?", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0, height=1, \
                 )
C1.pack()
C1.toggle()
C1.place(relx=0.1, rely=0.38, anchor=NW)

def b1CallBack():
   print("Values");
   print(var1.get());
   print(var2.get());
   print(CheckVar1.get());
   print(text.get(1.0,END));
   
def b2CallBack():
   exit()
   
def b3CallBack():
   print("Values");
   print(var1.get());
   print(var2.get());
   print(CheckVar1.get());
   print(text.get(1.0,END));
   
B1 = Button(frame, text ="START",width=15,command = b1CallBack) 
B2 = Button(frame, text ="QUIT",width=15,command = b2CallBack)
B3 = 

B1.pack()
B1.place(relx=0.1, rely=0.45, anchor=NW)
B2.pack()
B2.place(relx=0.5, rely=0.45, anchor=NW)

text = Text(frame,width=29,height=10)
text.pack()
text.place(relx=0.1, rely=0.53, anchor=NW)
text.insert(INSERT, "Log Messages here\n...\n..\n..\n..\n..")
root.mainloop()

