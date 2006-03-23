# TODO:
# - accept multiple config definition in /etc/sysconfig/mrtg by cron-started
#   mrtg. Thats why sysconfig file is in main package.
# - start mrtg daemon as non-root user (configurable, because root is required
#   for some sort of stats

%include	/usr/lib/rpm/macros.perl
Summary:	Multi Router Traffic Grapher
Summary(es):	Herramienta para hacer gr�ficos de empleo en la red
Summary(pl):	MRTG - generator obraz�w obci��enia ��cz
Summary(pt_BR):	Ferramenta para fazer gr�ficos do uso da rede
Summary(ru):	MRTG - ��������� ����������� ���������, ������������ ������� �� ��������� ��������
Name:		mrtg
Version:	2.13.2
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	http://people.ee.ethz.ch/~oetiker/webtools/mrtg/pub/%{name}-%{version}.tar.gz
# Source0-md5:	daab44b14d608cda831b4dc481cec38a
Source1:	%{name}.cfg
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source4:	%{name}.logrotate
Source5:	%{name}.cron
Source6:	%{name}-indexmaker.cron
Patch0:		%{name}.path.patch
Patch1:		%{name}-use-perl-pod.patch
URL:		http://people.ee.ethz.ch/~oetiker/webtools/mrtg/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gd-devel >= 2.0.1
BuildRequires:	libpng-devel >= 1.0.8
BuildRequires:	perl-SNMP_Session >= 1.05
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	perl(SNMP_util) >= 1.04
Requires:	rc-scripts >= 0.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_htmldir	/home/services/httpd/html/mrtg

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
Summary(pl):	Pliki pozwalaj�ce uruchamia� mrtg z crona
Group:		Applications/Networking
Requires:	crondaemon
Requires:	mrtg
Provides:	mrtg-start
Obsoletes:	mrtg-init
Obsoletes:	mrtg-start

%description cron
Files that allow running mrtg via crond.

%description cron -l pl
Pliki pozwalaj�ce uruchamia� mrtg z crona.

%package init
Summary:	Files that allow running mrtg via rc-scripts
Summary(pl):	Pliki pozwalaj�ce uruchamia� mrtg z poziomu rc-scripts
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	crondaemon
Requires:	mrtg
Provides:	mrtg-start
Obsoletes:	mrtg-cron
Obsoletes:	mrtg-start

%description init
Files that allow running mrtg via rc-scripts.

%description init -l pl
Pliki pozwalaj�ce uruchamia� mrtg z poziomu rc-scripts.

%prep
%setup -q
%patch0 -p1
#%patch1 -p1
rm -rf lib/mrtg2/Pod

%build
%{__aclocal}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{cron.d,rc.d/init.d,sysconfig,logrotate.d},%{_sysconfdir}/mrtg,%{_htmldir}} \
	$RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{perl_vendorlib},%{_mandir}/man1} \
	$RPM_BUILD_ROOT{/var/log/{mrtg,archiv/mrtg},/var/run/mrtg}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mrtg
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/mrtg
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/mrtg
install %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d/mrtg
install %{SOURCE5} $RPM_BUILD_ROOT%{_bindir}/mrtg-cronjob
install %{SOURCE6} $RPM_BUILD_ROOT%{_bindir}/indexmaker-cronjob
ln -sf %{_sysconfdir}/mrtg/mrtg.cfg $RPM_BUILD_ROOT%{_htmldir}/mrtg.cfg
install images/* $RPM_BUILD_ROOT%{_htmldir}

install bin/{cfgmaker,indexmaker} $RPM_BUILD_ROOT%{_libdir}/mrtg
install bin/{rateup,mrtg} $RPM_BUILD_ROOT%{_bindir}
install lib/mrtg2/locales_mrtg.pm $RPM_BUILD_ROOT%{perl_vendorlib}
install lib/mrtg2/MRTG_lib.pm $RPM_BUILD_ROOT%{perl_vendorlib}
install doc/*.1	$RPM_BUILD_ROOT%{_mandir}/man1

tar -cf contrib.tar contrib

cat  << EOF > $RPM_BUILD_ROOT/etc/cron.d/mrtg
*/5 * * * * root umask 022; /bin/nice -n 19 %{_bindir}/mrtg-cronjob
*/5 * * * * root umask 022; /bin/nice -n 19 %{_bindir}/indexmaker-cronjob 2> /dev/null
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add mrtg
%service mrtg restart

%preun init
if [ "$1" = "0" ]; then
	%service mrtg stop
	/sbin/chkconfig --del mrtg
fi

%files
%defattr(644,root,root,755)
%doc contrib.tar doc/*.txt
%dir %{_htmldir}
%dir %{_libdir}/mrtg
%attr(751,root,root) %dir %{_sysconfdir}/mrtg
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mrtg/mrtg.cfg
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mrtg
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/mrtg
%attr(644,root,root) %{_htmldir}/*
%attr(644,root,root) %{perl_vendorlib}/*.pm
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/mrtg/*
%attr(751,root,root) %dir /var/log/mrtg
%attr(751,root,root) %dir /var/log/archiv/mrtg
%dir /var/run/mrtg
%{_mandir}/man1/*

%files cron
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/mrtg

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/mrtg
