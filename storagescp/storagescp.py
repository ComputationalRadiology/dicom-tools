import subprocess
import argparse
import os
import uuid
from pathlib import Path
import shutil

from pynetdicom import (
     AE, debug_logger, evt, AllStoragePresentationContexts,
     ALL_TRANSFER_SYNTAXES
)

debug_logger()

def clean_text(string):
    # clean and standardize text descriptions, which makes searching files easier
    forbidden_symbols = ["*", ".", ",", "\"", "\\", "/", "|", "[", "]", ":", ";", " "]
    for symbol in forbidden_symbols:
        string = string.replace(symbol, "_") # replace everything with an underscore
    return string.lower()


def list_directories_pathlib(directory_path):
    """Lists all immediate subdirectories within a given directory using pathlib module."""
    path = Path(directory_path)
    directories = [entry.name for entry in path.iterdir() if entry.is_dir()]
    return directories

# Example usage:
# current_dir = Path.cwd()
# subdirs = list_directories_pathlib(current_dir)
# print(f"Directories in {current_dir}: {subdirs}")


# Implement a handler for evt.EVT_RELEASED
def handle_released(event, incomingDir, conversionDir, outgoingDir):
        """Handle an association release event."""
        assoc = event.assoc
        print(f"Association with {assoc.requestor.ae_title} released.")
        print(f"Directories are : {incomingDir} {conversionDir} {outgoingDir}")

        subdirs = list_directories_pathlib(incomingDir)
        print(f"Subdirectories are : {subdirs}")

        dockerprefix = ["docker", "run", "--volume", incomingDir+':/datain', 
                  "--volume", conversionDir+':/dataconv', "--rm", "-it",
            "--init", "--user", str(os.getuid())+":"+str(os.getgid()) ] 

        for subdir in subdirs:
          subdirPath = clean_text(os.path.basename(subdir))
          outDir = '/dataconv' + '/' + subdirPath
          print(f"outDir is {outDir}")
          inDirPath = os.path.basename(incomingDir) + subdir + '/'
          dockerinDir = '/datain/' + subdir + '/'

          for filename in os.listdir(os.path.join(incomingDir, subdir)):
            print(f"Found file: {filename}")
            subprocess.run( dockerprefix + ["dcm4che/dcm4che-tools", "emf2sf",
                "--out-dir", outDir, dockerinDir + filename])

        # Now that the data has been converted, move it into the outgoing dir.
        convdirs = list_directories_pathlib(conversionDir)
        print(f"Subdirectories are : {convdirs}")
        for convdir in convdirs:
          print(f"Place {convdir} in {outgoingDir}")
          shutil.copytree(os.path.join(conversionDir, convdir), outgoingDir, dirs_exist_ok=True)

        # Return a 'Success' status
        return 0x0000

# Implement a handler for evt.EVT_C_STORE
def handle_store(event, incomingDir):
    """Handle a C-STORE request event."""
    # Decode the C-STORE request's *Data Set* parameter to a pydicom Dataset
    ds = event.dataset

    # Add the File Meta Information
    ds.file_meta = event.file_meta

    print(f"SeriesInstanceUID is {ds.SeriesInstanceUID}.")
    # Select a UID for the directory

    fileName = incomingDir + '/' + str(ds.SeriesInstanceUID) + '/' + str(ds.SOPInstanceUID)
    os.makedirs(os.path.dirname(fileName), exist_ok=True)

    # Save the dataset using the SOP Instance UID as the filename
    ds.save_as(fileName, enforce_file_format=True)

    # Return a 'Success' status
    return 0x0000

parser = argparse.ArgumentParser(description='Sort DICOM files.')
parser.add_argument("incomingDir")
parser.add_argument("outgoingDir")
parser.add_argument("conversionDir")
args = parser.parse_args()

incomingDir = args.incomingDir
conversionDir = args.conversionDir
outgoingDir = args.outgoingDir

os.makedirs(incomingDir, exist_ok=True)
os.makedirs(conversionDir, exist_ok=True)
os.makedirs(outgoingDir, exist_ok=True)

handlers = [(evt.EVT_C_STORE, handle_store, [incomingDir]), (evt.EVT_RELEASED, handle_released, [incomingDir, conversionDir, outgoingDir])]

# Initialise the Application Entity
ae = AE()

# Support presentation contexts for all storage SOP Classes
# ae.supported_contexts = AllStoragePresentationContexts

storage_sop_classes = [
     cx.abstract_syntax for cx in AllStoragePresentationContexts
 ]

for uid in storage_sop_classes:
     ae.add_supported_context(uid, ALL_TRANSFER_SYNTAXES)

# Start listening for incoming association requests
ae.start_server(("127.0.0.1", 11112), evt_handlers=handlers)

