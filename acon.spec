# Arch-independent stuff which ought to be in DATADIR
%define kbddir	%{_prefix}/lib/kbd
%define acondir	%{_prefix}/lib/acon

Summary:	Arabic support for linuxconsole
Summary(ar):	دعم اللغة العربية في لينكس (للشاشات النصّية)
Name:		acon
Version:	1.0.5
Release:	16
License:	GPLv2+
Group:		System/Internationalization
Url:		http://members.tripod.com/ahmedahamid/arabic/arabic.html
Source0:	http://members.tripod.com/ahmedahamid/arabic/acon-%{version}.tar.bz2
Source1:	%{name}.sh
# author refuses to integrate Hebrew support, so we need to provide the
# needed files ourselves and do some small patches
Source2:	%{name}-1.0.4-mdk.tar.bz2
Patch0:		%{name}-1.0.4-mdk.patch
Patch1:		acon-1.0.5-fix-str-fmt.patch
Requires(post,preun):	rpm-helper

%description
The function of acon is to display arabic text from right to left,
and process it to change the letter shape according to its position
in the word.

%description -l ar
برنامج acon يقوم بعملية دعم عرض النصوص العربية من اليمين الى اليسار
واظهار الاشكال الصحيحة للأحرف حسب موقعها في الكلمة.

%prep
%setup -qn %{name} -a2
%patch0 -p1 -b .mdkpatch
%patch1 -p0 -b .str

%build
%serverbuild
%make CFLAGS="%{optflags}"

%install
install -d %{buildroot}%{_bindir}
%makeinstall_std

install -m 755 %{SOURCE1} -D %{buildroot}%{_initrddir}/%{name}

rm %{buildroot}%{acondir}/keymaps/*

%ifarch %{ix86} alpha amd64
cp keymaps/i386/* %{buildroot}%{acondir}/keymaps/
mkdir -p %{buildroot}%{kbddir}/keymaps/i386/qwerty
(cd %{buildroot}%{kbddir}/keymaps/i386/qwerty
 cp ../../../../acon/keymaps/*map .
 gzip -9 *map
)
%endif
%ifarch sparc sparc64
cp keymaps/sun/* %{buildroot}%{acondir}/keymaps/
mkdir -p %{buildroot}%{kbddir}/keymaps/sun
(cd %{buildroot}%{kbddir}/keymaps/sun
 cp ../../../%{name}/keymaps/*map .
 gzip -9 *map
)
%endif
%ifarch ppc
cp keymaps/mac/* %{buildroot}%{acondir}/keymaps/
mkdir -p %{buildroot}%{kbddir}/keymaps/mac
(cd %{buildroot}%{kbddir}/keymaps/mac
 cp ../../../acon/keymaps/*map .
 gzip -9 *map
)
%endif

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%doc doc/* README* AUTHORS CHANGES COPYING
%config(noreplace) %{_initrddir}/%{name}
%{_bindir}/%{name}
%dir %{acondir}
%{acondir}/*
%ifarch %ix86 alpha amd64
%{kbddir}/keymaps/i386/qwerty/*
%endif
%ifarch sparc sparc64
%{kbddir}/keymaps/sun/*
%endif
%ifarch ppc
%{kbddir}/keymaps/mac/*

