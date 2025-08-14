
#1 - Launch the Storage SCP listener daemon
nohup python3 storagescp.py &

#2 - Send a DICOM image to the listener.
docker run --network=host --rm -it -v `pwd`:/data crl/dicom-tools dcmsend  --verbose 127.0.0.1 11112 -aet COMPRES *.dcm

#3 - Check if a new and complete set of DICOM images has appeared in the input.

#4 - Convert the DICOM to single frame if it is multi-frame,
#  and write it to the file system.
docker run --rm -it --volume `pwd`:/data dcm4che/dcm4che-tools emf2sf \
 --out-file /data/singleframe-000.dcm /data/multiframe.dcm

#5 - Shift the converted data to a new directory.

