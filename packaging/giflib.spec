%bcond_with wayland

Name:           giflib
Version:        4.1.6
Release:        9
License:        MIT
Summary:        Library for manipulating GIF format image files
Url:            http://sourceforge.net/projects/giflib/
Group:          System/Libraries
Source0:        http://downloads.sourceforge.net/giflib/%{name}-%{version}.tar.bz2
Source1001: 	giflib.manifest
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)
%if %{with wayland}

%else
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xv)
%endif

%description
The giflib package contains a shared library of functions for
loading and saving GIF format image files.  It is API and ABI compatible
with libungif, the library which supported uncompressed GIFs while the
Unisys LZW patent was in effect.

Install the giflib package if you need to write programs that use GIF files.
You should also install the giflib-utils package if you need some simple
utilities to manipulate GIFs.

%package devel
Summary:        Development tools for programs which will use the libungif library
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
This package contains the static libraries, header files and
documentation necessary for development of programs that will use the
giflib library to load and save GIF format image files.

You should install this package if you need to develop programs which
will use giflib library functions.  You'll also need to install the
giflib package.

%package utils
Summary:        Programs for manipulating GIF format image files
Group:          Applications/Multimedia
Requires:       %{name} = %{version}

%description utils
The giflib-utils package contains various programs for manipulating
GIF format image files.

Install this package if you need to manipulate GIF format image files.
You'll also need to install the giflib package.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%configure  \
%if %{with wayland}
  --disable-x11
%endif

make %{?_smp_mflags} all

MAJOR=`echo '%{version}' | sed 's/\([0-9]\+\)\..*/\1/'`
gcc %{optflags} -shared -Wl,-soname,libungif.so.$MAJOR -Llib/.libs -lgif -o libungif.so.%{version}

%install
%make_install

install -m 0755 -p libungif.so.%{version} %{buildroot}%{_libdir}
ln -sf libungif.so.%{version} %{buildroot}%{_libdir}/libungif.so.4
ln -sf libungif.so.4 %{buildroot}%{_libdir}/libungif.so


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%{_libdir}/lib*.so.*

%files devel
%manifest %{name}.manifest
%{_libdir}/lib*.so
%{_includedir}/*.h

%files utils
%manifest %{name}.manifest
%{_bindir}/*
