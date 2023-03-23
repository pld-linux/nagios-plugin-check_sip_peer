Summary:	Nagios plugin to check SIP peer status
Name:		nagios-plugin-check_sip_peer
Version:	0.1
Release:	1
License:	GPL v3+
Group:		Networking
Source0:	check_sip_peer.py
# Source0-md5:	6bccc1b1fcd481df7065c6285aadbe25
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.654
Requires:	nagios-core
Requires:	nagios-plugins-libs
Requires:	python3-modules
Requires:	python3-sarge
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_prefix}/lib/nagios/plugins
%define		_sysconfdir	/etc/nagios/plugins

%define		_noautoreq_perl utils

%description
This plugin will test a SIP peer status.

%prep
%setup -q -c -T

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_plugindir}}

cp -p %{SOURCE0} $RPM_BUILD_ROOT%{_plugindir}/check_sip_peer

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_plugindir}/check_sip_peer
