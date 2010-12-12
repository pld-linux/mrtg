# TODO:
# - update _htmldir (/usr/share for static data, /var/lib for generated)
# - accept multiple config definition in /etc/sysconfig/mrtg by cron-started
#   mrtg. Thats why sysconfig file is in main package.
# - start mrtg cronjob as non-root user (configurable in sysconfig file, because
#   root is required for some sort of stats)
# - (blues?) update crontabs to accept the "new" config mode as well as the daemon mode does

%include	/usr/lib/rpm/macros.perl
Summary:	Multi Router Traffic Grapher
Summary(es.UTF-8):	Herramienta para hacer gráficos de empleo en la red
Summary(pl.UTF-8):	MRTG - generator obrazów obciążenia łącz
Summary(pt_BR.UTF-8):	Ferramenta para fazer gráficos do uso da rede
Summary(ru.UTF-8):	MRTG - программа изображения граффиков, изображающих траффик на множестве роутеров
Name:		mrtg
Version:	2.16.4
Release:	3
License:	GPL
Group:		Applications/Networking
Source0:	http://oss.oetiker.ch/mrtg/pub/%{name}-%{version}.tar.gz
# Source0-md5:	ec298200d239832ff1648fba488e1a9e
Source1:	%{name}.cfg
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source4:	%{name}.logrotate
Source5:	%{name}.cron
Source6:	%{name}-indexmaker.cron
Patch0:		%{name}.path.patch
URL:		http://oss.oetiker.ch/mrtg/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gd-devel >= 2.0.1
BuildRequires:	libpng-devel >= 1.0.8
BuildRequires:	perl-SNMP_Session >= 1.05
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	perl(SNMP_util) >= 1.04
Conflicts:	logrotate < 3.7-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_htmldir	/home/services/httpd/html/mrtg

%description
The Multi Router Traffic Grapher (MRTG) is a tool to monitor the
traffic load on network-links. MRTG generates HTML pages containing
PNG images which provide a LIVE visual representation of this traffic.

%description -l es.UTF-8
Herramienta para hacer gráficos de empleo en la red.

%description -l pl.UTF-8
Multi Router Traffic Grapher (MRTG) to narzędzie służące do
monitorowania obciążenia łącz sieciowych. MRTG generuje strony HTML
zawierające obrazki PNG przedstawiające aktualne obciążenie łącz.

%description -l pt_BR.UTF-8
O MRTG é uma ferramenta parar monitorar o tráfego de links de rede.
Ele gera páginas HTML contendo imagens GIF que provêm uma sensação
realística deste gráfico.

%package cron
Summary:	Files that allow running mrtg via crond
Summary(pl.UTF-8):	Pliki pozwalające uruchamiać mrtg z crona
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	crondaemon
Provides:	mrtg-start
Obsoletes:	mrtg-init
Obsoletes:	mrtg-start

%description cron
Files that allow running mrtg via crond.

%description cron -l pl.UTF-8
Pliki pozwalające uruchamiać mrtg z crona.

%package init
Summary:	Files that allow running mrtg via rc-scripts
Summary(pl.UTF-8):	Pliki pozwalające uruchamiać mrtg z poziomu rc-scripts
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	crondaemon
Requires:	rc-scripts >= 0.4.3.7
Provides:	mrtg-start
Obsoletes:	mrtg-cron
Obsoletes:	mrtg-start

%description init
Files that allow running mrtg via rc-scripts.

%description init -l pl.UTF-8
Pliki pozwalające uruchamiać mrtg z poziomu rc-scripts.

%prep
%setup -q
%patch0 -p1
rm -rf lib/mrtg2/Pod

%build
%{__aclocal}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{cron.d,rc.d/init.d,sysconfig,logrotate.d},%{_sysconfdir}/mrtg/conf.d,%{_htmldir}} \
	$RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{perl_vendorlib},%{_mandir}/man1} \
	$RPM_BUILD_ROOT{/var/log/{mrtg,archive/mrtg},/var/{lib,run}/mrtg}

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mrtg
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/mrtg
cp -a %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/mrtg
cp -a %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d/mrtg
install -p %{SOURCE5} $RPM_BUILD_ROOT%{_bindir}/mrtg-cronjob
install -p %{SOURCE6} $RPM_BUILD_ROOT%{_bindir}/indexmaker-cronjob
ln -sf %{_sysconfdir}/mrtg/mrtg.cfg $RPM_BUILD_ROOT%{_htmldir}/mrtg.cfg
cp -a images/* $RPM_BUILD_ROOT%{_htmldir}

install -p bin/{cfgmaker,indexmaker} $RPM_BUILD_ROOT%{_libdir}/mrtg
install -p bin/{rateup,mrtg} $RPM_BUILD_ROOT%{_bindir}
cp -a lib/mrtg2/locales_mrtg.pm $RPM_BUILD_ROOT%{perl_vendorlib}
cp -a lib/mrtg2/MRTG_lib.pm $RPM_BUILD_ROOT%{perl_vendorlib}
cp -a doc/*.1	$RPM_BUILD_ROOT%{_mandir}/man1

ln -sf ../mrtg.cfg $RPM_BUILD_ROOT%{_sysconfdir}/mrtg/conf.d

tar -cf contrib.tar contrib

cat  << EOF > $RPM_BUILD_ROOT/etc/cron.d/mrtg
*/5 * * * * stats umask 022; /bin/nice -n 19 %{_bindir}/mrtg-cronjob
*/5 * * * * stats umask 022; /bin/nice -n 19 %{_bindir}/indexmaker-cronjob 2> /dev/null
EOF

sed -i 's#/''usr/lib#%{_libdir}#' $RPM_BUILD_ROOT%{_bindir}/indexmaker-cronjob

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
%attr(751,root,stats) %dir %{_sysconfdir}/mrtg
%attr(751,root,stats) %dir %{_sysconfdir}/mrtg/conf.d
%attr(640,root,stats) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mrtg/mrtg.cfg
%attr(640,root,stats) %config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/mrtg/conf.d/mrtg.cfg
%attr(640,root,stats) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mrtg
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/mrtg
%attr(755,stats,logs) %dir %{_htmldir}
%{_htmldir}/*
%{perl_vendorlib}/*.pm
%attr(755,root,root) %{_bindir}/mrtg
%attr(755,root,root) %{_bindir}/rateup
%dir %{_libdir}/mrtg
%attr(755,root,root) %{_libdir}/mrtg/cfgmaker
%attr(755,root,root) %{_libdir}/mrtg/indexmaker
%attr(1751,stats,logs) %dir /var/log/mrtg
%attr(751,root,logs) %dir /var/log/archive/mrtg
%attr(755,stats,stats) %dir /var/run/mrtg
%attr(755,stats,stats) %dir /var/lib/mrtg
%{_mandir}/man1/*

%files cron
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/mrtg
%attr(755,root,root) %{_bindir}/indexmaker-cronjob
%attr(755,root,root) %{_bindir}/mrtg-cronjob

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/mrtg
