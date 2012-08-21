# INFO: Package contains data-only, no binaries, so no debuginfo is needed
%define debug_package %{nil}


Summary: X Keyboard Extension configuration data
Name: xkeyboard-config
Version: 2.6
Release: 3.2
License: MIT
Group: User Interface/X
URL: http://www.freedesktop.org/wiki/Software/XKeyboardConfig

Source: %{name}-%{version}.tar.gz

#%if 0%{?gitdate}
#Source0:    %{name}-%{gitdate}.tar.bz2
#Source1:    make-git-snapshot.sh
#Source2:    commitid
#%else
#Source0: http://xorg.freedesktop.org/archive/individual/data/xkeyboard-config/%{name}-%{version}.tar.bz2
#%endif

# Bug 826220 - Tilda is now a dead key (for accented chars)
#Patch01: 0001-Reverting-broken-fix-for-is-keyboard.patch

BuildArch: noarch

BuildRequires: pkgconfig
BuildRequires: xorg-x11-xutils-dev
BuildRequires: xkbcomp
BuildRequires: perl(XML::Parser)
BuildRequires: intltool
BuildRequires: gettext
#BuildRequires: git-core
BuildRequires: automake autoconf libtool pkgconfig
BuildRequires: glib2-devel
BuildRequires: pkgconfig(xproto)
BuildRequires: libX11-devel
BuildRequires: libxslt
Provides:    xkbdata

%package -n xkb-data
Summary:    X Keyboard Extension (XKB) configuration data
Group:      System/X11

%description -n xkb-data
%{summary}

%package -n xkb-data-i18n
Summary:    X Keyboard Extension (XKB) configuration data
Group:      System/X11

%description -n xkb-data-i18n
%{summary}

%description
This package contains configuration data used by the X Keyboard Extension 
(XKB), which allows selection of keyboard layouts when using a graphical 
interface. 

%package devel
Summary: Development files for %{name}
Group: User Interface/X
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
%{name} development package

%prep
%setup -q
#%setup -q -n %{name}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

#%if 0%{?gitdate}
#git checkout -b fedora
#sed -i 's/git/&+ssh/' .git/config
#if [ -z "$GIT_COMMITTER_NAME" ]; then
#    git config user.email "x@fedoraproject.org"
#    git config user.name "Fedora X Ninjas"
#fi
#git commit -am "%{name} %{version}"
#%else
#git init
#if [ -z "$GIT_COMMITTER_NAME" ]; then
#    git config user.email "x@fedoraproject.org"
#    git config user.name "Fedora X Ninjas"
#fi
#git add .
#git commit -a -q -m "%{name} %{version} baseline."
#%endif

#git am -p1 %{patches} < /dev/null

%build
#autoreconf -i -v -f
#AUTOPOINT="intltoolize --automake --copy" autoreconf -v --force --install || exit 1
#intltoolize -c -f   
#autoreconf -vfi
%configure \
    --enable-compat-rules \
    --with-xkb-base=/usr/etc/X11/xkb --datarootdir=/usr/etc \
    --disable-xkbcomp-symlink \
    --with-xkb-rules-symlink=xfree86,xorg

make %{?jobs:-j%jobs} %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%remove_docs

# Remove unnecessary symlink
rm -f $RPM_BUILD_ROOT%{_datadir}/X11/xkb/compiled
%find_lang %{name} 

mkdir -p  %{buildroot}/etc/X11/xkb/
mv %{buildroot}/usr/etc/X11/xkb/rules/base.xml %{buildroot}/etc/X11/xkb/
pushd %{buildroot}
ln -s etc/X11/xkb/base.xml usr/etc/X11/xkb/rules/base.xml
popd

# Create filelist
{
   FILESLIST=${PWD}/files.list
   pushd $RPM_BUILD_ROOT
   find .%{_datadir}/X11/xkb -type d | sed -e "s/^\./%dir /g" > $FILESLIST
   find .%{_datadir}/X11/xkb -type f | sed -e "s/^\.//g" >> $FILESLIST
   popd
}

%files -f files.list -f %{name}.lang
%defattr(-,root,root,-)
#%doc AUTHORS README NEWS TODO COPYING CREDITS docs/README.* docs/HOWTO.*
/etc/X11/xkb/base.xml
/usr/etc/X11/xkb/rules/base.xml
/usr/etc/X11/xkb/rules/xfree86
/usr/etc/X11/xkb/rules/xfree86.lst
/usr/etc/X11/xkb/rules/xfree86.xml
/usr/etc/X11/xkb/rules/xorg
/usr/etc/X11/xkb/rules/xorg.lst
/usr/etc/X11/xkb/rules/xorg.xml
#%{_mandir}/man7/xkeyboard-config.*

%files devel
%defattr(-,root,root,-)
%{_datadir}/pkgconfig/xkeyboard-config.pc

%files -n xkb-data
#%defattr(-,root,root,-)
/usr/etc/X11/*

%files -n xkb-data-i18n
#%defattr(-,root,root,-)
/usr/share/locale/*
