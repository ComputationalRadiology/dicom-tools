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

print("src is " + src + "\n")
print("dest is " + dst + "\n")

print('reading file list...')
filelist = []
for root, dirs, files in os.walk(src):
    for file in files: 
            filelist.append(os.path.join(root, file))

print('%s files found.' % len(filelist))
       
totalfiles = len(filelist)
onetenth = totalfiles / 10
count = 0
for dicom_loc in filelist:
  outname = os.path.join(dst, dicom_loc)
  print('inname: ' + dicom_loc + ', outfile : ' + outname)
  outdirname = os.path.dirname( outname )
  if not os.path.isdir( outdirname ):
    os.makedirs( outdirname )
  os.system('dcmdjpeg ' + dicom_loc + ' ' + outname)
  count = count + 1
  if (count % onetenth == 0):
    print('Processed ' + count + ' files.')

print('done.')
