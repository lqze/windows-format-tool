import os, shutil
import win32gui
from win32com.shell import shell, shellcon


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

    firmware_folder = shell.SHGetPathFromIDList(pidl)
    firmware_folder = firmware_folder.decode()
    
    return firmware_folder

    
def main():
    src = choose_firmware_folder()
    os.chdir('F:\\') # choose from volume list getText() from menubox
    dst = os.getcwd()
    print("copying...") # add to the logbox
    copytree(src, dst)
    print("copied", src, "to", dst) # add to the logbox

    
if __name__ == "__main__":   
    main()
    
    
    '''drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    
    for letter in 'ABCDEFGHIJKLM':
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    
    
    #drvs=[]
    for d in drives:
        if d == 'E': continue
        drivestr = '(' + d + ':\\' + ')'  + ' ' + win32api.GetVolumeInformation(d + ':\\')[0]
        print(drivestr)
        #drvs.append(drivestr)
    #print(drvs)
    '''
