import os, subprocess, shutil, wmi, win32gui
from win32com.shell import shell, shellcon

def copytree(src, dst, symlinks=False, ignore=None):
    #copytree recursively copies the source directory src and
    #all of its subdirectories to destination directory dst
    #shutil: NOTE: On Windows, file owners, ACLs and 
    #alternate data streams are not copied
    #c.f. https://docs.python.org/3/library/shutil.html
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)

def get_drives():
    #get_drives builds and returns a list of internal and external storage
    #devices on the system using the WMI module to enable communication
    #between Python and the Windows Management Instrumentation
    drives = []
    c = wmi.WMI().Win32_LogicalDisk()
    for d in c:
        if d.Caption != "C:": # skip system drive
            if d.Size or d.DriveType != 5:
                infostr = "{0:<3} {1:15}  {2:>6} {3:>4}".format(d.Caption+'/', d.VolumeName,
                    str(int(d.Size) // (1024*1024*1024))+'GB', d.FileSystem)
                drives.append(infostr)
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
    #format_disk runs fat32format.exe as a new process and returns its standard output
    #as a string
    p = subprocess.Popen('fat32format.exe ' + drive,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output_fd1, output_fd2 = p.communicate()
    return output_fd1.decode()
    
