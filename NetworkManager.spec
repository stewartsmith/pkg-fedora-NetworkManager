ExcludeArch: s390 s390x

##########################################################
# NetworkManager RPM Specfile
##########################################################

##################################
# Main Package Info
##################################
Name:		NetworkManager
Summary:		A network link manager and user applications
Version:		0.3.2
Release:		3.cvs20041117
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
rm -f $RPM_BUILD_ROOT/%{_bindir}/dhcp_test

##################################
# Clean
##################################
%clean
rm -rf $RPM_BUILD_ROOT


##################################
# Post-install
##################################
%post
if ! chkconfig --list | grep NetworkManager | grep on; then
	/sbin/chkconfig --add NetworkManager
	/sbin/chkconfig --level 123456 NetworkManager off
fi


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
%{_includedir}/NetworkManager/NetworkManager.h
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
%{_libexecdir}/NetworkManagerNotification
%{_datadir}/NetworkManagerNotification
%{_sysconfdir}/dbus-1/system.d/NetworkManagerInfo.conf
%{_datadir}/NetworkManagerInfo
%{_datadir}/icons/hicolor/22x22/apps/*.png
%{_datadir}/icons/hicolor/48x48/apps/*.png

##################################
# Changelog
##################################
%changelog
* Wed Nov 17 2004 <dcbw@redhat.com> - 0.3.2-3.cvs20041117
- Update to CVS
- Fixes to link detection
- Better detection of non-ESSID-broadcasting access points
- Don't dialog-spam the user if a connection fails

* Mon Nov 11 2004 <dcbw@redhat.com> - 0.3.2-2.cvs20041115
- Update to CVS
- Much better link detection, works with Open System authentication
- Blacklist wireless cards rather than whitelisting them

* Fri Oct 29 2004 <dcbw@redhat.com> - 0.3.2-2.cvs20041029
- #rh134893# NetworkManagerInfo and the panel-icon life-cycle
- #rh134895# Status icon should hide when in Wired-only mode
- #rh134896# Icon code needs rewrite
- #rh134897# "Other Networks..." dialog needs implementing
- #rh135055# Menu highlights incorrectly in NM
- #rh135648# segfault with cipsec0
- #rh135722# NetworkManager will not allow zaurus to sync via usb0
- #rh135999# NetworkManager-0.3.1 will not connect to 128 wep
- #rh136866# applet needs tooltips
- #rh137047# lots of applets, yay!
- #rh137341# Network Manager dies after disconnecting from wired network second time
- Better checking for wireless devices
- Fix some memleaks
- Fix issues with dhclient declining an offered address
- Fix an activation thread deadlock
- More accurately detect "Other wireless networks" that are encrypted
- Don't bring devices down as much, won't hotplug-spam as much anymore
	about firmware
- Add a "network not found" dialog when the user chooses a network that could
	not be connected to

* Tue Oct 26 2004 <dcbw@redhat.com> - 0.3.1-2
- Fix escaping of ESSIDs in gconf

* Tue Oct 19 2004  <jrb@redhat.com> - 0.3.1-1
- minor point release to improve error handling and translations

* Fri Oct 15 2004 Dan Williams <dcbw@redhat.com> 0.3-1
- Update from CVS, version 0.3

* Tue Oct 12 2004 Dan Williams <dcbw@redhat.com> 0.2-4
- Update from CVS
- Improvements:
	o Better link checking on wireless cards
	o Panel applet now a Notification Area icon
	o Static IP configuration support

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

