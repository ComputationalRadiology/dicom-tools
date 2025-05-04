FROM ubuntu:jammy
ENV DEBIAN_FRONTEND="noninteractive"

# A word about HTTP_PROXY
#
#   The Docker build networking and proxy will match the build host if you use:
# --network=host
#
# On systems that need to access a proxy to download packages, the build
# environment needs to know about the proxy to use.
#   apt-get and pip3 use different conventions for accessing a proxy.
# 
#  A symptom that this is needed is that apt-get cannot access packages.
#  A symptom that this is needed is that pip3 cannot access packages.
# This is not needed if building on a system that does not  use a proxy.
#   apt can be configured to read from archives via https.
#

LABEL maintainer="warfield@crl.med.harvard.edu"
LABEL vendor="Computational Radiology Laboratory"

# Update the ubuntu.
RUN apt-get -y update && \
    apt-get -y upgrade


RUN apt-get install -y build-essential git cmake pkg-config vim

RUN apt-get install -y --no-install-recommends \
    dcmtk \
    dicom3tools \
    jq \
    vim nano python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install pydicom pynetdicom SimpleITK numpy

RUN mkdir /src && cd /src && \
    git clone https://github.com/rordenlab/dcm2niix.git && \
    cd dcm2niix && mkdir build && cd build && cmake .. && make && make install

# Install the latest GDCM
RUN cd /src && \
    git clone --branch release https://git.code.sf.net/p/gdcm/gdcm && \
    mkdir build-gdcm && cd build-gdcm && \
    cmake -DGDCM_BUILD_APPLICATIONS=1 -DCMAKE_INSTALL_PREFIX=/opt/gdcm ../gdcm && make && make install


COPY sort_dicoms.py /usr/local/bin
COPY uncompress_dicoms.py /usr/local/bin
COPY dicom_tree_to_nifti.py /usr/local/bin
COPY retrieve_dicoms.py /usr/local/bin
RUN chmod a+rx /usr/local/bin/sort_dicoms.py /usr/local/bin/uncompress_dicoms.py /usr/local/bin/dicom_tree_to_nifti.py /usr/local/bin/retrieve_dicoms.py

COPY json_dicom_info.py /usr/local/bin
RUN chmod a+rx /usr/local/bin/json_dicom_info.py

ENV PATH=${PATH}:/usr/local/bin:/opt/gdcm/bin

WORKDIR /data
CMD ["echo", "Run binaries such as dcm2niix, dcmdjpeg, sort_dicoms.py"]


# DOCKER_BUILDKIT=1 docker build --network=host --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') -t crl/dicom-tools:latest --build-arg VERSION=$BUILD_DATE -f Dockerfile .
# 
#
# docker run -it --rm --entrypoint bash crl/dicom-tools
# docker run --rm crl/dicom-tools dcm2niix -v
# docker run -v datainputdir:/data/input -v dataoutputdir:/data/output \
#   --rm crl/dicom-tools sort_dicoms.py /data/input /data/output/sorted

# docker run -v datainputdir:/data/input -v dataoutputdir:/data/output \
#   --rm crl/dicom-tools sort_dicoms.py /data/input /data/output/sorted
# docker run -v datainputdir:/data/input -v dataoutputdir:/data/output --rm \
# crl/dicom-tools uncompress_dicoms.py /data/input /data/output/uncompressed
# docker run -v datainputdir:/data/input -v dataoutputdir:/data/output --rm \
# crl/dicom-tools dicom_tree_to_nifti.py /data/input /data/output/converted

