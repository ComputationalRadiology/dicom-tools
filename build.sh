#!/bin/sh

DOCKER_BUILDKIT=1 docker build --progress=plain --network=host --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') -t crl/dicom-tools:latest --build-arg VERSION="4.0.1" -f Dockerfile .

# Free the cache:
# DOCKER_BUILDKIT=1 docker build --no-cache --network=host --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') -t crl/dicom-tools:latest --build-arg VERSION="4.0.1" -f Dockerfile .
