Name:           groot
Version:        1.3.0
Release:        1%{?dist}
Summary:        A friendly sudo wrapper for Linux

License:        MIT
URL:            https://github.com/Willtech/groot
Source0:        %{name}-%{version}.tar.gz

# Disable debug packages (no source-level debugging)
%global debug_package %{nil}

BuildRequires:  bash
BuildRequires:  shc
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  coreutils
BuildRequires:  gzip

%description
groot is a lightweight privilege wrapper that provides a clean interface for
running commands as root. This package builds groot from source using the
included install.bin script.

%prep
%setup -q

%build
# Run your build script to produce the groot binary
chmod +x install.bin
./install.bin

# After this, the build directory must contain a compiled binary named "groot"
# If your script outputs groot.bin, rename it:
if [ -f groot.bin ]; then
    mv groot.bin groot
fi

%install
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/man/man1

install -m 0755 groot %{buildroot}/usr/bin/groot
install -m 0644 groot.1 %{buildroot}/usr/share/man/man1/groot.1

%files
%license LICENSE
%doc README.md
/usr/bin/groot
/usr/share/man/man1/groot.1*

%changelog
* Sun Mar 22 2026 MR. Damian A. James Williamson <willtech@live.com.au> - 1.3.0-1
- Initial Koji-compatible build of groot
