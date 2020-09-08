#!/bin/sh
set -e

PKG=cuda
MAJOR_VERSION=${MAJOR_VERSION:-11}
VERSION=${VERSION:-11.0.3}
TARBALL=${PKG}-${VERSION}-x86_64

get_run_file() {
    printf "Downloading ${RUN_FILE}... "
    [[ -f $RUN_FILE ]] || wget -c -q ${DL_SITE}/$RUN_FILE
    printf "OK\n"
}

# Main installer
DL_SITE=http://developer.download.nvidia.com/compute/cuda/$VERSION/local_installers
RUN_FILE=cuda_${VERSION}_450.51.06_linux.run
get_run_file

# Unpack installer
rm -fr extract
mkdir -p extract
sh $RUN_FILE --extract=$(pwd)/extract --override --override-driver-check --silent

printf "Creating tarball ${TARBALL}... "

cd extract

# Remove driver installer
rm -f NVIDIA-Linux*.run

# Move out GDB sources
mv cuda_gdb/extras/cuda-gdb-*.src.tar.gz .

# Remove stubs
rm -fr */targets/x86_64-linux/lib/stubs

# Remove OpenCL copy
rm -fr cuda_cudart/targets/x86_64-linux/lib/libOpenCL.so*

mv ${PKG}-gdb-*.src.tar.gz ..

# Create tarball
mkdir ../${TARBALL}
mv * ../${TARBALL}
cd ..
tar --remove-files -cJf ${TARBALL}.tar.xz ${TARBALL}

rm -fr extract

printf "OK\n"
