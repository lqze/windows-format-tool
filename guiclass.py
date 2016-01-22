from tkinter import *
import tkinter.messagebox
import drivetools
import sys
import os

class MainApp(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.frame = self.create_frame()   
        self.chkbox = self.create_checkbox(self.frame).toggle()
        self.btn_choose, self.btn_start, self.btn_quit, self.btn_update_list = self.create_btns(self.frame)
        self.create_static_labels(self.frame, self.btn_update_list)         
        self.drive_menu = self.select_drive_menu(self.frame)
        self.firmwarebox, self.logbox = self.create_txt_boxes(self.frame)
   
    def create_frame(self):
        root.title("Auto BlackBox")
        frame = Frame(root,width=300,height=420)
        frame.pack()
        
        return frame
        
    def create_static_labels(self, frame, bind_obj):
        l1 = Label(frame, text="Select Volume")
        l1.pack()
        l1.place(relx=0.1, rely=0.05, anchor=NW)
        l2 = Label(frame, text="")
        l2.pack(side="top")
        l2.place(relx=0.48, rely=0.05, anchor=NW)
        bind_obj.bind("<Enter>", lambda e: l2.configure(text="Refresh drive list"))
        bind_obj.bind("<Leave>", lambda e: l2.configure(text=""))
        
    def create_checkbox(self, frame):
        CheckVar1 = IntVar()
        C1 = Checkbutton(frame, text = "Quick Format?", variable = CheckVar1, \
                         onvalue = 1, offvalue = 0, height=1, \
                         )
        C1.pack()
        C1.place(relx=0.1, rely=0.34, anchor=NW)
        return C1
  
    def start_format(self, drive, firmware_folder):
        drivetools.format_disk(drive)
        with open('log.txt', 'r') as fin:
            for line in fin:
                line = line.strip()
                self.logbox.insert(INSERT, line + '\n')
        try:
            self.logbox.insert(INSERT, "Copying folder...\n")
            drivetools.copytree(firmware_folder, drive + '\\')
            self.logbox.insert(INSERT, 'Successfuly copied {} to location {}\\'.format(firmware_folder, drive))
        except Exception as e:
            self.logbox.insert(INSERT, "Error copying file. Reason:\n" + str(e))


    def btn_start_callback(self):
        self.drive_menu = self.select_drive_menu(self.frame)  
        self.btn_start.config(state=DISABLED)
        firmware_str = ''.join(self.firmwarebox.get("1.0", END).replace(' ', '').split())
        if not firmware_str:
            tkinter.messagebox.showerror("No Folder Selected" , "Select a firmware location first.")
        else:
            currentDrive = self.drive_menu.get()[0:2]
            b = tkinter.messagebox.askyesno("Format Disk?" , "Are you sure you wish to format volume {:}\\ ?\nAll data will be erased. This action is irreversible.".format(currentDrive))
            if b:
                self.logbox.delete(1.0, END)
                self.start_format(currentDrive, firmware_str)
        self.btn_start.config(state=NORMAL)
        
        
    def btn_choose_callback(self):
        self.firmwarebox.delete(1.0, END)
        folder = drivetools.choose_firmware_folder()
        self.firmwarebox.insert(INSERT, folder)
        
    def btn_quit_callback(self):
        sys.exit(0)
        
    def btn_update_list_callback(self):
        self.drive_menu = self.select_drive_menu(self.frame) 
    
    def create_btns(self, frame):
        btn_start = Button(frame, text ="START",width=15,command = self.btn_start_callback) 
        btn_quit = Button(frame, text ="QUIT",width=15,command = self.btn_quit_callback)
        btn_choose = Button(frame, text ="Select Firmware",width=32,command = self.btn_choose_callback)
        self.sicon_img = PhotoImage(file="sicon.png")
        btn_update_list = Button(frame, text='',width=18,command = self.btn_update_list_callback, image=self.sicon_img)
        btn_start.pack()
        btn_start.place(relx=0.1, rely=0.42, anchor=NW)
        btn_quit.pack()
        btn_quit.place(relx=0.5, rely=0.42, anchor=NW)
        btn_choose.pack()
        btn_choose.place(relx=0.1, rely=0.21, anchor=NW)
        btn_update_list.pack()
        btn_update_list.place(relx=0.8, rely=0.04, anchor=NW)

        return btn_choose, btn_start, btn_quit, btn_update_list
    
    def create_txt_boxes(self, frame):
        logbox = Text(frame,width=39,height=14, font='-size 8 -family Times')
        logbox.pack()
        logbox.place(relx=0.1, rely=0.50, anchor=NW)
        firmwarebox = Text(frame,width=29,height=1)
        firmwarebox.pack()
        firmwarebox.place(relx=0.1, rely=0.28, anchor=NW)
        
        return firmwarebox, logbox
    
    def select_drive_menu(self, frame):
        var1 = StringVar()
        drivestrs = drivetools.get_drives()
        var1.set(drivestrs[-1])
        option1 = OptionMenu(frame, var1, *drivestrs)
        option1.pack()
        option1.configure(width=32)
        option1.place(relx=0.1, rely=0.11, anchor=NW)
          
        return var1
 
if __name__ == "__main__":
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    MainApp(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
