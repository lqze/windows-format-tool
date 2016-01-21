from tkinter import *
import tkinter.messagebox

import drivetools, time

# www.m.betfair.com.au


class MainApp(Frame):

    # main body- controls the flow of the gui interface
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.frame = self.create_frame()
        self.create_static_labels(self.frame)
        self.chkbox = self.create_checkbox(self.frame).toggle()
        self.btn_choose, self.btn_start, self.btn_quit = self.create_btns(self.frame)      
        self.drive_menu = self.select_drive_menu(self.frame)       
        self.firmwarebox, self.logbox = self.create_txt_boxes(self.frame)
        
        #print(self.drive_menu.get()) # get this and change lower label with its value.
        
        
    def create_frame(self):
        root.title("Auto BlackBox disk Formatter")
        frame = Frame(root,width=300,height=400)
        frame.pack()
        return frame
        
    def create_static_labels(self, frame):
        w1 = Label(frame, text="Select Disk Volume")
        w1.pack()
        w1.place(relx=0.1, rely=0.05, anchor=NW)
        
    def create_checkbox(self, frame):
        CheckVar1 = IntVar()
        C1 = Checkbutton(frame, text = "Quick Format?", variable = CheckVar1, \
                         onvalue = 1, offvalue = 0, height=1, \
                         )
        C1.pack()
        C1.place(relx=0.1, rely=0.39, anchor=NW)
        return C1
  
    def start_format(self, drive):
            drivetools.format_disk(drive)           
            fin = open('log.txt', 'r')
            for line in fin:
                line = line.strip()
                self.logbox.insert(INSERT, line + '\n')
    
    
    def btn_start_callback(self):
        self.btn_start.config(state=DISABLED)
        st = self.firmwarebox.get("1.0", END).replace(' ', '').split()
        if not st:
            tkinter.messagebox.showerror("No Folder Selected" , "Select a firmware location first.")
        else:
            currentDrive = self.drive_menu.get()
            currentDrive = currentDrive[1:currentDrive.find(':')+1]
            b = tkinter.messagebox.askyesno("Format Disk?" , "Are you sure you wish to format volume\
            {:}?\n\tThis action is irreversible.".format(currentDrive))
            if b:
                self.logbox.delete(1.0, END)
                self.start_format(currentDrive)
        self.btn_start.config(state=NORMAL )
       
    def btn_choose_callback(self):
        # this function should now call the appropriate function to let user choose firmware folder
        folder = drivetools.choose_firmware_folder()
        self.firmwarebox.insert(INSERT, folder)
        
    def btn_quit_callback(self):
        exit() 
    
    def create_btns(self, frame):
        # create buttons
        btn_start = Button(frame, text ="START",width=15,command = self.btn_start_callback) 
        btn_quit = Button(frame, text ="QUIT",width=15,command = self.btn_quit_callback)
        btn_choose = Button(frame, text ="Select Firmware",width=32,command = self.btn_choose_callback)
        # pack buttons        
        btn_start.pack()
        btn_start.place(relx=0.1, rely=0.46, anchor=NW)
        btn_quit.pack()
        btn_quit.place(relx=0.5, rely=0.46, anchor=NW)
        btn_choose.pack()
        btn_choose.place(relx=0.1, rely=0.25, anchor=NW)

        return btn_choose, btn_start, btn_quit
    
    def create_txt_boxes(self, frame):
        logbox = Text(frame,width=39,height=12, font='-size 8 -family Times')
        logbox.pack()
        logbox.place(relx=0.1, rely=0.55, anchor=NW)
        firmwarebox = Text(frame,width=29,height=1)
        firmwarebox.pack()
        firmwarebox.place(relx=0.1, rely=0.33, anchor=NW)
        
        return firmwarebox, logbox
    
    def select_drive_menu(self, frame):
        var1 = StringVar()
        choices = drivetools.get_drives()

        #drivestrs = [choices[i][0] + choices[i][1] for i in range(len(choices))]
        #for i in range(len(choices)):
        #    print(choices[i][0] + choices[i][1])
        #print(drivestrs)
        drivestrs = choices
        var1.set(drivestrs[-1])
        option1 = OptionMenu(frame, var1, *drivestrs)
        option1.pack()
        option1.configure(width=32)
        option1.place(relx=0.1, rely=0.10, anchor=NW)
          
        return var1
 
            
if __name__ == "__main__":
    root = Tk()
    MainApp(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
