%define jetty_home /opt/jetty
%define jetty_user jetty
%define jetty_group jetty

Name:           jetty9
Version:        9.1.3.v20140225
Release:        1
Summary:        Jetty - Servlet Engine and Http Server.
License:        Creative Commons
URL:            http://www.eclipse.org/jetty/
Group:          System Environment/Daemons
Source0:        jetty-distribution-%{version}.tar.gz
Source1:        %{name}.sysconfig
Source2:        %{name}.logrotate
Requires:       java
BuildArch:      x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Jetty provides an Web server and javax.servlet container, plus support for SPDY, Web Sockets, OSGi, JMX, JNDI, JASPI, AJP and many other integrations. These components are open source and available for commercial use and distribution. Jetty is used in a wide variety of projects and products. Jetty can be embedded in devices, tools, frameworks, application servers, and clusters.

The Jetty project is hosted entirely at the Eclipse Foundation and has been for a number of years. Prior releases of Jetty have existed in part or completely under the Jetty project at the Codehaus. See the About page for more information about the history of Jetty.

%prep
%setup -q -n jetty-distribution-%{version}

%build

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}/%{jetty_home}/

# Remove unnecessary files
rm -rf demo-base

cp -R * %{buildroot}/%{jetty_home}/

# Put docs in /usr/share/doc/%{name}-%{version}
install -d -m 755 %{buildroot}/usr/share/doc/%{name}-%{version}/
mv README.TXT VERSION.txt license-eplv10-aslv20.html notice.html %{buildroot}/usr/share/doc/%{name}-%{version}/

# Put libs and modules in /usr/lib and link back.
install -d -m 755 %{buildroot}/usr/lib
mv %{buildroot}/%{jetty_home}/lib %{buildroot}/usr/lib/%{name}
mv %{buildroot}/%{jetty_home}/modules %{buildroot}/usr/lib/%{name}/
cd %{buildroot}/%{jetty_home}/
ln -s /usr/lib/%{name}/ lib
ln -s /usr/lib/%{name}/modules/ modules
cd -

# Put logging in /var/log and link back.
rm -rf %{buildroot}/%{jetty_home}/logs
install -d -m 755 %{buildroot}/var/log/%{name}/
cd %{buildroot}/%{jetty_home}/
ln -s /var/log/%{name}/ logs
cd -

# Put conf in /etc/ and link back.
install -d -m 755 %{buildroot}/%{_sysconfdir}
mv %{buildroot}/%{jetty_home}/etc %{buildroot}/%{_sysconfdir}/%{name}
mv %{buildroot}/%{jetty_home}/resources %{buildroot}/%{_sysconfdir}/%{name}/resources
cd %{buildroot}/%{jetty_home}/
ln -s %{_sysconfdir}/%{name} etc
ln -s %{_sysconfdir}/%{name}/resources resources
cd -

# Drop init script
install -d -m 755 %{buildroot}/%{_initrddir}
install    -m 755 bin/jetty.sh %{buildroot}/%{_initrddir}/jetty

# Drop sysconfig script
install -d -m 755 %{buildroot}/%{_sysconfdir}/default/
install    -m 644 %_sourcedir/%{name}.sysconfig %{buildroot}/%{_sysconfdir}/default/jetty

# Drop logrotate script
install -d -m 755 %{buildroot}/%{_sysconfdir}/logrotate.d
install    -m 644 %_sourcedir/%{name}.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/jetty

%clean
rm -rf %{buildroot}

%pre
getent group %{jetty_group} >/dev/null || groupadd -r %{jetty_group}
getent passwd %{jetty_user} >/dev/null || /usr/sbin/useradd --comment "Jetty Daemon User" --shell /bin/bash -M -r -g %{jetty_group} --home %{jetty_home} %{jetty_user}

%files
%defattr(-,%{jetty_user},%{jetty_group})
%{jetty_home}
/usr/lib/%{name}/
/var/log/%{name}/
%defattr(-,root,root)
%doc /usr/share/doc/%{name}-%{version}/*
%{_initrddir}/jetty
%{_sysconfdir}/logrotate.d/jetty
%config(noreplace) %{_sysconfdir}/default/jetty
%config(noreplace) %{_sysconfdir}/%{name}/*

%post
chkconfig --add jetty

%preun
if [ $1 = 0 ]; then
  service jetty stop > /dev/null 2>&1
  chkconfig --del jetty
fi

%postun
if [ $1 -ge 1 ]; then
  service jetty condrestart >/dev/null 2>&1
fi

%changelog
* Mon Apr 07 2014 Rafael Felix Correa <rafael.felix@rf4solucoes.com.br> - 9.1.3.v20140225-1
- First attempt.
