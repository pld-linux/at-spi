#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Assistive Technology Service Provider Interface
Summary(pl.UTF-8):	Interfejs pozwalający na korzystanie z urządzeń wspomagających
Name:		at-spi
Version:	1.22.0
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/at-spi/1.22/%{name}-%{version}.tar.bz2
# Source0-md5:	85dc343588016ecf854830fab0cd6fdc
URL:		http://developer.gnome.org/projects/gap/
BuildRequires:	ORBit2-devel >= 2.14.10
BuildRequires:	atk-devel >= 1:1.22.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gail-devel >= 1.22.0
BuildRequires:	gettext-devel
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gtk+2-devel >= 2:2.12.8
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	intltool >= 0.36.2
BuildRequires:	libbonobo-devel >= 2.20.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	xorg-lib-libXevie-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1
BuildRequires:	xorg-lib-libXtst-devel
Obsoletes:	libat-spi1
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
AT-SPI allows assistive technologies to access GTK-based applications.
Essentially it exposes the internals of applications for automation,
so tools such as screen readers, magnifiers, or even scripting
interfaces can query and interact with GUI controls.

%description -l pl.UTF-8
AT-SPI pozwala na korzystanie z urządzeń wspomagających w celu dostępu
do aplikacji bazujących na GTK. Przede wszystkim udostępnia wewnętrzne
interfejsy aplikacji dla automatyzacji, więc urządzenia takie jak
czytniki ekranu, lupy, czy nawet interfejsy skryptowe mogą odpytywać i
współpracować z kontrolkami interfejsu graficznego.

%package devel
Summary:	AT-SPI development files
Summary(pl.UTF-8):	Pliki programistyczne AT-SPI
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ORBit2-devel >= 2.14.10
Requires:	atk-devel >= 1:1.22.0
Requires:	gtk+2-devel >= 2:2.12.8
Requires:	libbonobo-devel >= 2.20.0
Obsoletes:	libat-spi1-devel

%description devel
AT-SPI development files.

%description devel -l pl.UTF-8
Pliki programistyczne AT-SPI.

%package static
Summary:	AT-SPI static library
Summary(pl.UTF-8):	Statyczna biblioteka AT-SPI
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
AT-SPI static library.

%description static -l pl.UTF-8
Statyczna biblioteka AT-SPI.

%package apidocs
Summary:	AT-SPI API documentation
Summary(pl.UTF-8):	Dokumentacja API AT-SPI
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
AT-SPI API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API AT-SPI.

%package -n python-pyatspi
Summary:	AT-SPI Python bindings
Summary(pl.UTF-8):	Wiązania AT-SPI dla Pythona
Group:		Development/Languages/Python
Requires:	python-pyorbit

%description -n python-pyatspi
AT-SPI Python bindings.

%description -n python-pyatspi -l pl.UTF-8
Wiązania AT-SPI dla Pythona.

%prep
%setup -q

%build
%{__glib_gettextize}
%{__intltoolize}
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

%py_postclean

[ -d $RPM_BUILD_ROOT%{_datadir}/locale/sr@latin ] || \
	mv -f $RPM_BUILD_ROOT%{_datadir}/locale/sr@{Latn,latin}
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcspi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcspi.so.0
%attr(755,root,root) %{_libdir}/libloginhelper.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libloginhelper.so.0
%attr(755,root,root) %{_libdir}/libspi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libspi.so.0
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/at-spi-registryd
%attr(755,root,root) %{_libdir}/orbit-2.0/Accessibility_LoginHelper_module.so
%attr(755,root,root) %{_libdir}/orbit-2.0/Accessibility_module.so
%attr(755,root,root) %{_libdir}/gtk-2.0/modules/libatk-bridge.so
%{_libdir}/bonobo/servers/Accessibility_Registry.server
%{_datadir}/idl/at-spi-1.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcspi.so
%attr(755,root,root) %{_libdir}/libloginhelper.so
%attr(755,root,root) %{_libdir}/libspi.so
%{_includedir}/at-spi-1.0
%{_libdir}/libcspi.la
%{_libdir}/libloginhelper.la
%{_libdir}/libspi.la
%{_pkgconfigdir}/cspi-1.0.pc
%{_pkgconfigdir}/libloginhelper-1.0.pc
%{_pkgconfigdir}/libspi-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcspi.a
%{_libdir}/libloginhelper.a
%{_libdir}/libspi.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/at-spi-cspi
%{_docdir}/%{name}-%{version}

%files -n python-pyatspi
%defattr(644,root,root,755)
%dir %{py_sitedir}/pyatspi
%{py_sitedir}/pyatspi/*.py[co]
