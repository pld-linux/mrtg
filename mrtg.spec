Summary:	Multi Router Traffic Grapher
Summary(pl):	MRTG
Name:		mrtg
Version:	2.7.4b
Release:	1
Group:		Applications/Networking
Group(pl):	Aplikacje/Sieciowe
Copyright:	distributable
Source0:	http://www.ee.ethz.ch/~oetiker/webtools/mrtg/pub/%{name}-%{version}.tar.gz
Source1:	mrtg.cfg
Patch:		mrtg.path.patch
Url:		http://www.ee.ethz.ch/~oetiker/webtools/mrtg/mrtg.html
Requires:	perl >= 5.004
Requires:	/etc/crontab.d
Buildroot:	/tmp/%{name}-%{version}-root

%description
The Multi Router Traffic Grapher (MRTG) is a tool to monitor the traffic
load on network-links. MRTG generates HTML pages containing GIF
images which provide a LIVE visual representation of this traffic.

%description -l pl
Multi Router Traffic Grapher (MRTG) to narzêdzie s³u¿±ce do monitorowania
obci±¿enia ³±cz sieciowych. MRTG generuje strony HTML zawieraj±ce
obrazki GIF przedstawiaj±ce aktualne obci±¿enie ³±cz.

%prep
%setup -q
%patch -p1 -b .path

%build
eval `perl '-V:installarchlib'`
CFLAGS="$RPM_OPT_FLAGS -I$installarchlib/CORE" \
./configure %{_target_platform} \
	--prefix=/usr \
	--with-gd-lib=%{_libdir} \
	--with-gd-inc=%{_includedir}
make

%install
rm -rf $RPM_BUILD_ROOT
eval `perl '-V:installarchlib'`

install -d $RPM_BUILD_ROOT/{etc/crontab.d,home/httpd/html/mrtg}
install -d $RPM_BUILD_ROOT/usr/{bin,lib/mrtg}
install -d $RPM_BUILD_ROOT/$installarchlib

install	%SOURCE1	$RPM_BUILD_ROOT/etc
ln -s   /etc/mrtg.cfg	$RPM_BUILD_ROOT/home/httpd/html/mrtg/mrtg.cfg
install images/*        $RPM_BUILD_ROOT/home/httpd/html/mrtg/
install run/cfgmaker	$RPM_BUILD_ROOT%{_libdir}/mrtg
install run/indexmaker  $RPM_BUILD_ROOT%{_libdir}/mrtg
install run/mrtg        $RPM_BUILD_ROOT%{_bindir}
install -s run/rateup   $RPM_BUILD_ROOT%{_bindir}
install run/*.pm        $RPM_BUILD_ROOT/$installarchlib

tar -cf contrib.tar contrib
gzip -9nf contrib.tar doc/*.txt doc/*.cfg

cat  << EOF > $RPM_BUILD_ROOT/etc/crontab.d/mrtg
*/5 * * * * root umask 022; %{_bindir}/mrtg /home/httpd/html/mrtg/mrtg.cfg
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
%attr(644,root,root) %{_libdir}/perl5/*/*/*.pm
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/mrtg/*
%attr(640,root,root) /etc/crontab.d/mrtg
