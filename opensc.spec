%define opensc_module "OpenSC PKCS #11 Module"
%define nssdb %{_sysconfdir}/pki/nssdb

Name:            opensc
Version:         0.20.0
Release:         6
License:         LGPLv2.1+
Summary:         Smart card library and applications
URL:             https://github.com/OpenSC/OpenSC/wiki
Source0:         https://github.com/OpenSC/OpenSC/releases/download/%{version}/%{name}-%{version}.tar.gz

Patch0:          myeid-fixed-memory-leak.patch
Patch1:          backport-CVE-2020-26570-Heap-buffer-overflow-WRITE.patch
Patch2:          backport-CVE-2020-26571-fixed-invalid-read.patch

BuildRequires:   openssl-devel pcsc-lite-devel bash-completion docbook-style-xsl readline-devel
BuildRequires:   desktop-file-utils /usr/bin/xsltproc autoconf automake libtool gcc
Requires:        pcsc-lite
Obsoletes:       coolkey <= 1.1.0-36
Obsoletes:       mozilla-opensc-signer < 0.12.0
Obsoletes:       opensc-devel < 0.12.0

%description
OpenSC provides a set of libraries and utilities to work with smart cards.
Its main focus is on cards that support cryptographic operations, and
facilitate their use in security applications such as authentication,
mail encryption and digital signatures. OpenSC implements the standard
APIs to smart cards, e.g. PKCS#11 API, Windows’ Smart Card Minidriver
and macOS Tokend.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

sed -i -e 's|/usr/local/towitoko/lib/|/usr/lib/ctapi/|' etc/opensc.conf.example.in
cp -p src/pkcs15init/README ./README.pkcs15init
cp -p src/scconf/README.scconf .

%build
autoreconf -fvi
sed -i -e 's/opensc.conf/opensc-%{_arch}.conf/g' src/libopensc/Makefile.in
sed -i -e 's|"/lib /usr/lib\b|"/%{_lib} %{_libdir}|' configure # lib64 rpaths
%configure  --disable-static \
  --disable-assert \
  --disable-tests \
  --enable-sm \
  --enable-pcsc \
  --with-pcsc-provider=libpcsclite.so.1
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/opensc.conf
install -Dpm 644 etc/opensc.conf $RPM_BUILD_ROOT%{_sysconfdir}/opensc-%{_arch}.conf
touch -r NEWS $RPM_BUILD_ROOT%{_sysconfdir}/opensc-%{_arch}.conf
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" | xargs rm
rm -rf %{buildroot}%{_mandir}/man1/npa-tool.1*
rm -f $RPM_BUILD_ROOT%{_libdir}/libsmm-local.so
rm -rf %{buildroot}%{_bindir}/npa-tool
rm -f $RPM_BUILD_ROOT%{_libdir}/libopensc.so
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/opensc

desktop-file-validate %{buildroot}/%{_datadir}/applications/org.opensc.notify.desktop

%check
make check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files help
%{_mandir}/man1/cardos-tool.1*
%{_mandir}/man1/cryptoflex-tool.1*
%{_mandir}/man1/dnie-tool.1*
%{_mandir}/man1/egk-tool.1*
%{_mandir}/man1/eidenv.1*
%{_mandir}/man1/gids-tool.1*
%{_mandir}/man1/iasecc-tool.1*
%{_mandir}/man1/netkey-tool.1*
%{_mandir}/man1/openpgp-tool.1*
%{_mandir}/man1/opensc-explorer.*
%{_mandir}/man1/opensc-tool.1*
%{_mandir}/man1/opensc-asn1.1*
%{_mandir}/man1/opensc-notify.1*
%{_mandir}/man1/piv-tool.1*
%{_mandir}/man1/pkcs11-tool.1*
%{_mandir}/man1/pkcs15-crypt.1*
%{_mandir}/man1/pkcs15-init.1*
%{_mandir}/man1/pkcs15-tool.1*
%{_mandir}/man1/sc-hsm-tool.1*
%{_mandir}/man1/westcos-tool.1*
%{_mandir}/man5/*.5*

%files
%doc COPYING NEWS README*
%{_datadir}/bash-completion/*
%config(noreplace) %{_sysconfdir}/opensc-%{_arch}.conf
%{_bindir}/cardos-tool
%{_bindir}/cryptoflex-tool
%{_bindir}/dnie-tool
%{_bindir}/egk-tool
%{_bindir}/eidenv
%{_bindir}/iasecc-tool
%{_bindir}/gids-tool
%{_bindir}/goid-tool
%{_bindir}/netkey-tool
%{_bindir}/openpgp-tool
%{_bindir}/opensc-explorer
%{_bindir}/opensc-tool
%{_bindir}/opensc-asn1
%{_bindir}/opensc-notify
%{_bindir}/piv-tool
%{_bindir}/pkcs11-tool
%{_bindir}/pkcs11-register
%{_bindir}/pkcs15-crypt
%{_bindir}/pkcs15-init
%{_bindir}/pkcs15-tool
%{_bindir}/sc-hsm-tool
%{_bindir}/westcos-tool
%{_libdir}/lib*.so.*
%{_libdir}/opensc-pkcs11.so
%{_libdir}/onepin-opensc-pkcs11.so
%{_libdir}/pkcs11-spy.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/pkcs11/opensc-pkcs11.so
%{_libdir}/pkcs11/onepin-opensc-pkcs11.so
%{_libdir}/pkcs11/pkcs11-spy.so
%dir %{_libdir}/pkcs11
%{_datadir}/applications/org.opensc.notify.desktop
%{_datadir}/opensc/
%{_sysconfdir}/xdg/autostart/pkcs11-register.desktop

%changelog
* Sat Jan 23 2021 zoulin <zoulin13@huawei.com> - 0.20.0-6
- fix CVE-2020-26571

* Thu Dec 31 2020 yangzhuangzhuang <yangzhuagzhuang1@huawei.com> - 0.20.0-5
- fix CVE-2020-26570

* Mon Sep 21 2020 liquor <lirui130@huawei.com> - 0.20.0-4
- myeid: fixed memory leak

* Tue Aug 18 2020 liquor <lirui130@huawei.com> - 0.20.0-3
- rebuild for requirement package update

* Fri Feb 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.20.0-2
- Make check after installation

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.20.0-1
- Update to 0.20.0

* Mon Dec 16 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.19.0-4
- Fix CVE-2019-6502

* Fri Sep 27 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.19.0-3
- Adjust requires

* Fri Sep 27 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.19.0-2
- Format patch

* Mon Aug 26 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.19.0-1
- Package init
