FROM ubuntu:jammy
ENV DEBIAN_FRONTEND="noninteractive"

# A word about HTTP_PROXY
# On systems that need to access a proxy to download packages, the build
# should be called with a build-arg that passes in the proxy to use.
#  A symptom that this is needed is that apt-get cannot access packages.
#  Another symptom is that pip cannot access packages.
# This is not needed if building on a system that does not  use a proxy.
#
# To set the proxy variable from the build environment:
# docker build --build-arg HTTP_PROXY="https://proxy.example.com:3128" .
#   OR

# docker build --build-arg HTTP_PROXY .
#   if the HTTP_PROXY environment variable is set.
# The above is important for pip to resolve repositories.
#
# To run the container with knowledge of a proxy, use:
# docker run --env HTTP_PROXY="https://proxy.example.com:3128" crl/dicom-tools
#
# If the build host is configured with the correct proxy information:
# docker build --network=host -t crl/dicom-tools:latest -f Dockerfile .


LABEL maintainer="warfield@crl.med.harvard.edu"
LABEL vendor="Computational Radiology Laboratory"

# Update the ubuntu.
RUN DEBIAN_FRONTEND=noninteractive apt-get \
    --option acquire::http::proxy="${HTTP_PROXY}" \
    --option acquire::https::proxy=false \
      -y update && \
    apt-get \
    --option acquire::http::proxy="${HTTP_PROXY}" \
    --option acquire::https::proxy=false \
      -y upgrade

RUN DEBIAN_FRONTEND=noninteractive apt-get \
    --option acquire::http::proxy="${HTTP_PROXY}" \
    --option acquire::https::proxy=false \
    install -y \
    apt-utils locales

ENV LANGUAGE=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

RUN DEBIAN_FRONTEND=noninteractive locale-gen en_US.UTF-8

RUN DEBIAN_FRONTEND=noninteractive apt-get \
    --option acquire::http::proxy="${HTTP_PROXY}" \
    --option acquire::https::proxy=false \
    install -y \
    build-essential git cmake pkg-config

RUN apt-get \
    --option acquire::http::proxy="${HTTP_PROXY}" \
    --option acquire::https::proxy=false \
    install -y --no-install-recommends \
    dcmtk \
    dicom3tools \
    jq \
    vim nano git curl wget \
    cron gnupg jq netcat tzdata \
    python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install pydicom pynetdicom SimpleITK numpy

RUN mkdir /src && cd /src && \
    git clone https://github.com/rordenlab/dcm2niix.git && \
    cd dcm2niix && mkdir build && cd build && cmake .. && make && make install

# Install the latest GDCM
# https://github.com/malaterre/GDCM/blob/master/INSTALL.txt
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

