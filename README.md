# dicom-tools
Collection of tools for reading, processing and converting DICOM images.

Step 1: Sort the DICOM files
python3 sort_dicoms.py  dicomInputDirectory/ sorted/

Step 2: Remove encoding
python3 uncompress_dicoms.py sorted/ uncompressed/

Step 3: Convert each of the DICOM series to NIFTI
python3 dicom_tree_to_nifti.py uncompressed/ converted/

