import os, shutil, wmi, win32gui
from win32com.shell import shell, shellcon

def main():
    get_drives()

def copytree(src, dst, symlinks=False, ignore=None):
    #copytree recursively copies source directory src to
    #destination directory dst
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
'''
    get_drives builds and returns a list of internal / external volumes
    returns: drive letter, label, capacity, filesystem (e.g F: AUDIO 10GB NTFS)

    TODO: revise d.DriveType check conditional.
        consider Win32_LogicalDisk.MediaType
'''
def get_drives():
    #get_drives builds and returns a list of internal and external volumes
    drives = []
    c = wmi.WMI()
    for d in c.Win32_LogicalDisk():
        if d.Caption != "C:": # skip ' default ' system drive
            # if DriveType = 5 then it is a compact disk
            # we also make sure the size of the drive we are selecting is not 0
            if int(str(d.DriveType)) is not 5 and d.Size:
                print("debugging: " + str(d.DriveType) + "\t" + d.Caption)
                infostr = "{0:<3} {1:15}  {2:>6} {3:>4}".format(d.Caption+'/',
                                                                d.VolumeName,
                                    str(int(d.Size) // (1024*1024*1024))+'GB',
                                                                d.FileSystem)
                drives.append(infostr)
                print(infostr)
    del(c)
    return drives

def choose_firmware_folder():
    #choose_firmware_folder opens up an interactive file explorer menu
    #enabling the user to browse and select the firmware folder
    desktop_pidl = shell.SHGetFolderLocation(0, shellcon.CSIDL_DESKTOP, 0, 0)
    pidl, display_name, image_list = shell.SHBrowseForFolder(
    win32gui.GetDesktopWindow(),
    desktop_pidl,
    "Choose a firmware folder", 0, None, None
    )
    try:
        firmware_folder = shell.SHGetPathFromIDList(pidl)
        firmware_folder = firmware_folder.decode()
    except:
        return ''

    return firmware_folder
'''
    TODO: add volume label check. do we want to assign a volume label?
    usage: fat32format.exe F: "LABEL"

'''
def format_disk(drive):
    #executes fat32format.exe, control is passed to this process
    systr = "fat32format " + drive + ' > log.txt'
    os.system(systr)

if __name__ == "__main__":
    main()
