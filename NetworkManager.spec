ExcludeArch: s390 s390x

##########################################################
# NetworkManager RPM Specfile
##########################################################

##################################
# Main Package Info
##################################
Name:		NetworkManager
Summary:		A network link manager and user applications
Version:		0.2
Release:		3
Group:		System Environment/Base
License:		GPL
Source:		%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

########################
PreReq:	chkconfig
Requires: wireless-tools >= 27
Requires: dbus >= 0.22
Requires: dbus-glib >= 0.22
Requires: hal >= 0.2.95
Requires: dhclient iproute openssl glib2


########################
BuildRequires: dbus-devel >= 0.22
BuildRequires: hal-devel >= 0.2.95
BuildRequires: wireless-tools >= 27
BuildRequires: glib2-devel gtk2-devel
BuildRequires: libglade2-devel
BuildRequires: openssl-devel
BuildRequires: GConf2-devel
BuildRequires: gnome-panel-devel
BuildRequires: libgnomeui-devel


##################################
%description
NetworkManager is a network link manager that attempts to keep a
wired or wireless network connection active at all times.


##################################
# GNOME Package Info
##################################
%package gnome
Summary: GNOME applications for use with NetworkManager
Group: Applications/Internet
Requires: NetworkManager
Requires: GConf2
Requires: gnome-panel
Requires: dbus >= 0.22
Requires: dbus-glib >= 0.22
Requires: glib2
Requires: libglade2

%description gnome
This package contains GNOME utilities and applications for use
with NetworkManager, including a panel applet for wireless
networks.


##################################
# Prep/Setup
##################################
%prep
%setup -q


##################################
# Build
##################################
%build

%configure
make


##################################
# Install
##################################
%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT


##################################
# Clean
##################################
%clean
rm -rf $RPM_BUILD_ROOT


##################################
# Post-install
##################################
%post
/sbin/chkconfig --add NetworkManager
/sbin/chkconfig --level 123456 NetworkManager off


##################################
# Pre-uninstall
##################################
%preun
if [ $1 = 0 ]; then
    service NetworkManager stop > /dev/null 2>&1
    /sbin/chkconfig --del NetworkManager
fi


##################################
# Post-uninstall
##################################
%postun
if [ "$1" -ge "1" ]; then
  service NetworkManager condrestart > /dev/null 2>&1
fi


##################################
# Main Package Files
##################################
%files
%defattr(-,root,root)
%doc COPYING ChangeLog NEWS AUTHORS README CONTRIBUTING TODO
%{_bindir}/%{name}
%{_bindir}/NMLoadModules
%{_bindir}/NMLaunchHelper
%{_bindir}/NetworkManagerDispatcher
%dir %{_sysconfdir}/dbus-1/system.d
%config %{_sysconfdir}/dbus-1/system.d/%{name}.conf
%config %{_sysconfdir}/rc.d/init.d/%{name}
%{_libdir}/pkgconfig/*
%{_datadir}/locale/*/*/*.mo

%files gnome
%defattr(-,root,root)
%{_bindir}/NetworkManagerInfo
%{_libexecdir}/NMWirelessApplet
%{_libdir}/bonobo/servers/NMWirelessApplet.server
%{_sysconfdir}/dbus-1/system.d/NetworkManagerInfo.conf
%{_datadir}/pixmaps/NMWirelessApplet/*
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/NetworkManagerInfo
%{_datadir}/NMWirelessApplet/wireless-applet.glade

##################################
# Changelog
##################################
%changelog
* Mon Sep 13 2004 Dan Williams <dcbw@redhat.com> 0.2-3
- Update from CVS

* Sat Sep 11 2004 Dan Williams <dcbw@redhat.com> 0.2-2
- Require gnome-panel, not gnome-panel-devel
- Turn off by default

* Thu Aug 26 2004 Dan Williams <dcbw@redhat.com> 0.2-1
- Update to 0.2

* Thu Aug 26 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- spec-changes to req glib2 instead of glib

* Fri Aug 20 2004 Dan Williams <dcbw@redhat.com> 0.1-3
- First public release

