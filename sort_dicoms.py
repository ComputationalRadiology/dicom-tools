#!/usr/bin/env python3

# Alex Weston
# Digital Innovation Lab, Mayo Clinic

import os
import pydicom # pydicom is using the gdcm package for decompression
import sys

def clean_text(string):
    # clean and standardize text descriptions, which makes searching files easier
    forbidden_symbols = ["*", ".", ",", "\"", "\\", "/", "|", "[", "]", ":", ";", " "]
    for symbol in forbidden_symbols:
        string = string.replace(symbol, "_") # replace everything with an underscore
    return string.lower()  

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
unsortedList = []
for root, dirs, files in os.walk(src):
    for file in files: 
#        if ".dcm" in file:# exclude non-dicoms, good for messy folders
            unsortedList.append(os.path.join(root, file))

print('%s files found.' % len(unsortedList))
       
for dicom_loc in unsortedList:
    # read the file
    ds = pydicom.read_file(dicom_loc, force=True)
   
    # get patient, study, and series information
    patientID = clean_text(ds.get("PatientID", "NA"))
    studyDate = clean_text(ds.get("StudyDate", "NA"))
    studyDescription = clean_text(ds.get("StudyDescription", "NA"))
    seriesDescription = clean_text(ds.get("SeriesDescription", "NA"))
   
    # generate new, standardized file name
    modality = ds.get("Modality","NA")
    studyInstanceUID = ds.get("StudyInstanceUID","NA")
    seriesInstanceUID = ds.get("SeriesInstanceUID","NA")
    instanceNumber = str(ds.get("InstanceNumber","0"))
    fileName = modality + "." + seriesInstanceUID + "." + instanceNumber + ".dcm"
       
#    # uncompress files (using the gdcm package)
#    try:
#        ds.decompress()
#    except:
#        print('an instance in file %s - %s - %s - %s" could not be decompressed. exiting.' % (patientID, studyDate, studyDescription, seriesDescription ))
   
    # save files to a 4-tier nested folder structure
    if not os.path.exists(os.path.join(dst, patientID)):
        os.makedirs(os.path.join(dst, patientID))
   
    if not os.path.exists(os.path.join(dst, patientID, studyDate)):
        os.makedirs(os.path.join(dst, patientID, studyDate))
       
    if not os.path.exists(os.path.join(dst, patientID, studyDate, studyDescription)):
        os.makedirs(os.path.join(dst, patientID, studyDate, studyDescription))
       
    if not os.path.exists(os.path.join(dst, patientID, studyDate, studyDescription, seriesDescription)):
        os.makedirs(os.path.join(dst, patientID, studyDate, studyDescription, seriesDescription))
        print('Saving out file: %s - %s - %s - %s.' % (patientID, studyDate, studyDescription, seriesDescription ))
       
    ds.save_as(os.path.join(dst, patientID, studyDate, studyDescription, seriesDescription, fileName))

print('done.')
