jetty9-rpm
===========

A spec file (and support files) to build a Jetty 9.x (http://www.eclipse.org/jetty/) RPM package.

To Build:

`sudo yum -y install rpmdevtools && rpmdev-setuptree`

`wget https://raw.github.com/rafaelfelix/jetty9-rpm/master/jetty9.spec -O ~/rpmbuild/SPECS/jetty9.spec`

`wget https://raw.github.com/rafaelfelix/jetty9-rpm/master/jetty9.sysconfig -O ~/rpmbuild/SOURCES/jetty9.sysconfig`

`wget https://raw.github.com/rafaelfelix/jetty9-rpm/master/jetty9.logrotate -O ~/rpmbuild/SOURCES/jetty9.logrotate`

`wget "http://eclipse.org/downloads/download.php?file=/jetty/9.1.3.v20140225/dist/jetty-distribution-9.1.3.v20140225.tar.gz&r=1" -O ~/rpmbuild/SOURCES/jetty-distribution-9.1.3.v20140225.tar.gz`

`rpmbuild -bb ~/rpmbuild/SPECS/jetty9.spec`
