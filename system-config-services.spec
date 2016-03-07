%bcond_without require_docs

Summary: Utility to start and stop system services
Name: system-config-services
Version: 0.111.4
Release: 1
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
BuildRequires: python2
BuildRequires: python2-devel
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: sed
BuildRequires: desktop-file-utils
Requires: chkconfig
Requires: python-gamin
Requires: hicolor-icon-theme
Requires: pygtk2.0
Requires: pygtk2.0-libglade
Requires: python2 >= 2.3.0
Requires: python2-dbus
Requires: python2-slip >= 0.1.11
Requires: python2-slip-dbus >= 0.2.8
Requires: python2-slip-gtk
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

sed -i 's/python/python2/' Makefile py_rules.mk

%build
%make

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

%files -f %{name}.lang
%doc COPYING
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/applications/system-config-services.desktop
%{_datadir}/icons/hicolor/*/apps/system-config-services*.*
%{_datadir}/system-config-services
%{python2_sitelib}/scservices
%{python2_sitelib}/scservices-%{version}-py*.egg-info
%{python2_sitelib}/scservices.dbus-%{version}-py*.egg-info
%{_sysconfdir}/pam.d/*
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.Config.Services.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.Config.Services.service
%{_datadir}/polkit-1/actions/org.freedesktop.config.services.policy
%{_mandir}/*/system-config-services.8*

