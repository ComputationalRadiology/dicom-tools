#!/bin/sh

#docker run --rm -v `pwd`:/data crl/dicom-tools ls

docker run --rm -v `pwd`:/data crl/dicom-tools uncompress_dicoms.py dicomdir uncompressed
docker run --rm -v `pwd`:/data crl/dicom-tools sort_dicoms.py uncompressed sorted
docker run --rm -v `pwd`:/data crl/dicom-tools dicom_tree_to_nifti.py sorted converted

exit 0
