Summary:	Assistive Technology Service Provider Interface
Summary(pl):	Interfejs pozwalaj±cy na korzystanie z urz±dzeñ wspomagaj±cych
Name:		at-spi
Version:	1.6.0
Release:	1
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/1.6/%{name}-%{version}.tar.bz2
# Source0-md5:	950fc9bb66cf90b720739f3ea5ad8b18
URL:		http://developer.gnome.org/projects/gap/
BuildRequires:	ORBit2-devel
BuildRequires:	atk-devel >= 1:1.8.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gail-devel >= 1.8.0
BuildRequires:	gnome-common
BuildRequires:	gtk-doc >= 1.1
BuildRequires:	gtk+2-devel >= 2.2.3
BuildRequires:	libbonobo-devel >= 2.4.0
BuildRequires:	libtool
BuildRequires:	perl-base
BuildRequires:	popt-devel
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	xft-devel >= 2.1
Obsoletes:	libat-spi1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

%description -l pl
at-spi pozwala na korzystanie z urz±dzeñ wspomagaj±cych w celu dostêpu
do aplikacji bazuj±cych na GTK. Przede wszystkim udostêpnia wewnêtrzne
interfejsy aplikacji dla automatyzacji, wiêc urz±dzenia takie jak
czytniki ekranu, lupy, czy nawet interfejsy skryptowe mog± odpytywaæ i
wspó³pracowaæ z kontrolkami interfejsu graficznego.

%package devel
Summary:	at-spi development files
Summary(pl):	Pliki programistyczne at-spi
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	atk-devel >= 1:1.8.0
Requires:	gtk+2-devel >= 2.2.3
Requires:	gtk-doc-common
Requires:	libbonobo-devel >= 2.4.0
Obsoletes:	libat-spi1-devel

%description devel
at-spi development files.

%description devel -l pl
Pliki programistyczne at-spi.

%package static
Summary:	at-spi static library
Summary(pl):	Statyczna biblioteka at-spi
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
at-spi static library.

%description static -l pl
Statyczna biblioteka at-spi.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I %{_aclocaldir}/gnome2-macros
%{__automake}
%{__autoconf}
%configure \
	--enable-static \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

# no static modules
rm -f $RPM_BUILD_ROOT%{_libdir}/{gtk-2.0/modules,orbit-2.0}/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/at-spi-registryd
%attr(755,root,root) %{_libdir}/orbit-2.0/*.so
%attr(755,root,root) %{_libdir}/gtk-2.0/modules/lib*.so
%{_libdir}/bonobo/servers/*
%{_datadir}/idl/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*
%{_gtkdocdir}/*
%{_pkgconfigdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
