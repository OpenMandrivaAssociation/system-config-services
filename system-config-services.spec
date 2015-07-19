%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}
%{!?python_version: %global python_version %(%{__python} -c "from distutils.sysconfig import get_python_version; print get_python_version()")}

%bcond_without require_docs

Summary: Utility to start and stop system services
Name: system-config-services
Version: 0.101.3
Release: 13
URL: http://fedorahosted.org/%{name}
Source0: http://fedorahosted.org/released/%{name}/%{name}-%{version}.tar.bz2
Source1: config.tar.gz
Patch0:	mdv_desktop.patch
Patch1: mdv_dbus.patch
Patch2:	mdv_make.patch
Patch3: mdv_gui.patch
License: GPLv2+
Group: System/Base
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python
BuildRequires: python-devel
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: sed
BuildRequires: desktop-file-utils
Requires: chkconfig
Requires: python-gamin
Requires: hicolor-icon-theme
Requires: pygtk2.0
Requires: pygtk2.0-libglade
Requires: python >= 2.3.0
Requires: python-dbus
Requires: python-slip >= 0.1.11
Requires: python-slip-dbus >= 0.2.8
Requires: python-slip-gtk
# Until version 0.99.28, system-config-services contained online documentation.
# From version 0.99.29 on, online documentation is split off into its own
# package system-config-services-docs. The following ensures that updating from
# earlier versions gives you both the main package and documentation.
Obsoletes: system-config-services < 0.99.29
%if %{with require_docs}
Requires: system-config-services-docs
%endif
Requires: systemd

%description
system-config-services is a utility which allows you to configure which
services should be enabled on your machine.

%prep
%setup -q -a 1
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0

rm -f config/org.fedoraproject.*

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%buildroot \
    POLKIT0_SUPPORTED=0 \
    install

desktop-file-install --vendor system --delete-original      \
  --dir %{buildroot}%{_datadir}/applications                \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %name

# for consolehelper config
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_sysconfdir}/pam.d/mandriva-simple-auth %{buildroot}%{_sysconfdir}/pam.d/system-config-services
ln -sf %{_bindir}/consolehelper %{buildroot}%{_bindir}/system-config-services

#fix desktop back for using /usr/bin dir

sed -i s/sbin/bin/ %{buildroot}%{_datadir}/applications/system-config-services.desktop

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/applications/system-config-services.desktop
%{_datadir}/icons/hicolor/48x48/apps/system-config-services.png
%{_datadir}/system-config-services
%{python_sitelib}/scservices
%{python_sitelib}/scservices-%{version}-py%{python_version}.egg-info
%{python_sitelib}/scservices.dbus-%{version}-py%{python_version}.egg-info
%{_sysconfdir}/pam.d/*
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.Config.Services.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.Config.Services.service
%{_datadir}/polkit-1/actions/org.freedesktop.config.services.policy
%{_mandir}/*/system-config-services.8*


%changelog
* Tue Aug 16 2011 Александр Казанцев <kazancas@mandriva.org> 0.101.3-5mdv2011.0
+ Revision: 694684
- add consolehelper link to prevent run as not root user

* Thu Aug 11 2011 Александр Казанцев <kazancas@mandriva.org> 0.101.3-4
+ Revision: 694028
- imported package system-config-services

