Name:           kernel
Version:        %{version}
Release:        %{release}%{?dist}
Summary:        Custom Linux Kernel

License:        GPLv2
URL:            https://www.kernel.org/
Source0:        https://cdn.kernel.org/pub/linux/kernel/v%{version}/linux-%{version}.tar.xz

BuildRequires:  gcc, make, bc, bison, flex, elfutils-libelf-devel, openssl-devel, perl, rpm-build
Requires(post): /sbin/new-kernel-pkg
Requires(postun): /sbin/new-kernel-pkg

%description
This package provides a custom Linux kernel built for specific configurations.

%prep
%setup -q -n linux-%{version}

%build
cp %{_sourcedir}/configs/rocky/%{_arch}/.config .
make olddefconfig
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/boot
cp arch/%{_arch}/boot/bzImage %{buildroot}/boot/vmlinuz-%{version}-%{release}
cp System.map %{buildroot}/boot/System.map-%{version}-%{release}
cp .config %{buildroot}/boot/config-%{version}-%{release}

%post
/sbin/new-kernel-pkg --package kernel --install %{version}-%{release}

%postun
if [ $1 -eq 0 ]; then
    /sbin/new-kernel-pkg --package kernel --remove %{version}-%{release}
fi

%files
/boot/vmlinuz-%{version}-%{release}
/boot/System.map-%{version}-%{release}
/boot/config-%{version}-%{release}

%changelog
* Sat Dec 14 2024 Your Name <you@example.com> - %{version}-%{release}
- Initial build.
