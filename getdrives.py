import string
from ctypes import windll
import win32api, win32file

def get_drives():
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
    
    import wmi
    
    drives = []

    c = wmi.WMI ()
    for d in c.Win32_LogicalDisk():
        if d.Caption != "C:" and d.Caption != "D:":
            if d.FreeSpace:
                drivestr = '(' + d.Caption + "/" + ') ' + d.VolumeName
                drives.append(drivestr)
                '''print( d.Caption, type(d.Size), d.DriveType, d.VolumeName, d.FileSystem)'''
                infostr = str(int(d.Size) // (1024*1024*1024)) + 'GB   (' + d.FileSystem + ')'
                print(infostr)
                activeDrive = "F:\\"
    
    print(drives)
    return activeDrive
	
def format_drive(activeDrive):

    '''uint32 Format(
  [in] string FileSystem = "NTFS",
  [in] boolean QuickFormat,
  [in] uint32 ClusterSize = 4096,
  [in] string Label = "",
  [in] boolean EnableCompression = false
    '''

    print("formatting??")
    activeDrive.Win32_Volume.Format("FAT32",True,4096,"TEST")
        
def main():
    activdrive = get_drives()
    format_drive(activdrive)
        
if __name__ == '__main__':
    main() 
