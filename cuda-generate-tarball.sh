#!/bin/sh
set -e

PKG=cuda
MAJOR_VERSION=${MAJOR_VERSION:-10.1}
VERSION=${VERSION:-10.1.168}
TARBALL=${PKG}-${VERSION}-x86_64

get_run_file() {
    printf "Downloading ${RUN_FILE}... "
    [[ -f $RUN_FILE ]] || wget -c -q ${DL_SITE}/$RUN_FILE
    printf "OK\n"
}

# Main installer
DL_SITE=https://developer.nvidia.com/compute/cuda/$MAJOR_VERSION/Prod/local_installers
RUN_FILE=cuda_${VERSION}_418.67_linux.run
get_run_file

# Unpack installer
sh $RUN_FILE --extract=`pwd` --override

printf "Creating tarball ${TARBALL}... "

# Remove binaries included in system packages
rm -fr cuda-toolkit/jre
rm -f cuda-toolkit/targets/x86_64-linux/lib/libOpenCL.so*
rm -fr cuda-samples/common/lib

# Remove stubs
rm -fr cuda-toolkit/targets/x86_64-linux/lib/stubs

# Remove installers
rm -fr cuda-toolkit/bin/cuda-uninstaller \
    cuda-samples/bin

# Move out gdb sources
mv cuda-toolkit/extras/${PKG}-gdb-*.src.tar.gz .

# Create tarball
mkdir ${TARBALL}
mv cuda-toolkit cuda-samples ${TARBALL}
tar --remove-files -cJf ${TARBALL}.tar.xz ${TARBALL}

printf "OK\n"
