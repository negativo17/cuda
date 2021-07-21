# Todo:
# - build cuda-gdb from source

%global         debug_package %{nil}
%global         __strip /bin/true
%global         _missing_build_ids_terminate_build 0
%global         _build_id_links none
%global         major_package_version 11-4

%global         __provides_exclude ^(libQt5.*\\.so.*|libq.*\\.so.*|libicu.*\\.so.*|libssl\\.so.*|libcrypto\\.so.*|libstdc\\+\\+\\.so.*|libprotobuf\\.so.*|libcupti\\.so.*|libboost_.*\\.so.*)$
%global         __requires_exclude ^(libQt5.*\\.so.*|libq.*\\.so.*|libicu.*\\.so.*|libssl\\.so.*|libcrypto\\.so.*|libstdc\\+\\+\\.so.*|libprotobuf\\.so.*|libcupti\\.so.*|libboost_.*\\.so.*)$

Name:           cuda
Version:        11.4.0
Release:        1%{?dist}
Summary:        NVIDIA Compute Unified Device Architecture Toolkit
Epoch:          1
License:        NVIDIA EULA
URL:            https://developer.nvidia.com/cuda-zone
ExclusiveArch:  x86_64

Source0:        %{name}-%{version}-x86_64.tar.xz
Source1:        %{name}-gdb-11.4.55.src.tar.gz
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
Conflicts:      libcublas-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cublas
The NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS) library is a
GPU-accelerated version of the complete standard BLAS library that delivers 6x
to 17x faster performance than the latest MKL BLAS.

%package cublas-devel
Summary:        Development files for NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS)
Requires:       %{name}-cublas%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cublas-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      libcublas-devel-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description cublas-devel
This package provides development files for the NVIDIA CUDA Basic Linear
Algebra Subroutines (cuBLAS) libraries.

%package cublas-static
Summary:        Static libraries for NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS)
Requires:       %{name}-cublas-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description cublas-static
This package contains static libraries for the NVIDIA CUDA Basic Linear Algebra
Subroutines (cuBLAS).

%package cudart
Summary:        NVIDIA CUDA Runtime API library
#Requires:       ocl-icd
Requires(post): ldconfig
Conflicts:      %{name}-cudart-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cudart
The CUDA runtime API eases device code management by providing implicit
initialization, context management, and module management. This leads to simpler
code, but it also lacks the level of control that the driver API has.

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
This package provides development files for the NVIDIA CUDA Runtime API library.

%package cudart-static
Summary:        Static libraries for NVIDIA CUDA Runtime API
Requires:       %{name}-cudart-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description cudart-static
This package contains static libraries for NVIDIA CUDA Runtime API.

%package cufft
Summary:        NVIDIA CUDA Fast Fourier Transform library (cuFFT) libraries
Requires(post): ldconfig
Conflicts:      %{name}-cufft-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      libcufft-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cufft
The NVIDIA CUDA Fast Fourier Transform libraries (cuFFT) provide a simple
interface for computing FFTs up to 10x faster.  By using hundreds of processor
cores inside NVIDIA GPUs, cuFFT delivers the floating‐point performance of a
GPU without having to develop your own custom GPU FFT implementation.

%package cufft-devel
Summary:        Development files for NVIDIA CUDA Fast Fourier Transform library (cuFFT)
Requires:       %{name}-cufft%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cufft-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      libcufft-devel-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description cufft-devel
This package provides development files for the NVIDIA CUDA Fast Fourier
Transform library (cuFFT) libraries.

%package cufft-static
Summary:        Static libraries for NVIDIA CUDA Fast Fourier Transform (cuFFT)
Requires:       %{name}-cufft-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description cufft-static
This package contains static libraries for NVIDIA CUDA Fast Fourier Transform (cuFFT).

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

%package cupti-static
Summary:        Static libraries for NVIDIA CUDA Profiling Tools Interface (CUPTI)
Requires:       %{name}-cupti-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description cupti-static
This package contains static libraries for NVIDIA CUDA Profiling Tools Interface
(CUPTI).

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

%package curand-static
Summary:        Static libraries for NVIDIA CUDA Random Number Generation (cuRAND)
Requires:       %{name}-curand-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description curand-static
This package contains static libraries for NVIDIA CUDA Random Number Generation
(cuRAND).

%package cusolver
Summary:        NVIDIA cuSOLVER library
Requires(post): ldconfig
Requires:       libgomp%{_isa}
Conflicts:      %{name}-cusolver-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      libcusolver-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cusolver
The NVIDIA cuSOLVER library provides a collection of dense and sparse direct
solvers which deliver significant acceleration for Computer Vision, CFD,
Computational Chemistry, and Linear Optimization applications.

%package cusolver-devel
Summary:        Development files for NVIDIA cuSOLVER library
Requires:       %{name}-cusolver%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cusolver-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      libcusolver-devel-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description cusolver-devel
This package provides development files for the NVIDIA cuSOLVER library.

%package cusolver-static
Summary:        Static libraries for NVIDIA cuSOLVER
Requires:       %{name}-cusolver-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description cusolver-static
This package contains static libraries for NVIDIA cuSOLVER.

%package cusparse
Summary:        NVIDIA CUDA Sparse Matrix library (cuSPARSE) library
Requires(post): ldconfig
Conflicts:      %{name}-cusparse-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      libcusparse-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description cusparse
The NVIDIA CUDA Sparse Matrix library (cuSPARSE) provides a collection of basic
linear algebra subroutines used for sparse matrices that delivers up to 8x
faster performance than the latest MKL. The cuSPARSE library is designed to be
called from C or C++, and the latest release includes a sparse triangular
solver.

%package cusparse-devel
Summary:        Development files for NVIDIA CUDA Sparse Matrix (cuSPARSE) library
Requires:       %{name}-cusparse%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-cusparse-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      libcusparse-devel-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description cusparse-devel
This package provides development files for the NVIDIA CUDA Sparse Matrix
library (cuSPARSE) library.

%package cusparse-static
Summary:        Static libraries for NVIDIA CUDA Sparse Matrix (cuSPARSE)
Requires:       %{name}-cusparse-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description cusparse-static
This package contains static libraries for NVIDIA CUDA Sparse Matrix (cuSPARSE).

%package npp
Summary:        NVIDIA Performance Primitives libraries
Requires(post): ldconfig
Conflicts:      %{name}-npp-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      libnpp-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

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
Conflicts:      libnpp-devel-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description npp-devel
This package provides development files for the NVIDIA Performance Primitives
libraries.

%package npp-static
Summary:        Static libraries for NVIDIA Performance Primitives
Requires:       %{name}-npp-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description npp-static
This package contains static libraries for NVIDIA Performance Primitives.

%package nvjpeg
Summary:        NVIDIA JPEG decoder (nvJPEG)
Requires(post): ldconfig
Conflicts:      %{name}-nvjpeg-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      libnvjpeg-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

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
Conflicts:      libnvjpeg-devel-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description nvjpeg-devel
This package provides development files for the NVIDIA JPEG decoder (nvJPEG).

%package nvjpeg-static
Summary:        Static libraries for NVIDIA JPEG decoder (nvJPEG)
Requires:       %{name}-nvjpeg-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description nvjpeg-static
This package contains static libraries for NVIDIA JPEG decoder (nvJPEG).

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
Conflicts:      %{name}-cccl-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      %{name}-headers-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      %{name}-libraries-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      %{name}-misc-headers-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      %{name}-toolkit-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Obsoletes:      %{name}-static < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-cub = %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-static = %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-toolkit-%{major_package_version} = %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-thrust-%{major_package_version} = %{?epoch:%{epoch}:}%{version}
Obsoletes:      %{name}-nvgraph-devel < %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
This package provides the development files of the %{name} package.

%package samples
Summary:        Compute Unified Device Architecture toolkit samples
Conflicts:      %{name}-demo-suite-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Conflicts:      %{name}-samples-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Obsoletes:      %{name}-samples < %{?epoch:%{epoch}:}%{version}
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

# ?
rm -frv cuda_nvrtc/lib64/nvrtc-prev

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
    cuda_thrust/include/* \
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
    cuda_cuxxfilt/bin/* \
    cuda_gdb/bin/* \
    cuda_memcheck/bin/* \
    cuda_nvcc/bin/* \
    cuda_nvcc/nvvm/bin/* \
    cuda_nvdisasm/bin/* \
    cuda_nvprof/bin/* \
    cuda_nvprune/bin/* \
    cuda_nvvp/bin/* \
    %{buildroot}%{_bindir}/

cp -a cuda_sanitizer_api/compute-sanitizer/*.so %{buildroot}/%{_libexecdir}/%{name}
cp -a cuda_sanitizer_api/compute-sanitizer/compute-sanitizer %{buildroot}%{_bindir}/compute-sanitizer

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
%{_bindir}/cu++filt
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
%license cuda_documentation/EULA.txt
%{_libdir}/libaccinj%{__isa_bits}.so.*
%{_libdir}/libcuinj%{__isa_bits}.so.*
%{_libdir}/libnvvm.so.*

%files cublas
%license cuda_documentation/EULA.txt
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
%{_libdir}/libcublas.so
%{_libdir}/libcublasLt.so
%{_libdir}/libnvblas.so
%{_libdir}/pkgconfig/cublas.pc
%{_libdir}/pkgconfig/cublasLt.pc

%files cublas-static
%{_libdir}/libcublas_static.a
%{_libdir}/libcublasLt_static.a

%files cudart
%license cuda_documentation/EULA.txt
%{_libdir}/libcudart.so.*

%files cudart-devel
%{_includedir}/%{name}/builtin_types.h
%{_includedir}/%{name}/channel_descriptor.h
%{_includedir}/%{name}/CL
%{_includedir}/%{name}/common_functions.h
%{_includedir}/%{name}/cooperative_groups
%{_includedir}/%{name}/cooperative_groups.h
%{_includedir}/%{name}/crt/
%{_includedir}/%{name}/cuComplex.h
%{_includedir}/%{name}/cuda_awbarrier.h
%{_includedir}/%{name}/cuda_awbarrier_helpers.h
%{_includedir}/%{name}/cuda_awbarrier_primitives.h
%{_includedir}/%{name}/cuda_bf16.h
%{_includedir}/%{name}/cuda_bf16.hpp
%{_includedir}/%{name}/cuda_device_runtime_api.h
%{_includedir}/%{name}/cudaEGL.h
%{_includedir}/%{name}/cuda_egl_interop.h
%{_includedir}/%{name}/cudaEGLTypedefs.h
%{_includedir}/%{name}/cuda_fp16.h
%{_includedir}/%{name}/cuda_fp16.hpp
%{_includedir}/%{name}/cudaGL.h
%{_includedir}/%{name}/cuda_gl_interop.h
%{_includedir}/%{name}/cudaGLTypedefs.h
%{_includedir}/%{name}/cuda.h
%{_includedir}/%{name}/cuda_occupancy.h
%{_includedir}/%{name}/cuda_pipeline.h
%{_includedir}/%{name}/cuda_pipeline_helpers.h
%{_includedir}/%{name}/cuda_pipeline_primitives.h
%{_includedir}/%{name}/cudaProfilerTypedefs.h
%{_includedir}/%{name}/cudart_platform.h
%{_includedir}/%{name}/cuda_runtime_api.h
%{_includedir}/%{name}/cuda_runtime.h
%{_includedir}/%{name}/cuda_surface_types.h
%{_includedir}/%{name}/cuda_texture_types.h
%{_includedir}/%{name}/cudaTypedefs.h
%{_includedir}/%{name}/cudaVDPAU.h
%{_includedir}/%{name}/cuda_vdpau_interop.h
%{_includedir}/%{name}/cudaVDPAUTypedefs.h
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
%{_includedir}/%{name}/vector_functions.h
%{_includedir}/%{name}/vector_functions.hpp
%{_includedir}/%{name}/vector_types.h
%{_libdir}/libcudadevrt.a
%{_libdir}/libcudart.so
%{_libdir}/libculibos.a
%{_libdir}/pkgconfig/cudart.pc

%files cudart-static
%{_libdir}/libcudart_static.a

%files nvtx
%license cuda_documentation/EULA.txt
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
%license cuda_documentation/EULA.txt
%{_libdir}/libcufft.so.*
%{_libdir}/libcufftw.so.*

%files cufft-devel
%{_includedir}/%{name}/cudalibxt.h
%{_includedir}/%{name}/cufft.h
%{_includedir}/%{name}/cufftw.h
%{_includedir}/%{name}/cufftXt.h
%{_libdir}/libcufft.so
%{_libdir}/libcufftw.so
%{_libdir}/pkgconfig/cufft.pc
%{_libdir}/pkgconfig/cufftw.pc

%files cufft-static
%{_libdir}/libcufft_static.a
%{_libdir}/libcufft_static_nocallback.a
%{_libdir}/libcufftw_static.a

%files cupti
%license cuda_documentation/EULA.txt
%{_libdir}/libcupti.so.*
%{_libdir}/libpcsamplingutil.so

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
%{_includedir}/%{name}/cupti_pcsampling.h
%{_includedir}/%{name}/cupti_pcsampling_util.h
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
%{_includedir}/%{name}/nvperf_common.h
%{_includedir}/%{name}/nvperf_cuda_host.h
%{_includedir}/%{name}/nvperf_host.h
%{_includedir}/%{name}/nvperf_target.h
%{_includedir}/%{name}/Openacc
%{_includedir}/%{name}/Openmp
%{_libdir}/libcupti.so
%{_libdir}/libnvperf_host.so
%{_libdir}/libnvperf_target.so

%files cupti-static
%{_libdir}/libcupti_static.a
%{_libdir}/libnvperf_host_static.a

%files curand
%license cuda_documentation/EULA.txt
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
%{_libdir}/libcurand.so
%{_libdir}/pkgconfig/curand.pc

%files curand-static
%{_libdir}/libcurand_static.a

%files cusolver
%license cuda_documentation/EULA.txt
%{_libdir}/libcusolver.so.*
%{_libdir}/libcusolverMg.so.*

%files cusolver-devel
%{_includedir}/%{name}/cusolver_common.h
%{_includedir}/%{name}/cusolverDn.h
%{_includedir}/%{name}/cusolverMg.h
%{_includedir}/%{name}/cusolverRf.h
%{_includedir}/%{name}/cusolverSp.h
%{_includedir}/%{name}/cusolverSp_LOWLEVEL_PREVIEW.h
%{_libdir}/libcusolver.so
%{_libdir}/libcusolverMg.so
%{_libdir}/liblapack_static.a
%{_libdir}/libmetis_static.a
%{_libdir}/pkgconfig/cusolver.pc

%files cusolver-static
%{_libdir}/libcusolver_static.a

%files cusparse
%license cuda_documentation/EULA.txt
%{_libdir}/libcusparse.so.*

%files cusparse-devel
%{_includedir}/%{name}/cusparse.h
%{_includedir}/%{name}/cusparse_v2.h
%{_includedir}/%{name}/cusparse_fortran.c
%{_includedir}/%{name}/cusparse_fortran_common.h
%{_includedir}/%{name}/cusparse_fortran.h
%{_libdir}/libcusparse.so
%{_libdir}/pkgconfig/cusparse.pc

%files cusparse-static
%{_libdir}/libcusparse_static.a

%files npp
%license cuda_documentation/EULA.txt
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
%{_libdir}/libnppial.so
%{_libdir}/libnppicc.so
%{_libdir}/libnppidei.so
%{_libdir}/libnppif.so
%{_libdir}/libnppig.so
%{_libdir}/libnppim.so
%{_libdir}/libnppist.so
%{_libdir}/libnppisu.so
%{_libdir}/libnppitc.so
%{_libdir}/libnpps.so
%{_libdir}/pkgconfig/npp*.pc

%files npp-static
%{_libdir}/libnppc_static.a
%{_libdir}/libnppial_static.a
%{_libdir}/libnppicc_static.a
%{_libdir}/libnppidei_static.a
%{_libdir}/libnppif_static.a
%{_libdir}/libnppig_static.a
%{_libdir}/libnppim_static.a
%{_libdir}/libnppist_static.a
%{_libdir}/libnppisu_static.a
%{_libdir}/libnppitc_static.a
%{_libdir}/libnpps_static.a

%files nvjpeg
%license cuda_documentation/EULA.txt
%{_libdir}/libnvjpeg.so.*

%files nvjpeg-static
%{_libdir}/libnvjpeg_static.a

%files nvjpeg-devel
%{_includedir}/%{name}/nvjpeg.h
%{_libdir}/libnvjpeg.so
%{_libdir}/pkgconfig/nvjpeg.pc

%files nvml-devel
%{_includedir}/%{name}/nvml*
%{_libdir}/libnvidia-ml.so
%{_libdir}/pkgconfig/nvml.pc

%files nvrtc
%license cuda_documentation/EULA.txt
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
%{_includedir}/%{name}/builtin_types.h
%{_includedir}/%{name}/channel_descriptor.h
%{_includedir}/%{name}/CL
%{_includedir}/%{name}/common_functions.h
%{_includedir}/%{name}/cooperative_groups.h
%{_includedir}/%{name}/cub/agent/agent_histogram.cuh
%{_includedir}/%{name}/cub/agent/agent_radix_sort_downsweep.cuh
%{_includedir}/%{name}/cub/agent/agent_radix_sort_histogram.cuh
%{_includedir}/%{name}/cub/agent/agent_radix_sort_onesweep.cuh
%{_includedir}/%{name}/cub/agent/agent_radix_sort_upsweep.cuh
%{_includedir}/%{name}/cub/agent/agent_reduce_by_key.cuh
%{_includedir}/%{name}/cub/agent/agent_reduce.cuh
%{_includedir}/%{name}/cub/agent/agent_rle.cuh
%{_includedir}/%{name}/cub/agent/agent_scan.cuh
%{_includedir}/%{name}/cub/agent/agent_segment_fixup.cuh
%{_includedir}/%{name}/cub/agent/agent_select_if.cuh
%{_includedir}/%{name}/cub/agent/agent_spmv_orig.cuh
%{_includedir}/%{name}/cub/agent/single_pass_scan_operators.cuh
%{_includedir}/%{name}/cub/block/block_adjacent_difference.cuh
%{_includedir}/%{name}/cub/block/block_discontinuity.cuh
%{_includedir}/%{name}/cub/block/block_exchange.cuh
%{_includedir}/%{name}/cub/block/block_histogram.cuh
%{_includedir}/%{name}/cub/block/block_load.cuh
%{_includedir}/%{name}/cub/block/block_radix_rank.cuh
%{_includedir}/%{name}/cub/block/block_radix_sort.cuh
%{_includedir}/%{name}/cub/block/block_raking_layout.cuh
%{_includedir}/%{name}/cub/block/block_reduce.cuh
%{_includedir}/%{name}/cub/block/block_scan.cuh
%{_includedir}/%{name}/cub/block/block_shuffle.cuh
%{_includedir}/%{name}/cub/block/block_store.cuh
%{_includedir}/%{name}/cub/block/radix_rank_sort_operations.cuh
%{_includedir}/%{name}/cub/block/specializations/block_histogram_atomic.cuh
%{_includedir}/%{name}/cub/block/specializations/block_histogram_sort.cuh
%{_includedir}/%{name}/cub/block/specializations/block_reduce_raking_commutative_only.cuh
%{_includedir}/%{name}/cub/block/specializations/block_reduce_raking.cuh
%{_includedir}/%{name}/cub/block/specializations/block_reduce_warp_reductions.cuh
%{_includedir}/%{name}/cub/block/specializations/block_scan_raking.cuh
%{_includedir}/%{name}/cub/block/specializations/block_scan_warp_scans2.cuh
%{_includedir}/%{name}/cub/block/specializations/block_scan_warp_scans3.cuh
%{_includedir}/%{name}/cub/block/specializations/block_scan_warp_scans.cuh
%{_includedir}/%{name}/cub/cmake/cub-config.cmake
%{_includedir}/%{name}/cub/cmake/cub-config-version.cmake
%{_includedir}/%{name}/cub/config.cuh
%{_includedir}/%{name}/cub/cub.cuh
%{_includedir}/%{name}/cub/device/device_histogram.cuh
%{_includedir}/%{name}/cub/device/device_partition.cuh
%{_includedir}/%{name}/cub/device/device_radix_sort.cuh
%{_includedir}/%{name}/cub/device/device_reduce.cuh
%{_includedir}/%{name}/cub/device/device_run_length_encode.cuh
%{_includedir}/%{name}/cub/device/device_scan.cuh
%{_includedir}/%{name}/cub/device/device_segmented_radix_sort.cuh
%{_includedir}/%{name}/cub/device/device_segmented_reduce.cuh
%{_includedir}/%{name}/cub/device/device_select.cuh
%{_includedir}/%{name}/cub/device/device_spmv.cuh
%{_includedir}/%{name}/cub/device/dispatch/dispatch_histogram.cuh
%{_includedir}/%{name}/cub/device/dispatch/dispatch_radix_sort.cuh
%{_includedir}/%{name}/cub/device/dispatch/dispatch_reduce_by_key.cuh
%{_includedir}/%{name}/cub/device/dispatch/dispatch_reduce.cuh
%{_includedir}/%{name}/cub/device/dispatch/dispatch_rle.cuh
%{_includedir}/%{name}/cub/device/dispatch/dispatch_scan.cuh
%{_includedir}/%{name}/cub/device/dispatch/dispatch_select_if.cuh
%{_includedir}/%{name}/cub/device/dispatch/dispatch_spmv_orig.cuh
%{_includedir}/%{name}/cub/grid/grid_barrier.cuh
%{_includedir}/%{name}/cub/grid/grid_even_share.cuh
%{_includedir}/%{name}/cub/grid/grid_mapping.cuh
%{_includedir}/%{name}/cub/grid/grid_queue.cuh
%{_includedir}/%{name}/cub/host/mutex.cuh
%{_includedir}/%{name}/cub/iterator/arg_index_input_iterator.cuh
%{_includedir}/%{name}/cub/iterator/cache_modified_input_iterator.cuh
%{_includedir}/%{name}/cub/iterator/cache_modified_output_iterator.cuh
%{_includedir}/%{name}/cub/iterator/constant_input_iterator.cuh
%{_includedir}/%{name}/cub/iterator/counting_input_iterator.cuh
%{_includedir}/%{name}/cub/iterator/discard_output_iterator.cuh
%{_includedir}/%{name}/cub/iterator/tex_obj_input_iterator.cuh
%{_includedir}/%{name}/cub/iterator/tex_ref_input_iterator.cuh
%{_includedir}/%{name}/cub/iterator/transform_input_iterator.cuh
%{_includedir}/%{name}/cub/thread/thread_load.cuh
%{_includedir}/%{name}/cub/thread/thread_operators.cuh
%{_includedir}/%{name}/cub/thread/thread_reduce.cuh
%{_includedir}/%{name}/cub/thread/thread_scan.cuh
%{_includedir}/%{name}/cub/thread/thread_search.cuh
%{_includedir}/%{name}/cub/thread/thread_store.cuh
%{_includedir}/%{name}/cub/util_allocator.cuh
%{_includedir}/%{name}/cub/util_arch.cuh
%{_includedir}/%{name}/cub/util_compiler.cuh
%{_includedir}/%{name}/cub/util_cpp_dialect.cuh
%{_includedir}/%{name}/cub/util_debug.cuh
%{_includedir}/%{name}/cub/util_deprecated.cuh
%{_includedir}/%{name}/cub/util_device.cuh
%{_includedir}/%{name}/cub/util_macro.cuh
%{_includedir}/%{name}/cub/util_math.cuh
%{_includedir}/%{name}/cub/util_namespace.cuh
%{_includedir}/%{name}/cub/util_ptx.cuh
%{_includedir}/%{name}/cub/util_type.cuh
%{_includedir}/%{name}/cub/version.cuh
%{_includedir}/%{name}/cub/warp/specializations/warp_reduce_shfl.cuh
%{_includedir}/%{name}/cub/warp/specializations/warp_reduce_smem.cuh
%{_includedir}/%{name}/cub/warp/specializations/warp_scan_shfl.cuh
%{_includedir}/%{name}/cub/warp/specializations/warp_scan_smem.cuh
%{_includedir}/%{name}/cub/warp/warp_reduce.cuh
%{_includedir}/%{name}/cub/warp/warp_scan.cuh
%{_includedir}/%{name}/cuComplex.h
%{_includedir}/%{name}/cuda/atomic
%{_includedir}/%{name}/cuda/barrier
%{_includedir}/%{name}/cudaEGL.h
%{_includedir}/%{name}/cuda_egl_interop.h
%{_includedir}/%{name}/cuda_fp16.h
%{_includedir}/%{name}/cuda_fp16.hpp
%{_includedir}/%{name}/cudaGL.h
%{_includedir}/%{name}/cuda_gl_interop.h
%{_includedir}/%{name}/cuda.h
%{_includedir}/%{name}/cuda/latch
%{_includedir}/%{name}/cudalibxt.h
%{_includedir}/%{name}/cuda_occupancy.h
%{_includedir}/%{name}/cuda/pipeline
%{_includedir}/%{name}/cuda_profiler_api.h
%{_includedir}/%{name}/cudaProfiler.h
%{_includedir}/%{name}/cuda/semaphore
%{_includedir}/%{name}/cuda/std/atomic
%{_includedir}/%{name}/cuda/std/barrier
%{_includedir}/%{name}/cuda/std/cassert
%{_includedir}/%{name}/cuda/std/ccomplex
%{_includedir}/%{name}/cuda/std/cfloat
%{_includedir}/%{name}/cuda/std/chrono
%{_includedir}/%{name}/cuda/std/climits
%{_includedir}/%{name}/cuda/std/cmath
%{_includedir}/%{name}/cuda/std/complex
%{_includedir}/%{name}/cuda/std/cstddef
%{_includedir}/%{name}/cuda/std/cstdint
%{_includedir}/%{name}/cuda/std/ctime
%{_includedir}/%{name}/cuda/std/detail/__atomic
%{_includedir}/%{name}/cuda/std/detail/__atomic_derived
%{_includedir}/%{name}/cuda/std/detail/__atomic_generated
%{_includedir}/%{name}/cuda/std/detail/__config
%{_includedir}/%{name}/cuda/std/detail/__functional_base
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/algorithm
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/any
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/array
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/atomic
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/barrier
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/bit
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__bit_reference
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/bitset
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__bsd_locale_defaults.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__bsd_locale_fallbacks.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cassert
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/ccomplex
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cctype
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cerrno
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cfenv
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cfloat
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/charconv
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/chrono
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cinttypes
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/ciso646
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/climits
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/clocale
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/CMakeLists.txt
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cmath
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/codecvt
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/compare
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/complex
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/complex.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/condition_variable
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__config
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__config_site.in
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/csetjmp
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/csignal
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cstdarg
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cstdbool
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cstddef
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cstdint
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cstdio
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cstdlib
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cstring
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/ctgmath
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/ctime
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/ctype.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cwchar
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/cwctype
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__debug
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/deque
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__errc
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/errno.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/exception
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/execution
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/algorithm
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/__config
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/coroutine
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/deque
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/filesystem
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/forward_list
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/functional
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/iterator
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/list
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/map
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/__memory
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/memory_resource
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/propagate_const
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/regex
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/set
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/simd
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/string
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/type_traits
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/unordered_map
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/unordered_set
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/utility
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/experimental/vector
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/ext/__hash
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/ext/hash_map
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/ext/hash_set
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/fenv.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/filesystem
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/float.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/forward_list
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/fstream
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/functional
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__functional_03
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__functional_base
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__functional_base_03
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/future
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__hash_table
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/initializer_list
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/inttypes.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/iomanip
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/ios
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/iosfwd
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/iostream
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/istream
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/iterator
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/latch
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__libcpp_version
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/limits
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/limits.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/list
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__locale
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/locale
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/locale.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/map
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/math.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/memory
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/module.modulemap
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/mutex
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__mutex_base
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/new
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__node_handle
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__nullptr
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/numeric
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/optional
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/ostream
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__pragma_pop
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__pragma_push
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/queue
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/random
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/ratio
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/regex
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/scoped_allocator
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/semaphore
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/set
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/setjmp.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/shared_mutex
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/span
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__split_buffer
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__sso_allocator
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/sstream
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/stack
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/stdbool.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/stddef.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/stdexcept
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/stdint.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/stdio.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/stdlib.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__std_stream
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/streambuf
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__string
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/string
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/string.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/string_view
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/strstream
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/android/locale_bionic.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/fuchsia/xlocale.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/ibm/limits.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/ibm/locale_mgmt_aix.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/ibm/support.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/ibm/xlocale.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/musl/xlocale.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/newlib/xlocale.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/solaris/floatingpoint.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/solaris/wchar.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/solaris/xlocale.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/win32/atomic_msvc.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/win32/limits_msvc_win32.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/win32/locale_win32.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/xlocale/__nop_locale_mgmt.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/xlocale/__posix_l_fallback.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/support/xlocale/__strtonum_fallback.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/system_error
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/tgmath.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/thread
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__threading_support
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__tree
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__tuple
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/tuple
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/typeindex
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/typeinfo
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/type_traits
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/__undef_macros
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/unordered_map
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/unordered_set
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/utility
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/valarray
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/variant
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/vector
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/version
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/wchar.h
%{_includedir}/%{name}/cuda/std/detail/libcxx/include/wctype.h
%{_includedir}/%{name}/cuda/std/detail/__pragma_pop
%{_includedir}/%{name}/cuda/std/detail/__pragma_push
%{_includedir}/%{name}/cuda/std/detail/__threading_support
%{_includedir}/%{name}/cuda/std/functional
%{_includedir}/%{name}/cuda/std/latch
%{_includedir}/%{name}/cuda/std/limits
%{_includedir}/%{name}/cuda/std/ratio
%{_includedir}/%{name}/cuda/std/semaphore
%{_includedir}/%{name}/cuda/std/tuple
%{_includedir}/%{name}/cuda/std/type_traits
%{_includedir}/%{name}/cuda/std/utility
%{_includedir}/%{name}/cuda/std/version
%{_includedir}/%{name}/cuda_surface_types.h
%{_includedir}/%{name}/cuda_texture_types.h
%{_includedir}/%{name}/cudaVDPAU.h
%{_includedir}/%{name}/cuda_vdpau_interop.h
%{_includedir}/%{name}/Debugger
%{_includedir}/%{name}/device_atomic_functions.h
%{_includedir}/%{name}/device_atomic_functions.hpp
%{_includedir}/%{name}/device_double_functions.h
%{_includedir}/%{name}/device_functions.h
%{_includedir}/%{name}/device_launch_parameters.h
%{_includedir}/%{name}/device_types.h
%{_includedir}/%{name}/driver_functions.h
%{_includedir}/%{name}/driver_types.h
%{_includedir}/%{name}/fatbinary_section.h
%{_includedir}/%{name}/host_config.h
%{_includedir}/%{name}/host_defines.h
%{_includedir}/%{name}/library_types.h
%{_includedir}/%{name}/math_constants.h
%{_includedir}/%{name}/math_functions.h
%{_includedir}/%{name}/mma.h
%{_includedir}/%{name}/nv/detail/__preprocessor
%{_includedir}/%{name}/nv/detail/__target_macros
%{_includedir}/%{name}/nvfunctional
%{_includedir}/%{name}/nvPTXCompiler.h
%{_includedir}/%{name}/nv/target
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
%{_includedir}/%{name}/thrust/addressof.h
%{_includedir}/%{name}/thrust/adjacent_difference.h
%{_includedir}/%{name}/thrust/advance.h
%{_includedir}/%{name}/thrust/allocate_unique.h
%{_includedir}/%{name}/thrust/async/copy.h
%{_includedir}/%{name}/thrust/async/for_each.h
%{_includedir}/%{name}/thrust/async/reduce.h
%{_includedir}/%{name}/thrust/async/scan.h
%{_includedir}/%{name}/thrust/async/sort.h
%{_includedir}/%{name}/thrust/async/transform.h
%{_includedir}/%{name}/thrust/binary_search.h
%{_includedir}/%{name}/thrust/cmake/FindTBB.cmake
%{_includedir}/%{name}/thrust/cmake/README.md
%{_includedir}/%{name}/thrust/cmake/thrust-config.cmake
%{_includedir}/%{name}/thrust/cmake/thrust-config-version.cmake
%{_includedir}/%{name}/thrust/complex.h
%{_includedir}/%{name}/thrust/copy.h
%{_includedir}/%{name}/thrust/count.h
%{_includedir}/%{name}/thrust/detail/adjacent_difference.inl
%{_includedir}/%{name}/thrust/detail/advance.inl
%{_includedir}/%{name}/thrust/detail/algorithm_wrapper.h
%{_includedir}/%{name}/thrust/detail/alignment.h
%{_includedir}/%{name}/thrust/detail/allocator/allocator_traits.h
%{_includedir}/%{name}/thrust/detail/allocator/allocator_traits.inl
%{_includedir}/%{name}/thrust/detail/allocator_aware_execution_policy.h
%{_includedir}/%{name}/thrust/detail/allocator/copy_construct_range.h
%{_includedir}/%{name}/thrust/detail/allocator/copy_construct_range.inl
%{_includedir}/%{name}/thrust/detail/allocator/default_construct_range.h
%{_includedir}/%{name}/thrust/detail/allocator/default_construct_range.inl
%{_includedir}/%{name}/thrust/detail/allocator/destroy_range.h
%{_includedir}/%{name}/thrust/detail/allocator/destroy_range.inl
%{_includedir}/%{name}/thrust/detail/allocator/fill_construct_range.h
%{_includedir}/%{name}/thrust/detail/allocator/fill_construct_range.inl
%{_includedir}/%{name}/thrust/detail/allocator/malloc_allocator.h
%{_includedir}/%{name}/thrust/detail/allocator/malloc_allocator.inl
%{_includedir}/%{name}/thrust/detail/allocator/no_throw_allocator.h
%{_includedir}/%{name}/thrust/detail/allocator/tagged_allocator.h
%{_includedir}/%{name}/thrust/detail/allocator/tagged_allocator.inl
%{_includedir}/%{name}/thrust/detail/allocator/temporary_allocator.h
%{_includedir}/%{name}/thrust/detail/allocator/temporary_allocator.inl
%{_includedir}/%{name}/thrust/detail/binary_search.inl
%{_includedir}/%{name}/thrust/detail/caching_allocator.h
%{_includedir}/%{name}/thrust/detail/complex/arithmetic.h
%{_includedir}/%{name}/thrust/detail/complex/c99math.h
%{_includedir}/%{name}/thrust/detail/complex/catrigf.h
%{_includedir}/%{name}/thrust/detail/complex/catrig.h
%{_includedir}/%{name}/thrust/detail/complex/ccoshf.h
%{_includedir}/%{name}/thrust/detail/complex/ccosh.h
%{_includedir}/%{name}/thrust/detail/complex/cexpf.h
%{_includedir}/%{name}/thrust/detail/complex/cexp.h
%{_includedir}/%{name}/thrust/detail/complex/clogf.h
%{_includedir}/%{name}/thrust/detail/complex/clog.h
%{_includedir}/%{name}/thrust/detail/complex/complex.inl
%{_includedir}/%{name}/thrust/detail/complex/cpow.h
%{_includedir}/%{name}/thrust/detail/complex/cproj.h
%{_includedir}/%{name}/thrust/detail/complex/csinhf.h
%{_includedir}/%{name}/thrust/detail/complex/csinh.h
%{_includedir}/%{name}/thrust/detail/complex/csqrtf.h
%{_includedir}/%{name}/thrust/detail/complex/csqrt.h
%{_includedir}/%{name}/thrust/detail/complex/ctanhf.h
%{_includedir}/%{name}/thrust/detail/complex/ctanh.h
%{_includedir}/%{name}/thrust/detail/complex/math_private.h
%{_includedir}/%{name}/thrust/detail/complex/stream.h
%{_includedir}/%{name}/thrust/detail/config/compiler_fence.h
%{_includedir}/%{name}/thrust/detail/config/compiler.h
%{_includedir}/%{name}/thrust/detail/config/config.h
%{_includedir}/%{name}/thrust/detail/config/cpp_compatibility.h
%{_includedir}/%{name}/thrust/detail/config/cpp_dialect.h
%{_includedir}/%{name}/thrust/detail/config/debug.h
%{_includedir}/%{name}/thrust/detail/config/deprecated.h
%{_includedir}/%{name}/thrust/detail/config/device_system.h
%{_includedir}/%{name}/thrust/detail/config/exec_check_disable.h
%{_includedir}/%{name}/thrust/detail/config/forceinline.h
%{_includedir}/%{name}/thrust/detail/config/global_workarounds.h
%{_includedir}/%{name}/thrust/detail/config.h
%{_includedir}/%{name}/thrust/detail/config/host_device.h
%{_includedir}/%{name}/thrust/detail/config/host_system.h
%{_includedir}/%{name}/thrust/detail/config/memory_resource.h
%{_includedir}/%{name}/thrust/detail/config/simple_defines.h
%{_includedir}/%{name}/thrust/detail/contiguous_storage.h
%{_includedir}/%{name}/thrust/detail/contiguous_storage.inl
%{_includedir}/%{name}/thrust/detail/copy.h
%{_includedir}/%{name}/thrust/detail/copy_if.h
%{_includedir}/%{name}/thrust/detail/copy_if.inl
%{_includedir}/%{name}/thrust/detail/copy.inl
%{_includedir}/%{name}/thrust/detail/count.inl
%{_includedir}/%{name}/thrust/detail/cpp11_required.h
%{_includedir}/%{name}/thrust/detail/cpp14_required.h
%{_includedir}/%{name}/thrust/detail/cstdint.h
%{_includedir}/%{name}/thrust/detail/dependencies_aware_execution_policy.h
%{_includedir}/%{name}/thrust/detail/device_delete.inl
%{_includedir}/%{name}/thrust/detail/device_free.inl
%{_includedir}/%{name}/thrust/detail/device_malloc.inl
%{_includedir}/%{name}/thrust/detail/device_new.inl
%{_includedir}/%{name}/thrust/detail/device_ptr.inl
%{_includedir}/%{name}/thrust/detail/distance.inl
%{_includedir}/%{name}/thrust/detail/equal.inl
%{_includedir}/%{name}/thrust/detail/event_error.h
%{_includedir}/%{name}/thrust/detail/execute_with_allocator_fwd.h
%{_includedir}/%{name}/thrust/detail/execute_with_allocator.h
%{_includedir}/%{name}/thrust/detail/execute_with_dependencies.h
%{_includedir}/%{name}/thrust/detail/execution_policy.h
%{_includedir}/%{name}/thrust/detail/extrema.inl
%{_includedir}/%{name}/thrust/detail/fill.inl
%{_includedir}/%{name}/thrust/detail/find.inl
%{_includedir}/%{name}/thrust/detail/for_each.inl
%{_includedir}/%{name}/thrust/detail/functional/actor.h
%{_includedir}/%{name}/thrust/detail/functional/actor.inl
%{_includedir}/%{name}/thrust/detail/functional/argument.h
%{_includedir}/%{name}/thrust/detail/functional/composite.h
%{_includedir}/%{name}/thrust/detail/functional.inl
%{_includedir}/%{name}/thrust/detail/functional/operators/arithmetic_operators.h
%{_includedir}/%{name}/thrust/detail/functional/operators/assignment_operator.h
%{_includedir}/%{name}/thrust/detail/functional/operators/bitwise_operators.h
%{_includedir}/%{name}/thrust/detail/functional/operators/compound_assignment_operators.h
%{_includedir}/%{name}/thrust/detail/functional/operators.h
%{_includedir}/%{name}/thrust/detail/functional/operators/logical_operators.h
%{_includedir}/%{name}/thrust/detail/functional/operators/operator_adaptors.h
%{_includedir}/%{name}/thrust/detail/functional/operators/relational_operators.h
%{_includedir}/%{name}/thrust/detail/functional/placeholder.h
%{_includedir}/%{name}/thrust/detail/functional/value.h
%{_includedir}/%{name}/thrust/detail/function.h
%{_includedir}/%{name}/thrust/detail/gather.inl
%{_includedir}/%{name}/thrust/detail/generate.inl
%{_includedir}/%{name}/thrust/detail/get_iterator_value.h
%{_includedir}/%{name}/thrust/detail/inner_product.inl
%{_includedir}/%{name}/thrust/detail/integer_math.h
%{_includedir}/%{name}/thrust/detail/integer_traits.h
%{_includedir}/%{name}/thrust/detail/internal_functional.h
%{_includedir}/%{name}/thrust/detail/logical.inl
%{_includedir}/%{name}/thrust/detail/malloc_and_free.h
%{_includedir}/%{name}/thrust/detail/memory_algorithms.h
%{_includedir}/%{name}/thrust/detail/memory_wrapper.h
%{_includedir}/%{name}/thrust/detail/merge.inl
%{_includedir}/%{name}/thrust/detail/minmax.h
%{_includedir}/%{name}/thrust/detail/mismatch.inl
%{_includedir}/%{name}/thrust/detail/modern_gcc_required.h
%{_includedir}/%{name}/thrust/detail/mpl/math.h
%{_includedir}/%{name}/thrust/detail/numeric_traits.h
%{_includedir}/%{name}/thrust/detail/overlapped_copy.h
%{_includedir}/%{name}/thrust/detail/pair.inl
%{_includedir}/%{name}/thrust/detail/partition.inl
%{_includedir}/%{name}/thrust/detail/pointer.h
%{_includedir}/%{name}/thrust/detail/pointer.inl
%{_includedir}/%{name}/thrust/detail/preprocessor.h
%{_includedir}/%{name}/thrust/detail/range/head_flags.h
%{_includedir}/%{name}/thrust/detail/range/tail_flags.h
%{_includedir}/%{name}/thrust/detail/raw_pointer_cast.h
%{_includedir}/%{name}/thrust/detail/raw_reference_cast.h
%{_includedir}/%{name}/thrust/detail/reduce.inl
%{_includedir}/%{name}/thrust/detail/reference_forward_declaration.h
%{_includedir}/%{name}/thrust/detail/reference.h
%{_includedir}/%{name}/thrust/detail/remove.inl
%{_includedir}/%{name}/thrust/detail/replace.inl
%{_includedir}/%{name}/thrust/detail/reverse.inl
%{_includedir}/%{name}/thrust/detail/scan.inl
%{_includedir}/%{name}/thrust/detail/scatter.inl
%{_includedir}/%{name}/thrust/detail/select_system.h
%{_includedir}/%{name}/thrust/detail/seq.h
%{_includedir}/%{name}/thrust/detail/sequence.inl
%{_includedir}/%{name}/thrust/detail/set_operations.inl
%{_includedir}/%{name}/thrust/detail/shuffle.inl
%{_includedir}/%{name}/thrust/detail/sort.inl
%{_includedir}/%{name}/thrust/detail/static_assert.h
%{_includedir}/%{name}/thrust/detail/static_map.h
%{_includedir}/%{name}/thrust/detail/swap.h
%{_includedir}/%{name}/thrust/detail/swap.inl
%{_includedir}/%{name}/thrust/detail/swap_ranges.inl
%{_includedir}/%{name}/thrust/detail/tabulate.inl
%{_includedir}/%{name}/thrust/detail/temporary_array.h
%{_includedir}/%{name}/thrust/detail/temporary_array.inl
%{_includedir}/%{name}/thrust/detail/temporary_buffer.h
%{_includedir}/%{name}/thrust/detail/transform.inl
%{_includedir}/%{name}/thrust/detail/transform_reduce.inl
%{_includedir}/%{name}/thrust/detail/transform_scan.inl
%{_includedir}/%{name}/thrust/detail/trivial_sequence.h
%{_includedir}/%{name}/thrust/detail/tuple_algorithms.h
%{_includedir}/%{name}/thrust/detail/tuple.inl
%{_includedir}/%{name}/thrust/detail/tuple_meta_transform.h
%{_includedir}/%{name}/thrust/detail/tuple_transform.h
%{_includedir}/%{name}/thrust/detail/type_deduction.h
%{_includedir}/%{name}/thrust/detail/type_traits/function_traits.h
%{_includedir}/%{name}/thrust/detail/type_traits.h
%{_includedir}/%{name}/thrust/detail/type_traits/has_member_function.h
%{_includedir}/%{name}/thrust/detail/type_traits/has_nested_type.h
%{_includedir}/%{name}/thrust/detail/type_traits/has_trivial_assign.h
%{_includedir}/%{name}/thrust/detail/type_traits/is_call_possible.h
%{_includedir}/%{name}/thrust/detail/type_traits/is_metafunction_defined.h
%{_includedir}/%{name}/thrust/detail/type_traits/iterator/is_discard_iterator.h
%{_includedir}/%{name}/thrust/detail/type_traits/iterator/is_output_iterator.h
%{_includedir}/%{name}/thrust/detail/type_traits/minimum_type.h
%{_includedir}/%{name}/thrust/detail/type_traits/pointer_traits.h
%{_includedir}/%{name}/thrust/detail/type_traits/result_of_adaptable_function.h
%{_includedir}/%{name}/thrust/detail/uninitialized_copy.inl
%{_includedir}/%{name}/thrust/detail/uninitialized_fill.inl
%{_includedir}/%{name}/thrust/detail/unique.inl
%{_includedir}/%{name}/thrust/detail/use_default.h
%{_includedir}/%{name}/thrust/detail/util/align.h
%{_includedir}/%{name}/thrust/detail/vector_base.h
%{_includedir}/%{name}/thrust/detail/vector_base.inl
%{_includedir}/%{name}/thrust/device_allocator.h
%{_includedir}/%{name}/thrust/device_delete.h
%{_includedir}/%{name}/thrust/device_free.h
%{_includedir}/%{name}/thrust/device_make_unique.h
%{_includedir}/%{name}/thrust/device_malloc_allocator.h
%{_includedir}/%{name}/thrust/device_malloc.h
%{_includedir}/%{name}/thrust/device_new_allocator.h
%{_includedir}/%{name}/thrust/device_new.h
%{_includedir}/%{name}/thrust/device_ptr.h
%{_includedir}/%{name}/thrust/device_reference.h
%{_includedir}/%{name}/thrust/device_vector.h
%{_includedir}/%{name}/thrust/distance.h
%{_includedir}/%{name}/thrust/equal.h
%{_includedir}/%{name}/thrust/event.h
%{_includedir}/%{name}/thrust/execution_policy.h
%{_includedir}/%{name}/thrust/extrema.h
%{_includedir}/%{name}/thrust/fill.h
%{_includedir}/%{name}/thrust/find.h
%{_includedir}/%{name}/thrust/for_each.h
%{_includedir}/%{name}/thrust/functional.h
%{_includedir}/%{name}/thrust/future.h
%{_includedir}/%{name}/thrust/gather.h
%{_includedir}/%{name}/thrust/generate.h
%{_includedir}/%{name}/thrust/host_vector.h
%{_includedir}/%{name}/thrust/inner_product.h
%{_includedir}/%{name}/thrust/iterator/constant_iterator.h
%{_includedir}/%{name}/thrust/iterator/counting_iterator.h
%{_includedir}/%{name}/thrust/iterator/detail/any_assign.h
%{_includedir}/%{name}/thrust/iterator/detail/any_system_tag.h
%{_includedir}/%{name}/thrust/iterator/detail/constant_iterator_base.h
%{_includedir}/%{name}/thrust/iterator/detail/counting_iterator.inl
%{_includedir}/%{name}/thrust/iterator/detail/device_system_tag.h
%{_includedir}/%{name}/thrust/iterator/detail/discard_iterator_base.h
%{_includedir}/%{name}/thrust/iterator/detail/distance_from_result.h
%{_includedir}/%{name}/thrust/iterator/detail/host_system_tag.h
%{_includedir}/%{name}/thrust/iterator/detail/is_iterator_category.h
%{_includedir}/%{name}/thrust/iterator/detail/iterator_adaptor_base.h
%{_includedir}/%{name}/thrust/iterator/detail/iterator_category_to_system.h
%{_includedir}/%{name}/thrust/iterator/detail/iterator_category_to_traversal.h
%{_includedir}/%{name}/thrust/iterator/detail/iterator_category_with_system_and_traversal.h
%{_includedir}/%{name}/thrust/iterator/detail/iterator_facade_category.h
%{_includedir}/%{name}/thrust/iterator/detail/iterator_traits.inl
%{_includedir}/%{name}/thrust/iterator/detail/iterator_traversal_tags.h
%{_includedir}/%{name}/thrust/iterator/detail/join_iterator.h
%{_includedir}/%{name}/thrust/iterator/detail/minimum_category.h
%{_includedir}/%{name}/thrust/iterator/detail/minimum_system.h
%{_includedir}/%{name}/thrust/iterator/detail/normal_iterator.h
%{_includedir}/%{name}/thrust/iterator/detail/permutation_iterator_base.h
%{_includedir}/%{name}/thrust/iterator/detail/retag.h
%{_includedir}/%{name}/thrust/iterator/detail/reverse_iterator_base.h
%{_includedir}/%{name}/thrust/iterator/detail/reverse_iterator.inl
%{_includedir}/%{name}/thrust/iterator/detail/tagged_iterator.h
%{_includedir}/%{name}/thrust/iterator/detail/transform_input_output_iterator.inl
%{_includedir}/%{name}/thrust/iterator/detail/transform_iterator.inl
%{_includedir}/%{name}/thrust/iterator/detail/transform_output_iterator.inl
%{_includedir}/%{name}/thrust/iterator/detail/tuple_of_iterator_references.h
%{_includedir}/%{name}/thrust/iterator/detail/universal_categories.h
%{_includedir}/%{name}/thrust/iterator/detail/zip_iterator_base.h
%{_includedir}/%{name}/thrust/iterator/detail/zip_iterator.inl
%{_includedir}/%{name}/thrust/iterator/discard_iterator.h
%{_includedir}/%{name}/thrust/iterator/iterator_adaptor.h
%{_includedir}/%{name}/thrust/iterator/iterator_categories.h
%{_includedir}/%{name}/thrust/iterator/iterator_facade.h
%{_includedir}/%{name}/thrust/iterator/iterator_traits.h
%{_includedir}/%{name}/thrust/iterator/permutation_iterator.h
%{_includedir}/%{name}/thrust/iterator/retag.h
%{_includedir}/%{name}/thrust/iterator/reverse_iterator.h
%{_includedir}/%{name}/thrust/iterator/transform_input_output_iterator.h
%{_includedir}/%{name}/thrust/iterator/transform_iterator.h
%{_includedir}/%{name}/thrust/iterator/transform_output_iterator.h
%{_includedir}/%{name}/thrust/iterator/zip_iterator.h
%{_includedir}/%{name}/thrust/limits.h
%{_includedir}/%{name}/thrust/logical.h
%{_includedir}/%{name}/thrust/memory.h
%{_includedir}/%{name}/thrust/merge.h
%{_includedir}/%{name}/thrust/mismatch.h
%{_includedir}/%{name}/thrust/mr/allocator.h
%{_includedir}/%{name}/thrust/mr/device_memory_resource.h
%{_includedir}/%{name}/thrust/mr/disjoint_pool.h
%{_includedir}/%{name}/thrust/mr/disjoint_sync_pool.h
%{_includedir}/%{name}/thrust/mr/disjoint_tls_pool.h
%{_includedir}/%{name}/thrust/mr/fancy_pointer_resource.h
%{_includedir}/%{name}/thrust/mr/host_memory_resource.h
%{_includedir}/%{name}/thrust/mr/memory_resource.h
%{_includedir}/%{name}/thrust/mr/new.h
%{_includedir}/%{name}/thrust/mr/polymorphic_adaptor.h
%{_includedir}/%{name}/thrust/mr/pool.h
%{_includedir}/%{name}/thrust/mr/pool_options.h
%{_includedir}/%{name}/thrust/mr/sync_pool.h
%{_includedir}/%{name}/thrust/mr/tls_pool.h
%{_includedir}/%{name}/thrust/mr/universal_memory_resource.h
%{_includedir}/%{name}/thrust/mr/validator.h
%{_includedir}/%{name}/thrust/optional.h
%{_includedir}/%{name}/thrust/pair.h
%{_includedir}/%{name}/thrust/partition.h
%{_includedir}/%{name}/thrust/per_device_resource.h
%{_includedir}/%{name}/thrust/random/detail/discard_block_engine.inl
%{_includedir}/%{name}/thrust/random/detail/linear_congruential_engine_discard.h
%{_includedir}/%{name}/thrust/random/detail/linear_congruential_engine.inl
%{_includedir}/%{name}/thrust/random/detail/linear_feedback_shift_engine.inl
%{_includedir}/%{name}/thrust/random/detail/linear_feedback_shift_engine_wordmask.h
%{_includedir}/%{name}/thrust/random/detail/mod.h
%{_includedir}/%{name}/thrust/random/detail/normal_distribution_base.h
%{_includedir}/%{name}/thrust/random/detail/normal_distribution.inl
%{_includedir}/%{name}/thrust/random/detail/random_core_access.h
%{_includedir}/%{name}/thrust/random/detail/subtract_with_carry_engine.inl
%{_includedir}/%{name}/thrust/random/detail/uniform_int_distribution.inl
%{_includedir}/%{name}/thrust/random/detail/uniform_real_distribution.inl
%{_includedir}/%{name}/thrust/random/detail/xor_combine_engine.inl
%{_includedir}/%{name}/thrust/random/detail/xor_combine_engine_max.h
%{_includedir}/%{name}/thrust/random/discard_block_engine.h
%{_includedir}/%{name}/thrust/random.h
%{_includedir}/%{name}/thrust/random/linear_congruential_engine.h
%{_includedir}/%{name}/thrust/random/linear_feedback_shift_engine.h
%{_includedir}/%{name}/thrust/random/normal_distribution.h
%{_includedir}/%{name}/thrust/random/subtract_with_carry_engine.h
%{_includedir}/%{name}/thrust/random/uniform_int_distribution.h
%{_includedir}/%{name}/thrust/random/uniform_real_distribution.h
%{_includedir}/%{name}/thrust/random/xor_combine_engine.h
%{_includedir}/%{name}/thrust/reduce.h
%{_includedir}/%{name}/thrust/remove.h
%{_includedir}/%{name}/thrust/replace.h
%{_includedir}/%{name}/thrust/reverse.h
%{_includedir}/%{name}/thrust/scan.h
%{_includedir}/%{name}/thrust/scatter.h
%{_includedir}/%{name}/thrust/sequence.h
%{_includedir}/%{name}/thrust/set_operations.h
%{_includedir}/%{name}/thrust/shuffle.h
%{_includedir}/%{name}/thrust/sort.h
%{_includedir}/%{name}/thrust/swap.h
%{_includedir}/%{name}/thrust/system/cpp/detail/adjacent_difference.h
%{_includedir}/%{name}/thrust/system/cpp/detail/assign_value.h
%{_includedir}/%{name}/thrust/system/cpp/detail/binary_search.h
%{_includedir}/%{name}/thrust/system/cpp/detail/copy.h
%{_includedir}/%{name}/thrust/system/cpp/detail/copy_if.h
%{_includedir}/%{name}/thrust/system/cpp/detail/count.h
%{_includedir}/%{name}/thrust/system/cpp/detail/equal.h
%{_includedir}/%{name}/thrust/system/cpp/detail/execution_policy.h
%{_includedir}/%{name}/thrust/system/cpp/detail/extrema.h
%{_includedir}/%{name}/thrust/system/cpp/detail/fill.h
%{_includedir}/%{name}/thrust/system/cpp/detail/find.h
%{_includedir}/%{name}/thrust/system/cpp/detail/for_each.h
%{_includedir}/%{name}/thrust/system/cpp/detail/gather.h
%{_includedir}/%{name}/thrust/system/cpp/detail/generate.h
%{_includedir}/%{name}/thrust/system/cpp/detail/get_value.h
%{_includedir}/%{name}/thrust/system/cpp/detail/inner_product.h
%{_includedir}/%{name}/thrust/system/cpp/detail/iter_swap.h
%{_includedir}/%{name}/thrust/system/cpp/detail/logical.h
%{_includedir}/%{name}/thrust/system/cpp/detail/malloc_and_free.h
%{_includedir}/%{name}/thrust/system/cpp/detail/memory.inl
%{_includedir}/%{name}/thrust/system/cpp/detail/merge.h
%{_includedir}/%{name}/thrust/system/cpp/detail/mismatch.h
%{_includedir}/%{name}/thrust/system/cpp/detail/par.h
%{_includedir}/%{name}/thrust/system/cpp/detail/partition.h
%{_includedir}/%{name}/thrust/system/cpp/detail/per_device_resource.h
%{_includedir}/%{name}/thrust/system/cpp/detail/reduce_by_key.h
%{_includedir}/%{name}/thrust/system/cpp/detail/reduce.h
%{_includedir}/%{name}/thrust/system/cpp/detail/remove.h
%{_includedir}/%{name}/thrust/system/cpp/detail/replace.h
%{_includedir}/%{name}/thrust/system/cpp/detail/reverse.h
%{_includedir}/%{name}/thrust/system/cpp/detail/scan_by_key.h
%{_includedir}/%{name}/thrust/system/cpp/detail/scan.h
%{_includedir}/%{name}/thrust/system/cpp/detail/scatter.h
%{_includedir}/%{name}/thrust/system/cpp/detail/sequence.h
%{_includedir}/%{name}/thrust/system/cpp/detail/set_operations.h
%{_includedir}/%{name}/thrust/system/cpp/detail/sort.h
%{_includedir}/%{name}/thrust/system/cpp/detail/swap_ranges.h
%{_includedir}/%{name}/thrust/system/cpp/detail/tabulate.h
%{_includedir}/%{name}/thrust/system/cpp/detail/temporary_buffer.h
%{_includedir}/%{name}/thrust/system/cpp/detail/transform.h
%{_includedir}/%{name}/thrust/system/cpp/detail/transform_reduce.h
%{_includedir}/%{name}/thrust/system/cpp/detail/transform_scan.h
%{_includedir}/%{name}/thrust/system/cpp/detail/uninitialized_copy.h
%{_includedir}/%{name}/thrust/system/cpp/detail/uninitialized_fill.h
%{_includedir}/%{name}/thrust/system/cpp/detail/unique_by_key.h
%{_includedir}/%{name}/thrust/system/cpp/detail/unique.h
%{_includedir}/%{name}/thrust/system/cpp/detail/vector.inl
%{_includedir}/%{name}/thrust/system/cpp/execution_policy.h
%{_includedir}/%{name}/thrust/system/cpp/memory.h
%{_includedir}/%{name}/thrust/system/cpp/memory_resource.h
%{_includedir}/%{name}/thrust/system/cpp/pointer.h
%{_includedir}/%{name}/thrust/system/cpp/vector.h
%{_includedir}/%{name}/thrust/system/cuda/config.h
%{_includedir}/%{name}/thrust/system/cuda/detail/adjacent_difference.h
%{_includedir}/%{name}/thrust/system/cuda/detail/assign_value.h
%{_includedir}/%{name}/thrust/system/cuda/detail/async/copy.h
%{_includedir}/%{name}/thrust/system/cuda/detail/async/customization.h
%{_includedir}/%{name}/thrust/system/cuda/detail/async/exclusive_scan.h
%{_includedir}/%{name}/thrust/system/cuda/detail/async/for_each.h
%{_includedir}/%{name}/thrust/system/cuda/detail/async/inclusive_scan.h
%{_includedir}/%{name}/thrust/system/cuda/detail/async/reduce.h
%{_includedir}/%{name}/thrust/system/cuda/detail/async/scan.h
%{_includedir}/%{name}/thrust/system/cuda/detail/async/sort.h
%{_includedir}/%{name}/thrust/system/cuda/detail/async/transform.h
%{_includedir}/%{name}/thrust/system/cuda/detail/binary_search.h
%{_includedir}/%{name}/thrust/system/cuda/detail/copy.h
%{_includedir}/%{name}/thrust/system/cuda/detail/copy_if.h
%{_includedir}/%{name}/thrust/system/cuda/detail/core/agent_launcher.h
%{_includedir}/%{name}/thrust/system/cuda/detail/core/alignment.h
%{_includedir}/%{name}/thrust/system/cuda/detail/core/triple_chevron_launch.h
%{_includedir}/%{name}/thrust/system/cuda/detail/core/util.h
%{_includedir}/%{name}/thrust/system/cuda/detail/count.h
%{_includedir}/%{name}/thrust/system/cuda/detail/cross_system.h
%{_includedir}/%{name}/thrust/system/cuda/detail/dispatch.h
%{_includedir}/%{name}/thrust/system/cuda/detail/equal.h
%{_includedir}/%{name}/thrust/system/cuda/detail/error.inl
%{_includedir}/%{name}/thrust/system/cuda/detail/execution_policy.h
%{_includedir}/%{name}/thrust/system/cuda/detail/extrema.h
%{_includedir}/%{name}/thrust/system/cuda/detail/fill.h
%{_includedir}/%{name}/thrust/system/cuda/detail/find.h
%{_includedir}/%{name}/thrust/system/cuda/detail/for_each.h
%{_includedir}/%{name}/thrust/system/cuda/detail/future.inl
%{_includedir}/%{name}/thrust/system/cuda/detail/gather.h
%{_includedir}/%{name}/thrust/system/cuda/detail/generate.h
%{_includedir}/%{name}/thrust/system/cuda/detail/get_value.h
%{_includedir}/%{name}/thrust/system/cuda/detail/guarded_cuda_runtime_api.h
%{_includedir}/%{name}/thrust/system/cuda/detail/guarded_driver_types.h
%{_includedir}/%{name}/thrust/system/cuda/detail/inner_product.h
%{_includedir}/%{name}/thrust/system/cuda/detail/internal/copy_cross_system.h
%{_includedir}/%{name}/thrust/system/cuda/detail/internal/copy_device_to_device.h
%{_includedir}/%{name}/thrust/system/cuda/detail/iter_swap.h
%{_includedir}/%{name}/thrust/system/cuda/detail/logical.h
%{_includedir}/%{name}/thrust/system/cuda/detail/make_unsigned_special.h
%{_includedir}/%{name}/thrust/system/cuda/detail/malloc_and_free.h
%{_includedir}/%{name}/thrust/system/cuda/detail/memory.inl
%{_includedir}/%{name}/thrust/system/cuda/detail/merge.h
%{_includedir}/%{name}/thrust/system/cuda/detail/mismatch.h
%{_includedir}/%{name}/thrust/system/cuda/detail/parallel_for.h
%{_includedir}/%{name}/thrust/system/cuda/detail/par.h
%{_includedir}/%{name}/thrust/system/cuda/detail/partition.h
%{_includedir}/%{name}/thrust/system/cuda/detail/par_to_seq.h
%{_includedir}/%{name}/thrust/system/cuda/detail/per_device_resource.h
%{_includedir}/%{name}/thrust/system/cuda/detail/reduce_by_key.h
%{_includedir}/%{name}/thrust/system/cuda/detail/reduce.h
%{_includedir}/%{name}/thrust/system/cuda/detail/remove.h
%{_includedir}/%{name}/thrust/system/cuda/detail/replace.h
%{_includedir}/%{name}/thrust/system/cuda/detail/reverse.h
%{_includedir}/%{name}/thrust/system/cuda/detail/scan_by_key.h
%{_includedir}/%{name}/thrust/system/cuda/detail/scan.h
%{_includedir}/%{name}/thrust/system/cuda/detail/scatter.h
%{_includedir}/%{name}/thrust/system/cuda/detail/sequence.h
%{_includedir}/%{name}/thrust/system/cuda/detail/set_operations.h
%{_includedir}/%{name}/thrust/system/cuda/detail/sort.h
%{_includedir}/%{name}/thrust/system/cuda/detail/swap_ranges.h
%{_includedir}/%{name}/thrust/system/cuda/detail/tabulate.h
%{_includedir}/%{name}/thrust/system/cuda/detail/temporary_buffer.h
%{_includedir}/%{name}/thrust/system/cuda/detail/terminate.h
%{_includedir}/%{name}/thrust/system/cuda/detail/transform.h
%{_includedir}/%{name}/thrust/system/cuda/detail/transform_reduce.h
%{_includedir}/%{name}/thrust/system/cuda/detail/transform_scan.h
%{_includedir}/%{name}/thrust/system/cuda/detail/uninitialized_copy.h
%{_includedir}/%{name}/thrust/system/cuda/detail/uninitialized_fill.h
%{_includedir}/%{name}/thrust/system/cuda/detail/unique_by_key.h
%{_includedir}/%{name}/thrust/system/cuda/detail/unique.h
%{_includedir}/%{name}/thrust/system/cuda/detail/util.h
%{_includedir}/%{name}/thrust/system/cuda/error.h
%{_includedir}/%{name}/thrust/system/cuda/execution_policy.h
%{_includedir}/%{name}/thrust/system/cuda/experimental/pinned_allocator.h
%{_includedir}/%{name}/thrust/system/cuda/future.h
%{_includedir}/%{name}/thrust/system/cuda/memory.h
%{_includedir}/%{name}/thrust/system/cuda/memory_resource.h
%{_includedir}/%{name}/thrust/system/cuda/pointer.h
%{_includedir}/%{name}/thrust/system/cuda/vector.h
%{_includedir}/%{name}/thrust/system/detail/adl/adjacent_difference.h
%{_includedir}/%{name}/thrust/system/detail/adl/assign_value.h
%{_includedir}/%{name}/thrust/system/detail/adl/async/copy.h
%{_includedir}/%{name}/thrust/system/detail/adl/async/for_each.h
%{_includedir}/%{name}/thrust/system/detail/adl/async/reduce.h
%{_includedir}/%{name}/thrust/system/detail/adl/async/scan.h
%{_includedir}/%{name}/thrust/system/detail/adl/async/sort.h
%{_includedir}/%{name}/thrust/system/detail/adl/async/transform.h
%{_includedir}/%{name}/thrust/system/detail/adl/binary_search.h
%{_includedir}/%{name}/thrust/system/detail/adl/copy.h
%{_includedir}/%{name}/thrust/system/detail/adl/copy_if.h
%{_includedir}/%{name}/thrust/system/detail/adl/count.h
%{_includedir}/%{name}/thrust/system/detail/adl/equal.h
%{_includedir}/%{name}/thrust/system/detail/adl/extrema.h
%{_includedir}/%{name}/thrust/system/detail/adl/fill.h
%{_includedir}/%{name}/thrust/system/detail/adl/find.h
%{_includedir}/%{name}/thrust/system/detail/adl/for_each.h
%{_includedir}/%{name}/thrust/system/detail/adl/gather.h
%{_includedir}/%{name}/thrust/system/detail/adl/generate.h
%{_includedir}/%{name}/thrust/system/detail/adl/get_value.h
%{_includedir}/%{name}/thrust/system/detail/adl/inner_product.h
%{_includedir}/%{name}/thrust/system/detail/adl/iter_swap.h
%{_includedir}/%{name}/thrust/system/detail/adl/logical.h
%{_includedir}/%{name}/thrust/system/detail/adl/malloc_and_free.h
%{_includedir}/%{name}/thrust/system/detail/adl/merge.h
%{_includedir}/%{name}/thrust/system/detail/adl/mismatch.h
%{_includedir}/%{name}/thrust/system/detail/adl/partition.h
%{_includedir}/%{name}/thrust/system/detail/adl/per_device_resource.h
%{_includedir}/%{name}/thrust/system/detail/adl/reduce_by_key.h
%{_includedir}/%{name}/thrust/system/detail/adl/reduce.h
%{_includedir}/%{name}/thrust/system/detail/adl/remove.h
%{_includedir}/%{name}/thrust/system/detail/adl/replace.h
%{_includedir}/%{name}/thrust/system/detail/adl/reverse.h
%{_includedir}/%{name}/thrust/system/detail/adl/scan_by_key.h
%{_includedir}/%{name}/thrust/system/detail/adl/scan.h
%{_includedir}/%{name}/thrust/system/detail/adl/scatter.h
%{_includedir}/%{name}/thrust/system/detail/adl/sequence.h
%{_includedir}/%{name}/thrust/system/detail/adl/set_operations.h
%{_includedir}/%{name}/thrust/system/detail/adl/sort.h
%{_includedir}/%{name}/thrust/system/detail/adl/swap_ranges.h
%{_includedir}/%{name}/thrust/system/detail/adl/tabulate.h
%{_includedir}/%{name}/thrust/system/detail/adl/temporary_buffer.h
%{_includedir}/%{name}/thrust/system/detail/adl/transform.h
%{_includedir}/%{name}/thrust/system/detail/adl/transform_reduce.h
%{_includedir}/%{name}/thrust/system/detail/adl/transform_scan.h
%{_includedir}/%{name}/thrust/system/detail/adl/uninitialized_copy.h
%{_includedir}/%{name}/thrust/system/detail/adl/uninitialized_fill.h
%{_includedir}/%{name}/thrust/system/detail/adl/unique_by_key.h
%{_includedir}/%{name}/thrust/system/detail/adl/unique.h
%{_includedir}/%{name}/thrust/system/detail/bad_alloc.h
%{_includedir}/%{name}/thrust/system/detail/errno.h
%{_includedir}/%{name}/thrust/system/detail/error_category.inl
%{_includedir}/%{name}/thrust/system/detail/error_code.inl
%{_includedir}/%{name}/thrust/system/detail/error_condition.inl
%{_includedir}/%{name}/thrust/system/detail/generic/adjacent_difference.h
%{_includedir}/%{name}/thrust/system/detail/generic/adjacent_difference.inl
%{_includedir}/%{name}/thrust/system/detail/generic/advance.h
%{_includedir}/%{name}/thrust/system/detail/generic/advance.inl
%{_includedir}/%{name}/thrust/system/detail/generic/binary_search.h
%{_includedir}/%{name}/thrust/system/detail/generic/binary_search.inl
%{_includedir}/%{name}/thrust/system/detail/generic/copy.h
%{_includedir}/%{name}/thrust/system/detail/generic/copy_if.h
%{_includedir}/%{name}/thrust/system/detail/generic/copy_if.inl
%{_includedir}/%{name}/thrust/system/detail/generic/copy.inl
%{_includedir}/%{name}/thrust/system/detail/generic/count.h
%{_includedir}/%{name}/thrust/system/detail/generic/count.inl
%{_includedir}/%{name}/thrust/system/detail/generic/distance.h
%{_includedir}/%{name}/thrust/system/detail/generic/distance.inl
%{_includedir}/%{name}/thrust/system/detail/generic/equal.h
%{_includedir}/%{name}/thrust/system/detail/generic/equal.inl
%{_includedir}/%{name}/thrust/system/detail/generic/extrema.h
%{_includedir}/%{name}/thrust/system/detail/generic/extrema.inl
%{_includedir}/%{name}/thrust/system/detail/generic/fill.h
%{_includedir}/%{name}/thrust/system/detail/generic/find.h
%{_includedir}/%{name}/thrust/system/detail/generic/find.inl
%{_includedir}/%{name}/thrust/system/detail/generic/for_each.h
%{_includedir}/%{name}/thrust/system/detail/generic/gather.h
%{_includedir}/%{name}/thrust/system/detail/generic/gather.inl
%{_includedir}/%{name}/thrust/system/detail/generic/generate.h
%{_includedir}/%{name}/thrust/system/detail/generic/generate.inl
%{_includedir}/%{name}/thrust/system/detail/generic/inner_product.h
%{_includedir}/%{name}/thrust/system/detail/generic/inner_product.inl
%{_includedir}/%{name}/thrust/system/detail/generic/logical.h
%{_includedir}/%{name}/thrust/system/detail/generic/memory.h
%{_includedir}/%{name}/thrust/system/detail/generic/memory.inl
%{_includedir}/%{name}/thrust/system/detail/generic/merge.h
%{_includedir}/%{name}/thrust/system/detail/generic/merge.inl
%{_includedir}/%{name}/thrust/system/detail/generic/mismatch.h
%{_includedir}/%{name}/thrust/system/detail/generic/mismatch.inl
%{_includedir}/%{name}/thrust/system/detail/generic/partition.h
%{_includedir}/%{name}/thrust/system/detail/generic/partition.inl
%{_includedir}/%{name}/thrust/system/detail/generic/per_device_resource.h
%{_includedir}/%{name}/thrust/system/detail/generic/reduce_by_key.h
%{_includedir}/%{name}/thrust/system/detail/generic/reduce_by_key.inl
%{_includedir}/%{name}/thrust/system/detail/generic/reduce.h
%{_includedir}/%{name}/thrust/system/detail/generic/reduce.inl
%{_includedir}/%{name}/thrust/system/detail/generic/remove.h
%{_includedir}/%{name}/thrust/system/detail/generic/remove.inl
%{_includedir}/%{name}/thrust/system/detail/generic/replace.h
%{_includedir}/%{name}/thrust/system/detail/generic/replace.inl
%{_includedir}/%{name}/thrust/system/detail/generic/reverse.h
%{_includedir}/%{name}/thrust/system/detail/generic/reverse.inl
%{_includedir}/%{name}/thrust/system/detail/generic/scalar/binary_search.h
%{_includedir}/%{name}/thrust/system/detail/generic/scalar/binary_search.inl
%{_includedir}/%{name}/thrust/system/detail/generic/scan_by_key.h
%{_includedir}/%{name}/thrust/system/detail/generic/scan_by_key.inl
%{_includedir}/%{name}/thrust/system/detail/generic/scan.h
%{_includedir}/%{name}/thrust/system/detail/generic/scan.inl
%{_includedir}/%{name}/thrust/system/detail/generic/scatter.h
%{_includedir}/%{name}/thrust/system/detail/generic/scatter.inl
%{_includedir}/%{name}/thrust/system/detail/generic/select_system_exists.h
%{_includedir}/%{name}/thrust/system/detail/generic/select_system.h
%{_includedir}/%{name}/thrust/system/detail/generic/select_system.inl
%{_includedir}/%{name}/thrust/system/detail/generic/sequence.h
%{_includedir}/%{name}/thrust/system/detail/generic/sequence.inl
%{_includedir}/%{name}/thrust/system/detail/generic/set_operations.h
%{_includedir}/%{name}/thrust/system/detail/generic/set_operations.inl
%{_includedir}/%{name}/thrust/system/detail/generic/shuffle.h
%{_includedir}/%{name}/thrust/system/detail/generic/shuffle.inl
%{_includedir}/%{name}/thrust/system/detail/generic/sort.h
%{_includedir}/%{name}/thrust/system/detail/generic/sort.inl
%{_includedir}/%{name}/thrust/system/detail/generic/swap_ranges.h
%{_includedir}/%{name}/thrust/system/detail/generic/swap_ranges.inl
%{_includedir}/%{name}/thrust/system/detail/generic/tabulate.h
%{_includedir}/%{name}/thrust/system/detail/generic/tabulate.inl
%{_includedir}/%{name}/thrust/system/detail/generic/tag.h
%{_includedir}/%{name}/thrust/system/detail/generic/temporary_buffer.h
%{_includedir}/%{name}/thrust/system/detail/generic/temporary_buffer.inl
%{_includedir}/%{name}/thrust/system/detail/generic/transform.h
%{_includedir}/%{name}/thrust/system/detail/generic/transform.inl
%{_includedir}/%{name}/thrust/system/detail/generic/transform_reduce.h
%{_includedir}/%{name}/thrust/system/detail/generic/transform_reduce.inl
%{_includedir}/%{name}/thrust/system/detail/generic/transform_scan.h
%{_includedir}/%{name}/thrust/system/detail/generic/transform_scan.inl
%{_includedir}/%{name}/thrust/system/detail/generic/uninitialized_copy.h
%{_includedir}/%{name}/thrust/system/detail/generic/uninitialized_copy.inl
%{_includedir}/%{name}/thrust/system/detail/generic/uninitialized_fill.h
%{_includedir}/%{name}/thrust/system/detail/generic/uninitialized_fill.inl
%{_includedir}/%{name}/thrust/system/detail/generic/unique_by_key.h
%{_includedir}/%{name}/thrust/system/detail/generic/unique_by_key.inl
%{_includedir}/%{name}/thrust/system/detail/generic/unique.h
%{_includedir}/%{name}/thrust/system/detail/generic/unique.inl
%{_includedir}/%{name}/thrust/system/detail/internal/decompose.h
%{_includedir}/%{name}/thrust/system/detail/sequential/adjacent_difference.h
%{_includedir}/%{name}/thrust/system/detail/sequential/assign_value.h
%{_includedir}/%{name}/thrust/system/detail/sequential/binary_search.h
%{_includedir}/%{name}/thrust/system/detail/sequential/copy_backward.h
%{_includedir}/%{name}/thrust/system/detail/sequential/copy.h
%{_includedir}/%{name}/thrust/system/detail/sequential/copy_if.h
%{_includedir}/%{name}/thrust/system/detail/sequential/copy.inl
%{_includedir}/%{name}/thrust/system/detail/sequential/count.h
%{_includedir}/%{name}/thrust/system/detail/sequential/equal.h
%{_includedir}/%{name}/thrust/system/detail/sequential/execution_policy.h
%{_includedir}/%{name}/thrust/system/detail/sequential/extrema.h
%{_includedir}/%{name}/thrust/system/detail/sequential/fill.h
%{_includedir}/%{name}/thrust/system/detail/sequential/find.h
%{_includedir}/%{name}/thrust/system/detail/sequential/for_each.h
%{_includedir}/%{name}/thrust/system/detail/sequential/gather.h
%{_includedir}/%{name}/thrust/system/detail/sequential/general_copy.h
%{_includedir}/%{name}/thrust/system/detail/sequential/generate.h
%{_includedir}/%{name}/thrust/system/detail/sequential/get_value.h
%{_includedir}/%{name}/thrust/system/detail/sequential/inner_product.h
%{_includedir}/%{name}/thrust/system/detail/sequential/insertion_sort.h
%{_includedir}/%{name}/thrust/system/detail/sequential/iter_swap.h
%{_includedir}/%{name}/thrust/system/detail/sequential/logical.h
%{_includedir}/%{name}/thrust/system/detail/sequential/malloc_and_free.h
%{_includedir}/%{name}/thrust/system/detail/sequential/merge.h
%{_includedir}/%{name}/thrust/system/detail/sequential/merge.inl
%{_includedir}/%{name}/thrust/system/detail/sequential/mismatch.h
%{_includedir}/%{name}/thrust/system/detail/sequential/partition.h
%{_includedir}/%{name}/thrust/system/detail/sequential/per_device_resource.h
%{_includedir}/%{name}/thrust/system/detail/sequential/reduce_by_key.h
%{_includedir}/%{name}/thrust/system/detail/sequential/reduce.h
%{_includedir}/%{name}/thrust/system/detail/sequential/remove.h
%{_includedir}/%{name}/thrust/system/detail/sequential/replace.h
%{_includedir}/%{name}/thrust/system/detail/sequential/reverse.h
%{_includedir}/%{name}/thrust/system/detail/sequential/scan_by_key.h
%{_includedir}/%{name}/thrust/system/detail/sequential/scan.h
%{_includedir}/%{name}/thrust/system/detail/sequential/scatter.h
%{_includedir}/%{name}/thrust/system/detail/sequential/sequence.h
%{_includedir}/%{name}/thrust/system/detail/sequential/set_operations.h
%{_includedir}/%{name}/thrust/system/detail/sequential/sort.h
%{_includedir}/%{name}/thrust/system/detail/sequential/sort.inl
%{_includedir}/%{name}/thrust/system/detail/sequential/stable_merge_sort.h
%{_includedir}/%{name}/thrust/system/detail/sequential/stable_merge_sort.inl
%{_includedir}/%{name}/thrust/system/detail/sequential/stable_primitive_sort.h
%{_includedir}/%{name}/thrust/system/detail/sequential/stable_primitive_sort.inl
%{_includedir}/%{name}/thrust/system/detail/sequential/stable_radix_sort.h
%{_includedir}/%{name}/thrust/system/detail/sequential/stable_radix_sort.inl
%{_includedir}/%{name}/thrust/system/detail/sequential/swap_ranges.h
%{_includedir}/%{name}/thrust/system/detail/sequential/tabulate.h
%{_includedir}/%{name}/thrust/system/detail/sequential/temporary_buffer.h
%{_includedir}/%{name}/thrust/system/detail/sequential/transform.h
%{_includedir}/%{name}/thrust/system/detail/sequential/transform_reduce.h
%{_includedir}/%{name}/thrust/system/detail/sequential/transform_scan.h
%{_includedir}/%{name}/thrust/system/detail/sequential/trivial_copy.h
%{_includedir}/%{name}/thrust/system/detail/sequential/uninitialized_copy.h
%{_includedir}/%{name}/thrust/system/detail/sequential/uninitialized_fill.h
%{_includedir}/%{name}/thrust/system/detail/sequential/unique_by_key.h
%{_includedir}/%{name}/thrust/system/detail/sequential/unique.h
%{_includedir}/%{name}/thrust/system/detail/system_error.inl
%{_includedir}/%{name}/thrust/system/error_code.h
%{_includedir}/%{name}/thrust/system_error.h
%{_includedir}/%{name}/thrust/system/omp/detail/adjacent_difference.h
%{_includedir}/%{name}/thrust/system/omp/detail/assign_value.h
%{_includedir}/%{name}/thrust/system/omp/detail/binary_search.h
%{_includedir}/%{name}/thrust/system/omp/detail/copy.h
%{_includedir}/%{name}/thrust/system/omp/detail/copy_if.h
%{_includedir}/%{name}/thrust/system/omp/detail/copy_if.inl
%{_includedir}/%{name}/thrust/system/omp/detail/copy.inl
%{_includedir}/%{name}/thrust/system/omp/detail/count.h
%{_includedir}/%{name}/thrust/system/omp/detail/default_decomposition.h
%{_includedir}/%{name}/thrust/system/omp/detail/default_decomposition.inl
%{_includedir}/%{name}/thrust/system/omp/detail/equal.h
%{_includedir}/%{name}/thrust/system/omp/detail/execution_policy.h
%{_includedir}/%{name}/thrust/system/omp/detail/extrema.h
%{_includedir}/%{name}/thrust/system/omp/detail/fill.h
%{_includedir}/%{name}/thrust/system/omp/detail/find.h
%{_includedir}/%{name}/thrust/system/omp/detail/for_each.h
%{_includedir}/%{name}/thrust/system/omp/detail/for_each.inl
%{_includedir}/%{name}/thrust/system/omp/detail/gather.h
%{_includedir}/%{name}/thrust/system/omp/detail/generate.h
%{_includedir}/%{name}/thrust/system/omp/detail/get_value.h
%{_includedir}/%{name}/thrust/system/omp/detail/inner_product.h
%{_includedir}/%{name}/thrust/system/omp/detail/iter_swap.h
%{_includedir}/%{name}/thrust/system/omp/detail/logical.h
%{_includedir}/%{name}/thrust/system/omp/detail/malloc_and_free.h
%{_includedir}/%{name}/thrust/system/omp/detail/memory.inl
%{_includedir}/%{name}/thrust/system/omp/detail/merge.h
%{_includedir}/%{name}/thrust/system/omp/detail/mismatch.h
%{_includedir}/%{name}/thrust/system/omp/detail/par.h
%{_includedir}/%{name}/thrust/system/omp/detail/partition.h
%{_includedir}/%{name}/thrust/system/omp/detail/partition.inl
%{_includedir}/%{name}/thrust/system/omp/detail/per_device_resource.h
%{_includedir}/%{name}/thrust/system/omp/detail/reduce_by_key.h
%{_includedir}/%{name}/thrust/system/omp/detail/reduce_by_key.inl
%{_includedir}/%{name}/thrust/system/omp/detail/reduce.h
%{_includedir}/%{name}/thrust/system/omp/detail/reduce.inl
%{_includedir}/%{name}/thrust/system/omp/detail/reduce_intervals.h
%{_includedir}/%{name}/thrust/system/omp/detail/reduce_intervals.inl
%{_includedir}/%{name}/thrust/system/omp/detail/remove.h
%{_includedir}/%{name}/thrust/system/omp/detail/remove.inl
%{_includedir}/%{name}/thrust/system/omp/detail/replace.h
%{_includedir}/%{name}/thrust/system/omp/detail/reverse.h
%{_includedir}/%{name}/thrust/system/omp/detail/scan_by_key.h
%{_includedir}/%{name}/thrust/system/omp/detail/scan.h
%{_includedir}/%{name}/thrust/system/omp/detail/scatter.h
%{_includedir}/%{name}/thrust/system/omp/detail/sequence.h
%{_includedir}/%{name}/thrust/system/omp/detail/set_operations.h
%{_includedir}/%{name}/thrust/system/omp/detail/sort.h
%{_includedir}/%{name}/thrust/system/omp/detail/sort.inl
%{_includedir}/%{name}/thrust/system/omp/detail/swap_ranges.h
%{_includedir}/%{name}/thrust/system/omp/detail/tabulate.h
%{_includedir}/%{name}/thrust/system/omp/detail/temporary_buffer.h
%{_includedir}/%{name}/thrust/system/omp/detail/transform.h
%{_includedir}/%{name}/thrust/system/omp/detail/transform_reduce.h
%{_includedir}/%{name}/thrust/system/omp/detail/transform_scan.h
%{_includedir}/%{name}/thrust/system/omp/detail/uninitialized_copy.h
%{_includedir}/%{name}/thrust/system/omp/detail/uninitialized_fill.h
%{_includedir}/%{name}/thrust/system/omp/detail/unique_by_key.h
%{_includedir}/%{name}/thrust/system/omp/detail/unique_by_key.inl
%{_includedir}/%{name}/thrust/system/omp/detail/unique.h
%{_includedir}/%{name}/thrust/system/omp/detail/unique.inl
%{_includedir}/%{name}/thrust/system/omp/execution_policy.h
%{_includedir}/%{name}/thrust/system/omp/memory.h
%{_includedir}/%{name}/thrust/system/omp/memory_resource.h
%{_includedir}/%{name}/thrust/system/omp/pointer.h
%{_includedir}/%{name}/thrust/system/omp/vector.h
%{_includedir}/%{name}/thrust/system/system_error.h
%{_includedir}/%{name}/thrust/system/tbb/detail/adjacent_difference.h
%{_includedir}/%{name}/thrust/system/tbb/detail/assign_value.h
%{_includedir}/%{name}/thrust/system/tbb/detail/binary_search.h
%{_includedir}/%{name}/thrust/system/tbb/detail/copy.h
%{_includedir}/%{name}/thrust/system/tbb/detail/copy_if.h
%{_includedir}/%{name}/thrust/system/tbb/detail/copy_if.inl
%{_includedir}/%{name}/thrust/system/tbb/detail/copy.inl
%{_includedir}/%{name}/thrust/system/tbb/detail/count.h
%{_includedir}/%{name}/thrust/system/tbb/detail/equal.h
%{_includedir}/%{name}/thrust/system/tbb/detail/execution_policy.h
%{_includedir}/%{name}/thrust/system/tbb/detail/extrema.h
%{_includedir}/%{name}/thrust/system/tbb/detail/fill.h
%{_includedir}/%{name}/thrust/system/tbb/detail/find.h
%{_includedir}/%{name}/thrust/system/tbb/detail/for_each.h
%{_includedir}/%{name}/thrust/system/tbb/detail/for_each.inl
%{_includedir}/%{name}/thrust/system/tbb/detail/gather.h
%{_includedir}/%{name}/thrust/system/tbb/detail/generate.h
%{_includedir}/%{name}/thrust/system/tbb/detail/get_value.h
%{_includedir}/%{name}/thrust/system/tbb/detail/inner_product.h
%{_includedir}/%{name}/thrust/system/tbb/detail/iter_swap.h
%{_includedir}/%{name}/thrust/system/tbb/detail/logical.h
%{_includedir}/%{name}/thrust/system/tbb/detail/malloc_and_free.h
%{_includedir}/%{name}/thrust/system/tbb/detail/memory.inl
%{_includedir}/%{name}/thrust/system/tbb/detail/merge.h
%{_includedir}/%{name}/thrust/system/tbb/detail/merge.inl
%{_includedir}/%{name}/thrust/system/tbb/detail/mismatch.h
%{_includedir}/%{name}/thrust/system/tbb/detail/par.h
%{_includedir}/%{name}/thrust/system/tbb/detail/partition.h
%{_includedir}/%{name}/thrust/system/tbb/detail/partition.inl
%{_includedir}/%{name}/thrust/system/tbb/detail/per_device_resource.h
%{_includedir}/%{name}/thrust/system/tbb/detail/reduce_by_key.h
%{_includedir}/%{name}/thrust/system/tbb/detail/reduce_by_key.inl
%{_includedir}/%{name}/thrust/system/tbb/detail/reduce.h
%{_includedir}/%{name}/thrust/system/tbb/detail/reduce.inl
%{_includedir}/%{name}/thrust/system/tbb/detail/reduce_intervals.h
%{_includedir}/%{name}/thrust/system/tbb/detail/remove.h
%{_includedir}/%{name}/thrust/system/tbb/detail/remove.inl
%{_includedir}/%{name}/thrust/system/tbb/detail/replace.h
%{_includedir}/%{name}/thrust/system/tbb/detail/reverse.h
%{_includedir}/%{name}/thrust/system/tbb/detail/scan_by_key.h
%{_includedir}/%{name}/thrust/system/tbb/detail/scan.h
%{_includedir}/%{name}/thrust/system/tbb/detail/scan.inl
%{_includedir}/%{name}/thrust/system/tbb/detail/scatter.h
%{_includedir}/%{name}/thrust/system/tbb/detail/sequence.h
%{_includedir}/%{name}/thrust/system/tbb/detail/set_operations.h
%{_includedir}/%{name}/thrust/system/tbb/detail/sort.h
%{_includedir}/%{name}/thrust/system/tbb/detail/sort.inl
%{_includedir}/%{name}/thrust/system/tbb/detail/swap_ranges.h
%{_includedir}/%{name}/thrust/system/tbb/detail/tabulate.h
%{_includedir}/%{name}/thrust/system/tbb/detail/temporary_buffer.h
%{_includedir}/%{name}/thrust/system/tbb/detail/transform.h
%{_includedir}/%{name}/thrust/system/tbb/detail/transform_reduce.h
%{_includedir}/%{name}/thrust/system/tbb/detail/transform_scan.h
%{_includedir}/%{name}/thrust/system/tbb/detail/uninitialized_copy.h
%{_includedir}/%{name}/thrust/system/tbb/detail/uninitialized_fill.h
%{_includedir}/%{name}/thrust/system/tbb/detail/unique_by_key.h
%{_includedir}/%{name}/thrust/system/tbb/detail/unique_by_key.inl
%{_includedir}/%{name}/thrust/system/tbb/detail/unique.h
%{_includedir}/%{name}/thrust/system/tbb/detail/unique.inl
%{_includedir}/%{name}/thrust/system/tbb/execution_policy.h
%{_includedir}/%{name}/thrust/system/tbb/memory.h
%{_includedir}/%{name}/thrust/system/tbb/memory_resource.h
%{_includedir}/%{name}/thrust/system/tbb/pointer.h
%{_includedir}/%{name}/thrust/system/tbb/vector.h
%{_includedir}/%{name}/thrust/tabulate.h
%{_includedir}/%{name}/thrust/transform.h
%{_includedir}/%{name}/thrust/transform_reduce.h
%{_includedir}/%{name}/thrust/transform_scan.h
%{_includedir}/%{name}/thrust/tuple.h
%{_includedir}/%{name}/thrust/type_traits/integer_sequence.h
%{_includedir}/%{name}/thrust/type_traits/is_contiguous_iterator.h
%{_includedir}/%{name}/thrust/type_traits/is_execution_policy.h
%{_includedir}/%{name}/thrust/type_traits/is_operator_less_or_greater_function_object.h
%{_includedir}/%{name}/thrust/type_traits/is_operator_plus_function_object.h
%{_includedir}/%{name}/thrust/type_traits/is_trivially_relocatable.h
%{_includedir}/%{name}/thrust/type_traits/logical_metafunctions.h
%{_includedir}/%{name}/thrust/type_traits/remove_cvref.h
%{_includedir}/%{name}/thrust/type_traits/void_t.h
%{_includedir}/%{name}/thrust/uninitialized_copy.h
%{_includedir}/%{name}/thrust/uninitialized_fill.h
%{_includedir}/%{name}/thrust/unique.h
%{_includedir}/%{name}/thrust/universal_allocator.h
%{_includedir}/%{name}/thrust/universal_ptr.h
%{_includedir}/%{name}/thrust/universal_vector.h
%{_includedir}/%{name}/thrust/version.h
%{_includedir}/%{name}/thrust/zip_function.h
%{_includedir}/%{name}/vector_functions.h
%{_includedir}/%{name}/vector_functions.hpp
%{_includedir}/%{name}/vector_types.h
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
%{_includedir}/%{name}/sanitizer_barrier.h
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
* Tue Jul 20 2021 Simone Caronni <negativo17@gmail.com> - 1:11.4.0-1
- Update to 11.4.0.
- Update package names used in conflict statements to match upstream changes.
- Add missing CCCL (C++ Core Compute libraries )headers to devel subpackage.

* Sun Apr 25 2021 Simone Caronni <negativo17@gmail.com> - 1:11.3.0-1
- Update to 11.3.0.
- Split static libraries in subpackages.

* Thu Feb 18 2021 Simone Caronni <negativo17@gmail.com> - 1:11.2.1-1
- Update to 11.2.1.

* Sun Dec 20 2020 Simone Caronni <negativo17@gmail.com> - 1:11.2.0-1
- Update to CUDA 11.2.0.

* Sat Nov 28 2020 Simone Caronni <negativo17@gmail.com> - 1:11.1.1-3
- GCC 10 works fine.
- rpmlint fixes.

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
