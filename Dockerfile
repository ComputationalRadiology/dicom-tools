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
#

LABEL maintainer="warfield@crl.med.harvard.edu"
LABEL vendor="Computational Radiology Laboratory"

# Update the ubuntu.
RUN apt-get -y update && \
    apt-get -y upgrade

RUN apt-get install -y build-essential git cmake pkg-config

RUN apt-get install -y --no-install-recommends \
    dcmtk \
    dicom3tools \
    vim nano python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir /src && cd /src && \
    git clone https://github.com/rordenlab/dcm2niix.git && \
    cd dcm2niix && mkdir build && cd build && cmake .. && make && make install

WORKDIR /data
CMD echo "Run binaries such as dcm2niix, dcmdjpeg, sort_dicoms.py"


# DOCKER_BUILDKIT=1 docker build --network=host --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') -t crl/dicom-tools:latest --build-arg VERSION=$BUILD_DATE -f Dockerfile .
# 
#
# docker run -it --rm --entrypoint bash crl/dicom-tools
#

