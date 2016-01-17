import os
import subprocess
from ctypes import *    
fm = windll.LoadLibrary('fmifs.dll')  

# relevant fmifs documentation http://doxygen.reactos.org/df/d85/fmifs_8h_source.html  
def main():
    test_format = "format F: /Q /V:test"
    print("running command: " + test_format)
    FMT_CB_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_void_p)
    FMIFS_HARDDISK = 0x00
    fm.FormatEx(c_wchar_p('F:\\'), FMIFS_HARDDISK, c_wchar_p('FAT32'),
    c_wchar_p('hello'), True, c_int(32678), FMT_CB_FUNC(myFmtCallback))
    

def myFmtCallback(command, modifier, arg):
    print(command)
    return 1	# TRUE

    
  #  p = subprocess.Popen([os.system(test_format)], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  #  stdout, stderr = p.communicate(input='/r')
 
    
if __name__ == '__main__':
    main()
