#!/bin/sh -x
set -e

PKG=cuda
VERSION=7.5.18
# Needs to be an absolute path
TARBALL=${PKG}-${VERSION}-x86_64

# Get installer & unpack it
wget -c http://developer.download.nvidia.com/compute/cuda/7.5/Prod/local_installers/cuda_${VERSION}_linux.run
sh cuda_${VERSION}_linux.run -extract=`pwd`

# Unpack bundled installers and delete makeself executables
./${PKG}-linux64-rel-${VERSION}-*.run -nosymlink -noprompt -prefix=`pwd`/${TARBALL}
./${PKG}-samples-linux-${VERSION}-*.run -noprompt -cudaprefix=/usr -prefix=`pwd`/${TARBALL}/samples 
rm -f cuda*.run NVIDIA-Linux-*.run

# Remove binaries included in system packages
rm -fr \
    ${TARBALL}/jre \
    ${TARBALL}/libnsight/libcairo-swt.so \
    ${TARBALL}/libnvvp/libcairo-swt.so

# Remove stubs
rm -fr ${TARBALL}/lib64/stubs

# Do not bundle 32 bit libraries in 64 bit packages
rm -fr ${TARBALL}/lib

# Create tarball
tar --remove-files -cJf ${TARBALL}.tar.xz ${TARBALL}
