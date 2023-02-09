#!/usr/bin/env python3

import os
import pydicom # pydicom is using the gdcm package for decompression
import sys

# Parse arguments
n = len(sys.argv) - 1
if n != 2:
  print("Usage: " + sys.argv[0] + " inputdir outputdir\n")
  print("Length is " + repr(n))
  sys.exit(1)

# user specified parameters
src = sys.argv[1]
dst = sys.argv[2]

print('reading list of directories to convert from ' + src)
filelist = []
for root, dirs, files in os.walk(src):
    if len(files) != 0:
      if len(dirs) == 0: 
        dirfullname = root
        outdirname = os.path.join(dst, dirfullname)
        if not os.path.isdir( outdirname ):
          os.makedirs( outdirname )
#      os.system('dcm2niix ' + '-o ' + outdirname + ' -b y -ba n ' + dirfullname)
        print('Converting : ' + dirfullname)
        os.system('dcm2niix ' + '-o ' + outdirname + ' -b y -ba n ' + dirfullname)

exit(0)
