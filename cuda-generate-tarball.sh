#!/bin/sh
set -e

PKG=cuda
MAJOR_VERSION=${MAJOR_VERSION:-10.1}
VERSION=${VERSION:-10.1.243}
TARBALL=${PKG}-${VERSION}-x86_64

get_run_file() {
    printf "Downloading ${RUN_FILE}... "
    [[ -f $RUN_FILE ]] || wget -c -q ${DL_SITE}/$RUN_FILE
    printf "OK\n"
}

# Main installer
DL_SITE=http://developer.download.nvidia.com/compute/cuda/$MAJOR_VERSION/Prod/local_installers
RUN_FILE=cuda_${VERSION}_418.87.00_linux.run
get_run_file

# Unpack installer
rm -fr extract
mkdir -p extract
sh $RUN_FILE --extract=$(pwd)/extract --override --override-driver-check --silent

printf "Creating tarball ${TARBALL}... "

cd extract

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
mv cuda-toolkit/extras/${PKG}-gdb-*.src.tar.gz ..

# Remove extra architectures for tools
rm -fr \
    cuda-toolkit/nsight-compute-*/target/linux-desktop-glibc*x86 \
    cuda-toolkit/nsight-compute-*/target/linux-desktop-glibc*ppc64le

# Create tarball
mkdir ../${TARBALL}
mv cuda-toolkit cuda-samples ../${TARBALL}
cd ..
tar --remove-files -cJf ${TARBALL}.tar.xz ${TARBALL}

rm -fr extract

printf "OK\n"
