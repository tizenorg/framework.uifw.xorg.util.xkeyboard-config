#sbs-git:slp/pkgs/xorg/util/xkeyboard-config xkeyboard-config 1.8 bbb9ce90976c61e3637ecc91006de87d9ff59dd7
Name:       xkeyboard-config
Summary:    Alternative xkb data files
Version: 1.8
Release:    1
Group:      System/X11
License:    MIT
BuildArch:  noarch
URL:        http://www.x.org
Source0:    http://xlibs.freedesktop.org/xkbdesc/%{name}-%{version}.tar.gz
Source1001: packaging/xkeyboard-config.manifest 
BuildRequires:  pkgconfig(xorg-macros)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  intltool
BuildRequires:  xorg-x11-xkb-utils
Provides:    xkbdata
Obsoletes:   xorg-x11-xkbdata


%description
Alternative xkb data files.

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

%prep
%setup -q

%build
cp %{SOURCE1001} .

intltoolize -c -f
autoreconf -vfi

%configure --disable-static \
    --disable-xkbcomp-symlink --with-xkb-rules-symlink=xfree86,xorg   \
    --with-xkb-base=/etc/X11/xkb --datarootdir=/etc

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install

# Remove unnecessary symlink
rm -f $RPM_BUILD_ROOT/etc/X11/xkb/compiled

mkdir -p  %{buildroot}/etc/X11/xkb/

# Create filelist
{
FILESLIST=${PWD}/files.list
pushd $RPM_BUILD_ROOT
find ./etc/X11 -type d | sed -e "s/^\./%dir /g" > $FILESLIST
find ./etc/X11 -type f | sed -e "s/^\.//g" >> $FILESLIST
popd
}

%files -f files.list
%manifest xkeyboard-config.manifest
/etc/X11/xkb/rules/base.xml
/etc/X11/xkb/rules/xfree86
/etc/X11/xkb/rules/xfree86.lst
/etc/X11/xkb/rules/xfree86.xml
/etc/X11/xkb/rules/xorg
/etc/X11/xkb/rules/xorg.lst
/etc/X11/xkb/rules/xorg.xml
/usr/share/locale/*/LC_MESSAGES/xkeyboard-config.mo

%files -n xkb-data
%manifest xkeyboard-config.manifest
#%defattr(-,root,root,-)
/etc/X11/*

%files -n xkb-data-i18n
%manifest xkeyboard-config.manifest
#%defattr(-,root,root,-)
/usr/share/locale/*

