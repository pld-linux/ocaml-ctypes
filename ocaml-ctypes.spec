#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%if %{without ocaml_opt}
%define		_enable_debug_packages	0
%endif

%define		module	ctypes
Summary:	Library for binding to C libraries using pure OCaml
Summary(pl.UTF-8):	Biblioteka do wiązania z bibliotekami C przy użyciu czystego OCamla
Name:		ocaml-%{module}
Version:	0.18.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/ocamllabs/ocaml-ctypes/releases
Source0:	https://github.com/ocamllabs/ocaml-ctypes/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	5d9ef3790fda7cd97a8cec08be4b5b61
URL:		https://github.com/ocamllabs/ocaml-ctypes
BuildRequires:	libffi-devel
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-bigarray-compat-devel
BuildRequires:	ocaml-integers-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ctypes is a library for binding to C libraries using pure OCaml. The
primary aim is to make writing C extensions as straightforward as
possible.

The core of ctypes is a set of combinators for describing the
structure of C types -- numeric types, arrays, pointers, structs,
unions and functions. You can use these combinators to describe the
types of the functions that you want to call, then bind directly to
those functions -- all without writing or generating any C!

This package contains files needed to run bytecode executables using
this library.

%description -l pl.UTF-8
ctypes to biblioteka do wiązania z bibliotekami C przy użyciu czystego
OCamla. Głównym celem jest uczynienie pisania rozszerzeń w C jak
najprostszym.

Serce ctypes to zbiór kombinatorów do opisu struktur typów C - typów
liczbowych, tablic, wskaźników, struktur, unii oraz funkcji. Można ich
używać do opisu typów funkcji, które mają być wywoływane, a następnie
dowiązać bezpośrednio do tych funkcji - bez pisania ani generowania
żadnego kodu w C!

Ten pakiet zawiera pliki niezbędne do uruchamiania programów
bajtkodowych wykorzystujących bibliotekę.

%package devel
Summary:	Library for binding to C libraries using pure OCaml - development part
Summary(pl.UTF-8):	Biblioteka do wiązania z bibliotekami C przy użyciu czystego OCamla - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq ocaml

%description devel
This package contains files needed to develop OCaml programs using
ctypes library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki niezbędne do tworzenia programów w OCamlu
wykorzystujących bibliotekę ctypes.

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

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/ctypes/CHANGES.md
# findlib files, useless when packaging to rpm
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/*.owner

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE README.md
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllctypes_stubs.so
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllctypes-foreign_stubs.so
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/META
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/%{module}/*.cmxs
%endif
%{_libdir}/ocaml/%{module}/*.cma

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/%{module}/*.h
%{_libdir}/ocaml/%{module}/*.cmi
%{_libdir}/ocaml/%{module}/*.cmti
%{_libdir}/ocaml/%{module}/*.mli
%{_libdir}/ocaml/%{module}/*.a
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/*.cmx
%{_libdir}/ocaml/%{module}/*.cmxa
%endif
%{_examplesdir}/%{name}-%{version}
