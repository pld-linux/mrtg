%include	/usr/lib/rpm/macros.perl
Summary:	Multi Router Traffic Grapher
Summary(pl):	MRTG
Name:		mrtg
Version:	2.8.12
Release:	1
Group:		Applications/Networking
Group(pl):	Aplikacje/Sieciowe
Copyright:	GPL
Source0:	http://www.ee.ethz.ch/~oetiker/webtools/mrtg/pub/%{name}-%{version}.tar.gz
Source1:	mrtg.cfg
Patch:		mrtg.path.patch
Url:		http://www.ee.ethz.ch/~oetiker/webtools/mrtg/mrtg.html
Requires:	perl >= 5.004
Requires:	/etc/cron.d
BuildRequires:	gd-devel
BuildRequires:	zlib-devel
BuildRequires:  libpng-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Multi Router Traffic Grapher (MRTG) is a tool to monitor the traffic
load on network-links. MRTG generates HTML pages containing PNG
images which provide a LIVE visual representation of this traffic.

%description -l pl
Multi Router Traffic Grapher (MRTG) to narzêdzie s³u¿±ce do monitorowania
obci±¿enia ³±cz sieciowych. MRTG generuje strony HTML zawieraj±ce
obrazki PNG przedstawiaj±ce aktualne obci±¿enie ³±cz.

%prep
%setup -q
%patch -p1 -b .path

%build
LDFLAGS="-s"; export LDFLAGS
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc/cron.d,home/httpd/html/mrtg} \
	$RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%perl_sitearch}

install	%SOURCE1 $RPM_BUILD_ROOT/etc
ln -s   /etc/mrtg.cfg $RPM_BUILD_ROOT/home/httpd/html/mrtg/mrtg.cfg
install images/* $RPM_BUILD_ROOT/home/httpd/html/mrtg/

install run/{cfgmaker,cfgmaker_ip,indexmaker} $RPM_BUILD_ROOT%{_libdir}/mrtg
install run/{rateup,mrtg} $RPM_BUILD_ROOT%{_bindir}
install run/*.pm $RPM_BUILD_ROOT/%{perl_sitearch}

tar -cf contrib.tar contrib
gzip -9nf contrib.tar doc/*.txt doc/*.cfg

cat  << EOF > $RPM_BUILD_ROOT/etc/cron.d/mrtg
*/5 * * * * root umask 022; %{_bindir}/mrtg /home/httpd/html/mrtg/mrtg.cfg
*/5 * * * * root umask 022; %{_libdir}/mrtg/indexmaker -t 'Statistics' -r '.' -o /home/httpd/html/mrtg/index.html /etc/mrtg.cfg
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc contrib.tar.gz doc/*.txt.gz doc/*.cfg.gz
%dir /home/httpd/html/mrtg
%dir %{_libdir}/mrtg
%config(noreplace) /etc/mrtg.cfg
%attr(644,root,root) /home/httpd/html/mrtg/*
%attr(644,root,root) %perl_sitearch/*.pm
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/mrtg/*
%config(noreplace) %verify(not size mtime md5) %attr(640,root,root) /etc/cron.d/mrtg
