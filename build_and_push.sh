#!/bin/sh

docker build --progress=plain -t benblamey/hom-impl-2.cp-notebook:latest .
docker push benblamey/hom-impl-2.cp-notebook:latest
