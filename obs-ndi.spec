# 	Spec example written by Charles K Barcza for blackPanther OS - www.blackpanther.hu

%define genlibndi 1
%define rel 3

Name: 	 obs-ndi
Version: 4.6.0
%if 0%{?fedora} || 0%{?rhel}
Release: %{rel}
%else
Release: %mkrel %{rel}
%endif
Source0: %name-%version.tar.gz
Source1: obs-studio-23.1.0-rc1.tar.gz
Patch0:	 %name-libdir.patch
Summary: OBS broadcast to OBS
License: GPLv2+
Group:   Multimedia/Video
Recommends: %{_lib}ndi3 >= 3.8.0

# Requires for OBS build
BuildRequires:  cmake
BuildRequires:  ffmpeg-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(jansson)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libvlc)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(udev)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)

%description
Network A/V in OBS Studio with NewTek's NDI technology.

Features:
- **NDI Source** : receive NDI video and audio in OBS
- **NDI Output** : transmit video and audio from OBS to NDI
- **NDI Filter** (a.k.a NDI Dedicated Output) : transmit a single source or scene to NDI

%files
%doc README.md
%license LICENSE
%dir %_datadir/obs/
%dir %_datadir/obs/obs-plugins/
%dir %_datadir/obs/obs-plugins/obs-ndi/
%dir %_datadir/obs/obs-plugins/obs-ndi/locale/
%_datadir/obs/obs-plugins/obs-ndi/locale/fr-FR.ini
%_datadir/obs/obs-plugins/obs-ndi/locale/en-US.ini
%dir %_libdir/obs-plugins/
%_libdir/obs-plugins/obs-ndi.so


%if 0%genlibndi
%global _missing_build_ids_terminate_build 0
%package -n %{_lib}ndi3
Version: 3.8.0
Release: %mkrel 1
Summary: NDI runtime for %name
License: Non-Free see: /usr/share/doc/libndi3/copyright or Url
Url:	http://obsproject.com
Group: Multimedia/Video
Requires: obs-studio >= 23.1.0

%description -n %{_lib}ndi3
NDI runtime library for %name

%files -n %{_lib}ndi3
%defattr(-,root,root,-)
%_prefix/lib/libndi.so.3.8.0
%_prefix/lib/libndi.so.3
%endif

%prep
%setup -q -a1
%patch0 -p1

%if 0%genlibndi
%ifarch %ix86
%define deb_package libndi3_3.8.0-1_i386.deb
%else
%define deb_package libndi3_3.8.0-1_amd64.deb
%endif
%endif


%if 0%genlibndi
cd $RPM_SOURCE_DIR
wget -c "https://github.com/Palakis/obs-ndi/releases/download/4.6.0/%{deb_package}"
%endif

%build
%cmake -DLIBOBS_INCLUDE_DIR=../obs-studio-23.1.0-rc1/libobs

%make_build

%install
%make_install -C build

%if 0%genlibndi
# extract data from the deb package
ar p $RPM_SOURCE_DIR/%{deb_package} data.tar.xz | xz -d -9 | tar x -C %buildroot
rm -f %buildroot/usr/lib/*.so
rm -f %buildroot/usr/lib/*.so.3
ln -sf libndi.so.3 %buildroot/usr/lib/
%endif


%changelog
* Thu May 09 2019 Charles K. Barcza <info@blackpanther.hu> 4.6.0-3bP
- fix : requires to recommends
------------------------------------------------------------------------

* Sun Mar 31 2019 Charles K. Barcza <info@blackpanther.hu> 4.6.0-2bP
- add gen multiple package with runtime depency 
- add patch for lib install pathfix
------------------------------------------------------------------------

* Sat Mar 30 2019 Charles K. Barcza <info@blackpanther.hu> 4.6.0-1bP
- build initial rpm package for blackPanther OS v17-19.x 32/64 bit
------------------------------------------------------------------------


