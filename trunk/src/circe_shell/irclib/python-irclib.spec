Summary: A set of Python modules for IRC support.
Name: python-irclib
Version: 0.4.1
Release: 1
Group: Development/Libraries
License: LGPL
URL: http://python-irclib.sourceforge.net
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-root
Requires: python
BuildPrereq: python
BuildArch: noarch

%description
This library is intended to encapsulate the IRC protocol at a quite
low level.  It provides an event-driven IRC client framework.  It has
a fairly thorough support for the basic IRC protocol, CTCP and DCC
connections.

%prep
%setup -q
chmod 644 *

%build
python -c "import py_compile; py_compile.compile('irclib.py')"
python -c "import py_compile; py_compile.compile('ircbot.py')"

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT/usr/lib/python1.5/site-packages
%{__install} -m 644 irclib.py* $RPM_BUILD_ROOT/usr/lib/python1.5/site-packages
%{__install} -m 644 ircbot.py* $RPM_BUILD_ROOT/usr/lib/python1.5/site-packages

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README ChangeLog COPYING irccat irccat2 servermap testbot.py dccsend dccreceive
/usr/lib/python*/site-packages/*

%changelog
* Mon Sep  1 2002 Gary Benson <gary@inauspicious.org> 0.4.0-1
- upgraded to 0.4.0

* Wed Feb 20 2002 Gary Benson <gary@inauspicious.org> 0.3.4-1
- upgraded to 0.3.4

* Wed Feb 20 2002 Gary Benson <gary@inauspicious.org> 0.3.3-1
- initial revision
