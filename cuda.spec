# Todo:
# - filter \*.so from Java programs
# - build cuda-gdb from source
# - build Java programs from source
# - /usr/include/cuda is owned by the cuda main package but the devel
#   subpackages use the directory

%global         debug_package %{nil}
#global         __strip /bin/true
%global         cuda_version 8.0
%global         major_package_version 8-0

Name:           cuda
Version:        %{cuda_version}.44
Release:        5%{?dist}
Summary:        NVIDIA Compute Unified Device Architecture Toolkit
Epoch:          1
License:        NVIDIA License
URL:            https://developer.nvidia.com/cuda-zone
ExclusiveArch:  x86_64 %{ix86}

# See Source1 for tarball generation - saves ~400Mb.
Source0:        %{name}-%{version}-x86_64.tar.xz
Source1:        %{name}-generate-tarballs.sh
Source2:        http://http.download.nvidia.com/cuda-toolkit/%{version}/cuda-gdb-%{version}.src.tar.gz

Source3:        %{name}.sh
Source4:        %{name}.csh
Source5:        nsight.desktop
Source6:        nsight.appdata.xml
Source7:        nvvp.desktop
Source8:        nvvp.appdata.xml

Source20:       cublas.pc
Source21:       cuda.pc
Source22:       cudart.pc
Source23:       cufft.pc
Source24:       cufftw.pc
Source25:       cuinj64.pc
Source26:       curand.pc
Source27:       cusolver.pc
Source28:       cusparse.pc
Source29:       nppc.pc
Source30:       nppial.pc
Source31:       nppicc.pc
Source32:       nppicom.pc
Source33:       nppidei.pc
Source34:       nppif.pc
Source35:       nppig.pc
Source36:       nppim.pc
Source37:       nppi.pc
Source38:       nppist.pc
Source39:       nppisu.pc
Source40:       nppitc.pc
Source41:       npps.pc
Source42:       nvgraph.pc
Source43:       nvml.pc
Source44:       nvrtc.pc
Source45:       nvToolsExt.pc

BuildRequires:  ImageMagick
BuildRequires:  desktop-file-utils
# For RUNPATH removal
BuildRequires:  chrpath
# For execstack removal
%if 0%{?fedora} >= 23 || 0%{?rhel} > 7
BuildRequires:  execstack
%else
BuildRequires:  prelink
%endif

Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-core-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-core-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-minimal-build-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-minimal-build-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
CUDA is a parallel computing platform and programming model that enables
dramatic increases in computing performance by harnessing the power of the
graphics processing unit (GPU).

%package cli-tools
Summary:        Compute Unified Device Architecture command-line tools
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       expat >= 1.95
Requires:       gdb
Obsoletes:      %{name}-command-line-tools-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-command-line-tools-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}

%description cli-tools
Contains the command line tools to debug and profile CUDA applications.

%package libs
Summary:        Compute Unified Device Architecture native run-time library
Requires(post): ldconfig
Obsoletes:      %{name}-core-libs-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-core-libs-%{major_package_version} = %{?epoch:%{epoch}:}%{version}
Obsoletes:      %{name}-driver-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-driver-dev-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-license-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-license-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}

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
Requires:       %{name}-nvgraph = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvrtc = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-runtime-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-runtime-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}

%description extra-libs
Metapackage that installs all runtime NVIDIA CUDA libraries.

%package cublas
Summary:        NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS) libraries
Requires(post): ldconfig
Obsoletes:      %{name}-cublas-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-cublas-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}

%description cublas
The NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS) library is a
GPU-accelerated version of the complete standard BLAS library that delivers 6x
to 17x faster performance than the latest MKL BLAS.

%package cublas-devel
Summary:        Development files for NVIDIA CUDA Basic Linear Algebra Subroutines (cuBLAS)
Requires:       %{name}-cublas%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-cublas-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-cublas-dev-%{major_package_version} = %{?epoch:%{epoch}:}%{version}

%description cublas-devel
This package provides development files for the NVIDIA CUDA Basic Linear
Algebra Subroutines (cuBLAS) libraries.

%package cudart
Summary:        NVIDIA CUDA Runtime API library
Requires(post): ldconfig
Obsoletes:      %{name}-cudart-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-cudart-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}

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
Obsoletes:      %{name}-cudart-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-cudart-dev-%{major_package_version} = %{?epoch:%{epoch}:}%{version}

%description cudart-devel
This package provides development files for the NVIDIA CUDA Runtime API library

%package cufft
Summary:        NVIDIA CUDA Fast Fourier Transform library (cuFFT) libraries
Requires(post): ldconfig
Obsoletes:      %{name}-cufft-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-cufft-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}

%description cufft
The NVIDIA CUDA Fast Fourier Transform libraries (cuFFT) provide a simple
interface for computing FFTs up to 10x faster.  By using hundreds of processor
cores inside NVIDIA GPUs, cuFFT delivers the floating‐point performance of a
GPU without having to develop your own custom GPU FFT implementation.

%package cufft-devel
Summary:        Development files for NVIDIA CUDA Fast Fourier Transform library (cuFFT)
Requires:       %{name}-cufft%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-cufft-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-cufft-dev-%{major_package_version} = %{?epoch:%{epoch}:}%{version}

%description cufft-devel
This package provides development files for the NVIDIA CUDA Fast Fourier
Transform library (cuFFT) libraries.

%package cupti
Summary:        NVIDIA CUDA Profiling Tools Interface (CUPTI) library
Requires(post): ldconfig

%description cupti
The NVIDIA CUDA Profiling Tools Interface (CUPTI) provides performance analysis
tools with detailed information about how applications are using the GPUs in a
system.

%package cupti-devel
Summary:        Development files for NVIDIA CUDA Profiling Tools Interface (CUPTI) library
Requires:       %{name}-cupti%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description cupti-devel
This package provides development files for the NVIDIA CUDA Profiling Tools
Interface (CUPTI) library.

%package curand
Summary:        NVIDIA CUDA Random Number Generation library (cuRAND)
Requires(post): ldconfig
Obsoletes:      %{name}-curand-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-curand-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}

%description curand
The NVIDIA CUDA Random Number Generation library (cuRAND) delivers high
performance GPU-accelerated random number generation (RNG). The cuRAND library
delivers high quality random numbers 8x faster using hundreds of processor
cores available in NVIDIA GPUs.

%package curand-devel
Summary:        Development files for NVIDIA CUDA Random Number Generation library (cuRAND)
Requires:       %{name}-curand%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-curand-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-curand-dev-%{major_package_version} = %{?epoch:%{epoch}:}%{version}

%description curand-devel
This package provides development files for the NVIDIA CUDA Random Number
Generation library (cuRAND).

%package cusolver
Summary:        NVIDIA cuSOLVER library
Requires(post): ldconfig
Obsoletes:      %{name}-cusolver-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-cusolver-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}

%description cusolver
The NVIDIA cuSOLVER library provides a collection of dense and sparse direct
solvers which deliver significant acceleration for Computer Vision, CFD,
Computational Chemistry, and Linear Optimization applications.

%package cusolver-devel
Summary:        Development files for NVIDIA cuSOLVER library
Requires:       %{name}-cusolver%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-cusolver-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-cusolver-dev-%{major_package_version} = %{?epoch:%{epoch}:}%{version}

%description cusolver-devel
This package provides development files for the NVIDIA cuSOLVER library.

%package cusparse
Summary:        NVIDIA CUDA Sparse Matrix library (cuSPARSE) library
Requires(post): ldconfig
Obsoletes:      %{name}-cusparse-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-cusparse-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}

%description cusparse
The NVIDIA CUDA Sparse Matrix library (cuSPARSE) provides a collection of basic
linear algebra subroutines used for sparse matrices that delivers up to 8x
faster performance than the latest MKL. The cuSPARSE library is designed to be
called from C or C++, and the latest release includes a sparse triangular
solver.

%package cusparse-devel
Summary:        Development files for NVIDIA CUDA Sparse Matrix library (cuSPARSE) library
Requires:       %{name}-cusparse%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-cusparse-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-cusparse-dev-%{major_package_version} = %{?epoch:%{epoch}:}%{version}

%description cusparse-devel
This package provides development files for the NVIDIA CUDA Sparse Matrix
library (cuSPARSE) library.

%package npp
Summary:        NVIDIA Performance Primitives libraries
Requires(post): ldconfig
Obsoletes:      %{name}-npp-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-npp-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}

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
Obsoletes:      %{name}-npp-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-npp-dev-%{major_package_version} = %{?epoch:%{epoch}:}%{version}

%description npp-devel
This package provides development files for the NVIDIA Performance Primitives
libraries.

%package nvgraph
Summary:        NVIDIA Graph Analytics library (nvGRAPH)
Requires(post): ldconfig
Obsoletes:      %{name}-nvgraph-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-nvgraph-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}

%description nvgraph
The NVIDIA Graph Analytics library (nvGRAPH) comprises of parallel algorithms
for high performance analytics on graphs with up to 2 billion edges. nvGRAPH
makes it possible to build interactive and high throughput graph analytics
applications.

%package nvgraph-devel
Summary:        Development files for NVIDIA Graph Analytics library (nvGRAPH)
Requires:       %{name}-nvgraph%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-nvgraph-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-nvgraph-dev-%{major_package_version} = %{?epoch:%{epoch}:}%{version}

%description nvgraph-devel
This package provides development files for the NVIDIA Graph Analytics library
(nvGRAPH).

# Actual libnvidia-ml library (cuda-nvml) is in the Nvidia driver

%package nvml-devel
Summary:        Development files for NVIDIA Management library (nvML)
# Unversioned as it is provided by the driver's NVML library
Requires:       %{name}-nvml%{_isa}
Obsoletes:      %{name}-nvml-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-nvml-dev-%{major_package_version} = %{?epoch:%{epoch}:}%{version}
# Latest standalone version released is 352.79
Obsoletes:      nvidia-driver-NVML-devel < 2:352.80
Provides:       nvidia-driver-NVML-devel = %{?epoch:%{epoch}:}%{version}

%description nvml-devel
This package provides development files for the NVIDIA Management library
(nvML).

%package nvrtc
Summary:        NVRTC runtime compilation library
Requires(post): ldconfig
Obsoletes:      %{name}-nvrtc-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-nvrtc-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}

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
Obsoletes:      %{name}-nvrtc-dev-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-nvrtc-dev-%{major_package_version} = %{?epoch:%{epoch}:}%{version}

%description nvrtc-devel
This package provides development files for the NVRTC runtime compilation
library.

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
Requires:       %{name}-nvgraph-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvml-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-nvrtc-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       nvidia-driver-NVML%{_isa}
Obsoletes:      %{name}-headers-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-headers-%{major_package_version} = %{?epoch:%{epoch}:}%{version}
Obsoletes:      %{name}-misc-headers-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-misc-headers-%{major_package_version} = %{?epoch:%{epoch}:}%{version}
Obsoletes:      %{name}-toolkit-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-toolkit-%{major_package_version} = %{?epoch:%{epoch}:}%{version}
Obsoletes:      %{name}-static < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-static = %{?epoch:%{epoch}:}%{version}

%description devel
This package provides the development files of the %{name} package.

%package docs
Summary:        Compute Unified Device Architecture toolkit documentation
BuildArch:      noarch
Obsoletes:      %{name}-documentation-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-documentation-%{major_package_version} = %{?epoch:%{epoch}:}%{version}

%description docs
Contains all guides and library documentation for CUDA.

%package samples
Summary:        Compute Unified Device Architecture toolkit samples
Obsoletes:      %{name}-demo-suite-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-demo-suite-%{major_package_version} = %{?epoch:%{epoch}:}%{version}
Obsoletes:      %{name}-samples-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-samples-%{major_package_version} = %{?epoch:%{epoch}:}%{version}
Obsoletes:      %{name}-samples < %{?epoch:%{epoch}:}%{version}
Provides:       %{name}-samples = %{?epoch:%{epoch}:}%{version}
Requires:       cuda-devel = %{?epoch:%{epoch}:}%{version}
Requires:       gcc
Requires:       freeglut-devel
Requires:       make
Requires:       mesa-libGLU-devel
Requires:       libX11-devel
Requires:       libXmu-devel
Requires:       libXi-devel

%description samples
Contains an extensive set of example CUDA programs.

%package nsight
Summary:        NVIDIA Nsight Eclipse Edition
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-visual-tools-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-visual-tools-%{major_package_version} = %{?epoch:%{epoch}:}%{version}-%{release}

%description nsight
NVIDIA Nsight Eclipse Edition is a full-featured IDE powered by the Eclipse
platform that provides an all-in-one integrated environment to edit, build,
debug and profile CUDA-C applications. Nsight Eclipse Edition supports a rich
set of commercial and free plugins.

%package nvvp
Summary:        NVIDIA Visual Profiler
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description nvvp
The NVIDIA Visual Profiler is a cross-platform performance profiling tool that
delivers developers vital feedback for optimizing CUDA C/C++ applications.


%prep
%setup -q -n %{name}-%{version}-x86_64

%ifarch x86_64

# Remove execstack on binaries
execstack -c nvvm/bin/cicc nvvm/%{_lib}/*

# Remove RUNPATH on binaries
chrpath -d nvvm/bin/cicc

# RPMlint issues
find . -name "*.h" -exec chmod 644 {} \;
find . -name "*.hpp" -exec chmod 644 {} \;
find . -name "*.bat" -delete
find . -size 0 -delete

# Works also with GCC 4.9+ but only if C++11 is not enabled
sed -i -e '/#error -- unsupported GNU version!/d' include/host_config.h

# Remove double quotes in samples' Makefiles (cosmetical)
find samples -name "Makefile" -exec sed -i -e 's|"/usr"|/usr|g' {} \;

# Remove unused stuff
rm -f doc/man/man1/cuda-install-samples-%{major_package_version}.sh.1
rm -f samples/uninstall_cuda_samples_%{cuda_version}.pl
rm -f samples/.uninstall_manifest_do_not_delete.txt
rm -f bin/uninstall_cuda_toolkit_%{cuda_version}.pl
rm -f bin/cuda-install-samples-%{major_package_version}.sh
rm -f bin/.uninstall_manifest_do_not_delete.txt

%endif

%build
# Nothing to build

%install
%ifarch x86_64

# Create empty tree
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}%{_datadir}/%{name}/
mkdir -p %{buildroot}%{_datadir}/libnsight/
mkdir -p %{buildroot}%{_datadir}/libnvvp/
mkdir -p %{buildroot}%{_datadir}/pixmaps/
mkdir -p %{buildroot}%{_includedir}/%{name}/
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
mkdir -p %{buildroot}%{_libexecdir}/%{name}/
mkdir -p %{buildroot}%{_mandir}/man{1,3,7}/
mkdir -p %{buildroot}%{_sysconfdir}/profile.d/

# Environment settings
rm -f bin/nvcc.profile
install -pm 644 %{SOURCE3} %{SOURCE4} %{buildroot}%{_sysconfdir}/profile.d

# Man pages
rm -f doc/man/man1/cuda-install-samples-*
for man in doc/man/man{1,3,7}/*; do gzip -9 $man; done
cp -fr doc/man/* %{buildroot}%{_mandir}
# This man page conflicts with *a lot* of other packages
mv %{buildroot}%{_mandir}/man3/deprecated.3.gz \
    %{buildroot}%{_mandir}/man3/cuda_deprecated.3.gz

# Docs
mv extras/CUPTI/Readme.txt extras/CUPTI/Readme-CUPTI.txt
mv extras/Debugger/Readme.txt extras/Debugger/Readme-Debugger.txt

# Base license file
mv samples/EULA.txt .

# Headers
cp -fr src %{buildroot}%{_includedir}/%{name}/fortran/
cp -fr include/* nvvm/include/* %{buildroot}%{_includedir}/%{name}/
cp -fr extras/CUPTI/include %{buildroot}%{_includedir}/%{name}/CUPTI/
cp -fr extras/Debugger/include %{buildroot}%{_includedir}/%{name}/Debugger/

# Libraries
cp -fr %{_lib}/* nvvm/%{_lib}/* %{buildroot}%{_libdir}/
cp -fr extras/CUPTI/%{_lib}/* %{buildroot}%{_libdir}/
cp -fr nvvm/libdevice/* %{buildroot}%{_datadir}/%{name}/

# Libraries in the driver package
rm -f %{buildroot}%{_libdir}/libOpenCL.so*
ln -sf libnvidia-ml.so.1 %{buildroot}%{_libdir}/libnvidia-ml.so

# pkg-config files
install -pm 644 %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} \
    %{SOURCE25} %{SOURCE26} %{SOURCE27} %{SOURCE28} %{SOURCE29} %{SOURCE30} \
    %{SOURCE31} %{SOURCE32} %{SOURCE33} %{SOURCE34} %{SOURCE35} %{SOURCE36} \
    %{SOURCE37} %{SOURCE38} %{SOURCE39} %{SOURCE40} %{SOURCE41} %{SOURCE42} \
    %{SOURCE43} %{SOURCE44} %{SOURCE45} %{buildroot}/%{_libdir}/pkgconfig
sed -i -e 's/CUDA_VERSION/%{cuda_version}/g' %{buildroot}/%{_libdir}/pkgconfig/*.pc

# Binaries
cp -fr bin/* nvvm/bin/* %{buildroot}%{_bindir}/

# GDB stuff
cp -fr share/gdb %{buildroot}%{_datadir}/gdb

# Additional samples
cp -fr samples %{buildroot}%{_datadir}/%{name}/
cp -fr extras/CUPTI/sample %{buildroot}%{_datadir}/%{name}/samples/CUPTI
mv nvml/example %{buildroot}%{_datadir}/%{name}/samples/nvml
mv nvvm/libnvvm-samples %{buildroot}%{_datadir}/%{name}/samples/nvvm
mv extras/demo_suite %{buildroot}%{_datadir}/%{name}/

# Java stuff
sed -i -e '/^-vm/d' -e '/jre\/bin\/java/d' libnsight/nsight.ini libnvvp/nvvp.ini

# Convert icons for appstream
convert libnsight/icon.xpm nsight.png
convert libnvvp/icon.xpm nvvp.png

# Install Java GUI programs
install -m 644 -p nsight.png %{buildroot}%{_datadir}/pixmaps/nsight.png
install -m 644 -p nvvp.png %{buildroot}%{_datadir}/pixmaps/nvvp.png
cp -fr libnsight %{buildroot}%{_libdir}/nsight
cp -fr libnvvp %{buildroot}%{_libdir}/nvvp
ln -sf %{_libdir}/nsight/nsight %{buildroot}%{_bindir}/
ln -sf %{_libdir}/nvvp/nvvp %{buildroot}%{_bindir}/
desktop-file-install --dir %{buildroot}%{_datadir}/applications/ %{SOURCE5} %{SOURCE7}

# Only Fedora and RHEL 7+ desktop-file-validate binaries can check multiple
# desktop files at the same time
desktop-file-validate %{buildroot}%{_datadir}/applications/nsight.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/nvvp.desktop

%if 0%{?fedora} >= 25
# install AppData and add modalias provides
mkdir -p %{buildroot}%{_datadir}/appdata
install -p -m 0644 %{SOURCE6} %{SOURCE8} %{buildroot}%{_datadir}/appdata/
%endif

%endif

# For i686 just create the nvml-devel subpackage
%ifarch %{ix86}
mkdir -p %{buildroot}%{_includedir}/%{name}/
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
ln -sf libnvidia-ml.so.1 %{buildroot}%{_libdir}/libnvidia-ml.so
install -pm 644 %{SOURCE43} %{buildroot}/%{_libdir}/pkgconfig
sed -i -e 's/CUDA_VERSION/%{cuda_version}/g' %{buildroot}/%{_libdir}/pkgconfig/*.pc
install -pm 644 include/nvml.h %{buildroot}%{_includedir}/%{name}/
%endif

%post -p /sbin/ldconfig

%post libs -p /sbin/ldconfig

%post cublas -p /sbin/ldconfig

%post cudart -p /sbin/ldconfig

%post cufft -p /sbin/ldconfig

%post cupti -p /sbin/ldconfig

%post curand -p /sbin/ldconfig

%post cusolver -p /sbin/ldconfig

%post cusparse -p /sbin/ldconfig

%post npp -p /sbin/ldconfig

%post nvgraph -p /sbin/ldconfig

%post nvrtc -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%postun cublas -p /sbin/ldconfig

%postun cudart -p /sbin/ldconfig

%postun cufft -p /sbin/ldconfig

%postun cupti -p /sbin/ldconfig

%postun curand -p /sbin/ldconfig

%postun cusolver -p /sbin/ldconfig

%postun cusparse -p /sbin/ldconfig

%postun npp -p /sbin/ldconfig

%postun nvgraph -p /sbin/ldconfig

%postun nvrtc -p /sbin/ldconfig

%post nsight
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun nsight
%{_bindir}/update-desktop-database &> /dev/null || :

%post nvvp
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun nvvp
%{_bindir}/update-desktop-database &> /dev/null || :

%ifarch x86_64

%files
%{_bindir}/bin2c
%{_bindir}/cicc
# There should be no folder there, but binaries look for things here
%{_bindir}/crt/
%{_bindir}/cudafe
%{_bindir}/cudafe++
%{_bindir}/cuobjdump
%{_bindir}/gpu-library-advisor
%{_bindir}/fatbinary
%{_bindir}/nvcc
%{_bindir}/nvlink
%{_bindir}/nvprune
%{_bindir}/ptxas
%dir %{_includedir}/%{name}
%{_libexecdir}/%{name}/
%{_mandir}/man1/cuda-binaries.*
%{_mandir}/man1/cuobjdump.*
%{_mandir}/man1/nvcc.*
%{_mandir}/man1/nvprune.*
%{_datadir}/%{name}/
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh

%files cli-tools
%{_bindir}/cuda-gdb
%{_bindir}/cuda-gdbserver
%{_bindir}/cuda-memcheck
%{_bindir}/nvdisasm
%{_bindir}/nvprof
%{_datadir}/gdb/*
%{_mandir}/man1/cuda-gdb.*
%{_mandir}/man1/cuda-gdbserver.*
%{_mandir}/man1/cuda-memcheck.*
%{_mandir}/man1/nvdisasm.*
%{_mandir}/man1/nvprof.*

%files libs
%license EULA.txt
%{_libdir}/libcudart.so.*
%{_libdir}/libcuinj%{__isa_bits}.so.*
%{_libdir}/libnvToolsExt.so.*
%{_libdir}/libnvvm.so.*

%files cublas
%license EULA.txt
%{_libdir}/libcublas.so.*
%{_libdir}/libnvblas.so.*

%files cublas-devel
%{_includedir}/%{name}/cublas*
%{_includedir}/%{name}/nvblas*
%{_libdir}/libcublas_device.a
%{_libdir}/libcublas_static.a
%{_libdir}/libcublas.so
%{_libdir}/libnvblas.so
%{_libdir}/pkgconfig/cublas.pc

%files cudart
%license EULA.txt
%{_libdir}/libcudart.so.*
%{_libdir}/libnvToolsExt.so.*

%files cudart-devel
%{_includedir}/%{name}/crt
%{_includedir}/%{name}/cuda_device_runtime_api.h
%{_includedir}/%{name}/cuda_runtime.h
%{_includedir}/%{name}/cuda_runtime_api.h
%{_includedir}/%{name}/nvToolsExtCudaRt.h
%{_libdir}/libcudadevrt.a
%{_libdir}/libcudart_static.a
%{_libdir}/libcudart.so
%{_libdir}/libculibos.a
%{_libdir}/libnvToolsExt.so
%{_libdir}/pkgconfig/cudart.pc
%{_libdir}/pkgconfig/nvToolsExt.pc

%files cufft
%license EULA.txt
%{_libdir}/libcufft.so.*
%{_libdir}/libcufftw.so.*

%files cufft-devel
%{_includedir}/%{name}/cufft*
%{_libdir}/libcufft_static.a
%{_libdir}/libcufft.so
%{_libdir}/libcufftw_static.a
%{_libdir}/libcufftw.so
%{_libdir}/pkgconfig/cufft.pc
%{_libdir}/pkgconfig/cufftw.pc

%files cupti
%license EULA.txt
%{_libdir}/libcupti.so.*

%files cupti-devel
%doc extras/CUPTI/Readme-CUPTI.txt
%{_includedir}/%{name}/CUPTI
%{_libdir}/libcupti.so

%files curand
%license EULA.txt
%{_libdir}/libcurand.so.*

%files curand-devel
%{_includedir}/%{name}/curand*
%{_includedir}/%{name}/sobol_direction_vectors.h
%{_libdir}/libcurand_static.a
%{_libdir}/libcurand.so
%{_libdir}/pkgconfig/curand.pc

%files cusolver
%license EULA.txt
%{_libdir}/libcusolver.so.*

%files cusolver-devel
%{_includedir}/%{name}/cusolver*
%{_libdir}/libcusolver_static.a
%{_libdir}/libcusolver.so
%{_libdir}/pkgconfig/cusolver.pc

%files cusparse
%license EULA.txt
%{_libdir}/libcusparse.so.*

%files cusparse-devel
%{_includedir}/%{name}/cusparse*
%{_libdir}/libcusparse_static.a
%{_libdir}/libcusparse.so
%{_libdir}/pkgconfig/cusparse.pc

%files npp
%license EULA.txt
%{_libdir}/libnpp*.so.*

%files npp-devel
%{_includedir}/%{name}/npp*
%{_libdir}/libnpp*_static.a
%{_libdir}/libnpp*.so
%{_libdir}/pkgconfig/npp*.pc

%files nvgraph
%license EULA.txt
%{_libdir}/libnvgraph_static.a
%{_libdir}/libnvgraph.so.*

%files nvgraph-devel
%{_includedir}/%{name}/nvgraph*
%{_libdir}/libnvgraph.so
%{_libdir}/pkgconfig/nvgraph.pc

%endif

%files nvml-devel
%{_includedir}/%{name}/nvml*
%{_libdir}/libnvidia-ml.so
%{_libdir}/pkgconfig/nvml.pc

%ifarch x86_64

%files nvrtc
%license EULA.txt
%{_libdir}/libnvrtc-builtins.so.*
%{_libdir}/libnvrtc.so.*

%files nvrtc-devel
%{_includedir}/%{name}/nvrtc*
%{_libdir}/libnvrtc-builtins.so
%{_libdir}/libnvrtc.so
%{_libdir}/pkgconfig/nvrtc.pc

%files extra-libs
# Empty metapackage

%files devel
%doc extras/Debugger/Readme-Debugger.txt
%{_includedir}/%{name}/CL
%{_includedir}/%{name}/Debugger
%{_includedir}/%{name}/builtin_types.h
%{_includedir}/%{name}/channel_descriptor.h
%{_includedir}/%{name}/common_functions.h
%{_includedir}/%{name}/cuComplex.h
%{_includedir}/%{name}/cuda.h
%{_includedir}/%{name}/cudaGL.h
%{_includedir}/%{name}/cudaProfiler.h
%{_includedir}/%{name}/cudaVDPAU.h
%{_includedir}/%{name}/cuda_fp16.h
%{_includedir}/%{name}/cuda_gl_interop.h
%{_includedir}/%{name}/cuda_occupancy.h
%{_includedir}/%{name}/cuda_profiler_api.h
%{_includedir}/%{name}/cuda_surface_types.h
%{_includedir}/%{name}/cuda_texture_types.h
%{_includedir}/%{name}/cuda_vdpau_interop.h
%{_includedir}/%{name}/cudalibxt.h
%{_includedir}/%{name}/cuviddec.h
%{_includedir}/%{name}/device_atomic_functions.h
%{_includedir}/%{name}/device_atomic_functions.hpp
%{_includedir}/%{name}/device_double_functions.h
%{_includedir}/%{name}/device_double_functions.hpp
%{_includedir}/%{name}/device_functions.h
%{_includedir}/%{name}/device_functions.hpp
%{_includedir}/%{name}/device_functions_decls.h
%{_includedir}/%{name}/device_launch_parameters.h
%{_includedir}/%{name}/device_types.h
%{_includedir}/%{name}/driver_functions.h
%{_includedir}/%{name}/driver_types.h
%{_includedir}/%{name}/fatBinaryCtl.h
%{_includedir}/%{name}/fatbinary.h
%{_includedir}/%{name}/fortran  
%{_includedir}/%{name}/host_config.h
%{_includedir}/%{name}/host_defines.h
%{_includedir}/%{name}/library_types.h
%{_includedir}/%{name}/math_constants.h
%{_includedir}/%{name}/math_functions.h
%{_includedir}/%{name}/math_functions.hpp
%{_includedir}/%{name}/math_functions_dbl_ptx3.h
%{_includedir}/%{name}/math_functions_dbl_ptx3.hpp
%{_includedir}/%{name}/nvToolsExt.h
%{_includedir}/%{name}/nvToolsExtCuda.h
%{_includedir}/%{name}/nvToolsExtMeta.h
%{_includedir}/%{name}/nvToolsExtSync.h
%{_includedir}/%{name}/nvcuvid.h
%{_includedir}/%{name}/nvfunctional
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
%{_libdir}/libcuinj%{__isa_bits}.so
%{_libdir}/libnvvm.so
%{_mandir}/man3/*
%{_mandir}/man7/*
%{_libdir}/pkgconfig/cuda.pc
%{_libdir}/pkgconfig/cuinj64.pc

%files docs
%doc doc/pdf doc/html tools/*

%files samples
%{_datadir}/%{name}/samples
%{_datadir}/%{name}/demo_suite

%files nsight
%{_bindir}/nsight
%if 0%{?fedora} >= 25
%{_datadir}/appdata/nsight.appdata.xml
%endif
%{_datadir}/applications/nsight.desktop
%{_datadir}/pixmaps/nsight.png
%{_libdir}/nsight
%{_mandir}/man1/nsight.*

%files nvvp
%{_bindir}/computeprof
%{_bindir}/nvvp
%if 0%{?fedora} >= 25
%{_datadir}/appdata/nvvp.appdata.xml
%endif
%{_datadir}/applications/nvvp.desktop
%{_datadir}/pixmaps/nvvp.png
%{_mandir}/man1/nvvp.*
%{_libdir}/nvvp

%endif

%changelog
* Sat Oct 22 2016 Simone Caronni <negativo17@gmail.com> - 1:8.0.44-5
- Make the package not exclusive to x86_64 and let the nvml-devel subpackage
  build on i386.

* Thu Oct 20 2016 Simone Caronni <negativo17@gmail.com> - 1:8.0.44-4
- SPEC file cleanups.

* Tue Oct 18 2016 Simone Caronni <negativo17@gmail.com> - 1:8.0.44-3
- Make cuda-nvml-devel require an unversioned base package as it is provided by
  the driver's NVML library.

* Mon Oct 17 2016 Simone Caronni <negativo17@gmail.com> - 1:8.0.44-2
- Add missing nvToolsExt.pc pkgconfig file.
- Split libraries into subpackages for easier consumption by dependent packages
  (i.e. FFMpeg). More similar to what Nvidia provides.

* Sun Oct 02 2016 Simone Caronni <negativo17@gmail.com> - 1:8.0.44-1
- Update to 8.0.44:
  * Add additional nvgraph library and gpu-library-advisor command.
  * Obsoletes/Provides nvidia-driver-NVML-devel in devel subpackage.
- Make major version conditional for most of the SPEC file.
- Move samples under /usr/share.
- Add base text license (EULA) to libs subpackage.
- Make samples package architecture dependent as it contains pre-built binaries
  and objects. Make it obsolete the noarch one.

* Sun Sep 11 2016 Simone Caronni <negativo17@gmail.com> - 1:7.5.18-5
- Convert Java GUI programs icons to png for AppStream metadata.
- Add AppStream metadata for Fedora 25+.

* Thu Mar 24 2016 Simone Caronni <negativo17@gmail.com> - 1:7.5.18-4
- Streamline pkg-config files versioning.
- Fix cuFFT library versions.

* Fri Feb 26 2016 Simone Caronni <negativo17@gmail.com> - 1:7.5.18-3
- Fix CUDA_PATH variable hardcoded in samples.

* Sun Nov 15 2015 Simone Caronni <negativo17@gmail.com> - 1:7.5.18-2
- Rename man page deprecated(3) to cuda_deprecated(3) so it does not conflict
  with a lot of other packages that ship the same man page.

* Fri Sep 18 2015 Simone Caronni <negativo17@gmail.com> - 1:7.5.18-1
- Update to 7.5.18.

* Mon Aug 17 2015 Simone Caronni <negativo17@gmail.com> - 1:7.0.28-2
- Add missing cuda-binaries(1) man page.
- Move libcudadevrt.a and libcublas_device.a in main devel subpackage, those are
  always statically linked.

* Thu Jul 30 2015 Simone Caronni <negativo17@gmail.com> - 1:7.0.28-1
- Update to 7.0.28 + cuFFT 7.0.35 patch.
- Rework provides/obsoletes for every package, following the original Nvidia
  CUDA 7.5 repository layout.
- Remove all vestiges of 32 bit binaries.
- Add pkg-config files from Nvidia RPMs (not available in makeself installers).
- Removed Open64.
- The check for GCC 4.9+ has been removed. It works on GCC 5.1 but only if C++11
  is not enabled.
- Build requires execstack in place of prelink on Fedora 23+.

* Wed Apr 15 2015 Simone Caronni <negativo17@gmail.com> - 1:6.5.19-5
- Remove native cairo libraries from Java programs.
- Add samples sub package.
- Rework script to generate tarballs. Also i386 headers are a subset of x86_64
  headers.

* Tue Jan 27 2015 Simone Caronni <negativo17@gmail.com> - 1:6.5.19-4
- Enable GCC version 4.9.

* Mon Jan 12 2015 Simone Caronni <negativo17@gmail.com> - 1:6.5.19-3
- Fix csh environment files and add CUDA_INC_PATH to both sh/csh environment
  profiles (thanks Jans Springer).

* Mon Nov 10 2014 Simone Caronni <negativo17@gmail.com> - 1:6.5.19-2
- Filter out libraries in the stubs directory.

* Thu Nov 06 2014 Simone Caronni <negativo17@gmail.com> - 1:6.5.19-1
- Update to 6.5.19.

* Mon Jul 28 2014 Simone Caronni <negativo17@gmail.com> - 1:6.0.37-3
- Fix Nvidia Open64.

* Sun Jul 20 2014 Simone Caronni <negativo17@gmail.com> - 1:6.0.37-2
- Fix rpmlint errors.

* Mon Jul 14 2014 Simone Caronni <negativo17@gmail.com> - 1:6.0.37-1
- First build.
