import os, shutil, wmi, win32gui
from win32com.shell import shell, shellcon
from ctypes import *

def copytree(src, dst, symalinks=False, ignore=None):
    #copytree recursively copies source directory src to
    #destination directory dst
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
            
def get_drives():
    #get_drives builds and returns a list of internal and external volumes  
    drives = []
    c = wmi.WMI()
    for d in c.Win32_LogicalDisk():
        if d.Caption != "C:": # skip system drive
            if d.Size:        # skip compact disks                
                #drivestr = '(' + d.Caption + "/" + ') ' + d.VolumeName
                #infostr = str(int(d.Size) // (1024*1024*1024)) + 'GB   (' + d.FileSystem + ')'
                infostr = "{0:3<3}  {1:} {2:4>4}   {3:4>4}".format(d.Caption+'/', d.VolumeName, str(int(d.Size) // (1024*1024*1024))+'GB', d.FileSystem)
                
                drives.append(infostr)
                #drives.append((drivestr, infostr))
    del(c)
    return drives
       
def choose_firmware_folder():
    #choose_firmware_folder opens up an interactive file explorer menu 
    #enabling the user to browse and select the firmware folder
    desktop_pidl = shell.SHGetFolderLocation(0, shellcon.CSIDL_DESKTOP, 0, 0)
    pidl, display_name, image_list = shell.SHBrowseForFolder(
    win32gui.GetDesktopWindow(),
    desktop_pidl,
    "Choose a firmware folder",
    0,
    None,
    None
    )    
    try:
        firmware_folder = shell.SHGetPathFromIDList(pidl)
        firmware_folder = firmware_folder.decode()
    except:
        return ''
    
    return firmware_folder
    
def format_disk(drive):
    #executes fat32format.exe, control is passed to this process
    systr = "fat32format " + drive + ' > log.txt'
    os.system(systr)
    
