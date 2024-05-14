#!/usr/bin/env python3

import os
import pydicom # pydicom is using the gdcm package for decompression
import sys
import subprocess
import logging
import argparse
import json

from pydicom import dcmread

# MRN is a 7 digit number
# StudyDate format is YYYYMMDD
#


def clean_text(string):
  # clean and standardize text descriptions, to make searching files easier
  forbidden_symbols = ["*", ".", ",", "\"", "\\", "/", "|", "[", "]", ":", ";", " "]
  for symbol in forbidden_symbols:
    string = string.replace(symbol, "_") # replace everything with an underscore
  return string.lower()

# Initialize logging and set its level
logging.basicConfig()
log = logging.getLogger()
log.setLevel( logging.DEBUG )
log.setLevel( logging.INFO )

# Parse the arguments.
parser = argparse.ArgumentParser(description='Retrieve DICOM files.')
parser.add_argument("--outputDir", required=True)
parser.add_argument("--subjectID", required=True)
parser.add_argument("--studyDate", required=False)
parser.add_argument("--modality", required=False)
parser.add_argument("--aet", required=False, default="PACSDCM", help="The calling Application Entity Title is used to identify a DICOM application")
parser.add_argument("--aec", required=False, default="SYNAPSERESEARCH", help="The called Application Entity Title of the DICOM node that is called.")
parser.add_argument("--namednode", required=False, default="10.20.2.28", help="The DICOM peer that is called.")
parser.add_argument("--dicomport", required=False, default="104", help="The port on the DICOM peer.")
parser.add_argument("--accessionNumberFile", required=False, help="A file to report the discovered accession numbers into.")
args = parser.parse_args()

# user specified parameters
dst = args.outputDir
mrn = args.subjectID
if args.studyDate != None:
  StudyDateVar = args.studyDate
else:
  StudyDateVar = ""

if args.modality != None:
  Modality = args.modality
else:
  Modality = ""

if args.accessionNumberFile != None:
  accFile = args.accessionNumberFile
else:
  accFile = ""

logging.info('Retrieving subject with mrn : %s.' % mrn )
logging.info('Storing DICOM to directory %s.' % dst )

# print("mrn is " + mrn + "\n")
# print("dest is " + dst + "\n")

if not os.path.isdir( dst + '/STUDY_QUERY_INFO'):
  os.makedirs(dst+'/STUDY_QUERY_INFO')

# Search the DICOM node for the study info.
# AET: Application Entity Title is used to identify a DICOM application
#AET = 'RESEARCHPACS'
# AEC: The called Application Entity Title of the DICOM node that is called.
#AEC = 'PACSDCM'
# The named node is the DICOM peer that is called.
#NAMEDNODE = 'pacsstor.tch.harvard.edu'
#PORT = 104

# AE: SYNAPSERESEARCH
# Port: 104
# IP: 10.20.2.28

# 2BP research
# AEC: 2BPMRI_1
# AEC: 2BPMRI_2
# Named node: 10.27.107.244
# Port: 104

AET = args.aet
AEC = args.aec
NAMEDNODE = args.namednode
PORT = args.dicomport


# Create the output directory for the query.
retrieveOutdir = dst + '/STUDY_QUERY_INFO'
if not os.path.isdir( retrieveOutdir ):
  os.makedirs(retrieveOutdir)

# Display the command that will be run:
print(["findscu", "-od", retrieveOutdir,
    "--extract", "--show-responses", 
    "-aet", AET, "-aec", AEC, "--study", "--key", "QueryRetrieveLevel=STUDY",
    "--key", 'PatientID=' + mrn, 
    "--key", 'StudyDate=' + StudyDateVar, 
    "--key", 'Modality=' + Modality, 
    "--key", 'StudyInstanceUID', 
    "--key", 'AccessionNumber', 
    str(NAMEDNODE), str(PORT)])

# Search the PACS for studies that match and create rsp*.dcm files:
subprocess.run(["findscu", "-od", retrieveOutdir,
    "--extract", "--show-responses", 
    "-aet", AET, "-aec", AEC, "--study", "--key", "QueryRetrieveLevel=STUDY",
    "--key", 'PatientID=' + mrn, 
    "--key", 'StudyDate=' + StudyDateVar, 
    "--key", 'Modality=' + Modality, 
    "--key", 'StudyInstanceUID', 
    "--key", 'AccessionNumber', 
    str(NAMEDNODE), str(PORT)])

# Get the studies from the PACS and write to the output directory:
# Scan the directory and get an iterator of os.DirEntry objects
# corresponding to entries in it using os.scandir() method
obj = os.scandir(retrieveOutdir)

accessionNumberList = []

for entry in obj :
    if entry.is_file():
        fname = entry.name
        print('fname is : ' + fname)
        print('path of file is : ' + entry.path)
        ds = dcmread(entry.path)
        print(ds)
        AccessionNumber = ds['AccessionNumber'].value
        print('AccessionNumber is :' + str(AccessionNumber))
        print('StudyDate searching for :' + str(StudyDateVar))
        print('StudyDate is :' + str(ds['StudyDate'].value))
        if StudyDateVar != "":
          if StudyDateVar != ds['StudyDate'].value:
            continue
        print('Modality search for : ' + str(Modality))
        print('Modality is :' + str(ds['Modality'].value))
        if Modality != "":
          if Modality != ds['Modality'].value:
            continue
        outdir = dst + '/' + str(AccessionNumber)
        accessionNumberList.append( AccessionNumber )
        print(' Retrieving for AccessionNumber :' + str(AccessionNumber) )
        print(' Retrieving for AccessionNumber :' + str(AccessionNumber) +
            '\nStudyDate is :' + str(ds['StudyDate'].value) +
            '\nModality is : ' + ds['Modality'].value + '\n' )
        print('DICOM data retrieved to : ' + outdir)
        if not os.path.isdir( outdir ):
          os.mkdir(outdir)
        subprocess.run(["getscu", 
          "--output-directory", outdir, 
          "--verbose",
          "-aet", AET, 
          "-aec", AEC, 
          "--study", 
          str(NAMEDNODE), str(PORT), entry.path ])

print('Retrieved accession numbers:')
print(accessionNumberList)

if accFile != "":
  with open(accFile, "w") as outfile:
    outfile.write( json.dumps(accessionNumberList, indent=4) )


exit()

