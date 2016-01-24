from tkinter import *
import tkinter.messagebox
from sys import exit
import drivetools

class MainApp(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.initialize_window()

    def initialize_window(self):
        #create and setup all the UI widgets
        self.frame = self.create_frame()
        self.chkbox = self.create_checkbox(self.frame).toggle()
        self.btn_choose, self.btn_start, self.btn_quit, self.btn_update_list \
                                                = self.create_btns(self.frame)
        self.create_static_labels(self.frame, self.btn_update_list)
        self.drive_menu = self.select_drive_menu(self.frame)
        self.firmwarebox, self.logbox = self.create_txt_boxes(self.frame)

    def create_frame(self, w=300, h=420):
        root.title("Auto BlackBox")
        frame = Frame(root, width=w, height=h)
        frame.pack()

        return frame

    def create_static_labels(self, frame, bind_obj):
        lbl_select_volume = Label(frame, text="Select Volume")
        lbl_select_volume.pack()
        lbl_select_volume.place(relx=0.1, rely=0.05, anchor=NW)
        l2 = Label(frame, text="")
        l2.pack(side="top")
        l2.place(relx=0.48, rely=0.05, anchor=NW)
        bind_obj.bind("<Enter>", lambda e: l2.configure(text="Refresh drive "+
                                                                      "list"))
        bind_obj.bind("<Leave>", lambda e: l2.configure(text=""))

    def create_checkbox(self, frame):
        CheckVar1 = IntVar()
        C1 = Checkbutton(frame, text = "Quick Format?", variable = CheckVar1,
                                        onvalue = 1, offvalue = 0, height=1, )
        C1.pack()
        C1.place(relx=0.1, rely=0.34, anchor=NW)
        return C1

    def format_disk(self, drive, firmware_folder):
        output = drivetools.format_disk(drive)
        for line in output:
            self.logbox.insert(INSERT, line)
        self.logbox.insert(INSERT, "\n")

    def copy_folder(self, drive, firmware_folder):
        try:
            self.logbox.insert(INSERT, "Copying folder...\n")
            drivetools.copy_tree(firmware_folder, drive + '\\')
            self.logbox.insert(INSERT, ("Successfully copied {} to " +
                                "location {}\\").format(firmware_folder, drive))
        except Exception as e:
            self.logbox.insert(INSERT, "Error copying file. Reason:\n" + str(e))
        print('\a')

    def start_operation(self):
        firmware_str = ''.join(self.firmwarebox.get("1.0", END).split('\n'))   
        copy_folder_yes = True
        continue_op = True
        if not firmware_str:
            b = tkinter.messagebox.askyesno("",
            "No Folder Selected. Continue formatting without copying a folder?")
            if b == True:
                continue_op = True
                copy_folder_yes = False
            else:
                continue_op = False     
        if continue_op == True:
            currentDrive = self.drive_menu.get()[0:2]
            is_format = tkinter.messagebox.askyesno("Format Disk?" ,
                        ("Are you sure you wish to format volume {:}\\ ? " +
                        "\nAll data will be erased. This action is " +
                        "irreversible.").format(currentDrive))
            if is_format:
                    self.logbox.delete(1.0, END)
                    self.format_disk(currentDrive, firmware_str)
                    if copy_folder_yes == True:
                        self.copy_folder(currentDrive, firmware_str)

    def btn_start_callback(self):
        self.drive_menu = self.select_drive_menu(self.frame)
        self.btn_start.config(state=DISABLED)
        self.start_operation()
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
        btn_start = Button(frame, text ="START", width=15,
                        command = self.btn_start_callback)
        btn_quit = Button(frame, text ="QUIT", width=15,
                        command = self.btn_quit_callback)
        btn_choose = Button(frame, text ="Select Firmware", width=32,
                                    command = self.btn_choose_callback)
        self.sicon_img = PhotoImage(file="sicon.png")
        btn_update_list = Button(frame, text='', width=18,
                command = self.btn_update_list_callback, image=self.sicon_img)
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
        log_box = Text(frame, width=39, height=14, font='-size 8 -family Arial')
        log_box.pack()
        log_box.place(relx=0.1, rely=0.50, anchor=NW)
        firmware_box = Text(frame, width=29, height=1)
        firmware_box.pack()
        firmware_box.place(relx=0.1, rely=0.28, anchor=NW)

        return firmware_box, log_box

    def select_drive_menu(self, frame):
        var1 = StringVar()
        drivestrs = drivetools.get_drives()
        var1.set(drivestrs[-1])
        drive_selection = OptionMenu(frame, var1, *drivestrs)
        drive_selection.pack()
        drive_selection.configure(width=32)
        drive_selection.place(relx=0.1, rely=0.11, anchor=NW)

        return var1

if __name__ == "__main__":
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    MainApp(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
