#
# Conditional build:
%bcond_without	ocaml_opt		# build opt

%ifarch x32
# not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
%undefine	with_ocaml_opt
%endif

%if %{without ocaml_opt}
%define		no_install_post_strip	1
# no opt means no native binary, stripping bytecode breaks such programs
%define		_enable_debug_packages	0
%endif

%define		module	ctypes
Summary:	Library for binding to C libraries using pure OCaml
Name:		ocaml-%{module}
Version:	0.3.4
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/ocamllabs/ocaml-ctypes/archive/%{version}.tar.gz?/%{module}-%{version}.tar.gz
# Source0-md5:	5356f0bab5cbc29eba3dded5e35a9e9d
URL:		https://github.com/ocamllabs/ocaml-ctypes
#BuildRequires:	-devel
BuildRequires:	ocaml >= 3.04-7
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ctypes is a library for binding to C libraries using pure OCaml.
The primary aim is to make writing C extensions as straightforward
as possible.

The core of ctypes is a set of combinators for describing
the structure of C types -- numeric types, arrays, pointers, structs,
unions and functions. You can use these combinators to describe the
types of the functions that you want to call, then bind directly to
those functions -- all without writing or generating any C!
This package contains files needed to run bytecode executables using
this library.

%package devel
Summary:	TEMPLATE binding for OCaml - development part
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
TEMPLATE library.

%prep
%setup -q

%build
%{__make} -j1 all \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
install -d $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# move to dir pld ocamlfind looks
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
mv $OCAMLFIND_DESTDIR/%{module}/META \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
cat <<EOF >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}/META
directory="+%{module}"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so

%files devel
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/ocaml/%{module}/*.cm[xi]
%{_libdir}/ocaml/%{module}/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/*.[ao]
%{_libdir}/ocaml/%{module}/*.cmxa
%endif
%{_libdir}/ocaml/site-lib/%{module}
%{_examplesdir}/%{name}-%{version}
