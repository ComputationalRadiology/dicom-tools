#!/bin/sh

export HTTP_PROXY=http://proxy.tch.harvard.edu:3128

DOCKER_BUILDKIT=1 docker build --network=host \
  --build-arg HTTP_PROXY=${HTTP_PROXY} \
  --progress=plain \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  -t crl/dicom-tools:latest --build-arg VERSION="4.0.1" -f Dockerfile .

# Free the cache:
# DOCKER_BUILDKIT=1 docker build --no-cache --network=host --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') -t crl/dicom-tools:latest --build-arg VERSION="4.0.1" -f Dockerfile .

