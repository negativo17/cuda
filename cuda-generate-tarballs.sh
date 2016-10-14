#!/bin/sh -x
set -e

PKG=cuda
VERSION=8.0.44
TARBALL=${PKG}-${VERSION}-x86_64

# Get installer & unpack it
wget -O cuda_${VERSION}_linux.run \
    -c https://developer.nvidia.com/compute/cuda/8.0/prod/local_installers/cuda_${VERSION}_linux-run
sh ${PKG}_${VERSION}_linux.run -extract=`pwd`

# Unpack bundled installers and delete makeself executables
./${PKG}-linux64-rel-${VERSION}-*.run -nosymlink -noprompt -prefix=`pwd`/${TARBALL}
./${PKG}-samples-linux-${VERSION}-*.run -noprompt -cudaprefix=/usr -prefix=`pwd`/${TARBALL}/samples
rm -f cuda*.run NVIDIA-Linux-*.run

# Remove binaries included in system packages
rm -fr ${TARBALL}/jre

# Remove stubs
rm -fr ${TARBALL}/lib64/stubs

# Move out sources
mv ${TARBALL}/extras/${PKG}-gdb-${VERSION}.src.tar.gz .

# Create tarball
tar --remove-files -cJf ${TARBALL}.tar.xz ${TARBALL}
