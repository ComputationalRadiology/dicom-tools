#!/usr/bin/env python3

import os
import pydicom # pydicom is using the gdcm package for decompression
import sys
import subprocess
import logging
import argparse
import pathlib

parser = argparse.ArgumentParser(description='Convert DICOM files.')
parser.add_argument("inputDir")
parser.add_argument("outputDir")
args = parser.parse_args()

src = args.inputDir
dst = args.outputDir

logging.basicConfig(
  level=logging.DEBUG,
  format="%(asctime)s %(levelname)s %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S",
  )

logging.debug('Reading list of directories to convert from ' + src)

commonp = os.path.commonpath( [ src , dst ] )
posixpath = pathlib.PurePosixPath(commonp)
anothercommonpath = pathlib.PurePosixPath( src ).relative_to( posixpath )

filelist = []
for root, dirs, files in os.walk(src):
    if len(files) != 0:
      if len(dirs) == 0: 
        dirfullname = root
        dirpath = pathlib.PurePosixPath( root ).relative_to( src )
        outdirname = os.path.join(dst, dirpath)
        if not os.path.isdir( outdirname ):
          os.makedirs( outdirname )
        logging.debug('Converting : ' + dirfullname)
        logging.debug('Writing to : ' + outdirname)
        subprocess.run(['dcm2niix', '-o', outdirname, 
                         '-b', 'y', '-ba', 'n', dirfullname])

exit(0)
