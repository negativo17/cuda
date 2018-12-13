#!/bin/sh
set -e

PKG=cuda
MAJOR_VERSION=${MAJOR_VERSION:-9.2}
VERSION=${VERSION:-9.2.148}
PATCH_VERSION=${VERSION}.${PATCH_VERSION:-1}
TARBALL=${PKG}-${PATCH_VERSION}-x86_64

get_run_file() {
    printf "Downloading ${RUN_FILE}... "
    [[ -f $RUN_FILE ]] || wget -c -q ${DL_SITE}/$RUN_FILE
    printf "OK\n"
}

run_patch() {
    sh $RUN_FILE --silent --accept-eula --installdir=`pwd`/${TARBALL}
}

# Main installer
DL_SITE=https://developer.nvidia.com/compute/cuda/$MAJOR_VERSION/Prod2/local_installers
RUN_FILE=cuda_${VERSION}_396.37_linux
get_run_file

# Unpack installer
sh $RUN_FILE -extract=`pwd`
# Unpack bundled installers
sh ${PKG}-linux.${VERSION}-*.run -nosymlink -noprompt -prefix=`pwd`/${TARBALL}
sh ${PKG}-samples.${VERSION}-*.run -noprompt -cudaprefix=/usr -prefix=`pwd`/${TARBALL}/samples

# Patches
DL_SITE=https://developer.nvidia.com/compute/cuda/$MAJOR_VERSION/Prod2/patches/1
RUN_FILE=cuda_${VERSION}.1_linux
get_run_file
run_patch

# Update release notes
# https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html
printf "Downloading updated release notes... "
rm -f ${TARBALL}/doc/pdf/CUDA_Toolkit_Release_Notes.pdf
wget -c -q https://docs.nvidia.com/${PKG}/pdf/CUDA_Toolkit_Release_Notes.pdf
printf "OK\n"

printf "Creating tarball ${TARBALL}... "

# Remove binaries included in system packages
rm -fr ${TARBALL}/jre
rm -f ${TARBALL}/lib64/libOpenCL.so*

# Remove left overs from updates
rm -f ${TARBALL}/lib64/lib{cublas,cuinj64,nvblas}.so.9.2.148

# Remove stubs
rm -fr ${TARBALL}/lib64/stubs

# Remove unused stuff
find ${TARBALL}/bin ${TARBALL}/samples -name "*install*" -delete

# Move out sources
mv ${TARBALL}/extras/${PKG}-gdb-${VERSION}.src.tar.gz .

# Create tarball
tar --remove-files -cJf ${TARBALL}.tar.xz ${TARBALL}

printf "OK\n"