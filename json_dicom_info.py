#!/usr/bin/env python3

import os
import pydicom # pydicom is using the gdcm package for decompression
import sys
import logging
import argparse
import shutil
import math
import json

#
# Make a pretty display of the contents of a json file:
# jq . jsonout.json
#


def clean_text(string):
    # clean and standardize text descriptions, which makes searching files easier
    forbidden_symbols = ["*", ".", ",", "\"", "\\", "/", "|", "[", "]", ":", ";", " "]
    for symbol in forbidden_symbols:
        string = string.replace(symbol, "_") # replace everything with an underscore
    return string.lower()  

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s %(levelname)s %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S",
  )

logger = logging.getLogger()
logger.setLevel( logging.DEBUG )

parser = argparse.ArgumentParser(description='Save DICOM file information as json.')
parser.add_argument("--input")
parser.add_argument("--output_json")
args = parser.parse_args()

src = args.input
dst = args.output_json

logging.debug('reading file list...')
unsortedList = []
for root, dirs, files in os.walk(src):
    for file in files: 
#        if ".dcm" in file:# exclude non-dicoms, good for messy folders
            unsortedList.append(os.path.join(root, file))

fileCount = len(unsortedList)
logging.debug('Working on sorting %s files.' % len(unsortedList))

maxSeriesNumber = 1
for dicom_loc in unsortedList:
    base_dicom_name = os.path.basename(dicom_loc)
    # read the file
    ds = pydicom.dcmread(dicom_loc, force=True)
    seriesNumber = ds.get("SeriesNumber", "NA")
    seriesNumberStr = clean_text(str(ds.get("SeriesNumber", "NA")))
    if seriesNumberStr.isdigit() == False:
      continue
    if seriesNumber > maxSeriesNumber:
      maxSeriesNumber = seriesNumber

maxSeriesNumberDigits = int(math.log10(maxSeriesNumber))+1
logging.debug('Max series number is ' + str(maxSeriesNumber) + '.')
logging.debug('Max series number digits ' + str(maxSeriesNumberDigits))

series_dict = {}

count = 0
for dicom_loc in unsortedList:
    base_dicom_name = os.path.basename(dicom_loc)
    # read the file
    ds = pydicom.dcmread(dicom_loc, force=True)

    seriesNumber = clean_text(str(ds.get("SeriesNumber", "NA")))
    seriesNumber = seriesNumber.rjust(maxSeriesNumberDigits,'0')

    if seriesNumber in series_dict:
        continue

#    seriesDescription = clean_text(ds.get("SeriesDescription", "NA"))
#    if seriesDescription == "NA":
#      continue
#    if seriesDescription in series_dict:
#        continue

    subset_json = {}
    
    keys = [ "PatientID", "StudyDate", "StationName", "DeviceSerialNumber", "MagneticFieldStrength", "StudyDescription", "SeriesDescription", "SeriesNumber", "Modality", "AcquisitionDuration", "PulseSequenceName", "InstanceNumber", "SeriesInstanceUID", "StudyInstanceUID" ]

    for key in keys:
      value = ds.get(key, "NA")
      subset_json.update( { key : value } )

   
    count = count + 1
    series_dict[seriesNumber] = subset_json

# Get the first series key
series_key = ""
for new_k, new_v in series_dict.items():
  series_key = new_k
  break

sessions_dict = {}
sessions_dict.update( { "SessionID" : series_dict[series_key]["StudyDate"] } ) 
sessions_dict.update( { "Acquisitions" : series_dict } ) 

sessions_list = []
sessions_list.append( sessions_dict )

subject_dict = {}
subject_dict.update( { "SubjectID" : series_dict[series_key]["PatientID"] } ) 
subject_dict.update( { "Sessions" : sessions_list } ) 

print(subject_dict)

with open(dst, "w") as outfile:
    json.dump(subject_dict, outfile)

