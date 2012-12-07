%define	name	acon
%define	version	1.0.5
%define	release	%mkrel 15
# Arch-independent stuff which ought to be in DATADIR
%define kbddir	%{_prefix}/lib/kbd
%define acondir	%{_prefix}/lib/acon

Summary:	Arabic support for linuxconsole
# Support for localized summaries is obsolete,
# should go to specspo
#Summary(ar):	Ø¯Ø¹Ù… Ø§Ù„Ù„ØºØ© Ø§Ù„Ø¹Ø±Ø¨ÙŠØ© ÙÙŠ Ù„ÙŠÙ†ÙƒØ³ (Ù„Ù„Ø´Ø§Ø´Ø§Øª Ø§Ù„Ù†ØµÙ‘ÙŠØ©)
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		System/Internationalization
Source:		http://members.tripod.com/ahmedahamid/arabic/acon-%{version}.tar.bz2
Source1:	%{name}.sh
# author refuses to integrate Hebrew support, so we need to provide the
# needed files ourselves and do some small patches
Source2:	%{name}-1.0.4-mdk.tar.bz2
Patch0:		%{name}-1.0.4-mdk.patch
Patch1:		acon-1.0.5-fix-str-fmt.patch
URL:		http://members.tripod.com/ahmedahamid/arabic/arabic.html
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Requires(post): rpm-helper
Requires(preun):rpm-helper

%description
The function of acon is to display arabic text from right to left,
and process it to change the letter shape according to its position
in the word.

# Support for localized descriptions is obsolete,
# should go to specspo
#%description -l ar
#Ø¨Ø±Ù†Ø§Ù…Ø¬ acon ÙŠÙ‚ÙˆÙ… Ø¨Ø¹Ù…Ù„ÙŠØ© Ø¯Ø¹Ù… Ø¹Ø±Ø¶ Ø§Ù„Ù†ØµÙˆØµ Ø§Ù„Ø¹Ø±Ø¨ÙŠØ© Ù…Ù† Ø§Ù„ÙŠÙ…ÙŠÙ† Ø§Ù„Ù‰ Ø§Ù„ÙŠØ³Ø§Ø±
#ÙˆØ§Ø¸Ù‡Ø§Ø± Ø§Ù„Ø§Ø´ÙƒØ§Ù„ Ø§Ù„ØµØ­ÙŠØ­Ø© Ù„Ù„Ø£Ø­Ø±Ù Ø­Ø³Ø¨ Ù…ÙˆÙ‚Ø¹Ù‡Ø§ ÙÙŠ Ø§Ù„ÙƒÙ„Ù…Ø©.

%prep
%setup -q -n %{name} -a2

%patch0 -p1 -b .mdkpatch
%patch1 -p0 -b .str

%build
%serverbuild
%make CFLAGS="%{optflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
%makeinstall_std

install -m 755 %{SOURCE1} -D $RPM_BUILD_ROOT%{_initrddir}/%{name}

rm $RPM_BUILD_ROOT%{acondir}/keymaps/*

%ifarch %{ix86} alpha amd64
cp keymaps/i386/* $RPM_BUILD_ROOT%{acondir}/keymaps/
mkdir -p $RPM_BUILD_ROOT%{kbddir}/keymaps/i386/qwerty
(cd $RPM_BUILD_ROOT%{kbddir}/keymaps/i386/qwerty
 cp ../../../../acon/keymaps/*map .
 gzip -9 *map
)
%endif
%ifarch sparc sparc64
cp keymaps/sun/* $RPM_BUILD_ROOT%{acondir}/keymaps/
mkdir -p $RPM_BUILD_ROOT%{kbddir}/keymaps/sun
(cd $RPM_BUILD_ROOT%{kbddir}/keymaps/sun
 cp ../../../%{name}/keymaps/*map .
 gzip -9 *map
)
%endif
%ifarch ppc
cp keymaps/mac/* $RPM_BUILD_ROOT%{acondir}/keymaps/
mkdir -p $RPM_BUILD_ROOT%{kbddir}/keymaps/mac
(cd $RPM_BUILD_ROOT%{kbddir}/keymaps/mac
 cp ../../../acon/keymaps/*map .
 gzip -9 *map
)
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(-,root,root)
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
%endif


%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-14mdv2011.0
+ Revision: 662750
- mass rebuild

* Mon Nov 29 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-13mdv2011.0
+ Revision: 603168
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-12mdv2010.1
+ Revision: 521932
- rebuilt for 2010.1

  + Sandro Cazzaniga <kharec@mandriva.org>
    - fix version

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-10mdv2010.0
+ Revision: 413020
- rebuild

* Tue Apr 07 2009 Funda Wang <fwang@mandriva.org> 1.0.5-9mdv2009.1
+ Revision: 364706
- fix str fmt
- bunzip the patch
- fix patch num

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 1.0.5-9mdv2009.0
+ Revision: 220326
- rebuild

* Wed Jan 23 2008 Thierry Vignaud <tv@mandriva.org> 1.0.5-8mdv2008.1
+ Revision: 157235
- rebuild with fixed %%serverbuild macro

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 1.0.5-7mdv2008.1
+ Revision: 148410
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed May 23 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.0.5-6mdv2008.0
+ Revision: 30220
- Import acon



* Mon Aug 21 2006 Emmanuel Andry <eandry@mandriva.com> 1.0.5-6mdv2007.0
- Rebuild

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.0.5-5mdk
- Rebuild

* Thu Aug 11 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.0.5-4mdk
- fix rpmlint errors(bis)

* Wed Aug 10 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.0.5-3mdk
- fix rpmlint errors

* Tue Oct 21 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.5-2mdk
- fix build

* Fri Jul 18 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.0.5-1mdk
- rebuild
- s/Copyright/License/
- move changelog to the end of the spec file
- use %%make macro
- quiet setup
- macroize
- cosmetics
- be sure to use $RPM_OPT_FLAGS
- build on other archs too, seems to build just fine on sparc, report if
  problems on other archs

* Fri Aug 31 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 1.0.4-6mdk
- fixed a typo in init script; converted translatable strings to simpler
  format.

* Wed Apr  4 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.0.4-5mdk
- use /var/lock/subsys/acon in intscript
- use server macros

* Tue Mar 27 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.4-4mdk
- macrozifaction
- use %%ix86
- fix tmppath
- get rid of tar

* Tue Mar 06 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 1.0.4-3mdk
- rebuild for new glibc and distrib.
- adapted the rc.d script
- converted descriptions to UTF-8

* Wed Jul 19 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 1.0.4-2mdk
- fixed keymaps
- made it exclusivearch for the PC (until the sources are fixed)

* Thu Jun  8 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 1.0.4-1mdk
- updated to 1.0.4
- added support for Farsi and Hebrew
- improved sysinit script

* Wed Mar 22 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 1.0.3-1mdk
- updated to 1.0.3
- new Group: naming
- added doc/ directory
- moved *.map files to {_libdir}/kbd/i386/qwerty/ where they belong
  (yes, this package needs adaptation to PPC and such)

* Sat Oct 30 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- updated to 1.0.2

* Fri Aug 13 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- first rpm version
