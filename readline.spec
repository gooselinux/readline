Summary: A library for editing typed command lines
Name: readline
Version: 6.0
Release: 3%{?dist}
License: GPLv3+
Group: System Environment/Libraries
URL: http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
Source: ftp://ftp.gnu.org/gnu/readline/readline-%{version}.tar.gz
Patch1: ftp://ftp.gnu.org/gnu/readline/readline-6.0-patches/readline60-001
Patch2: ftp://ftp.gnu.org/gnu/readline/readline-6.0-patches/readline60-002
Patch3: ftp://ftp.gnu.org/gnu/readline/readline-6.0-patches/readline60-003
Patch4: ftp://ftp.gnu.org/gnu/readline/readline-6.0-patches/readline60-004
# fix file permissions, remove RPATH, use CFLAGS
Patch20: readline-6.0-shlib.patch
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildRequires: ncurses-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Readline library provides a set of functions that allow users to
edit command lines. Both Emacs and vi editing modes are available. The
Readline library includes additional functions for maintaining a list
of previously-entered command lines for recalling or editing those
lines, and for performing csh-like history expansion on previous
commands.

%package devel
Summary: Files needed to develop programs which use the readline library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: ncurses-devel
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description devel
The Readline library provides a set of functions that allow users to
edit typed command lines. If you want to develop programs that will
use the readline library, you need to have the readline-devel package
installed. You also need to have the readline package installed.

%package static
Summary: Static libraries for the readline library
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The readline-static package contains the static version of the readline
library.

%prep
%setup -q
%patch1 -p0 -b .001
%patch2 -p0 -b .002
%patch3 -p0 -b .003
%patch4 -p0 -b .004
%patch20 -p1 -b .shlib

pushd examples
rm -f rlfe/configure
iconv -f iso8859-1 -t utf8 -o rl-fgets.c{_,}
touch -r rl-fgets.c{,_}
mv -f rl-fgets.c{_,}
popd

%build
export CPPFLAGS="-I%{_includedir}/ncurses"
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

mkdir $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libreadline.so.* $RPM_BUILD_ROOT/%{_lib}
for l in $RPM_BUILD_ROOT%{_libdir}/libreadline.so; do
    ln -sf $(echo %{_libdir} | \
        sed 's,\(^/\|\)[^/][^/]*,..,g')/%{_lib}/$(readlink $l) $l
done

rm -rf $RPM_BUILD_ROOT%{_datadir}/readline
rm -f $RPM_BUILD_ROOT%{_infodir}/dir*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/install-info %{_infodir}/history.info.gz %{_infodir}/dir &> /dev/null
/sbin/install-info %{_infodir}/rluserman.info.gz %{_infodir}/dir &> /dev/null
:

%postun -p /sbin/ldconfig

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/history.info.gz %{_infodir}/dir &> /dev/null
   /sbin/install-info --delete %{_infodir}/rluserman.info.gz %{_infodir}/dir &> /dev/null
fi
:

%post devel
/sbin/install-info %{_infodir}/readline.info.gz %{_infodir}/dir &> /dev/null
:

%preun devel
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/readline.info.gz %{_infodir}/dir &> /dev/null
fi
:

%files
%defattr(-,root,root,-)
%doc CHANGES COPYING NEWS README USAGE
/%{_lib}/libreadline*.so.*
%{_libdir}/libhistory*.so.*
%{_infodir}/history.info*
%{_infodir}/rluserman.info*

%files devel
%defattr(-,root,root,-)
%doc examples/*.c examples/*.h examples/rlfe
%{_includedir}/readline
%{_libdir}/lib*.so
%{_mandir}/man3/*
%{_infodir}/readline.info*

%files static
%defattr(-,root,root,-)
%{_libdir}/lib*.a

%changelog
* Tue Aug 25 2009 Miroslav Lichvar <mlichvar@redhat.com> 6.0-3
- include patch 004
- suppress install-info errors (#515910)
- remove dir* in infodir after install (#492097)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Miroslav Lichvar <mlichvar@redhat.com> 6.0-1
- update to 6.0
- include patches 001, 002, 003

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Mar 23 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 5.2-13
- Fix the previous %%changelog entry authorship.

* Sun Mar 23 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 5.2-12
- Fix excessive prompts on CTRL-C abort while the prompt is being printed.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.2-11
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.2-10
- move libreadline to /lib

* Thu Jan 03 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.2-9
- include upstream patches 008-011

* Mon Nov 05 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.2-8
- fix cursor position when prompt has one invisible character (#358231)
- merge review fixes (#226361)
- fix source URL

* Mon Aug 27 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.2-7
- include patches 005, 006, 007

* Wed Aug 22 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.2-6
- update license tag

* Tue May 29 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.2-5
- include patches 5.2-003, 5.2-004

* Thu Mar 22 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.2-4
- apply 5.2-002 patch

* Thu Mar 15 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.2-3
- link libreadline with libtinfo (#232277)
- include upstream 5.2-001 patch
- move static libraries to -static subpackage, spec cleanup

* Thu Nov 30 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.2-2
- require ncurses-devel instead of libtermcap-devel

* Mon Nov 13 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.2-1
- update to 5.2 (#213795)
- use CFLAGS when linking (#199374)
- package docs and examples (#172497)
- spec cleanup

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.1-1.1
- rebuild

* Mon Jul 10 2006 Jindrich Novy <jnovy@redhat.com> 5.1-1
- update to readline-5.1
- apply new proposed upstream patches for 5.1 (001-004)
- drop "read -e" patch, applied upstream

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.0-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.0-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 5.0-3
- Rebuild for new GCC.

* Tue Jan 18 2005 Tim Waugh <twaugh@redhat.com> 5.0-2
- Fix line-wrapping (bug #145329).
- Apply "read -e" patch from bash package.

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 5.0-1
- 5.0 (bug #144835).

* Mon Nov 29 2004 Tim Waugh <twaugh@redhat.com> 4.3-14
- Added URL tag (bug #141106).

* Thu Sep  2 2004 Jeremy Katz <katzj@redhat.com> - 4.3-13
- rebuild so that static linking against readline will work on ppc64 
  without dot symbols

* Mon Jun 28 2004 Tim Waugh <twaugh@redhat.com> 4.3-12
- Build requires libtool (bug #126589).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Nov 28 2003 Thomas Woerner <twoerner@redhat.com> 4.3-9
- removed rpath

* Thu Nov  6 2003 Tim Waugh <twaugh@redhat.com> 4.3-8
- Apply upstream patches (bug #109240 among others).

* Wed Jun 25 2003 Tim Waugh <twaugh@redhat.com>
- devel package requires libtermcap-devel (bug #98015).

* Wed Jun 25 2003 Tim Waugh <twaugh@redhat.com> 4.3-7
- Fixed recursion loop (bug #92372).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 20 2002 Tim Powers <timp@redhat.com>
- rebuild in current collinst
- BuildRequires autoconf only

* Wed Aug 07 2002 Phil Knirsch <pknirsch@redhat.com> 4.3-3
- Fixed Esc-O-M stack overflow bug.

* Mon Jul 22 2002 Phil Knirsch <pknirsch@redhat.com> 4.3-1
- Updated to latest readline release 4.3

* Thu Jul 11 2002 Phil Knirsch <pknirsch@redhat.com> 4.2a-7
- Fixed problem with alpha build.

* Wed Jul 10 2002 Phil Knirsch <pknirsch@redhat.com>
- Fixed utf8 problem (originally observed in bash).

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 4.2a-6
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com> 4.2a-5
- automated rebuild

* Wed Mar 20 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.2a-4
- Use autoconf 2.53, not 2.52

* Mon Mar  4 2002 Bernhard Rosenkraenzer <bero@redhat.com> 4.2a-3
- Rebuild

* Mon Nov 26 2001 Matt Wilson <msw@redhat.com> 4.2a-2
- removed the manual symlinking of .so, readline handles this by itself
- call only %%makeinstall, not %%makeinstall install install-shared as
  this makes bogus .old files in the buildroot

* Tue Nov 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 4.2a-1
- 4.2a

* Tue Oct  2 2001 Bernhard Rosenkraenzer <bero@redhat.com> 4.2-4
- Work around autoconf bug

* Mon Oct  1 2001 Bernhard Rosenkraenzer <bero@redhat.com> 4.2-3
- Don't use readline's internal re-implementation of strpbrk on systems
  that have strpbrk - the system implementation is faster and better maintained.

* Tue Aug  7 2001 Bernhard Rosenkraenzer <bero@redhat.com> 4.2-2
- Make sure headers can be included from C++ applications (#51131)
  (Patch based on Debian's with the bugs removed ;) )

* Wed May 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.2 and adapt patches

* Fri Apr  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- change the paths listed for the header files in the man page to reflect
  the location changes from previous versions (#35073)
- note that "on" is acceptable instead of "On" in the man page (#21327)

* Thu Mar  8 2001 Preston Brown <pbrown@redhat.com>
- fix reading of end key termcap value (@7 is correct, was kH) (#30884)

* Tue Jan 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- mark the man page as currently out-of-date (#25294)

* Thu Sep  7 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging (64bit systems need to use libdir).

* Thu Aug 17 2000 Jeff Johnson <jbj@redhat.com>
- summaries from specspo.

* Wed Aug  2 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- use "rm -f" in specfile

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Tue Mar 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 4.1

* Thu Feb 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0

* Fri Apr 09 1999 Michael K. Johnson <johnsonm@redhat.com>
- added guard patch from Taneli Huuskonen <huuskone@cc.helsinki.fi>

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Sun Jul 26 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.2.1

* Wed May 06 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- don't package /usr/info/dir

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- devel package moved to Development/Libraries

* Tue Apr 21 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.2

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Fri Oct 10 1997 Erik Troan <ewt@redhat.com>
- added proper sonames

* Tue Jul 08 1997 Erik Troan <ewt@redhat.com>
- updated to readline 2.1

* Tue Jun 03 1997 Erik Troan <ewt@redhat.com>
- built against glibc
