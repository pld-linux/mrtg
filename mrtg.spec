%include	/usr/lib/rpm/macros.perl
Summary:	Multi Router Traffic Grapher
Summary(es):	Herramienta para hacer gr�ficos de empleo en la red
Summary(pl):	MRTG - generator obraz�w obci��enia ��cz
Summary(pt_BR):	Ferramenta para fazer gr�ficos do uso da rede
Summary(ru):	MRTG - ��������� ����������� ���������, ������������ ������� �� ��������� ��������
Name:		mrtg
Version:	2.9.29
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	http://people.ee.ethz.ch/~oetiker/webtools/%{name}/pub/%{name}-%{version}.tar.gz
# Source0-md5:	17ae5e4cdd69a8995e3a861f6a00e153
Source1:	%{name}.cfg
Source2:	%{name}.init
Patch0:		%{name}.path.patch
Patch1:		%{name}-use-perl-pod.patch
URL:		http://people.ee.ethz.ch/~oetiker/webtools/mrtg/mrtg.html
PreReq:		rc-scripts >= 0.2.0
Requires:	mrtg-start
BuildRequires:	gd-devel >= 2.0.1
BuildRequires:	libpng >= 1.0.8
BuildRequires:	perl-devel >= 5.6.1
BuildRequires:	perl(SNMP_Session)
BuildRequires:	rrdtool
BuildRequires:	autoconf
BuildRequires:	automake

BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Multi Router Traffic Grapher (MRTG) is a tool to monitor the
traffic load on network-links. MRTG generates HTML pages containing
PNG images which provide a LIVE visual representation of this traffic.

%description -l es
Herramienta para hacer gr�ficos de empleo en la red.

%description -l pl
Multi Router Traffic Grapher (MRTG) to narz�dzie s�u��ce do
monitorowania obci��enia ��cz sieciowych. MRTG generuje strony HTML
zawieraj�ce obrazki PNG przedstawiaj�ce aktualne obci��enie ��cz.

%description -l pt_BR
O MRTG � uma ferramenta parar monitorar o tr�fego de links de rede.
Ele gera p�ginas HTML contendo imagens GIF que prov�m uma sensa��o
real�stica deste gr�fico.

%package cron
Summary:	Files that allow running mrtg via crond
Summary(pl):	Pliki pozwalaj�ce uruchamia� mrtg via crond.
Group:		Applications/Networking
Requires:	/etc/cron.d
Requires:	mrtg
Obsoletes:	mrtg-start
Provides:	mrtg-start

%description cron
Files that allow running mrtg via crond.

%description cron -l pl
Pliki pozwalaj�ce uruchamia� mrtg via crond.

%package init
Summary:	Files that allow running mrtg via rc-scripts
Summary(pl):	Pliki pozwalaj�ce uruchamia� mrtg via rc-scripts.
Group:		Daemons
Requires:	/etc/cron.d
Requires:	mrtg
Obsoletes:	mrtg-start
Provides:	mrtg-start
Requires(post,preun):	/sbin/chkconfig

%description init
Files that allow running mrtg via rc-scripts.

%description init -l pl
Pliki pozwalaj�ce uruchamia� mrtg via rc-scripts.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
rm -rf lib/mrtg2/Pod

%build
%{__aclocal}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/cron.d,etc/mrtg,home/services/httpd/html/mrtg} \
	$RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{perl_vendorlib},%{_mandir}/man1}

install %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/mrtg
ln -sf %{_sysconfdir}/mrtg/mrtg.cfg $RPM_BUILD_ROOT/home/services/httpd/html/mrtg/mrtg.cfg
install images/* $RPM_BUILD_ROOT/home/services/httpd/html/mrtg/

install bin/{cfgmaker,indexmaker} $RPM_BUILD_ROOT%{_libdir}/mrtg
install bin/{rateup,mrtg} $RPM_BUILD_ROOT%{_bindir}
install lib/mrtg2/locales_mrtg.pm $RPM_BUILD_ROOT%{perl_vendorlib}
install lib/mrtg2/MRTG_lib.pm $RPM_BUILD_ROOT%{perl_vendorlib}
install doc/*.1	$RPM_BUILD_ROOT%{_mandir}/man1/


tar -cf contrib.tar contrib

cat  << EOF > $RPM_BUILD_ROOT/etc/cron.d/mrtg
*/5 * * * * root umask 022; /bin/nice -n 19 %{_bindir}/mrtg %{_sysconfdir}/mrtg/mrtg.cfg
*/5 * * * * root umask 022; /bin/nice -n 19 %{_libdir}/mrtg/indexmaker --title 'Statistics' --prefix '.' --output /home/services/httpd/html/mrtg/index.html %{_sysconfdir}/mrtg/mrtg.cfg 2> /dev/null
EOF

install -d $RPM_BUILD_ROOT%{_initrddir}
install %SOURCE2 $RPM_BUILD_ROOT%{_initrddir}/mrtg

%post init
/sbin/chkconfig --add mrtg
if [ -f /var/lock/subsys/mrtg ]; then
	/etc/rc.d/init.d/mrtg restart >&2
else
	echo "Run \"/etc/rc.d/init.d/mrtg start\" to start mrtg." >&2
fi

%preun init
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/mrtg ]; then
		/etc/rc.d/init.d/mrtg stop
	fi
	/sbin/chkconfig --del mrtg
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc contrib.tar doc/*.txt
%dir /home/services/httpd/html/mrtg
%dir %{_libdir}/mrtg
%attr(751,root,root) %dir %{_sysconfdir}/mrtg
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mrtg/mrtg.cfg
%attr(644,root,root) /home/services/httpd/html/mrtg/*
%attr(644,root,root) %{perl_vendorlib}/*.pm
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/mrtg/*
%{_mandir}/man1/*

%files cron
%defattr(644,root,root,755)
%config(noreplace) %verify(not size mtime md5) %attr(640,root,root) /etc/cron.d/mrtg

%files init
%defattr(644,root,root,755)
%attr(754,root,root) %{_initrddir}/mrtg
