#!/usr/bin/env python3

import os
import pydicom # pydicom is using the gdcm package for decompression
import sys
import subprocess
import logging

# Parse arguments
n = len(sys.argv) - 1
if n != 2:
  print("Usage: " + sys.argv[0] + " inputdir outputdir\n")
  print("Length is " + repr(n))
  sys.exit(1)

# user specified parameters
src = sys.argv[1]
dst = sys.argv[2]

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s %(levelname)s %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S",
  )

logging.debug('Reading list of directories to convert from ' + src)
filelist = []
for root, dirs, files in os.walk(src):
    if len(files) != 0:
      if len(dirs) == 0: 
        dirfullname = root
        outdirname = os.path.join(dst, dirfullname)
        if not os.path.isdir( outdirname ):
          os.makedirs( outdirname )
        logging.debug('Converting : ' + dirfullname)
        subprocess.run(['dcm2niix', '-o', outdirname, 
                         '-b', 'y', '-ba', 'n', dirfullname])

exit(0)
