#!/bin/sh

DOCKER_BUILDKIT=1 docker build --network=host --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') -t crl/dicom-tools:latest --build-arg VERSION="3.1.0" -f Dockerfile .

