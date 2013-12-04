%global cartridgedir %{_libexecdir}/openshift/cartridges/wildfly
%global namedreltag .Beta1
%global namedversion %{version}%{?namedreltag}

Summary:       Provides WildFly support
Name:          openshift-origin-cartridge-wildfly
Version:       8.0.0
Release:       0.1%{namedreltag}%{?dist}
Group:         Development/Languages
License:       ASL 2.0
URL:           http://www.openshift.com
Source0:       https://github.com/goldmann/openshift-origin-cartridge-wildfly/archive/1.0.0.tar.gz
Requires:      rubygem(openshift-origin-node)
Requires:      openshift-origin-node-util
Requires:      lsof
Requires:      java-1.7.0-openjdk
Requires:      java-1.7.0-openjdk-devel
#Requires:      jboss-as7-modules >= %{wildflyver}
Requires:      facter
Requires:      bc
%if 0%{?rhel}
#Requires:      wildfly >= %{namedversion}
Requires:      maven3
%endif
%if 0%{?fedora}
Requires:      wildfly
Requires:      maven
%endif
BuildRequires: jpackage-utils
BuildArch:     noarch

%description
Provides WildFly support to OpenShift. (Cartridge Format V2)

%prep
%setup -q

%build
%__rm %{name}.spec


%install
%__mkdir -p %{buildroot}%{cartridgedir}
%__cp -r * %{buildroot}%{cartridgedir}


%post

%if 0%{?rhel}
alternatives --install /etc/alternatives/maven-3.0 maven-3.0 /usr/share/java/apache-maven-3.0.3 100
alternatives --set maven-3.0 /usr/share/java/apache-maven-3.0.3

alternatives --remove wildfly-8 /opt/wildfly-8
alternatives --install /etc/alternatives/wildfly-8 wildfly-8 /opt/wildfly-%{namedversion} 102
alternatives --set wildfly-8 /opt/wildfly-%{namedversion}
%endif

%if 0%{?fedora}
alternatives --remove maven-3.0 /usr/share/java/apache-maven-3.0.3
alternatives --install /etc/alternatives/maven-3.0 maven-3.0 /usr/share/maven 102
alternatives --set maven-3.0 /usr/share/maven

alternatives --remove wildfly-8 /usr/share/wildfly
alternatives --install /etc/alternatives/wildfly-8 wildlfy-8 /usr/share/wildfly 102
alternatives --set wildfly-8 /usr/share/wildfly
%endif

# Temp placeholder to add a postgresql datastore -- keep this until the
# the postgresql module is added to wildfly upstream.
mkdir -p /etc/alternatives/wildfly-8/modules/system/layers/base/org/postgresql/jdbc/main
ln -fs /usr/share/java/postgresql-jdbc3.jar /etc/alternatives/wildfly-8/modules/system/layers/base/org/postgresql/jdbc/main
cp -p %{cartridgedir}/versions/8/modules/postgresql_module.xml /etc/alternatives/wildfly-8/modules/system/layers/base/org/postgresql/jdbc/main/module.xml

%postun
# Cleanup alternatives if uninstall only
# This is run after %post so we do not want to remove if an upgrade
# Don't uninstall the maven alternative, since it is also used by jbosseap and jbossews carts
if [ $1 -eq 0 ]; then
  %if 0%{?rhel}
    alternatives --remove wildfly-8 /opt/wildfly-%{namedversion}
  %endif

  %if 0%{?fedora}
    alternatives --remove wildfly-7 /usr/share/wildfly
  %endif
fi

%files
%dir %{cartridgedir}
%attr(0755,-,-) %{cartridgedir}/bin/
%attr(0755,-,-) %{cartridgedir}/versions/7/bin/
%attr(0755,-,-) %{cartridgedir}/hooks/
%{cartridgedir}
%doc %{cartridgedir}/README.md
%doc %{cartridgedir}/COPYRIGHT
%doc %{cartridgedir}/LICENSE

%changelog
* Wed Dec 04 2013 Marek Goldmann <mgoldman@redhat.com> - 8.0.0-0.1.Beta1
- Initial packaging


