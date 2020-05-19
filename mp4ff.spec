#
# Conditional build:
%bcond_without	static_libs	# static libraries

Summary:	MP4 file format library from FAAD2 project
Summary(pl.UTF-8):	Biblioteka formatu plików MP4 z projektu FAAD2
Name:		mp4ff
Version:	2.8.8
Release:	1
License:	GPL v2+ or commercial
Group:		Applications/Sound
Source0:	http://downloads.sourceforge.net/faac/faad2-%{version}.tar.gz
# Source0-md5:	28f6116efdbe9378269f8a6221767d1f
Patch0:		faad2-mp4ff.patch
URL:		https://www.audiocoding.com/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool >= 2:1.4d-3
BuildRequires:	rpmbuild(macros) >= 1.721
Conflicts:	faad2-libs < 2.9.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MP4 file format library from FAAD2 project.

%description -l pl.UTF-8
Biblioteka formatu plików MP4 z projektu FAAD2.

%package devel
Summary:	Header files for mp4ff library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki mp4ff
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Conflicts:	faad2-devel < 2.9.0

%description devel
Header files for mp4ff library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki mp4ff.

%package static
Summary:	Static mp4ff library
Summary(pl.UTF-8):	Statyczna biblioteka mp4ff
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Conflicts:	faad2-static < 2.9.0

%description static
Static mp4ff library.

%description static -l pl.UTF-8
Statyczna biblioteka mp4ff.

%prep
%setup -q -n faad2-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--without-xmms \
	--without-mpeg4ip \
	%{!?with_static_libs:--disable-static}

%{__make} -C common/mp4ff

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C common/mp4ff install \
	DESTDIR=$RPM_BUILD_ROOT

# no external dependencies
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmp4ff.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmp4ff.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmp4ff.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmp4ff.so
%{_includedir}/mp4ff.h
%{_includedir}/mp4ffint.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmp4ff.a
%endif
