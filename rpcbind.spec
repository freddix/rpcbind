Summary:	portmap replacement which supports RPC over various protocols
Name:		rpcbind
Version:	0.2.1
Release:	3
License:	BSD
Group:		Daemons
Source0:	http://downloads.sourceforge.net/rpcbind/%{name}-%{version}.tar.bz2
# Source0-md5:	0a5f9c2142af814c55d957aaab3bcc68
Source1:	%{name}.service
Source2:	%{name}.socket
Patch0:		%{name}-syslog.patch
Patch1:		%{name}-sunrpc.patch
URL:		http://rpcbind.sourceforge.net
BuildRequires:	libtirpc-devel
BuildRequires:	pkg-config
Requires(post,preun):	pwdutils
Requires(post,preun,postun):	systemd-units
Provides:	group(rpc)
Provides:	user(rpc)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The rpcbind utility is a server that converts RPC program numbers into
universal addresses. It must be running on the host to be able to make
RPC calls on a server on that machine.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure \
	--enable-warmstarts	\
	--with-rpcuser=rpc	\
	--with-statedir=/run
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{systemdunitdir}}

install rpcbind $RPM_BUILD_ROOT%{_sbindir}
install rpcinfo $RPM_BUILD_ROOT%{_sbindir}

install man/{rpcbind,rpcinfo}.8 $RPM_BUILD_ROOT%{_mandir}/man8

install %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}/rpcbind.service
install %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/rpcbind.socket

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 32 -r -f rpc
%useradd -u 32 -d /usr/share/empty -s /usr/bin/false -c "Portmapper RPC User" -g nobody rpc

%post
%systemd_post rpcbind.service

%preun
%systemd_preun rpcbind.service

%postun
if [ "$1" = "0" ]; then
	%userremove rpc
	%groupremove rpc
fi
%systemd_postun

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_sbindir}/rpcbind
%attr(755,root,root) %{_sbindir}/rpcinfo
%{systemdunitdir}/rpcbind.service
%{systemdunitdir}/rpcbind.socket
%{_mandir}/man8/rpcbind.8*
%{_mandir}/man8/rpcinfo.8*

