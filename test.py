import os, sys

def _mainfile():
    file = os.path.abspath(sys.executable if hasattr(sys, "frozen") else sys.modules['__main__'].__file__)
    #while stat.S_ISLNK(os.lstat(file).st_mode): file = os.readlink(file)
    print file
    return file
    
    
    
_mainfile()