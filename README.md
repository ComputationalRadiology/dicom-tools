# crl/dicom-tools
Collection of tools for retrieving, formatting, organizing and converting DICOM images.

Step 1: Remove encoding
python3 uncompress_dicoms.py dicomInputDirectory uncompressed/

Step 2: Sort the DICOM files
python3 sort_dicoms.py  uncompressed/ sorted/

Step 3: Convert each of the DICOM series to NIFTI
python3 dicom_tree_to_nifti.py sorted/ converted/

These can be done from the command line with these steps:

* Remove JPEG2000 DICOM compression if needed:
```
docker run --rm -v "`pwd`":/data crl/dicom-tools uncompress_dicoms.py dicomdir dicomdir-uncompressed
```

* Sort the DICOM files into one series per directory:
```
docker run --rm -v "`pwd`":/data crl/dicom-tools sort_dicoms.py dicomdir-uncompressed dicomdir-sorted
```

* Convert the entire sorted DICOM directory tree to NIFTI format:
```
docker run --rm -v "`pwd`":/data crl/dicom-tools dicom_tree_to_nifti.py dicomdir-sorted dicomdir-converted
```

# Getting the container at Boston Children's Hospital:

To pull the container from the BCH gitlab container registry:
```
docker pull ccts3.aws.chboston.org:5151/computationalradiology/dicom-tools
```

Tag the local container with a shorter name:

```
docker tag ccts3.aws.chboston.org:5151/computationalradiology/dicom-tools crl/dicom-tools
```

