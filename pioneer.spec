## This package uses an own miniz.h file.
## Upstream: taken from http://miniz.googlecode.com/svn/trunk/miniz.c. I've cut this into
## header and implementation files and disabled (via define) some interfaces that
## we don't need:
# - MINIZ_NO_ARCHIVE_WRITING_APIS
# - MINIZ_NO_ZLIB_COMPATIBLE_NAMES

Name:          pioneer
Summary:       A game of lonely space adventure
Version:       20161022
Release:       2%{?dist}

## Main license: GPLv3
## Dejavu font license: Bitstream Vera and Public Domain
## Pioneer's art, music and other assets (including Lua model scripts): CC-BY-SA
License:       GPLv3 and CC-BY-SA and Bitstream Vera and Public Domain
Group:         Amusements/Games
URL:           http://pioneerspacesim.net/
Source0:       https://github.com/pioneerspacesim/pioneer/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:       %{name}.desktop
Source2:       %{name}.appdata.xml

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: chrpath
BuildRequires: desktop-file-utils
BuildRequires: doxygen
BuildRequires: fontpackages-devel
BuildRequires: graphviz
BuildRequires: ImageMagick
BuildRequires: pkgconfig
BuildRequires: pkgconfig(vorbis)
BuildRequires: pkgconfig(sigc++-2.0)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(SDL2_image)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(libpng)
#BuildRequires: pkgconfig(lua)
BuildRequires: assimp-devel >= 3.2
BuildRequires: pkgconfig(gl)
BuildRequires: miniz-devel
BuildRequires: NaturalDocs
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib

Requires: %{name}-data = %{version}-%{release}
Requires: hicolor-icon-theme
Requires: graphviz

%description
A space adventure game set in the Milky Way galaxy at the turn of
the 31st century.

The game is open-ended, and you are free to explore the millions of star
systems in the game. You can land on planets, slingshot past gas giants, and
burn yourself to a crisp flying between binary star systems. You can try your
hand at piracy, make your fortune trading between systems, or do missions for
the various factions fighting for power, freedom or self-determination.

####################
%package data
Summary: Data files of %{name}
BuildArch: noarch
Group:     Amusements/Games
Requires: %{name}-inpionata-fonts = %{version}-%{release}
Requires: %{name}-orbiteer-bold-fonts = %{version}-%{release}
Requires: %{name}-pionilliumtext22l-medium-fonts = %{version}-%{release}
Requires: wqy-microhei-fonts
Requires: dejavu-sans-fonts
Requires: dejavu-sans-mono-fonts

%description data
Data files of %{name}.

####################
%package doc
Summary: HTML documentation files of %{name}
BuildArch: noarch
%description doc
Lua API NaturalDocs and C++ documentation files of %{name}.

####################
%package inpionata-fonts
Summary: Inpionata font file for %{name}
BuildArch: noarch
License:   OFL
Requires:  fontpackages-filesystem

%description inpionata-fonts
Inpionata font file based on Inconsolata.

####################
%package orbiteer-bold-fonts
Summary: Orbiteer Bold font file for %{name}
BuildArch: noarch
License:   OFL
Requires:  fontpackages-filesystem

%description orbiteer-bold-fonts
Orbiteer Bold font file based on Orbitron.

####################
%package pionilliumtext22l-medium-fonts
Summary: PionilliumText22L Medium font file for %{name}
BuildArch: noarch
License:   OFL
Requires:  fontpackages-filesystem

%description pionilliumtext22l-medium-fonts
PionilliumText22L Medium font file based on Titillium.

%prep
%setup -q -n %{name}-%{version}

## Strip all .png files 
## 'iCCP: known incorrect sRGB profile' warnings
find . -type f -name "*.png" -exec convert {} -strip {} \;

## Pioneer does not work with Lua 5.3.2
## We cannot unbundle internal Lua yet
## See https://github.com/pioneerspacesim/pioneer/issues/3712
#rm -f contrib/lua/lua.h
#rm -f contrib/lua/lauxlib.h
#rm -f contrib/lua/lua.hpp
#rm -f contrib/lua/luaconf.h
#rm -f contrib/lua/lualib.h

## Set NaturalDocs name
sed -e 's|naturaldocs|NaturalDocs|g' -i Makefile.am

# https://github.com/pioneerspacesim/pioneer/issues/3846
%ifarch aarch64
sed -e '/^SUBDIRS/s/ profiler//' -i.bak contrib/Makefile.am
sed -e '/libprofiler.a/d; $!N; /libprofiler.a$/s| \\||; P; D' -i.p.bak src/Makefile.am
sed -e '/contrib\/profiler/d' -i.p.bak configure.ac
sed -e 's/defined(__arm__)/(& || defined(__aarch64__))/' -i.bak contrib/profiler/Profiler.h
%endif

%build
./bootstrap

%configure --disable-silent-rules --with-ccache --without-strip \
 --with-version --with-extra-version --without-extra-warnings \
 --without-thirdparty --without-external-liblua --with-no-optimise \
 PIONEER_DATA_DIR=%{_datadir}/%{name}


make %{?_smp_mflags} V=1 OPTIMISE=""

## Build documentation
make codedoc
pushd doxygen
doxygen

%install
%make_install

## Remove rpaths
chrpath -d %{buildroot}%{_bindir}/%{name}
chrpath -d %{buildroot}%{_bindir}/modelcompiler

## Install icons
mkdir -p %{buildroot}%{_datadir}/icons/%{name}
install -pm 644 application-icon/*.ico %{buildroot}%{_datadir}/icons/%{name}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -pm 644 application-icon/badge-* %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/16x16/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/22x22/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/24x24/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/40x40/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -Dpm 644 application-icon/pngs/%{name}-16x16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps
install -Dpm 644 application-icon/pngs/%{name}-22x22.png %{buildroot}%{_datadir}/icons/hicolor/22x22/apps
install -Dpm 644 application-icon/pngs/%{name}-24x24.png %{buildroot}%{_datadir}/icons/hicolor/24x24/apps
install -Dpm 644 application-icon/pngs/%{name}-32x32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -Dpm 644 application-icon/pngs/%{name}-40x40.png %{buildroot}%{_datadir}/icons/hicolor/40x40/apps
install -Dpm 644 application-icon/pngs/%{name}-48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
install -Dpm 644 application-icon/pngs/%{name}-64x64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
install -Dpm 644 application-icon/pngs/%{name}-128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
install -Dpm 644 application-icon/pngs/%{name}-256x256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps

## Install desktop file
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install %{SOURCE1} --dir=%{buildroot}%{_datadir}/applications

## Install appdata file
mkdir -p %{buildroot}%{_datadir}/appdata
install -pm 644 %{SOURCE2} %{buildroot}%{_datadir}/appdata
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/*.appdata.xml

## Remove empty directories
find %{buildroot} -name '.gitignore' -exec rm -rf {} ';'

## Unbundle DejaVuSans.ttf, DejaVuSansMono.ttf and wqy-microhei.ttc
mkdir -p %{buildroot}%{_fontdir}
mv %{buildroot}%{_datadir}/%{name}/fonts/Inpionata.ttf %{buildroot}%{_fontdir}
mv %{buildroot}%{_datadir}/%{name}/fonts/Orbiteer-Bold.ttf %{buildroot}%{_fontdir}
mv %{buildroot}%{_datadir}/%{name}/fonts/PionilliumText22L-Medium.ttf %{buildroot}%{_fontdir}

ln -sf %{_fontdir}/Inpionata.ttf %{buildroot}%{_datadir}/%{name}/fonts/Inpionata.ttf
ln -sf %{_fontdir}/Orbiteer-Bold.ttf %{buildroot}%{_datadir}/%{name}/fonts/Orbiteer-Bold.ttf
ln -sf %{_fontdir}/PionilliumText22L-Medium.ttf %{buildroot}%{_datadir}/%{name}/fonts/PionilliumText22L-Medium.ttf

ln -sf %{_fontbasedir}/wqy-microhei/wqy-microhei.ttc %{buildroot}%{_datadir}/%{name}/fonts/wqy-microhei.ttc
ln -sf %{_fontbasedir}/dejavu/DejaVuSansMono.ttf %{buildroot}%{_datadir}/%{name}/fonts/DejaVuSansMono.ttf
ln -sf %{_fontbasedir}/dejavu/DejaVuSans.ttf %{buildroot}%{_datadir}/%{name}/fonts/DejaVuSans.ttf

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%{_bindir}/%{name}
%{_bindir}/modelcompiler
%{_datadir}/icons/hicolor/16x16/apps/*.png
%{_datadir}/icons/hicolor/22x22/apps/*.png
%{_datadir}/icons/hicolor/24x24/apps/*.png
%{_datadir}/icons/hicolor/32x32/apps/*.png
## Following directories are not owned by hicolor-icon-theme
%dir %{_datadir}/icons/hicolor/40x40
%dir %{_datadir}/icons/hicolor/40x40/apps
##
%{_datadir}/icons/hicolor/40x40/apps/*.png
%{_datadir}/icons/hicolor/48x48/apps/*.png
%{_datadir}/icons/hicolor/64x64/apps/*.png
%{_datadir}/icons/hicolor/128x128/apps/*.png
%{_datadir}/icons/hicolor/256x256/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/appdata/*.appdata.xml

%files data
%license licenses/GPL-3.txt licenses/*.html licenses/CC-BY-SA-3.0.txt licenses/DejaVu-license.txt
%doc AUTHORS.txt Changelog.txt Quickstart.txt README.md
%{_datadir}/%{name}/

%files doc
%license licenses/GPL-3.txt
%doc doxygen/html AUTHORS.txt README.md codedoc

%_font_pkg -n inpionata Inpionata.ttf
%license licenses/SIL-1.1.txt
%dir %{_fontdir}

%_font_pkg -n orbiteer-bold Orbiteer-Bold.ttf
%license licenses/SIL-1.1.txt
%dir %{_fontdir}

%_font_pkg -n pionilliumtext22l-medium PionilliumText22L-Medium.ttf
%license licenses/SIL-1.1.txt
%dir %{_fontdir}

%changelog
* Tue Oct 25 2016 Antonio Trande <sagitterATfedoraproject.org> 20161022-2
- 'sed' patch for AARCH64 builds

* Mon Oct 24 2016 Jon Ciesla <limburgher@gmail.com> 20161022-1
- 20161022

* Thu Oct 13 2016 Jon Ciesla <limburgher@gmail.com> 20160907-1
- 20160907

* Sun Aug 14 2016 Antonio Trande <sagitterATfedoraproject.org>  20160814-1
- Update to the version 20160814

* Tue Jul 19 2016 Ben Rosser <rosser.bjr@gmail.com> 20160710-1
- Update to latest release

* Sat Jul 09 2016 Antonio Trande <sagitterATfedoraproject.org>  20160701-2
- Fix typos in the appdata file

* Sat Jul 09 2016 Antonio Trande <sagitterATfedoraproject.org>  20160701-1
- Update to release 20160701

* Sun Jun 12 2016 Antonio Trande <sagitterATfedoraproject.org>  20160512-6
- Patched for EXTRA_CXXFLAGS

* Thu Jun 02 2016 Antonio Trande <sagitterATfedoraproject.org>  20160512-5
- Patched for aarch64 build

* Thu Jun 02 2016 Antonio Trande <sagitterATfedoraproject.org>  20160512-4
- hardened_builds flags enabled
- assimp libraries linked manually

* Sat May 28 2016 Antonio Trande <sagitterATfedoraproject.org>  20160512-3
- Unbundle DejaVuSans.ttf DejaVuSansMono.ttf wqy-microhei.ttc font files
- Made Inpionata Orbiteer-Bold PionilliumText22L-Medium fonts sub-packages

* Fri May 27 2016 Antonio Trande <sagitterATfedoraproject.org>  20160512-2
- Made /usr/share/icons/hicolor/40x40 owned
- Replace Summary
- Made a doc sub-package

* Fri May 20 2016 Antonio Trande <sagitterATfedoraproject.org>  20160512-1
- First package
