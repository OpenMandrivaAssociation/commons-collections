%bcond_with	bootstrap

Name:       commons-collections
Version:    3.2.1
Release:    1
Epoch:      0
Summary:    Provides new interfaces, implementations and utilities for Java Collections
License:    Apache Software License 
Group:      Development/Java
Source0:    http://apache.openmirror.de/commons/collections/source/%name-%version-src.tar.gz
Source1:    pom-maven2jpp-depcat.xsl
Source2:    pom-maven2jpp-newdepmap.xsl
Source3:    pom-maven2jpp-mapdeps.xsl
Source4:    commons-collections-3.2-jpp-depmap.xml
# svn export -r '{2007-02-15}' http://svn.apache.org/repos/asf/jakarta/commons/proper/commons-build/trunk/ commons-build
# tar czf commons-build.tar.gz commons-build
Source6:    collections-tomcat5-build.xml

Patch0:         %{name}-javadoc-nonet.patch

Url:            http://commons.apache.org/collections/
BuildRequires:  ant
%if !%{with bootstrap}
#BuildRequires:  ant-junit
%endif
BuildRequires:  java-rpmbuild >= 0:1.7.2
BuildRequires:  xml-commons-apis >= 1.3

BuildArch:      noarch
BuildRequires:	java-1.6.0-openjdk-devel

%rename jakarta-%name

%description
The introduction of the Collections API by Sun in JDK 1.2 has been a
boon to quick and effective Java programming. Ready access to powerful
data structures has accelerated development by reducing the need for
custom container classes around each core object. Most Java2 APIs are
significantly easier to use because of the Collections API.
However, there are certain holes left unfilled by Sun's
implementations, and the Commons Collections Component strives
to fulfill them. Among the features of this package are:
- special-purpose implementations of Lists and Maps for fast access
- adapter classes from Java1-style containers (arrays, enumerations) to
Java2-style collections.
- methods to test or create typical set-theory properties of collections
such as union, intersection, and closure.

%package testframework
Summary:        Testframework for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description testframework
%{summary}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
%{summary}.

%package tomcat5
Summary:        Jakarta Commons Collection dependency for Tomcat5
Group:          Development/Java

%description tomcat5
A package that is specifically designed to fulfill to a Tomcat5 dependency.

%package testframework-javadoc
Summary:        Javadoc for %{name}-testframework
Group:          Development/Java

%description testframework-javadoc
%{summary}.

%package manual
Summary:        Documents for %{name}
Group:          Development/Java

%description manual
%{summary}.

%prep
%setup -q -n %name-%version-src
%remove_java_binaries
%patch0 -p1 -b .sav0
cp %{SOURCE6} .

# Fix file eof
%{__sed} -i 's/\r//' LICENSE.txt
%{__sed} -i 's/\r//' PROPOSAL.html
%{__sed} -i 's/\r//' RELEASE-NOTES.html
%{__sed} -i 's/\r//' README.txt
%{__sed} -i 's/\r//' NOTICE.txt

%build
export JAVA_HOME=%_prefix/lib/jvm/java-1.6.0
export CLASSPATH=%_datadir/java/junit.jar

ant -Djava.io.tmpdir=. test dist tf.javadoc jar javadoc dist.bin dist.src

# commons-collections-tomcat5
ant -f collections-tomcat5-build.xml

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 build/%name-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
%if !%{with bootstrap}
install -m 644 build/%name-testframework-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-testframework-%{version}.jar
%endif

#tomcat5
install -m 644 collections-tomcat5/%name-tomcat5.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-tomcat5-%{version}.jar
%add_to_maven_depmap %name %name %{version} JPP %name
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} jakarta-${jar}; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%name.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf target/docs/apidocs

# testframework-javadoc
%if !%{with bootstrap}
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-testframework-%{version}
cp -pr build/docs/testframework/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-testframework-%{version}
ln -s %{name}-testframework-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-testframework 
%endif

# manual
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr dist/*/docs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(0644,root,root,0755)
%doc PROPOSAL.html README.txt LICENSE.txt RELEASE-NOTES.html NOTICE.txt
%{_javadir}/jakarta-%name-%{version}.jar
%{_javadir}/jakarta-%name.jar
%{_javadir}/%name-%{version}.jar
%{_javadir}/%name.jar
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}

%if !%{with bootstrap}
%files testframework
%defattr(0644,root,root,0755)
%{_javadir}/jakarta-%name-testframework-%{version}.jar
%{_javadir}/jakarta-%name-testframework.jar
%{_javadir}/%name-testframework-%{version}.jar
%{_javadir}/%name-testframework.jar
%endif

%files tomcat5
%defattr(0644,root,root,0755)
%{_javadir}/*-tomcat5*.jar
%doc LICENSE.txt NOTICE.txt

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%if !%{with bootstrap}
%files testframework-javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-testframework-%{version}
%{_javadocdir}/%{name}-testframework
%endif

%files manual
%defattr(0644,root,root,0755)
%{_docdir}/%{name}-%{version}



%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:3.2.1-2.0.6mdv2011.0
+ Revision: 665798
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:3.2.1-2.0.5mdv2011.0
+ Revision: 606049
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:3.2.1-2.0.4mdv2010.1
+ Revision: 522964
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:3.2.1-2.0.3mdv2010.0
+ Revision: 425412
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:3.2.1-2.0.2mdv2009.1
+ Revision: 351269
- rebuild

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 0:3.2.1-2.0.1mdv2009.0
+ Revision: 264714
- rebuild early 2009.0 package (before pixel changes)

* Fri Apr 18 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:3.2.1-0.0.1mdv2009.0
+ Revision: 195553
- new version, removed now bundled pom and unneeded patch1

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Wed Dec 12 2007 Alexander Kurtakov <akurtakov@mandriva.org> 0:3.2-2.0.2mdv2008.1
+ Revision: 117605
- bump release
- install poms (jpp sync)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:3.2-1.4mdv2008.0
+ Revision: 87401
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Jun 30 2007 Anssi Hannula <anssi@mandriva.org> 0:3.2-1.3mdv2008.0
+ Revision: 46066
- sync with FC


* Wed Mar 14 2007 Christiaan Welvaart <spturtle@mandriva.org> 3.2-1.2mdv2007.1
+ Revision: 143751
- rebuild for 2007.1

  + Per Øyvind Karlsen <pkarlsen@mandriva.com>
    - Import jakarta-commons-collections

* Fri Jun 02 2006 David Walluck <walluck@mandriva.org> 0:3.2-1.1mdv2007.0
- 3.2
- rebuild for libgcj.so.7

* Fri Dec 02 2005 David Walluck <walluck@mandriva.org> 0:3.1-2.2mdk
- sync with 2jpp_2fc

* Fri May 20 2005 David Walluck <walluck@mandriva.org> 0:3.1-1.1mdk
- release

* Fri Sep 17 2004 Ralph Apel <r.apel at r-apel.de> - 0:3.1-1jpp
- Upgrade to 3.1

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:2.1.1-2jpp
- Rebuild with ant-1.6.2

* Mon Jun 28 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:2.1.1-1jpp
- Update to 2.1.1

