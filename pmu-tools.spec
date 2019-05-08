Name:           pmu-tools
Version:        108
Release:        3%{?dist}
Summary:        Intel PMU profiling tools

License:        GPLv2 and BSD
URL:            https://github.com/andikleen/pmu-tools
Source0:        https://github.com/andikleen/%{name}/archive/r%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-g++

%description
pmu tools is a collection of tools for profile collection and performance
analysis on Intel CPUs on top of Linux perf. This uses performance counters
in the CPU.

%package -n jevents
Summary: Library to make access to the kernel Linux perf interface easier

%description -n jevents

jevents is a C library to use from C programs to make access to the kernel
Linux perf interface easier. It also includes some examples to use the
library.

%package -n jevents-devel
Summary: Development files to build against jevents library

Provides: jevents-static = %{version}-%{release}

Requires: jevents = %{version}-%{release}
%description -n jevents-devel
%{summary}


%prep
%autosetup -n %{name}-r%{version}

pushd jevents
sed -i -e 's|PREFIX=.*|PREFIX= %{buildroot}/usr|' Makefile
popd

%build
make

pushd jevents
make
popd

%install

pushd jevents
%make_install
popd


%files
%license COPYING
%doc README.md

%files -n jevents
%license COPYING
%doc jevents/README.md
%{_bindir}/event-rmap
%{_bindir}/listevents
%{_bindir}/showevent

%files -n jevents-devel
%{_includedir}/jevents.h
%{_includedir}/jsession.h
%{_includedir}/measure.h
%{_includedir}/perf-iter.h
%{_includedir}/rdpmc.h
%{_libdir}/libjevents.a


%changelog
* Tue May 07 2019 Matthias Runge <mrunge@redhat.com> - 108-3
- fix .a file location, fix license (rhbz#1705981)
- add provides for -static jevents lib

* Fri May 03 2019 Matthias Runge <mrunge@redhat.com> - 108-1
- initial packaging
