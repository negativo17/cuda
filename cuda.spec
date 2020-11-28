# Todo:
# - build cuda-gdb from source
# - /usr/include/cuda is owned by the cuda main package but the devel
#   subpackages use the directory

%global         debug_package %{nil}
%global         __strip /bin/true
%global         _missing_build_ids_terminate_build 0
%global         major_package_version 11-0

%if 0%{?rhel} == 6
%{?filter_setup:
%filter_from_provides /libQt5.*\.so.*/d; /libq.*\.so.*/d; /libicu.*\.so.*/d; /libssl\.so.*/d; /libcrypto\.so.*/d; /libstdc++\.so.*/d; /libprotobuf\.so.*/d; /libcupti\.so.*/d; /libboost_.*\.so.*/d
%filter_from_requires /libQt5.*\.so.*/d; /libq.*\.so.*/d; /libicu.*\.so.*/d; /libssl\.so.*/d; /libcrypto\.so.*/d; /libstdc++\.so.*/d; /libprotobuf\.so.*/d; /libcupti\.so.*/d; /libboost_.*\.so.*/d
%filter_setup
}
%else
%global         __provides_exclude ^(libQt5.*\\.so.*|libq.*\\.so.*|libicu.*\\.so.*|libssl\\.so.*|libcrypto\\.so.*|libstdc\\+\\+\\.so.*|libprotobuf\\.so.*|libcupti\\.so.*|libboost_.*\\.so.*)$
%global         __requires_exclude ^(libQt5.*\\.so.*|libq.*\\.so.*|libicu.*\\.so.*|libssl\\.so.*|libcrypto\\.so.*|libstdc\\+\\+\\.so.*|libprotobuf\\.so.*|libcupti\\.so.*|libboost_.*\\.so.*)$
%endif

Name:           cuda
Version:        11.1.1
Release:        3%{?dist}
Summary:        NVIDIA Compute Unified Device Architecture Toolkit
Epoch:          1
License:        NVIDIA License
URL:            https://developer.nvidia.com/cuda-zone
ExclusiveArch:  x86_64

Source0:        %{name}-%{version}-x86_64.tar.xz
Source1:        %{name}-gdb-11.1.105.src.tar.gz
Source2:        %{name}-generate-tarball.sh
Source3:        %{name}.sh
Source4:        %{name}.csh
Source5:        nvcc.profile

Source12:       nvvp.desktop
Source13:       nvvp.appdata.xml

Source19:       accinj64.pc
Source20:       cublas.pc
Source21:       cublasLt.pc
Source22:       cuda.pc
Source23:       cudart.pc
Source24:       cufft.pc
Source25:       cufftw.pc
Source26:       cuinj64.pc
Source27:       curand.pc
Source28:       cusolver.pc
Source29:       cusparse.pc
Source30:       nppc.pc
Source31:       nppial.pc
Source32:       nppicc.pc
Source33:       nppicom.pc
Source34:       nppidei.pc
Source35:       nppif.pc
Source36:       nppig.pc
Source37:       nppim.pc
Source38:       nppi.pc
Source39:       nppist.pc
Source40:       nppisu.pc
Source41:       nppitc.pc
Source42:       npps.pc
Source43:       nvml.pc
Source44:       nvrtc.pc
Source45:       nvToolsExt.pc
Source46:       nvjpeg.pc

BuildRequires:  ImageMagick
BuildRequires:  desktop-file-utils
# For RUNPATH removal
BuildRequires:  chrpath
# For execstack removal
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  execstack
BuildRequires:  perl(Getopt::Long)
%else
BuildRequires:  prelink
%endif

Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-core-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-minimal-build-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-gpu-library-advisor-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvcc-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvprune-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-docs < %{?epoch:%{epoch}:}%{version}-%{release}

%description
CUDA is a parallel computing platform and programming model that enables
dramatic increases in computing performance by harnessing the power of the
graphics processing unit (GPU).

%package cli-tools
Summary:        Compute Unified Device Architecture command-line tools
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       expat >= 1.95
Conflicts:      %{name}-command-line-tools-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cuobjdump-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-gdb-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-memcheck-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvdisasm-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvprof-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cli-tools
Contains the command line tools to debug and profile CUDA applications.

%package libs
Summary:        Compute Unified Device Architecture native run-time library
Requires(post): ldconfig
Conflicts:      %{name}-core-libs-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      %{name}-driver-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-license-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-libraries-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
# Explicitly declare the dependency or libcuda.so.1()(64bit) will pull in xorg-x11-drv-cuda-libs
Requires:       nvidia-driver-cuda-libs%{_isa}

%description libs
Contains the CUDA run-time library required to run CUDA application natively.

%package extra-libs
Summary:        All runtime NVIDIA CUDA libraries
Requires(post): ldconfig
Requires:       %{name}-cublas = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cudart = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cufft = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cupti = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-curand = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cusolver = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cusparse = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-npp = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvjpeg = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvrtc = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvtx = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-runtime-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-nvgraph < %{?epoch:%{epoch}:}%{version}-%{release}

%description extra-libs
Metapackage that installs all runtime NVIDIA CUDA libraries.

%package cublas
Summary:        NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS) libraries
Requires(post): ldconfig
Conflicts:      %{name}-cublas-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cublas
The NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS) library is a
GPU-accelerated version of the complete standard BLAS library that delivers 6x
to 17x faster performance than the latest MKL BLAS.

%package cublas-devel
Summary:        Development files for NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS)
Requires:       %{name}-cublas%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cublas-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description cublas-devel
This package provides development files for the NVIDIA CUDA Basic Linear
Algebra Subroutines (cuBLAS) libraries.

%package cudart
Summary:        NVIDIA CUDA Runtime API library
#Requires:       ocl-icd
Requires(post): ldconfig
Conflicts:      %{name}-cudart-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cudart
The runtime API eases device code management by providing implicit initialization,
context management, and module management. This leads to simpler code, but it
also lacks the level of control that the driver API has.

In comparison, the driver API offers more fine-grained control, especially over
contexts and module loading. Kernel launches are much more complex to implement,
as the execution configuration and kernel parameters must be specified with
explicit function calls. However, unlike the runtime, where all the kernels are
automatically loaded during initialization and stay loaded for as long as the
program runs, with the driver API it is possible to only keep the modules that
are currently needed loaded, or even dynamically reload modules. The driver API
is also language-independent as it only deals with cubin objects.

%package cudart-devel
Summary:        Development files for NVIDIA CUDA Runtime API library
Requires:       %{name}-cudart%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cudart-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description cudart-devel
This package provides development files for the NVIDIA CUDA Runtime API library

%package cufft
Summary:        NVIDIA CUDA Fast Fourier Transform library (cuFFT) libraries
Requires(post): ldconfig
Conflicts:      %{name}-cufft-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cufft
The NVIDIA CUDA Fast Fourier Transform libraries (cuFFT) provide a simple
interface for computing FFTs up to 10x faster.  By using hundreds of processor
cores inside NVIDIA GPUs, cuFFT delivers the floating‐point performance of a
GPU without having to develop your own custom GPU FFT implementation.

%package cufft-devel
Summary:        Development files for NVIDIA CUDA Fast Fourier Transform library (cuFFT)
Requires:       %{name}-cufft%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cufft-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description cufft-devel
This package provides development files for the NVIDIA CUDA Fast Fourier
Transform library (cuFFT) libraries.

%package cupti
Summary:        NVIDIA CUDA Profiling Tools Interface (CUPTI) library
Requires(post): ldconfig
Conflicts:      %{name}-cupti-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cupti
The NVIDIA CUDA Profiling Tools Interface (CUPTI) provides performance analysis
tools with detailed information about how applications are using the GPUs in a
system.

%package cupti-devel
Summary:        Development files for NVIDIA CUDA Profiling Tools Interface (CUPTI) library
Requires:       %{name}-cupti%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cupti-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cupti-devel
This package provides development files for the NVIDIA CUDA Profiling Tools
Interface (CUPTI) library.

%package curand
Summary:        NVIDIA CUDA Random Number Generation library (cuRAND)
Requires(post): ldconfig
Conflicts:      %{name}-curand-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description curand
The NVIDIA CUDA Random Number Generation library (cuRAND) delivers high
performance GPU-accelerated random number generation (RNG). The cuRAND library
delivers high quality random numbers 8x faster using hundreds of processor
cores available in NVIDIA GPUs.

%package curand-devel
Summary:        Development files for NVIDIA CUDA Random Number Generation library (cuRAND)
Requires:       %{name}-curand%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-curand-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description curand-devel
This package provides development files for the NVIDIA CUDA Random Number
Generation library (cuRAND).

%package cusolver
Summary:        NVIDIA cuSOLVER library
Requires(post): ldconfig
Requires:       libgomp%{_isa}
Conflicts:      %{name}-cusolver-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cusolver
The NVIDIA cuSOLVER library provides a collection of dense and sparse direct
solvers which deliver significant acceleration for Computer Vision, CFD,
Computational Chemistry, and Linear Optimization applications.

%package cusolver-devel
Summary:        Development files for NVIDIA cuSOLVER library
Requires:       %{name}-cusolver%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cusolver-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description cusolver-devel
This package provides development files for the NVIDIA cuSOLVER library.

%package cusparse
Summary:        NVIDIA CUDA Sparse Matrix library (cuSPARSE) library
Requires(post): ldconfig
Conflicts:      %{name}-cusparse-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cusparse
The NVIDIA CUDA Sparse Matrix library (cuSPARSE) provides a collection of basic
linear algebra subroutines used for sparse matrices that delivers up to 8x
faster performance than the latest MKL. The cuSPARSE library is designed to be
called from C or C++, and the latest release includes a sparse triangular
solver.

%package cusparse-devel
Summary:        Development files for NVIDIA CUDA Sparse Matrix library (cuSPARSE) library
Requires:       %{name}-cusparse%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cusparse-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description cusparse-devel
This package provides development files for the NVIDIA CUDA Sparse Matrix
library (cuSPARSE) library.

%package npp
Summary:        NVIDIA Performance Primitives libraries
Requires(post): ldconfig
Conflicts:      %{name}-npp-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description npp
The NVIDIA Performance Primitives library (NPP) is a collection of
GPU-accelerated image, video, and signal processing functions that deliver 5x
to 10x faster performance than comparable CPU-only implementations. Using NPP,
developers can take advantage of over 1900 image processing and approx 600
signal processing primitives to achieve significant improvements in application
performance in a matter of hours.

%package npp-devel
Summary:        Development files for NVIDIA Performance Primitives
Requires:       %{name}-npp%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-npp-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description npp-devel
This package provides development files for the NVIDIA Performance Primitives
libraries.

%package nvjpeg
Summary:        NVIDIA JPEG decoder (nvJPEG)
Requires(post): ldconfig
Conflicts:      %{name}-nvjpeg-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description nvjpeg
nvJPEG is a high-performance GPU-accelerated library for JPEG decoding. nvJPEG
supports decoding of single and batched images, color space conversion, multiple
phase decoding, and hybrid decoding using both CPU and GPU. Applications that
rely on nvJPEG for decoding deliver higher throughput and lower latency JPEG
decode compared CPU-only decoding.

%package nvjpeg-devel
Summary:        Development files for NVIDIA JPEG decoder (nvJPEG)
Requires:       %{name}-nvjpeg%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvjpeg-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description nvjpeg-devel
This package provides development files for the NVIDIA JPEG decoder (nvJPEG).

%package nvml-devel
Summary:        Development files for NVIDIA Management library (nvML)
# Unversioned as it is provided by the driver's NVML library
Requires:       %{name}-nvml%{_isa}
Conflicts:      %{name}-nvml-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description nvml-devel
This package provides development files for the NVIDIA Management library
(nvML).

%package nvrtc
Summary:        NVRTC runtime compilation library
Requires(post): ldconfig
Conflicts:      %{name}-nvrtc-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description nvrtc
NVRTC is a runtime compilation library for CUDA C++. It accepts CUDA C++ source
code in character string form and creates handles that can be used to obtain
the PTX. The PTX string generated by NVRTC can be loaded by cuModuleLoadData and
cuModuleLoadDataEx, and linked with other modules by cuLinkAddData of the CUDA
Driver API. This facility can often provide optimizations and performance not
possible in a purely offline static compilation.

%package nvrtc-devel
Summary:        Development files for the NVRTC runtime compilation library
Requires:       %{name}-nvrtc%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvrtc-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description nvrtc-devel
This package provides development files for the NVRTC runtime compilation
library.

%package nvtx
Summary:        NVIDIA Tools Extension
Requires(post): ldconfig
Conflicts:      %{name}-nvtx-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description nvtx
A C-based API for annotating events, code ranges, and resources in your
applications. Applications which integrate NVTX can use the Visual Profiler to
capture and visualize these events and ranges.

%package nvtx-devel
Summary:        Development files for NVIDIA Tools Extension
Requires:       %{name}-nvtx%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvtx-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description nvtx-devel
This package provides development files for the NVIDIA Tools Extension.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-libs%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cupti-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cublas-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cudart-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cufft-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cupti-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-curand-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cusolver-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cusparse-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-npp-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvjpeg-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvml-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvrtc-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvtx-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-headers-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      %{name}-libraries-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      %{name}-misc-headers-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      %{name}-toolkit-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Obsoletes:      %{name}-static < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-static = %{?epoch:%{epoch}:}%{version}
Obsoletes:      %{name}-nvgraph-devel < %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
This package provides the development files of the %{name} package.

%package samples
Summary:        Compute Unified Device Architecture toolkit samples
Conflicts:      %{name}-demo-suite-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      %{name}-samples-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Obsoletes:      %{name}-samples < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-samples = %{?epoch:%{epoch}:}%{version}
Requires:       cuda-devel = %{?epoch:%{epoch}:}%{version}
Requires:       gcc-c++
Requires:       freeglut-devel
Requires:       make
Requires:       mesa-libGLU-devel
Requires:       libX11-devel
Requires:       libXmu-devel
Requires:       libXi-devel

%description samples
Contains an extensive set of example CUDA programs.

%package nvvp
Summary:        NVIDIA Visual Profiler
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-nvvp-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-visual-tools-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description nvvp
The NVIDIA Visual Profiler is a cross-platform performance profiling tool that
delivers developers vital feedback for optimizing CUDA C/C++ applications.

%package sanitizer
Summary:        CUDA Sanitizer
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cupti-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-sanitizer-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description sanitizer
Provides a set of API's to enable third party tools to write GPU sanitizing
tools, such as memory and race checkers.

%prep
%setup -q -n %{name}-%{version}-x86_64

# Remove crypto libraries not linked correctly
find . -name "libcrypto.so*" -delete
find . -name "libssl.so*" -delete

# Remove RUNPATH on binaries
chrpath -d cuda_nvcc/nvvm/bin/cicc

# Replaced later
rm -f cuda_nvcc/bin/nvcc.profile

# RPMlint issues
find . -name "*.h" -exec chmod 644 {} \;
find . -name "*.hpp" -exec chmod 644 {} \;
find . -name "*.bat" -delete
find . -size 0 -delete

sed -i -e 's/env python/python2/g' cuda_samples/6_Advanced/matrixMulDynlinkJIT/extras/ptx2c.py

# Remove double quotes in samples' Makefiles (cosmetical)
find cuda_samples -name "Makefile" -exec sed -i -e 's|"/usr"|/usr|g' {} \;
# Make samples build without specifying anything on the command line for the
# include directories so people stop asking
find cuda_samples -type f -exec sed -i -e 's|/bin/nvcc|/bin/nvcc --include-path %{_includedir}/cuda|g' {} \;
find cuda_samples -name "Makefile" -exec sed -i -e 's|$(CUDA_PATH)/include|%{_includedir}/cuda|g' {} \;

%build
# Nothing to build

%install
# Create empty tree
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}%{_datadir}/%{name}/
mkdir -p %{buildroot}%{_datadir}/libnsight/
mkdir -p %{buildroot}%{_datadir}/libnvvp/
mkdir -p %{buildroot}%{_datadir}/pixmaps/
mkdir -p %{buildroot}%{_includedir}/%{name}/f
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
mkdir -p %{buildroot}%{_libexecdir}/%{name}/
mkdir -p %{buildroot}%{_sysconfdir}/profile.d/

# Environment settings
install -pm 644 %{SOURCE3} %{SOURCE4} %{buildroot}%{_sysconfdir}/profile.d

# Docs
mv cuda_gdb/extras/Debugger/Readme.txt cuda_gdb/extras/Debugger/Readme-Debugger.txt

# Remove duplicate headers
rm -f cuda_sanitizer_api/compute-sanitizer/include/generated*
# Headers
cp -fr \
    cuda_cudart/include/* \
    cuda_cupti/extras/CUPTI/include/* \
    cuda_nvcc/nvvm/include/* cuda_nvcc/include/* \
    cuda_nvml_dev/include/* \
    cuda_nvprof/include/* \
    cuda_nvrtc/include/* \
    cuda_nvtx/include/* \
    libcublas/include/* libcublas/src/* \
    libcufft/include/* \
    libcurand/include/* \
    libcusolver/include/* \
    libcusparse/include/* libcusparse/src/* \
    libnpp/include/* \
    libnvjpeg/include/* \
    cuda_sanitizer_api/compute-sanitizer/include/* \
    %{buildroot}%{_includedir}/%{name}/

cp -fr cuda_gdb/extras/Debugger/include %{buildroot}%{_includedir}/%{name}/Debugger/

# Libraries
cp -fr \
    cuda_cudart/lib64/* \
    cuda_cupti/extras/CUPTI/lib64/* \
    cuda_nvcc/nvvm/lib64/* \
    cuda_nvprof/lib64/* \
    cuda_nvrtc/lib64/* \
    cuda_nvtx/lib64/* \
    libcublas/lib64/* \
    libcufft/lib64/* \
    libcurand/lib64/* \
    libcusolver/lib64/* \
    libcusparse/lib64/* \
    libnpp/lib64/* \
    libnvjpeg/lib64/* \
    %{buildroot}%{_libdir}/

cp -fr cuda_nvcc/nvvm/libdevice/* %{buildroot}%{_datadir}/%{name}/

# Libraries in the driver package
ln -sf libnvidia-ml.so.1 %{buildroot}%{_libdir}/libnvidia-ml.so

# pkg-config files
install -pm 644 \
    %{SOURCE19} %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} \
    %{SOURCE25} %{SOURCE26} %{SOURCE27} %{SOURCE28} %{SOURCE29} %{SOURCE30} \
    %{SOURCE31} %{SOURCE32} %{SOURCE33} %{SOURCE34} %{SOURCE35} %{SOURCE36} \
    %{SOURCE37} %{SOURCE38} %{SOURCE39} %{SOURCE40} %{SOURCE41} %{SOURCE42} \
    %{SOURCE43} %{SOURCE44} %{SOURCE45} %{SOURCE46} \
    %{buildroot}/%{_libdir}/pkgconfig

# nvcc settings
install -pm 644 %{SOURCE5} %{buildroot}%{_bindir}/

# Set proper variables
sed -i \
    -e 's|CUDA_VERSION|%{version}|g' \
    -e 's|LIBDIR|%{_libdir}|g' \
    -e 's|INCLUDE_DIR|%{_includedir}/cuda|g' \
    %{buildroot}/%{_libdir}/pkgconfig/*.pc %{buildroot}/%{_bindir}/nvcc.profile

# Binaries
cp -fr \
    cuda_cuobjdump/bin/* \
    cuda_gdb/bin/* \
    cuda_memcheck/bin/* \
    cuda_nvcc/bin/* \
    cuda_nvcc/nvvm/bin/* \
    cuda_nvdisasm/bin/* \
    cuda_nvprof/bin/* \
    cuda_nvprune/bin/* \
    cuda_nvvp/bin/* \
    %{buildroot}%{_bindir}/

cp -fr cuda_sanitizer_api/compute-sanitizer/*.so %{buildroot}/%{_libexecdir}/%{name}

ln -sf %{_libexecdir}/%{name}/compute-sanitizer %{buildroot}%{_bindir}/compute-sanitizer

# Additional samples
cp -fr cuda_samples %{buildroot}%{_datadir}/%{name}/samples
cp -fr cuda_cupti/extras/CUPTI/samples %{buildroot}%{_datadir}/%{name}/samples/CUPTI
cp -fr cuda_nvml_dev/nvml/example %{buildroot}%{_datadir}/%{name}/samples/nvml
cp -fr cuda_nvcc/nvvm/libnvvm-samples %{buildroot}%{_datadir}/%{name}/samples/nvvm
cp -fr cuda_demo_suite/extras %{buildroot}%{_datadir}/%{name}/demo_suite

# Remove non-working libcrypto libraries
find . -name "*libcrypto*" -delete

# Nvidia Visual Profiler
convert cuda_nvvp/libnvvp/icon.xpm nvvp.png
install -m 644 -p nvvp.png %{buildroot}%{_datadir}/pixmaps/nvvp.png
cp -fr cuda_nvvp/libnvvp %{buildroot}%{_libdir}/nvvp
ln -sf ../%{_lib}/nvvp/nvvp %{buildroot}%{_bindir}/

# Desktop files
desktop-file-install --dir %{buildroot}%{_datadir}/applications/ %{SOURCE12}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/nvvp.desktop

%if 0%{?fedora}
# install AppData and add modalias provides
mkdir -p %{buildroot}%{_metainfodir}
install -p -m 0644 %{SOURCE13} %{buildroot}%{_metainfodir}/
%endif

%ldconfig_scriptlets

%ldconfig_scriptlets cli-tools

%ldconfig_scriptlets libs

%ldconfig_scriptlets cublas

%ldconfig_scriptlets cudart

%ldconfig_scriptlets cufft

%ldconfig_scriptlets cupti

%ldconfig_scriptlets curand

%ldconfig_scriptlets cusolver

%ldconfig_scriptlets cusparse

%ldconfig_scriptlets npp

%ldconfig_scriptlets nvjpeg

%ldconfig_scriptlets nvrtc

%ldconfig_scriptlets nvtx

%files
%{_bindir}/bin2c
%{_bindir}/cicc
# There should be no folder there, but binaries look for things here
%{_bindir}/crt/
%{_bindir}/cudafe++
%{_bindir}/cuobjdump
#%{_bindir}/gpu-library-advisor
%{_bindir}/fatbinary
%{_bindir}/nvcc
%{_bindir}/nvcc.profile
%{_bindir}/nvlink
%{_bindir}/nvprune
%{_bindir}/ptxas
%dir %{_includedir}/%{name}
%{_libexecdir}/%{name}/
%{_datadir}/%{name}/
%exclude %{_datadir}/%{name}/samples
%exclude %{_datadir}/%{name}/demo_suite
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh

%files cli-tools
%{_bindir}/cuda-gdb
%{_bindir}/cuda-gdbserver
%{_bindir}/cuda-memcheck
%{_bindir}/nvdisasm
%{_bindir}/nvprof

%files libs
%license EULA.txt
%{_libdir}/libaccinj%{__isa_bits}.so.*
%{_libdir}/libcuinj%{__isa_bits}.so.*
%{_libdir}/libnvvm.so.*

%files cublas
%license EULA.txt
%{_libdir}/libcublas.so.*
%{_libdir}/libcublasLt.so.*
%{_libdir}/libnvblas.so.*

%files cublas-devel
%{_includedir}/%{name}/nvblas.h
%{_includedir}/%{name}/cublasLt.h
%{_includedir}/%{name}/cublas_v2.h
%{_includedir}/%{name}/cublas.h
%{_includedir}/%{name}/cublas_api.h
%{_includedir}/%{name}/cublasXt.h
%{_includedir}/%{name}/fortran.c
%{_includedir}/%{name}/fortran_common.h
%{_includedir}/%{name}/fortran.h
%{_includedir}/%{name}/fortran_thunking.c
%{_includedir}/%{name}/fortran_thunking.h
%{_libdir}/libcublas_static.a
%{_libdir}/libcublas.so
%{_libdir}/libcublasLt_static.a
%{_libdir}/libcublasLt.so
%{_libdir}/libnvblas.so
%{_libdir}/pkgconfig/cublas.pc
%{_libdir}/pkgconfig/cublasLt.pc

%files cudart
%license EULA.txt
%{_libdir}/libcudart.so.*

%files cudart-devel
%{_includedir}/%{name}/crt/
%{_includedir}/%{name}/builtin_types.h
%{_includedir}/%{name}/channel_descriptor.h
%{_includedir}/%{name}/CL
%{_includedir}/%{name}/common_functions.h
%{_includedir}/%{name}/cooperative_groups
%{_includedir}/%{name}/cooperative_groups.h
%{_includedir}/%{name}/cub
%{_includedir}/%{name}/cuComplex.h
#%{_includedir}/%{name}/cuda
%{_includedir}/%{name}/cuda/atomic
%{_includedir}/%{name}/cuda_awbarrier.h
%{_includedir}/%{name}/cuda_awbarrier_helpers.h
%{_includedir}/%{name}/cuda_awbarrier_primitives.h
%{_includedir}/%{name}/cuda/barrier
%{_includedir}/%{name}/cuda_bf16.h
%{_includedir}/%{name}/cuda_bf16.hpp
%{_includedir}/%{name}/cuda_device_runtime_api.h
%{_includedir}/%{name}/cudaEGL.h
%{_includedir}/%{name}/cuda_egl_interop.h
%{_includedir}/%{name}/cuda_fp16.h
%{_includedir}/%{name}/cuda_fp16.hpp
%{_includedir}/%{name}/cudaGL.h
%{_includedir}/%{name}/cuda_gl_interop.h
%{_includedir}/%{name}/cuda.h
%{_includedir}/%{name}/cuda_occupancy.h
%{_includedir}/%{name}/cuda_pipeline.h
%{_includedir}/%{name}/cuda_pipeline_helpers.h
%{_includedir}/%{name}/cuda_pipeline_primitives.h
%{_includedir}/%{name}/cudart_platform.h
%{_includedir}/%{name}/cuda_runtime_api.h
%{_includedir}/%{name}/cuda_runtime.h
#%{_includedir}/%{name}/cuda/std
%{_includedir}/%{name}/cuda/std
%{_includedir}/%{name}/cuda_surface_types.h
%{_includedir}/%{name}/cuda_texture_types.h
%{_includedir}/%{name}/cudaVDPAU.h
%{_includedir}/%{name}/cuda_vdpau_interop.h
%{_includedir}/%{name}/device_atomic_functions.h
%{_includedir}/%{name}/device_atomic_functions.hpp
%{_includedir}/%{name}/device_double_functions.h
%{_includedir}/%{name}/device_functions.h
%{_includedir}/%{name}/device_launch_parameters.h
%{_includedir}/%{name}/device_types.h
%{_includedir}/%{name}/driver_functions.h
%{_includedir}/%{name}/driver_types.h
%{_includedir}/%{name}/host_config.h
%{_includedir}/%{name}/host_defines.h
%{_includedir}/%{name}/library_types.h
%{_includedir}/%{name}/math_constants.h
%{_includedir}/%{name}/math_functions.h
%{_includedir}/%{name}/mma.h
%{_includedir}/%{name}/nvfunctional
%{_includedir}/%{name}/sm_20_atomic_functions.h
%{_includedir}/%{name}/sm_20_atomic_functions.hpp
%{_includedir}/%{name}/sm_20_intrinsics.h
%{_includedir}/%{name}/sm_20_intrinsics.hpp
%{_includedir}/%{name}/sm_30_intrinsics.h
%{_includedir}/%{name}/sm_30_intrinsics.hpp
%{_includedir}/%{name}/sm_32_atomic_functions.h
%{_includedir}/%{name}/sm_32_atomic_functions.hpp
%{_includedir}/%{name}/sm_32_intrinsics.h
%{_includedir}/%{name}/sm_32_intrinsics.hpp
%{_includedir}/%{name}/sm_35_atomic_functions.h
%{_includedir}/%{name}/sm_35_intrinsics.h
%{_includedir}/%{name}/sm_60_atomic_functions.h
%{_includedir}/%{name}/sm_60_atomic_functions.hpp
%{_includedir}/%{name}/sm_61_intrinsics.h
%{_includedir}/%{name}/sm_61_intrinsics.hpp
%{_includedir}/%{name}/surface_functions.h
%{_includedir}/%{name}/surface_functions.hpp
%{_includedir}/%{name}/surface_indirect_functions.h
%{_includedir}/%{name}/surface_indirect_functions.hpp
%{_includedir}/%{name}/surface_types.h
%{_includedir}/%{name}/texture_fetch_functions.h
%{_includedir}/%{name}/texture_fetch_functions.hpp
%{_includedir}/%{name}/texture_indirect_functions.h
%{_includedir}/%{name}/texture_indirect_functions.hpp
%{_includedir}/%{name}/texture_types.h
%{_includedir}/%{name}/thrust
%{_includedir}/%{name}/vector_functions.h
%{_includedir}/%{name}/vector_functions.hpp
%{_includedir}/%{name}/vector_types.h
%{_libdir}/libcudadevrt.a
%{_libdir}/libcudart_static.a
%{_libdir}/libcudart.so
%{_libdir}/libculibos.a
%{_libdir}/pkgconfig/cudart.pc

%files nvtx
%license EULA.txt
%{_libdir}/libnvToolsExt.so.*

%files nvtx-devel
%{_includedir}/%{name}/nvToolsExt.h
%{_includedir}/%{name}/nvToolsExtCuda.h
%{_includedir}/%{name}/nvToolsExtCudaRt.h
%{_includedir}/%{name}/nvToolsExtOpenCL.h
%{_includedir}/%{name}/nvToolsExtSync.h
%{_includedir}/%{name}/nvtx3
%{_libdir}/libnvToolsExt.so
%{_libdir}/pkgconfig/nvToolsExt.pc

%files cufft
%license EULA.txt
%{_libdir}/libcufft.so.*
%{_libdir}/libcufftw.so.*

%files cufft-devel
%{_includedir}/%{name}/cudalibxt.h
%{_includedir}/%{name}/cufft.h
%{_includedir}/%{name}/cufftw.h
%{_includedir}/%{name}/cufftXt.h
%{_libdir}/libcufft_static.a
%{_libdir}/libcufft_static_nocallback.a
%{_libdir}/libcufft.so
%{_libdir}/libcufftw_static.a
%{_libdir}/libcufftw.so
%{_libdir}/pkgconfig/cufft.pc
%{_libdir}/pkgconfig/cufftw.pc

%files cupti
%license EULA.txt
%{_libdir}/libcupti.so.*

%files cupti-devel
%doc cuda_cupti/extras/CUPTI/doc/*
%{_includedir}/%{name}/cuda_stdint.h
%{_includedir}/%{name}/cupti_activity.h
%{_includedir}/%{name}/cupti_callbacks.h
%{_includedir}/%{name}/cupti_driver_cbid.h
%{_includedir}/%{name}/cupti_events.h
%{_includedir}/%{name}/cupti.h
%{_includedir}/%{name}/cupti_metrics.h
%{_includedir}/%{name}/cupti_nvtx_cbid.h
%{_includedir}/%{name}/cupti_profiler_target.h
%{_includedir}/%{name}/cupti_result.h
%{_includedir}/%{name}/cupti_runtime_cbid.h
%{_includedir}/%{name}/cupti_target.h
%{_includedir}/%{name}/cupti_version.h
%{_includedir}/%{name}/generated_cuda_gl_interop_meta.h
%{_includedir}/%{name}/generated_cudaGL_meta.h
%{_includedir}/%{name}/generated_cuda_meta.h
%{_includedir}/%{name}/generated_cuda_runtime_api_meta.h
%{_includedir}/%{name}/generated_cuda_vdpau_interop_meta.h
%{_includedir}/%{name}/generated_cudaVDPAU_meta.h
%{_includedir}/%{name}/generated_nvtx_meta.h
%{_includedir}/%{name}/nvperf_cuda_host.h
%{_includedir}/%{name}/nvperf_host.h
%{_includedir}/%{name}/nvperf_target.h
%{_includedir}/%{name}/Openacc
%{_includedir}/%{name}/Openmp
%{_libdir}/libcupti_static.a
%{_libdir}/libcupti.so
%{_libdir}/libnvperf_host.so
%{_libdir}/libnvperf_host_static.a
%{_libdir}/libnvperf_target.so

%files curand
%license EULA.txt
%{_libdir}/libcurand.so.*

%files curand-devel
%{_includedir}/%{name}/curand_discrete2.h
%{_includedir}/%{name}/curand_discrete.h
%{_includedir}/%{name}/curand_globals.h
%{_includedir}/%{name}/curand.h
%{_includedir}/%{name}/curand_kernel.h
%{_includedir}/%{name}/curand_lognormal.h
%{_includedir}/%{name}/curand_mrg32k3a.h
%{_includedir}/%{name}/curand_mtgp32dc_p_11213.h
%{_includedir}/%{name}/curand_mtgp32.h
%{_includedir}/%{name}/curand_mtgp32_host.h
%{_includedir}/%{name}/curand_mtgp32_kernel.h
%{_includedir}/%{name}/curand_normal.h
%{_includedir}/%{name}/curand_normal_static.h
%{_includedir}/%{name}/curand_philox4x32_x.h
%{_includedir}/%{name}/curand_poisson.h
%{_includedir}/%{name}/curand_precalc.h
%{_includedir}/%{name}/curand_uniform.h
%{_libdir}/libcurand_static.a
%{_libdir}/libcurand.so
%{_libdir}/pkgconfig/curand.pc

%files cusolver
%license EULA.txt
%{_libdir}/libcusolver.so.*
%{_libdir}/libcusolverMg.so.*

%files cusolver-devel
%{_includedir}/%{name}/cusolver_common.h
%{_includedir}/%{name}/cusolverDn.h
%{_includedir}/%{name}/cusolverMg.h
%{_includedir}/%{name}/cusolverRf.h
%{_includedir}/%{name}/cusolverSp.h
%{_includedir}/%{name}/cusolverSp_LOWLEVEL_PREVIEW.h
%{_libdir}/libcusolver_static.a
%{_libdir}/libcusolver.so
%{_libdir}/libcusolverMg.so
%{_libdir}/liblapack_static.a
%{_libdir}/libmetis_static.a
%{_libdir}/pkgconfig/cusolver.pc

%files cusparse
%license EULA.txt
%{_libdir}/libcusparse.so.*

%files cusparse-devel
%{_includedir}/%{name}/cusparse.h
%{_includedir}/%{name}/cusparse_v2.h
%{_includedir}/%{name}/cusparse_fortran.c
%{_includedir}/%{name}/cusparse_fortran_common.h
%{_includedir}/%{name}/cusparse_fortran.h
%{_libdir}/libcusparse_static.a
%{_libdir}/libcusparse.so
%{_libdir}/pkgconfig/cusparse.pc

%files npp
%license EULA.txt
%{_libdir}/libnppc.so.*
%{_libdir}/libnppial.so.*
%{_libdir}/libnppicc.so.*
%{_libdir}/libnppidei.so.*
%{_libdir}/libnppif.so.*
%{_libdir}/libnppig.so.*
%{_libdir}/libnppim.so.*
%{_libdir}/libnppist.so.*
%{_libdir}/libnppisu.so.*
%{_libdir}/libnppitc.so.*
%{_libdir}/libnpps.so.*

%files npp-devel
%{_includedir}/%{name}/nppcore.h
%{_includedir}/%{name}/nppdefs.h
%{_includedir}/%{name}/npp.h
%{_includedir}/%{name}/nppi_arithmetic_and_logical_operations.h
%{_includedir}/%{name}/nppi_color_conversion.h
%{_includedir}/%{name}/nppi_data_exchange_and_initialization.h
%{_includedir}/%{name}/nppi_filtering_functions.h
%{_includedir}/%{name}/nppi_geometry_transforms.h
%{_includedir}/%{name}/nppi.h
%{_includedir}/%{name}/nppi_linear_transforms.h
%{_includedir}/%{name}/nppi_morphological_operations.h
%{_includedir}/%{name}/nppi_statistics_functions.h
%{_includedir}/%{name}/nppi_support_functions.h
%{_includedir}/%{name}/nppi_threshold_and_compare_operations.h
%{_includedir}/%{name}/npps_arithmetic_and_logical_operations.h
%{_includedir}/%{name}/npps_conversion_functions.h
%{_includedir}/%{name}/npps_filtering_functions.h
%{_includedir}/%{name}/npps.h
%{_includedir}/%{name}/npps_initialization.h
%{_includedir}/%{name}/npps_statistics_functions.h
%{_includedir}/%{name}/npps_support_functions.h
%{_libdir}/libnppc.so
%{_libdir}/libnppc_static.a
%{_libdir}/libnppial.so
%{_libdir}/libnppial_static.a
%{_libdir}/libnppicc.so
%{_libdir}/libnppicc_static.a
%{_libdir}/libnppidei.so
%{_libdir}/libnppidei_static.a
%{_libdir}/libnppif.so
%{_libdir}/libnppif_static.a
%{_libdir}/libnppig.so
%{_libdir}/libnppig_static.a
%{_libdir}/libnppim.so
%{_libdir}/libnppim_static.a
%{_libdir}/libnppist.so
%{_libdir}/libnppist_static.a
%{_libdir}/libnppisu.so
%{_libdir}/libnppisu_static.a
%{_libdir}/libnppitc.so
%{_libdir}/libnppitc_static.a
%{_libdir}/libnpps.so
%{_libdir}/libnpps_static.a
%{_libdir}/pkgconfig/npp*.pc

%files nvjpeg
%license EULA.txt
%{_libdir}/libnvjpeg_static.a
%{_libdir}/libnvjpeg.so.*

%files nvjpeg-devel
%{_includedir}/%{name}/nvjpeg.h
%{_libdir}/libnvjpeg.so
%{_libdir}/pkgconfig/nvjpeg.pc

%files nvml-devel
%{_includedir}/%{name}/nvml*
%{_libdir}/libnvidia-ml.so
%{_libdir}/pkgconfig/nvml.pc

%files nvrtc
%license EULA.txt
%{_libdir}/libnvrtc-builtins.so.*
%{_libdir}/libnvrtc.so.*

%files nvrtc-devel
%{_includedir}/%{name}/nvrtc.h
%{_libdir}/libnvrtc-builtins.so
%{_libdir}/libnvrtc.so
%{_libdir}/pkgconfig/nvrtc.pc

%files extra-libs
# Empty metapackage

%files devel
%doc cuda_gdb/extras/Debugger/Readme-Debugger.txt
%{_includedir}/%{name}/CL
%{_includedir}/%{name}/Debugger
%{_includedir}/%{name}/builtin_types.h
%{_includedir}/%{name}/channel_descriptor.h
%{_includedir}/%{name}/common_functions.h
%{_includedir}/%{name}/cooperative_groups.h
%{_includedir}/%{name}/cuComplex.h
%{_includedir}/%{name}/cuda.h
%{_includedir}/%{name}/cudaEGL.h
%{_includedir}/%{name}/cudaGL.h
%{_includedir}/%{name}/cudaProfiler.h
%{_includedir}/%{name}/cudaVDPAU.h
%{_includedir}/%{name}/cuda_egl_interop.h
%{_includedir}/%{name}/cuda_fp16.h
%{_includedir}/%{name}/cuda_fp16.hpp
%{_includedir}/%{name}/cuda_gl_interop.h
%{_includedir}/%{name}/cuda_occupancy.h
%{_includedir}/%{name}/cuda_profiler_api.h
%{_includedir}/%{name}/cuda_surface_types.h
%{_includedir}/%{name}/cuda_texture_types.h
%{_includedir}/%{name}/cuda_vdpau_interop.h
%{_includedir}/%{name}/cudalibxt.h
%{_includedir}/%{name}/device_atomic_functions.h
%{_includedir}/%{name}/device_atomic_functions.hpp
%{_includedir}/%{name}/device_double_functions.h
%{_includedir}/%{name}/device_functions.h
%{_includedir}/%{name}/device_launch_parameters.h
%{_includedir}/%{name}/device_types.h
%{_includedir}/%{name}/driver_functions.h
%{_includedir}/%{name}/driver_types.h
%{_includedir}/%{name}/fatBinaryCtl.h
%{_includedir}/%{name}/fatbinary.h
%{_includedir}/%{name}/fatbinary_section.h
%{_includedir}/%{name}/host_config.h
%{_includedir}/%{name}/host_defines.h
%{_includedir}/%{name}/library_types.h
%{_includedir}/%{name}/math_constants.h
%{_includedir}/%{name}/math_functions.h
%{_includedir}/%{name}/mma.h
%{_includedir}/%{name}/nvfunctional
%{_includedir}/%{name}/nvPTXCompiler.h
%{_includedir}/%{name}/nvvm.h
%{_includedir}/%{name}/sm_20_atomic_functions.h
%{_includedir}/%{name}/sm_20_atomic_functions.hpp
%{_includedir}/%{name}/sm_20_intrinsics.h
%{_includedir}/%{name}/sm_20_intrinsics.hpp
%{_includedir}/%{name}/sm_30_intrinsics.h
%{_includedir}/%{name}/sm_30_intrinsics.hpp
%{_includedir}/%{name}/sm_32_atomic_functions.h
%{_includedir}/%{name}/sm_32_atomic_functions.hpp
%{_includedir}/%{name}/sm_32_intrinsics.h
%{_includedir}/%{name}/sm_32_intrinsics.hpp
%{_includedir}/%{name}/sm_35_atomic_functions.h
%{_includedir}/%{name}/sm_35_intrinsics.h
%{_includedir}/%{name}/sm_60_atomic_functions.h
%{_includedir}/%{name}/sm_60_atomic_functions.hpp
%{_includedir}/%{name}/sm_61_intrinsics.h
%{_includedir}/%{name}/sm_61_intrinsics.hpp
%{_includedir}/%{name}/surface_functions.h
%{_includedir}/%{name}/surface_functions.hpp
%{_includedir}/%{name}/surface_indirect_functions.h
%{_includedir}/%{name}/surface_indirect_functions.hpp
%{_includedir}/%{name}/surface_types.h
%{_includedir}/%{name}/texture_fetch_functions.h
%{_includedir}/%{name}/texture_fetch_functions.hpp
%{_includedir}/%{name}/texture_indirect_functions.h
%{_includedir}/%{name}/texture_indirect_functions.hpp
%{_includedir}/%{name}/texture_types.h
%{_includedir}/%{name}/thrust
%{_includedir}/%{name}/vector_functions.h
%{_includedir}/%{name}/vector_functions.hpp
%{_includedir}/%{name}/vector_types.h
# libcu++ headers:
%{_includedir}/%{name}/cuda/
%{_libdir}/libaccinj%{__isa_bits}.so
%{_libdir}/libcuinj%{__isa_bits}.so
%{_libdir}/libnvvm.so
%{_libdir}/pkgconfig/accinj64.pc
%{_libdir}/pkgconfig/cuda.pc
%{_libdir}/pkgconfig/cuinj64.pc

%files samples
%{_datadir}/%{name}/samples
%{_datadir}/%{name}/demo_suite

%files nvvp
%{_bindir}/computeprof
%{_bindir}/nvvp
%if 0%{?fedora}
%{_metainfodir}/nvvp.appdata.xml
%endif
%{_datadir}/applications/nvvp.desktop
%{_datadir}/pixmaps/nvvp.png
%{_libdir}/nvvp

%files sanitizer
%doc cuda_sanitizer_api/compute-sanitizer/docs
%{_bindir}/compute-sanitizer
%{_includedir}/%{name}/sanitizer_callbacks.h
%{_includedir}/%{name}/sanitizer_driver_cbid.h
%{_includedir}/%{name}/sanitizer.h
%{_includedir}/%{name}/sanitizer_memory.h
%{_includedir}/%{name}/sanitizer_patching.h
%{_includedir}/%{name}/sanitizer_result.h
%{_includedir}/%{name}/sanitizer_runtime_cbid.h
%{_includedir}/%{name}/sanitizer_stream.h
%{_libexecdir}/%{name}/libInterceptorInjectionTarget.so
%{_libexecdir}/%{name}/libsanitizer-collection.so
%{_libexecdir}/%{name}/libsanitizer-public.so
%{_libexecdir}/%{name}/libTreeLauncherPlaceholder.so
%{_libexecdir}/%{name}/libTreeLauncherTargetInjection.so
%{_libexecdir}/%{name}/libTreeLauncherTargetUpdatePreloadInjection.so

%changelog
* Sat Nov 28 2020 Simone Caronni <negativo17@gmail.com> - 1:11.1.1-3
- GCC 10 works fine.

* Mon Nov 16 2020 Simone Caronni <negativo17@gmail.com> - 1:11.1.1-2
- Nsight Compute & Systems are available separately.

* Sat Nov 14 2020 Simone Caronni <negativo17@gmail.com> - 1:11.1.1-1
- Update to 11.1.1.

* Sat Sep 05 2020 Simone Caronni <negativo17@gmail.com> - 1:11.0.3-1
- Update to 11.0.3.

* Mon Mar 16 2020 Simone Caronni <negativo17@gmail.com> - 1:10.2.89-2
- Do not merge the CUDA C++ standard library headers with the rest.

* Sun Feb 02 2020 Simone Caronni <negativo17@gmail.com> - 1:10.2.89-1
- Update to 10.2.89.

* Wed Oct 02 2019 Simone Caronni <negativo17@gmail.com> - 1:10.1.243-1
- Update to CUDA 10.1 update 2.

* Mon Jun 10 2019 Simone Caronni <negativo17@gmail.com> - 1:10.1.168-1
- Update to 10.1.168.
- Remove post* scriptlets.

* Sat Apr 06 2019 Simone Caronni <negativo17@gmail.com> - 1:10.1.105-1
- Update to 10.1.105.
- Trim changelog.
- Require cuda-gcc only on Fedora 30+ (GCC 9).

* Sat Jan 12 2019 Simone Caronni <negativo17@gmail.com> - 1:10.0.130-2
- Update SPEC file.

* Thu Jan 03 2019 Simone Caronni <negativo17@gmail.com> - 1:10.0.130-1
- Update to 10.0.130.

* Tue Aug 28 2018 Simone Caronni <negativo17@gmail.com> - 1:9.2.148.1-2
- Require GCC < 8 only on Fedora 28+.

* Mon Aug 27 2018 Simone Caronni <negativo17@gmail.com> - 1:9.2.148.1-1
- Update to 9.2.148.1.

* Fri Jun 01 2018 Simone Caronni <negativo17@gmail.com> - 1:9.1.85.3-7
- Remove cuda-nvml-devel package for i686, make the package x86_64 only.

* Wed May 09 2018 Simone Caronni <negativo17@gmail.com> - 1:9.1.85.3-6
- Add back CUDA_INC_PATH to environment.

* Wed Mar 07 2018 Simone Caronni <negativo17@gmail.com> - 1:9.1.85.3-5
- Add CUDA 9.1 patches and updated release notes.

* Sat Mar 03 2018 Simone Caronni <negativo17@gmail.com> - 1:9.1.85-4
- Fix nvcc.profile being replaced by default one.

* Thu Mar 01 2018 Simone Caronni <negativo17@gmail.com> - 1:9.1.85-3
- Re-add nvcc.profile in place of some environment variables. Used by CMake
  programs to find variables through nvcc verbose mode.
- Split Tools Extension out of CUDA runtime in its own package like upstream
  packages.
- Conflict also with the new upstream subpackages introduced in CUDA 9.1.
