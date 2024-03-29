#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	Assistive Technology Service Provider Interface
Summary(pl.UTF-8):	Interfejs pozwalający na korzystanie z urządzeń wspomagających
Name:		at-spi
Version:	1.32.0
Release:	9
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/at-spi/1.32/%{name}-%{version}.tar.bz2
# Source0-md5:	bc62c41f18529d56271fa1ae6cad8629
Patch0:		%{name}-format.patch
Patch1:		%{name}-gtkdoc.patch
Patch2:		%{name}-ac.patch
URL:		http://developer.gnome.org/projects/gap/
BuildRequires:	GConf2-devel >= 2.24.0
BuildRequires:	ORBit2-devel >= 2.14.10
BuildRequires:	atk-devel >= 1:1.30.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gtk+2-devel >= 2:2.20.0
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libbonobo-devel >= 2.24.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	python >= 1:2.4
BuildRequires:	python-modules >= 1:2.4
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXtst-devel
Requires(post,preun):	GConf2
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package libs
Summary:	Base at-spi libraries and modules
Summary(pl.UTF-8):	Podstawowe biblioteki i moduły at-spi
Group:		Libraries
Obsoletes:	libat-spi1

%description libs
Base at-spi libraries and modules.

%description libs -l pl.UTF-8
Podstawowe biblioteki i moduły at-spi.

%package devel
Summary:	AT-SPI development files
Summary(pl.UTF-8):	Pliki programistyczne AT-SPI
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	ORBit2-devel >= 2.14.10
Requires:	atk-devel >= 1:1.30.0
Requires:	gtk+2-devel >= 2:2.20.0
Requires:	libbonobo-devel >= 2.24.0
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
BuildArch:	noarch

%description apidocs
AT-SPI API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API AT-SPI.

%package -n python-pyatspi_corba
Summary:	AT-SPI Python bindings
Summary(pl.UTF-8):	Wiązania AT-SPI dla Pythona
Group:		Development/Languages/Python
Requires:	python-pyorbit
# python-pyatspi 2 is new, at-spi2 based implementation
Obsoletes:	python-pyatspi < 2
Obsoletes:	python-pyspi

%description -n python-pyatspi_corba
AT-SPI Python bindings.

%description -n python-pyatspi_corba -l pl.UTF-8
Wiązania AT-SPI dla Pythona.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-compile-warnings=minimum \
	--enable-gtk-doc \
	--enable-relocate \
	%{__enable_disable static_libs static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

# no static modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{gtk-2.0/modules/at-spi-corba/modules,orbit-2.0}/*.{la,a}
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{sr@ije,sr@ijekavian}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install at-spi.schemas

%preun
%gconf_schema_uninstall at-spi.schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%{_sysconfdir}/gconf/schemas/at-spi.schemas
%{_sysconfdir}/xdg/autostart/at-spi-registryd.desktop
%{_datadir}/idl/at-spi-1.0

%files libs
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README TODO
%attr(755,root,root) %{_libdir}/libcspi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcspi.so.0
%attr(755,root,root) %{_libdir}/libloginhelper.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libloginhelper.so.0
%attr(755,root,root) %{_libdir}/libspi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libspi.so.0
%attr(755,root,root) %{_libexecdir}/at-spi-registryd
%attr(755,root,root) %{_libdir}/orbit-2.0/Accessibility_LoginHelper_module.so
%attr(755,root,root) %{_libdir}/orbit-2.0/Accessibility_module.so
%dir %{_libdir}/gtk-2.0/modules/at-spi-corba
%dir %{_libdir}/gtk-2.0/modules/at-spi-corba/modules
%attr(755,root,root) %{_libdir}/gtk-2.0/modules/at-spi-corba/modules/libatk-bridge.so
%{_libdir}/bonobo/servers/Accessibility_Registry.server

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcspi.so
%attr(755,root,root) %{_libdir}/libloginhelper.so
%attr(755,root,root) %{_libdir}/libspi.so
%{_includedir}/at-spi-1.0
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

%files -n python-pyatspi_corba
%defattr(644,root,root,755)
%dir %{py_sitedir}/pyatspi_corba
%{py_sitedir}/pyatspi_corba/*.py[co]
