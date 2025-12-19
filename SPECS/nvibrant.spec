%global forgeurl        https://github.com/Tremeschin/nvibrant
%global nvidia_version  590.44.01
%global _unitdir    /usr/lib/systemd/system/

Name:           nvibrant
Version:        1.1.0
Release:        2%{?dist}
Summary:        Nvidia Digital Virbrance on Wayland

%forgemeta

# Source for nvibrant is GPL-3.0, Nvidia headers is MIT
License:        GPL-3.0 AND MIT
URL:            %{forgeurl}
Source0:        %{forgesource}
Source1:        https://github.com/NVIDIA/open-gpu-kernel-modules/archive/refs/tags/%{nvidia_version}.tar.gz
Source2:        https://github.com/ykshek/nvibrant-specs/raw/refs/heads/main/SOURCES/nvibrant.service

BuildRequires:  git
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson

# Requires:       python3

%description
NVIDIA GPUs have a nice feature called Digital Vibrance that increases the colors saturation of the display. The option is readily available on nvidia-settings in Linux, but is too coupled with libxnvctrl, making it softly "exclusive" to the X11 display server over wayland; but I paid for my pixels to glow :^)

An interesting observation is that the setting persists after modifying it on X11 and then switching to Wayland. I theorized (1) (2) it was possible to call some shared library or interface to configure it directly in their driver, independently of the display server, and indeed, it is possible!

This repository uses nvidia-modeset and nvkms headers found at nvidia/open-gpu-kernel-modules to make ioctl calls in the /dev/nvidia-modeset device for configuring display attributes. These headers are synced with the proprietary releases, should work fine if you're on any of nvidia-dkms, nvidia-open or nvidia.

Note: A future, and intended way, will be through NVML, as evident by some nvidia-settings comments.


%prep
%setup
%setup -T -D -a 1 -q
mv open-gpu-kernel-modules-%{nvidia_version}/* open-gpu


%build
%meson
%meson_build


%install
%meson_install


%files
%license license.txt
%doc readme.md
%{_bindir}/%{name}
%{_unitdir}/nvibrant.service


%changelog
* Fri Dec 19 2025 Alex Shek <hms.starryfish@gmail.com> - 1.1.0-2
- Add example systemd service.

* Fri Dec 19 2025 Alex Shek <hms.starryfish@gmail.com> - 1.1.0-1
- Initial packaged version.
