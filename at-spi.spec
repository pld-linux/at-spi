Summary:	Assistive Technology Service Provider Interface
Name:		at-spi
Version:	1.0.1
Release:	2
Group:		X11/-
License:	GPL
Source0:	ftp://ftp.gnome.org/pub/gnome/pre-gnome2/sources/%{name}/%{name}-%{version}.tar.bz2
URL:		http://developer.gnome.org/projects/gap
BuildRequires:	gtk-doc >= 0.9-2
BuildRequires:	libbonobo-devel >= 2.0.0
BuildRequires:	gail-devel >= 0.13
BuildRequires:	gtk+2-devel >= 2.0.3
BuildRequires:	atk-devel >= 1.0.2
BuildRequires:	popt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_gtkdocdir 	%{_defaultdocdir}/gtk-doc/html

%description
This is the Early Access Release of the Gnome Accessibility Project's           
Assistive Technology Service Provider Interface. 

%package devel
Summary:	at-spi devel files
Group:		-
Requires:	%{name} = %{version}
Requires:	gtk-doc-common

%description devel

%package static
Summary:	at-spi static library
Group:		-
Requires:	%{name}-devel = %{version}

%description static

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
