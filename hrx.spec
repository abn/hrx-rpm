%global debug_package %{nil}

Name:           hrx
Version:        0.3.0
Release:        1%{?dist}
Summary:        Hip Runtime Extended (HRX) runtime for AMD NPU and GPU

License:        Apache-2.0 WITH LLVM-exception
URL:            https://github.com/ROCm/hrx-system
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.26
BuildRequires:  ninja-build
BuildRequires:  python3
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  libdrm-devel
BuildRequires:  systemd-devel

Provides:       libhrx = %{version}-%{release}

%description
HRX (Hip Runtime Extended) is a collection of minimal runtime components
providing low-latency, high-performance integration across AMD NPU, GPU,
and CPU hardware architectures.

%package devel
Summary:        Development headers and CMake configuration for HRX
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libhrx-devel = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%description devel
Development headers, static interface definitions, and CMake targets for
compiling applications against the HRX runtime API.

%package -n hrx-hip
Summary:        HIP compatibility runtime layer powered by HRX
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libamdhip64 = %{version}-%{release}

%description -n hrx-hip
HIP (Heterogeneous-Compute Interface for Portability) drop-in compatibility
layer implemented on top of the HRX streaming runtime.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -S hrx-system -B %{_vpath_builddir} \
    -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DBUILD_SHARED_LIBS=OFF \
    -DLIBHRX_BUILD=ON \
    -DLIBHRX_BUILD_HIP_BINDING=ON \
    -DIREE_HAL_DRIVER_AMDGPU=OFF \
    -DIREE_BUILD_TESTS=OFF \
    -DIREE_BUILD_BENCHMARKS=OFF \
    -DLOOM_BUILD=OFF \
    -DIREE_ENABLE_WERROR_FLAG=OFF

%cmake_build

%install
DESTDIR=%{buildroot} cmake --install %{_vpath_builddir} --component HrxPublicDist

%files
%license hrx-system/LICENSE
%doc hrx-system/README.md
%{_bindir}/hrx-info
%{_libdir}/libhrx.so.0*

%files devel
%{_includedir}/hrx/
%{_libdir}/libhrx.so
%{_libdir}/cmake/hrx/

%files -n hrx-hip
%{_libdir}/libamdhip64.so.*
%{_libdir}/libamdhip64.so

%changelog
* Mon Aug 17 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.1.0-1
- new package built with tito

* Mon Aug 17 2026 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.1.0-1
- Initial packaging of HRX (ROCm/hrx-system)
