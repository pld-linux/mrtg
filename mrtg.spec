%include	/usr/lib/rpm/macros.perl
Summary:	Multi Router Traffic Grapher
Summary(pl):	MRTG
Name:		mrtg
Version:	2.9.11pre1
Release:	1
License:	GPL
Group:		Applications/Networking
Group(de):	Applikationen/Netzwerkwesen
Group(pl):	Aplikacje/Sieciowe
Source0:	http://www.ee.ethz.ch/~oetiker/webtools/mrtg/pub/%{name}-%{version}.tar.gz
Source1:	%{name}.cfg
Patch0:		%{name}.path.patch
Patch1:		%{name}-use-perl-pod.patch
BuildRequires:	gd-devel
BuildRequires:	zlib-devel
BuildRequires:	libpng >= 1.0.8
BuildRequires:	perl => 5.004
URL:		http://www.ee.ethz.ch/~oetiker/webtools/mrtg/mrtg.html
%requires_eq    perl
Requires:	/etc/cron.d
BuildRequires:	rrdtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Multi Router Traffic Grapher (MRTG) is a tool to monitor the
traffic load on network-links. MRTG generates HTML pages containing
PNG images which provide a LIVE visual representation of this traffic.

%description -l pl
Multi Router Traffic Grapher (MRTG) to narzêdzie s³u¿±ce do
monitorowania obci±¿enia ³±cz sieciowych. MRTG generuje strony HTML
zawieraj±ce obrazki PNG przedstawiaj±ce aktualne obci±¿enie ³±cz.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
rm -rf lib/mrtg2/Pod

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/cron.d,etc/mrtg,home/httpd/html/mrtg} \
	$RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%perl_sitearch}

install %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/mrtg
ln -s ../../../..%{_sysconfdir}/mrtg/mrtg.cfg $RPM_BUILD_ROOT/home/httpd/html/mrtg/mrtg.cfg
install images/* $RPM_BUILD_ROOT/home/httpd/html/mrtg/

install bin/{cfgmaker,indexmaker} $RPM_BUILD_ROOT%{_libdir}/mrtg
install bin/{rateup,mrtg} $RPM_BUILD_ROOT%{_bindir}
install lib/mrtg2/*.pm $RPM_BUILD_ROOT/%{perl_sitearch}

tar -cf contrib.tar contrib
gzip -9nf contrib.tar

cat  << EOF > $RPM_BUILD_ROOT/etc/cron.d/mrtg
*/5 * * * * root umask 022; /bin/nice -n 20 %{_bindir}/mrtg /home/httpd/html/mrtg/mrtg.cfg
*/5 * * * * root umask 022; /bin/nice -n 20 %{_libdir}/mrtg/indexmaker -t 'Statistics' -r '.' -o /home/httpd/html/mrtg/index.html %{_sysconfdir}/mrtg/mrtg.cfg 2> /dev/null
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc contrib.tar.gz doc/*.txt doc/*.cfg
%dir /home/httpd/html/mrtg
%dir %{_libdir}/mrtg
%config(noreplace) %{_sysconfdir}/mrtg/mrtg.cfg
%attr(644,root,root) /home/httpd/html/mrtg/*
%attr(644,root,root) %perl_sitearch/*.pm
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/mrtg/*
%config(noreplace) %verify(not size mtime md5) %attr(640,root,root) /etc/cron.d/mrtg
