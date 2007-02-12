#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Assistive Technology Service Provider Interface
Summary(pl.UTF-8):	Interfejs pozwalający na korzystanie z urządzeń wspomagających
Name:		at-spi
Version:	1.7.15
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/at-spi/1.7/%{name}-%{version}.tar.bz2
# Source0-md5:	b8af15556d24e850feb2ffb40eda1d31
URL:		http://developer.gnome.org/projects/gap/
BuildRequires:	ORBit2-devel >= 2.14.4
BuildRequires:	atk-devel >= 1:1.12.4
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gail-devel >= 1.9.3
BuildRequires:	gnome-common >= 2.12.0
BuildRequires:	gtk+2-devel >= 2:2.10.7
BuildRequires:	gtk-doc >= 1.7
BuildRequires:	intltool
BuildRequires:	libbonobo-devel >= 2.16.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	xorg-lib-libXft-devel >= 2.1
BuildRequires:	xorg-lib-libXtst-devel
Obsoletes:	libat-spi1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

%description -l pl.UTF-8
at-spi pozwala na korzystanie z urządzeń wspomagających w celu dostępu
do aplikacji bazujących na GTK. Przede wszystkim udostępnia wewnętrzne
interfejsy aplikacji dla automatyzacji, więc urządzenia takie jak
czytniki ekranu, lupy, czy nawet interfejsy skryptowe mogą odpytywać i
współpracować z kontrolkami interfejsu graficznego.

%package devel
Summary:	at-spi development files
Summary(pl.UTF-8):	Pliki programistyczne at-spi
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ORBit2-devel >= 2.14.4
Requires:	atk-devel >= 1:1.12.4
Requires:	gail-devel >= 1.9.3
Requires:	gtk+2-devel >= 2:2.10.7
Requires:	libbonobo-devel >= 2.16.0
Obsoletes:	libat-spi1-devel

%description devel
at-spi development files.

%description devel -l pl.UTF-8
Pliki programistyczne at-spi.

%package static
Summary:	at-spi static library
Summary(pl.UTF-8):	Statyczna biblioteka at-spi
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
at-spi static library.

%description static -l pl.UTF-8
Statyczna biblioteka at-spi.

%package apidocs
Summary:	at-spi API documentation
Summary(pl.UTF-8):	Dokumentacja API at-spi
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
at-spi API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API at-spi.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	%{!?with_static_libs:--disable-static} \
	--enable-gtk-doc \
	--enable-static \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

# no static modules
rm -f $RPM_BUILD_ROOT%{_libdir}/{gtk-2.0/modules,orbit-2.0}/*.{la,a}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/at-spi-registryd
%attr(755,root,root) %{_libdir}/orbit-2.0/*.so
%attr(755,root,root) %{_libdir}/gtk-2.0/modules/lib*.so
%{_libdir}/bonobo/servers/*
%{_datadir}/idl/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_pkgconfigdir}/*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/*
%{_docdir}/%{name}-%{version}
