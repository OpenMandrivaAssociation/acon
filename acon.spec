# Arch-independent stuff which ought to be in DATADIR
%define kbddir	%{_prefix}/lib/kbd
%define acondir	%{_prefix}/lib/acon

Summary:	Arabic support for linuxconsole
Name:		acon
Version:	1.0.5
Release:	17
License:	GPLv2+
Group:		System/Internationalization
Source:		http://members.tripod.com/ahmedahamid/arabic/acon-%{version}.tar.bz2
Source1:	%{name}.service
Source3:	%{name}.launcher
# author refuses to integrate Hebrew support, so we need to provide the
# needed files ourselves and do some small patches
Source2:	%{name}-1.0.4-mdk.tar.bz2
Patch0:		%{name}-1.0.4-mdk.patch
Patch1:		acon-1.0.5-fix-str-fmt.patch
URL:		http://members.tripod.com/ahmedahamid/arabic/arabic.html
Requires(post): rpm-helper
Requires(preun):rpm-helper

%description
The function of acon is to display arabic text from right to left,
and process it to change the letter shape according to its position
in the word.

%prep
%setup -q -n %{name} -a2

%patch0 -p1 -b .mdkpatch
%patch1 -p0 -b .str

%build
%serverbuild
%make CFLAGS="%{optflags}"

%install
install -d %{buildroot}%{_bindir}
%makeinstall_std

install -m 755 %{SOURCE1} -D %{buildroot}%{_unitdir}/%{name}.service
install -m 755 %{SOURCE3} -D %{buildroot}%{_bindir}/%{name}.launcher

rm %{buildroot}%{acondir}/keymaps/*

cp keymaps/i386/* %{buildroot}%{acondir}/keymaps/
mkdir -p %{buildroot}%{kbddir}/keymaps/i386/qwerty
(cd %{buildroot}%{kbddir}/keymaps/i386/qwerty
 cp ../../../../acon/keymaps/*map .
 gzip -9 *map
)

%clean

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%doc doc/* README* AUTHORS CHANGES COPYING
%{_unitdir}/%{name}.service
%{_bindir}/%{name}*
%dir %{acondir}
%{acondir}/*
%{kbddir}/keymaps/i386/qwerty/*


