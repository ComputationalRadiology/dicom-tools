#!/usr/bin/env python3

import os
import pydicom # pydicom is using the gdcm package for decompression
import sys
import logging
import subprocess
import pathlib


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
#  level=logging.INFO,
  level=logging.DEBUG,
  format="%(asctime)s %(levelname)s %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S",
  )

logging.debug("src is " + src + "\n")
logging.debug("dest is " + dst + "\n")

logging.debug('reading file list...')
filelist = []
for root, dirs, files in os.walk(src):
    for file in files: 
            filelist.append(os.path.join(root, file))

logging.info('%s files found.' % len(filelist))
if len(filelist) == 0:
  logging.debug('No files to process were found.')
  exit(1)

commonp = os.path.commonpath( [ root, dst ] )

totalfiles = len(filelist)
onetenth = totalfiles / 10
count = 0
for dicom_loc in filelist:
  relname = pathlib.PurePath(dicom_loc).relative_to( commonp )
  outname = pathlib.PurePath(dst).joinpath( relname )
  outdirname = os.path.dirname( outname )
  if not os.path.isdir( outdirname ):
    os.makedirs( outdirname )
  subprocess.run(['dcmdjpeg', dicom_loc, outname])
  count = count + 1
  if (count % onetenth == 0):
    logging.info('Processed set of ' + str(count) + ' files.')

logging.debug('uncompress_dicoms.py completed.')
