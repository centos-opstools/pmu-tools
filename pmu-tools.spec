Name:           pmu-tools
Version:        109
Release:        3%{?dist}
Summary:        Intel PMU profiling tools

License:        GPLv2 and BSD
# jevents subdir is BSD licensed
URL:            https://github.com/andikleen/pmu-tools
Source0:        https://github.com/andikleen/%{name}/archive/r%{version}.tar.gz#/%{name}-%{version}.tar.gz

# pmu-data is BSD licensed, see
# https://download.01.org/perfmon/readme.txt
Source1:        https://download.01.org/perfmon/perfmon_server_events_v1.3.zip
# non-versioned(!) mapping file to map server events to cpu generations
Source2:        https://download.01.org/perfmon/mapfile.csv

ExclusiveArch:  x86_64

BuildRequires:  gcc
BuildRequires:  gcc-c++

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

%package -n pmu-data
Summary: data files for pmu-tools

%description -n pmu-data
data files for pmu-tools


%prep
%autosetup -n %{name}-r%{version}
unzip %SOURCE1

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

pushd perfmon_server_events_v1.3
mkdir -p %{buildroot}%{_datadir}/perfmon
cp -r * %{buildroot}%{_datadir}/perfmon
cp %SOURCE2 %{buildroot}%{_datadir}/perfmon
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

%files -n pmu-data
%{_datadir}/perfmon



%changelog
* Thu Feb 03 2022 Emma Foley <efoley@redhat.com> - 109-3
- Bump release to trigger builds on CentOS Stream 8 & 9

* Fri Jun 26 2020 Matthias Runge <mrunge@redhat.com> - 109-2
- add the mapping file mapping.csv
- bump server events to version 1.3

* Thu Jun 06 2019 Matthias Runge <mrunge@redhat.com> - 108-4
- add pmu-data to pmu-tools, required for collectd-pmu

* Tue May 07 2019 Matthias Runge <mrunge@redhat.com> - 108-3
- fix .a file location, fix license (rhbz#1705981)
- add provides for -static jevents lib

* Fri May 03 2019 Matthias Runge <mrunge@redhat.com> - 108-1
- initial packaging
