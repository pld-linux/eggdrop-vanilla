%define		_name	eggdrop
Summary:	Eggdrop is an IRC bot, written in C
Summary(pl.UTF-8):	Eggdrop jest botem IRC napisanym w C
Name:		eggdrop-vanilla
Version:	1.6.19
Release:	2
License:	GPL v2
Group:		Applications/Communications
Source0:	ftp://ftp.eggheads.org/pub/eggdrop/source/1.6/%{_name}%{version}.tar.bz2
# Source0-md5:	b706bbe4fdd05964e0ea0cd920f28539
Patch0:		%{name}-FHS.patch
Patch1:		%{name}-topicprot.patch
Patch2:		%{name}-autobotchk.patch
Patch3:		%{name}-nolibs.patch
Patch4:		%{name}-ssl.patch
Patch5:		%{name}-nohostwhowhom.patch
Patch6:		%{name}-bz-463.patch
URL:		http://www.eggheads.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	tcl-devel
Requires:	tcl
Obsoletes:	eggdrop
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Eggdrop is an IRC bot, written in C. If you don't know what IRC is,
this is probably not whatever you're looking for! Eggdrop, being a
bot, sits on a channel and takes protective measures: to keep the
channel from being taken over (in the few ways that anything CAN), to
recognize banished users or sites and reject them, to recognize
privileged users and let them gain ops, etc. Eggdrop also contains
many modules and scripts, for example for sending files.

%description -l pl.UTF-8
Eggdrop jest IRCowym botem napisanym w C. Eggdrop, będąc botem jest
na kanale i zajmuje się jego ochroną: zabezpieczeniem przed
przejęciem, nadawaniem odpowiednich przywilejów zarejestrowanym
użytkownikom, pilnowanie tzw. banów itp. Eggdrop poza tymi funkcjami
posiada także wiele dodatków, jak przesyłanie plików czy inne
skrypty dla rozrywki.

%prep
%setup -q -n %{_name}%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
mv aclocal.m4 acinclude.m4
cp -f /usr/share/automake/config.sub misc/
cp -f %{_name}.conf doc/%{_name}.conf.example
%{__aclocal}
%{__autoheader}
%{__autoconf}
cd src/mod/compress.mod
%{__autoconf}
%configure
cd ../dns.mod
%{__autoconf}
%configure
cd ../../..
%configure
%{__make} config
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{_name}/modules,%{_mandir}/man1,%{_datadir}/%{_name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT/%{_name}-%{version} $RPM_BUILD_ROOT%{_bindir}/%{_name}
mv -f $RPM_BUILD_ROOT{/{text/*,help,scripts,language},%{_datadir}/%{_name}/}
mv -f $RPM_BUILD_ROOT/modules/* $RPM_BUILD_ROOT%{_libdir}/%{_name}/modules/
mv -f $RPM_BUILD_ROOT{/doc,%{_mandir}}/man1/%{_name}.1
rm -rf $RPM_BUILD_ROOT/{doc,README,logs,eggdrop.conf}

rm -rf docs
cp -a doc docs
rm -rf docs/{man1,Makefile*}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*
%attr(755,root,root) %{_bindir}/%{_name}
%dir %{_libdir}/%{_name}
%dir %{_libdir}/%{_name}/modules
%attr(755,root,root) %{_libdir}/%{_name}/modules/*.so
%{_datadir}/%{_name}
%{_mandir}/man1/%{_name}.1*
