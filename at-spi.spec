Summary:	Assistive Technology Service Provider Interface
Name:		at-spi
Version:	1.0.2
Release:	1
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/2.0.1/sources/%{name}/%{name}-%{version}.tar.bz2
URL:		http://developer.gnome.org/projects/gap
BuildRequires:	gtk-doc >= 0.9-2
BuildRequires:	libbonobo-devel >= 2.0.0
BuildRequires:	gail-devel >= 0.17
BuildRequires:	gtk+2-devel >= 2.0.6
BuildRequires:	atk-devel >= 1.0.3
BuildRequires:	popt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	libat-spi1

%define		_prefix		/usr/X11R6
%define		_gtkdocdir 	%{_defaultdocdir}/gtk-doc/html

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

%package devel
Summary:	at-spi development files
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}
Requires:	gtk-doc-common
Obsoletes:	libat-spi1-devel

%description devel
at-spi development files.

%package static
Summary:	at-spi static library
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
at-spi static library.

%prep
%setup -q

%build
%{configure} \
	--with-html-path=%{_gtkdocdir} \
	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir} \
	pkgconfigdir=%{_pkgconfigdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
#%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so.*.*
%attr(755,root,root) %{_libdir}/at-spi-registryd
%{_libdir}/bonobo/servers/*
%attr(755,root,root) %{_libdir}/orbit-2.0/*.??
%{_datadir}/idl/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%attr(755,root,root) %{_libdir}/*.la
%{_includedir}/*
%doc %{_gtkdocdir}/*
%{_pkgconfigdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
