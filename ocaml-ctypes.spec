%define		module	ctypes
Summary:	Library for binding to C libraries using pure OCaml
Summary(pl.UTF-8):	Biblioteka do wiązania z bibliotekami C przy użyciu czystego OCamla
Name:		ocaml-%{module}
Version:	0.3.4
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/ocamllabs/ocaml-ctypes/archive/%{version}.tar.gz?/%{module}-%{version}.tar.gz
# Source0-md5:	5356f0bab5cbc29eba3dded5e35a9e9d
URL:		https://github.com/ocamllabs/ocaml-ctypes
BuildRequires:	libffi-devel
BuildRequires:	ocaml >= 3.04-7
%requires_eq	ocaml-runtime
# requires opt not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
ExclusiveArch:	%{ix86} %{x8664}
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
%requires_eq	ocaml

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
%doc CHANGES.md LICENSE README.md
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllctypes-foreign-base_stubs.so
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllctypes_stubs.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/%{module}/*.h
%{_libdir}/ocaml/%{module}/*.cm[xi]
%{_libdir}/ocaml/%{module}/*.mli
%{_libdir}/ocaml/%{module}/*.[ao]
%{_libdir}/ocaml/%{module}/*.cma
%{_libdir}/ocaml/%{module}/*.cmxa
%{_libdir}/ocaml/%{module}/*.cmxs
%{_libdir}/ocaml/site-lib/%{module}
%{_examplesdir}/%{name}-%{version}
