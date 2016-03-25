%global         debug_package %{nil}
#global         __strip /bin/true

# Todo: filter libunixfile_1_0_0.so from cuda-nsight.

Name:           cuda
Version:        7.5.18
Release:        4%{?dist}
Summary:        NVIDIA Compute Unified Device Architecture Toolkit
Epoch:          1
License:        NVIDIA License
URL:            https://developer.nvidia.com/cuda-zone
ExclusiveArch:  %{ix86} x86_64

# See Source1 for tarball generation - saves ~400Mb.
Source0:        %{name}-%{version}-x86_64.tar.xz
Source1:        %{name}-generate-tarballs.sh

Source3:        %{name}.sh
Source4:        %{name}.csh
Source5:        nsight.desktop
Source6:        nvvp.desktop
Source7:        http://docs.nvidia.com/cuda/pdf/CUDA_Toolkit_Release_Notes.pdf

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
Source30:       nppi.pc
Source31:       npps.pc
Source32:       nvrtc.pc
Source33:       nvToolsExt.pc

BuildRequires:  desktop-file-utils
# For RUNPATH removal
BuildRequires:  chrpath
# For execstack removal
%if 0%{?fedora} >= 23 || 0%{?rhel} > 7
BuildRequires:  execstack
%else
BuildRequires:  prelink
%endif

Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-7-5 = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-core-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-core-7-5 = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-minimal-build-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-minimal-build-7-5 = %{?epoch}:%{version}-%{release}

%description
CUDA is a parallel computing platform and programming model that enables
dramatic increases in computing performance by harnessing the power of the
graphics processing unit (GPU).

%package cli-tools
Summary:        Compute Unified Device Architecture command-line tools
Requires:       %{name} = %{?epoch}:%{version}-%{release}
Requires:       %{name}-devel = %{?epoch}:%{version}-%{release}
Requires:       expat >= 1.95
Obsoletes:      %{name}-command-line-tools-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-command-line-tools-7-5 = %{?epoch}:%{version}-%{release}

%description cli-tools
Contains the command line tools to debug and profile CUDA applications.

%package libs
Summary:        Compute Unified Device Architecture native run-time library
Requires(post): ldconfig
Obsoletes:      %{name}-license-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-license-7-5 = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-cudart-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-cudart-7-5 = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-core-libs-7-5 < %{?epoch}:%{version}
Provides:       %{name}-core-libs-7-5 = %{?epoch}:%{version}

%description libs
Contains the CUDA run-time library required to run CUDA application natively.

%package extra-libs
Summary:        Compute Unified Device Architecture native libraries
Requires(post): ldconfig
Obsoletes:      %{name}-cublas-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-cublas-7-5 = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-cudart-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-cudart-7-5 = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-cufft-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-cufft-7-5 = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-curand-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-curand-7-5 = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-cusolver-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-cusolver-7-5 = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-cusparse-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-cusparse-7-5 = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-npp-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-npp-7-5 = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-nvrtc-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-nvrtc-7-5 = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-runtime-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-runtime-7-5 = %{?epoch}:%{version}-%{release}

%description extra-libs
Native CUDA platform libraries (CUBLAS, CUFFT, CURAND, CUSPARSE, NPP, Thrust).

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{_isa} = %{?epoch}:%{version}-%{release}
Requires:       %{name}-libs%{_isa} = %{?epoch}:%{version}-%{release}
Requires:       %{name}-extra-libs%{_isa} = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-headers-7-5 < %{?epoch}:%{version}
Provides:       %{name}-headers-7-5 = %{?epoch}:%{version}
Obsoletes:      %{name}-cublas-dev-7-5 < %{?epoch}:%{version}
Provides:       %{name}-cublas-dev-7-5 = %{?epoch}:%{version}
Obsoletes:      %{name}-cudart-dev-7-5 < %{?epoch}:%{version}
Provides:       %{name}-cudart-dev-7-5 = %{?epoch}:%{version}
Obsoletes:      %{name}-cufft-dev-7-5 < %{?epoch}:%{version}
Provides:       %{name}-cufft-dev-7-5 = %{?epoch}:%{version}
Obsoletes:      %{name}-curand-dev-7-5 < %{?epoch}:%{version}
Provides:       %{name}-curand-dev-7-5 = %{?epoch}:%{version}
Obsoletes:      %{name}-cusolver-dev-7-5 < %{?epoch}:%{version}
Provides:       %{name}-cusolver-dev-7-5 = %{?epoch}:%{version}
Obsoletes:      %{name}-cusparse-dev-7-5 < %{?epoch}:%{version}
Provides:       %{name}-cusparse-dev-7-5 = %{?epoch}:%{version}
Obsoletes:      %{name}-npp-dev-7-5 < %{?epoch}:%{version}
Provides:       %{name}-npp-dev-7-5 = %{?epoch}:%{version}
Obsoletes:      %{name}-nvrtc-dev-7-5 < %{?epoch}:%{version}
Provides:       %{name}-nvrtc-dev-7-5 = %{?epoch}:%{version}
Obsoletes:      %{name}-toolkit-7-5 < %{?epoch}:%{version}
Provides:       %{name}-toolkit-7-5 = %{?epoch}:%{version}

%description devel
This package provides the development files of the %{name} package.

%package static
Summary:        Static libraries for %{name}
Requires:       %{name}-devel%{_isa} = %{?epoch}:%{version}-%{release}

%description static
This package provides static archives for normal CUDA libraries.

%package docs
Summary:        Compute Unified Device Architecture toolkit documentation
BuildArch:      noarch
Obsoletes:      %{name}-documentation-7-5 < %{?epoch}:%{version}
Provides:       %{name}-documentation-7-5 = %{?epoch}:%{version}

%description docs
Contains all guides and library documentation for CUDA.

%package samples
Summary:        Compute Unified Device Architecture toolkit samples
BuildArch:      noarch
Obsoletes:      %{name}-samples-7-5 < %{?epoch}:%{version}
Provides:       %{name}-samples-7-5 = %{?epoch}:%{version}
Requires:       cuda-devel = %{?epoch}:%{version}
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
Requires:       %{name} = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-visual-tools-7-5 < %{?epoch}:%{version}-%{release}
Provides:       %{name}-visual-tools-7-5 = %{?epoch}:%{version}-%{release}

%description nsight
NVIDIA Nsight Eclipse Edition is a full-featured IDE powered by the Eclipse
platform that provides an all-in-one integrated environment to edit, build,
debug and profile CUDA-C applications. Nsight Eclipse Edition supports a rich
set of commercial and free plugins.

%package nvvp
Summary:        NVIDIA Visual Profiler
Requires:       %{name} = %{?epoch}:%{version}-%{release}

%description nvvp
The NVIDIA Visual Profiler is a cross-platform performance profiling tool that
delivers developers vital feedback for optimizing CUDA C/C++ applications.


%prep
%setup -q -n %{name}-%{version}-x86_64

# Remove execstack on binaries
execstack -c nvvm/bin/cicc nvvm/%{_lib}/*

# Remove RUNPATH on binaries
#chrpath -d {libnsight,libnvvp}/libcairo-swt.so
chrpath -d nvvm/bin/cicc

# RPMlint issues
find . -name "*.h" -exec chmod 644 {} \;
find . -name "*.bat" -delete
find . -size 0 -delete

# Works also with GCC 4.9+ but only if C++11 is not enabled
sed -i -e '/#error -- unsupported GNU version!/d' include/host_config.h

# Remove double quotes in samples' Makefiles (cosmetical)
find samples -name "Makefile" -exec sed -i -e 's|"/usr"|/usr|g' {} \;

# Remove unused stuff
rm -f doc/man/man1/cuda-install-samples-7.5.sh.1
rm -f samples/uninstall_cuda_samples_7.5.pl
rm -f samples/.uninstall_manifest_do_not_delete.txt
rm -f bin/uninstall_cuda_toolkit_7.5.pl
rm -f bin/cuda-install-samples-7.5.sh
rm -f bin/.uninstall_manifest_do_not_delete.txt

%build
# Nothing to build

%install
# Create empty tree
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}%{_datadir}/cuda/
mkdir -p %{buildroot}%{_datadir}/libnsight/
mkdir -p %{buildroot}%{_datadir}/libnvvp/
mkdir -p %{buildroot}%{_datadir}/pixmaps/
mkdir -p %{buildroot}%{_includedir}/%{name}/
mkdir -p %{buildroot}/%{_libdir}/pkgconfig
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
# This man page conflicts *a lot* of other packages
mv %{buildroot}%{_mandir}/man3/deprecated.3.gz \
    %{buildroot}%{_mandir}/man3/cuda_deprecated.3.gz

# Docs
mv extras/CUPTI/Readme.txt extras/CUPTI/Readme-CUPTI.txt
mv extras/Debugger/Readme.txt extras/Debugger/Readme-Debugger.txt
cp %{SOURCE7} .

# Headers
cp -fr src %{buildroot}%{_includedir}/%{name}/fortran/
cp -fr include/* nvvm/include/* %{buildroot}%{_includedir}/%{name}/
cp -fr extras/CUPTI/include %{buildroot}%{_includedir}/%{name}/CUPTI/
cp -fr extras/Debugger/include %{buildroot}%{_includedir}/%{name}/Debugger/

# Libraries
cp -fr %{_lib}/* nvvm/%{_lib}/* %{buildroot}%{_libdir}/
cp -fr extras/CUPTI/%{_lib}/* %{buildroot}%{_libdir}/
cp -fr nvvm/libdevice/* %{buildroot}%{_datadir}/%{name}/

# Fix duplicate libraries
rm -f %{buildroot}%{_libdir}/libOpenCL.so*

# pkg-config files
install -pm 644 %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} \
    %{SOURCE25} %{SOURCE26} %{SOURCE27} %{SOURCE28} %{SOURCE29} %{SOURCE30} \
    %{SOURCE31} %{SOURCE32} %{SOURCE33} %{buildroot}/%{_libdir}/pkgconfig
sed -i -e 's/CUDA_VERSION/7.5/g' %{buildroot}/%{_libdir}/pkgconfig/*.pc

# Binaries
cp -fr bin/* nvvm/bin/* %{buildroot}%{_bindir}/

# Additional samples
mv extras/CUPTI/sample samples/CUPTI

# Java stuff
sed -i -e '/^-vm/d' -e '/jre\/bin\/java/d' libnsight/nsight.ini libnvvp/nvvp.ini

install -m 644 -p libnsight/icon.xpm %{buildroot}%{_datadir}/pixmaps/nsight.xpm
install -m 644 -p libnvvp/icon.xpm %{buildroot}%{_datadir}/pixmaps/nvvp.xpm
rm -f libnsight/icon.xpm libnvvp/icon.xpm

cp -fr libnsight %{buildroot}%{_libdir}/nsight
cp -fr libnvvp %{buildroot}%{_libdir}/nvvp

ln -sf %{_libdir}/nsight/nsight %{buildroot}%{_bindir}/
ln -sf %{_libdir}/nvvp/nvvp %{buildroot}%{_bindir}/

desktop-file-install --dir %{buildroot}%{_datadir}/applications/ %{SOURCE5} %{SOURCE6}

# Only Fedora and RHEL 7+ desktop-file-validate binaries can check multiple
# desktop files at the same time
desktop-file-validate %{buildroot}%{_datadir}/applications/nsight.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/nvvp.desktop


%post -p /sbin/ldconfig

%post libs -p /sbin/ldconfig

%post extra-libs -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%postun extra-libs -p /sbin/ldconfig

%post nsight
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun nsight
%{_bindir}/update-desktop-database &> /dev/null || :

%post nvvp
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun nvvp
%{_bindir}/update-desktop-database &> /dev/null || :


%files
%{_bindir}/bin2c
%{_bindir}/cicc
# FIXME, there should be no folder there, but binaries look for things here
%{_bindir}/crt/
%{_bindir}/cudafe
%{_bindir}/cudafe++
%{_bindir}/cuobjdump
%{_bindir}/fatbinary
%{_bindir}/filehash
%{_bindir}/nvcc
%{_bindir}/nvlink
%{_bindir}/nvprune
%{_bindir}/ptxas
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
%{_mandir}/man1/cuda-gdb.*
%{_mandir}/man1/cuda-gdbserver.*
%{_mandir}/man1/cuda-memcheck.*
%{_mandir}/man1/nvdisasm.*
%{_mandir}/man1/nvprof.*

%files libs
%{_libdir}/libcudart.so.*
%{_libdir}/libcuinj%{__isa_bits}.so.*
%{_libdir}/libnvToolsExt.so.*
%{_libdir}/libnvvm.so.*

%files extra-libs
%{_libdir}/libcupti.so.*
%{_libdir}/libcublas.so.*
%{_libdir}/libcufft.so.*
%{_libdir}/libcufftw.so.*
%{_libdir}/libcurand.so.*
%{_libdir}/libcusolver.so.*
%{_libdir}/libcusparse.so.*
%{_libdir}/libnppc.so.*
%{_libdir}/libnppi.so.*
%{_libdir}/libnpps.so.*
%{_libdir}/libnvblas.so.*
%{_libdir}/libnvrtc.so.*
%{_libdir}/libnvrtc-builtins.so.*

%files devel
%doc extras/CUPTI/Readme-CUPTI.txt
%doc extras/Debugger/Readme-Debugger.txt
%{_includedir}/%{name}/
%{_libdir}/libcudadevrt.a
%{_libdir}/libcublas_device.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
%{_mandir}/man7/*

%files static
%{_libdir}/libcublas_static.a
%{_libdir}/libcudart_static.a
%{_libdir}/libcufft_static.a
%{_libdir}/libcufftw_static.a
%{_libdir}/libculibos.a
%{_libdir}/libcurand_static.a
%{_libdir}/libcusolver_static.a
%{_libdir}/libcusparse_static.a
%{_libdir}/libnppc_static.a
%{_libdir}/libnppi_static.a
%{_libdir}/libnpps_static.a

%files docs
%doc doc/pdf doc/html tools/*
%doc *.pdf

%files samples
%doc samples/*
%doc nvvm/libnvvm-samples

%files nsight
%{_bindir}/nsight
%{_libdir}/nsight
%{_datadir}/applications/nsight.desktop
%{_datadir}/pixmaps/nsight.xpm
%{_mandir}/man1/nsight.*

%files nvvp
%{_bindir}/computeprof
%{_bindir}/nvvp
%{_libdir}/nvvp
%{_datadir}/applications/nvvp.desktop
%{_datadir}/pixmaps/nvvp.xpm
%{_mandir}/man1/nvvp.*

%changelog
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
