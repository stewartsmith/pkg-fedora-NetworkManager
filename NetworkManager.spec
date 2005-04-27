ExcludeArch: s390 s390x

%define hal_version		0.5.0
%define dbus_version	0.31
%define gtk2_version	2.6.0

Name: NetworkManager
Summary: Network link manager and user applications
Version: 0.4
Release: 8.cvs20050404
Group: System Environment/Base
License: GPL
URL: http://people.redhat.com/dcbw/NetworkManager/
Source: %{name}-%{version}.cvs20050404.tar.gz
Patch0: NetworkManager-0.4-newdbus.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root

PreReq:   chkconfig
Requires: wireless-tools >= 27
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_version}
Requires: hal >= %{hal_version}
Requires: iproute openssl
Requires: bind caching-nameserver

BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: hal-devel >= %{hal_version}
BuildRequires: wireless-tools >= 28
BuildRequires: glib2-devel gtk2-devel
BuildRequires: libglade2-devel
BuildRequires: openssl-devel
BuildRequires: GConf2-devel
BuildRequires: gnome-panel-devel
BuildRequires: libgnomeui-devel
BuildRequires: gnome-keyring-devel
BuildRequires: gettext-devel
BuildRequires: pkgconfig

%description
NetworkManager attempts to keep an active network connection available at all
times.  It is intended only for the desktop use-case, and is not intended for
usage on servers.   The point of NetworkManager is to make networking
configuration and setup as painless and automatic as possible.  If using DHCP,
NetworkManager is _intended_ to replace default routes, obtain IP addresses
from a DHCP server, and change nameservers whenever it sees fit.


%package gnome
Summary: GNOME applications for use with NetworkManager
Group: Applications/Internet
Requires: %{name} = %{version}-%{release}
Requires: gnome-panel
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_version}
Requires: hal >= %{hal_version}
PreReq:  gtk2 >= %{gtk2_version}

%description gnome
This package contains GNOME utilities and applications for use with
NetworkManager, including a panel applet for wireless networks.


%package devel
Summary: Libraries and headers for adding NetworkManager support to applications
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_version}

%description devel
This package contains various headers accessing some NetworkManager functionality
from applications.


%package glib
Summary: Libraries and headers for adding NetworkManager support to applications that use glib.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_version}

%description glib
This package contains the headers and libraries that make it easier to use some Network Manager
functionality from applications that use glib.


%prep
%setup -q
%patch0 -p1


%build
export LDFLAGS="$LDFLAGS -lrt -lpthread"
%configure --with-named=/usr/sbin/named --with-named-dir=/var/named/data --with-named-user=named
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}
rm -f $RPM_BUILD_ROOT%{_bindir}/dhcp_test
rm -f $RPM_BUILD_ROOT%{_libdir}/libnm_glib.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libnm_glib.a


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/chkconfig --add NetworkManager

%preun
if [ $1 -eq 0 ]; then
    /sbin/service NetworkManager stop >/dev/null 2>&1
    /sbin/chkconfig --del NetworkManager
fi


%postun
if [ $1 -ge 1 ]; then
    /sbin/service NetworkManager condrestart >/dev/null 2>&1
fi

%post gnome
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%postun gnome
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc COPYING ChangeLog NEWS AUTHORS README CONTRIBUTING TODO
%config %{_sysconfdir}/dbus-1/system.d/%{name}.conf
%config %{_sysconfdir}/rc.d/init.d/%{name}
%config %{_datadir}/%{name}/named.conf
%{_bindir}/%{name}
%{_bindir}/NMLoadModules
%{_bindir}/NetworkManagerDispatcher
%{_libdir}/pkgconfig/%{name}.pc

%files gnome
%defattr(-,root,root,0755)
%config %{_sysconfdir}/dbus-1/system.d/NetworkManagerInfo.conf
%{_bindir}/NetworkManagerInfo
%{_libexecdir}/NetworkManagerNotification
%{_datadir}/NetworkManagerNotification/
%{_datadir}/NetworkManagerInfo/
%{_datadir}/icons/hicolor/22x22/apps/*.png
%{_datadir}/icons/hicolor/48x48/apps/*.png

%files devel
%defattr(-,root,root,0755)
%{_includedir}/%{name}/%{name}.h

%files glib
%defattr(-,root,root,0755)
%{_libdir}/libnm_glib.so*
%{_includedir}/%{name}/libnm_glib.h
%{_libdir}/pkgconfig/libnm_glib.pc


%changelog
* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 0.4-8.cvs20050404
- fix build with newer dbus

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 0.4-7.cvs20050404
- silence %%post

* Mon Apr  4 2005 Dan Williams <dcbw@redhat.com> 0.4-6.cvs20050404
- #rh153234# NetworkManager quits/cores just as a connection is made

* Fri Apr  2 2005 Dan Williams <dcbw@redhat.com> 0.4-5.cvs20050402
- Update from latest CVS HEAD

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> 0.4-4.cvs20050315
- Update the GTK+ theme icon cache on (un)install

* Tue Mar 15 2005 Ray Strode <rstrode@redhat.com> 0.4-3.cvs20050315
- Pull from latest CVS HEAD

* Tue Mar 15 2005 Ray Strode <rstrode@redhat.com> 0.4-2.cvs20050315
- Upload new source tarball (woops)

* Tue Mar 15 2005 Ray Strode <rstrode@redhat.com> 0.4-1.cvs20050315
- Pull from latest CVS HEAD (hopefully works again)

* Mon Mar  7 2005 Ray Strode <rstrode@redhat.com> 0.4-1.cvs20050307
- Pull from latest CVS HEAD
- Commit broken NetworkManager to satisfy to dbus dependency

* Fri Mar  4 2005 Dan Williams <dcbw@redhat.com> 0.3.4-1.cvs20050304
- Pull from latest CVS HEAD
- Rebuild for gcc 4.0

* Tue Feb 22 2005 Dan Williams <dcbw@redhat.com> 0.3.3-2.cvs20050222
- Update from CVS

* Mon Feb 14 2005 Dan Williams <dcbw@redhat.com> 0.3.3-2.cvs20050214.x.1
- Fix free of invalid pointer for multiple search domains

* Mon Feb 14 2005 Dan Williams <dcbw@redhat.com> 0.3.3-2.cvs20050214
- Never automatically choose a device that doesn't support carrier detection
- Add right-click menu to applet, can now "Pause/Resume" scanning through it
- Fix DHCP Renew/Rebind timeouts
- Fix frequency cycling problem on some cards, even when scanning was off
- Play better with IPv6
- Don't send kernel version in DHCP packets, and ensure DHCP packets are at
	least 300 bytes in length to work around broken router
- New DHCP options D-BUS API by Dan Reed
- Handle multiple domain search options in DHCP responses

* Wed Feb  2 2005 Dan Williams <dcbw@redhat.com> 0.3.3-1.cvs20050202
- Display wireless network name in applet tooltip
- Hopefully fix double-default-route problem
- Write out valid resolv.conf when we exit
- Make multi-domain search options work
- Rework signal strength code to be WEXT conformant, if strength is
	still wierd then its 95% surely a driver problem
- Fix annoying instances of suddenly dropping and reactivating a
	wireless device (Cisco cards were worst offenders here)
- Fix some instances of NetworkManager not remembering your WEP key
- Fix some races between NetworkManager and NetworkManagerInfo where
	NetworkManager wouldn't recognize changes in the allowed list
- Don't shove Ad-Hoc Access Point MAC addresses into GConf

* Tue Jan 25 2005 Dan Williams <dcbw@redhat.com> 0.3.3-1.cvs20050125
- Play nice with dbus 0.23
- Update our list of Allowed Wireless Networks more quickly

* Mon Jan 24 2005 Dan Williams <dcbw@redhat.com> 0.3.3-1.cvs20050124
- Update to latest CVS
- Make sure we start as late as possible so that we ensure dbus & HAL
	are already around
- Fix race in initial device activation

* Mon Jan 24 2005 Than Ngo <than@redhat.com> 0.3.3-1.cvs20050112.4
- rebuilt against new wireless tool

* Thu Jan 21 2005 <dcbw@redhat.com> - 0.3.3-1.cvs20050118
- Fix issue where NM wouldn't recognize that access points were
	encrypted, and then would try to connect without encryption
- Refine packaging to put client library in separate package
- Remove bind+caching-nameserver dep for FC-3, use 'nscd -i hosts'
	instead.  DNS queries may timeout now right after device
	activation due to this change.

* Wed Jan 12 2005 <dcbw@redhat.com> - 0.3.3-1.cvs20050112
- Update to latest CVS
- Fixes to DHCP code
- Link-Local (ZeroConf/Rendezvous) support
- Use bind in "caching-nameserver" mode to work around stupidity
	in glibc's resolver library not recognizing resolv.conf changes
- #rh144818# Clean up the specfile (Patch from Matthias Saou)
- Ad-Hoc mode support with Link-Local addressing only (for now)
- Fixes for device activation race conditions
- Wireless scanning in separate thread

* Wed Dec  8 2004 <dcbw@redhat.com> - 0.3.2-4.3.cvs20041208
- Update to CVS
- Updates to link detection, DHCP code
- Remove NMLaunchHelper so we start up faster and don't
	block for a connection.  This means services that depend
	on the network may fail if they start right after NM
- Make sure DHCP renew/rebinding works

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

