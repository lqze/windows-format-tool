import os, subprocess, wmi
from win32com.shell import shell, shellcon
from win32gui import GetDesktopWindow
from shutil import copytree

'''
    copytree recursively copies the source directory src and
    all of its contents to destination directory dst
    shutil: NOTE: On Windows, file owners, ACLs and
    alternate data streams are not copied
    c.f. https://docs.python.org/3/library/shutil.html
'''
def copy_tree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)

'''
    get_drives builds and returns a list of internal / external volumes
    devices on the system using the WMI module to enable communication
    between Python and the Windows Management Instrumentation

    returns: drive letter, label, capacity, filesystem (e.g F: AUDIO 10GB NTFS)
'''
def get_drives():
    drives = []
    c = wmi.WMI().Win32_LogicalDisk()
    for d in c:
        if d.Caption != "C:":       # skip system drive
            # skip optical disks if DriveType is equal to 5
            if d.Size and d.DriveType != 5:
                infostr = "{0:<3} {1:15}  {2:>6} {3:>4}".format(d.Caption+'/',
                                                                d.VolumeName,
                                    str(int(d.Size) // (1024*1024*1024))+'GB',
                                                              d.FileSystem)
                drives.append(infostr)
    return drives

'''
    choose_firmware_folder opens up an interactive interface to the
    native win32 GUI API enabling the user to browse and select a
    folder location in the filesystem
'''
def choose_firmware_folder():
    desktop_pidl = shell.SHGetFolderLocation(0, shellcon.CSIDL_DESKTOP, 0, 0)
    pidl, display_name, image_list = shell.SHBrowseForFolder(
    GetDesktopWindow(),
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
    format_disk runs fat32format.exe as a new process and returns its
    standard output as a string.
    -c64 specifies 64 sectors per cluster with an allocation unit size (cluster size)
    at 32K
'''
def format_disk(drive):
    p = subprocess.Popen('fat32format.exe -c64 ' + drive,stdout=subprocess.PIPE,
                                                        stderr=subprocess.PIPE)
    output_fd1, output_fd2 = p.communicate()
    return output_fd1.decode()
