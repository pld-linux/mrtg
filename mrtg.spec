%include	/usr/lib/rpm/macros.perl
Summary:	Multi Router Traffic Grapher
Summary(es):	Herramienta para hacer gráficos de empleo en la red
Summary(pl):	MRTG - generator obrazów obci±¿enia ³±cz
Summary(pt_BR):	Ferramenta para fazer gráficos do uso da rede
Summary(ru):	MRTG - ÐÒÏÇÒÁÍÍÁ ÉÚÏÂÒÁÖÅÎÉÑ ÇÒÁÆÆÉËÏ×, ÉÚÏÂÒÁÖÁÀÝÉÈ ÔÒÁÆÆÉË ÎÁ ÍÎÏÖÅÓÔ×Å ÒÏÕÔÅÒÏ×
Name:		mrtg
Version:	2.9.18
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	http://www.ee.ethz.ch/~oetiker/webtools/mrtg/pub/%{name}-%{version}.tar.gz
Source1:	%{name}.cfg
Patch0:		%{name}.path.patch
Patch1:		%{name}-use-perl-pod.patch
URL:		http://www.ee.ethz.ch/~oetiker/webtools/mrtg/mrtg.html
BuildRequires:	gd-devel >= 2.0.1
BuildRequires:	libpng >= 1.0.8
BuildRequires:	perl-devel >= 5.6.1
BuildRequires:	perl(SNMP_Session)
BuildRequires:	rrdtool
BuildRequires:	autoconf
BuildRequires:	automake
Requires:	/etc/cron.d
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Multi Router Traffic Grapher (MRTG) is a tool to monitor the
traffic load on network-links. MRTG generates HTML pages containing
PNG images which provide a LIVE visual representation of this traffic.

%description -l es
Herramienta para hacer gráficos de empleo en la red.

%description -l pl
Multi Router Traffic Grapher (MRTG) to narzêdzie s³u¿±ce do
monitorowania obci±¿enia ³±cz sieciowych. MRTG generuje strony HTML
zawieraj±ce obrazki PNG przedstawiaj±ce aktualne obci±¿enie ³±cz.

%description -l pt_BR
O MRTG é uma ferramenta parar monitorar o tráfego de links de rede.
Ele gera páginas HTML contendo imagens GIF que provêm uma sensação
realística deste gráfico.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
rm -rf lib/mrtg2/Pod

%build
aclocal
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/cron.d,etc/mrtg,home/httpd/html/mrtg} \
	$RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{perl_sitelib}}

install %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/mrtg
ln -sf %{_sysconfdir}/mrtg/mrtg.cfg $RPM_BUILD_ROOT/home/httpd/html/mrtg/mrtg.cfg
install images/* $RPM_BUILD_ROOT/home/httpd/html/mrtg/

install bin/{cfgmaker,indexmaker} $RPM_BUILD_ROOT%{_libdir}/mrtg
install bin/{rateup,mrtg} $RPM_BUILD_ROOT%{_bindir}
install lib/mrtg2/locales_mrtg.pm $RPM_BUILD_ROOT%{perl_sitelib}
install lib/mrtg2/MRTG_lib.pm $RPM_BUILD_ROOT%{perl_sitelib}

tar -cf contrib.tar contrib
gzip -9nf contrib.tar

cat  << EOF > $RPM_BUILD_ROOT/etc/cron.d/mrtg
*/5 * * * * root umask 022; /bin/nice -n 20 %{_bindir}/mrtg %{_sysconfdir}/mrtg/mrtg.cfg
*/5 * * * * root umask 022; /bin/nice -n 20 %{_libdir}/mrtg/indexmaker -t 'Statistics' -r '.' -o /home/httpd/html/mrtg/index.html %{_sysconfdir}/mrtg/mrtg.cfg 2> /dev/null
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc contrib.tar.gz doc/*.txt
%dir /home/httpd/html/mrtg
%dir %{_libdir}/mrtg
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mrtg/mrtg.cfg
%attr(644,root,root) /home/httpd/html/mrtg/*
%attr(644,root,root) %{perl_sitelib}/*.pm
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/mrtg/*
%config(noreplace) %verify(not size mtime md5) %attr(640,root,root) /etc/cron.d/mrtg
