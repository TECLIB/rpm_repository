%global gh_owner   xivo.solutions
%global gh_project xivo-client-qt
%global gh_commit  1399a27f1a2e171a9f6b14f18bf3822f66996678
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
%global gh_date    1506935228
%global real_name  xivo-client

Name:     xivo-client
Summary:  A desktop client to the XiVO Open Source IPBX
Version:  2018.01
Release:  2.git%{gh_short}%{?dist}
License:  GPLv3
Group:    Applications/System
URL:      https://gitlab.com/xivo.solutions/xivo-client-qt/

Source0:  https://gitlab.com/%{gh_owner}/%{gh_project}/repository/archive.tar.gz?ref=%{gh_commit}#/%{gh_project}-%{version}-%{gh_short}.tar.gz
Source1:  %{name}.desktop
Source2:  xivoclient

Patch0:   xivo-client-premake.patch
Patch1:   0001-try-to-fix-F-28-build-issue.patch

BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-linguist
BuildRequires: qt5-qttools-devel
BuildRequires: qt5-qttools-static
BuildRequires: qt5-qtsvg-devel
BuildRequires: desktop-file-utils

BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)


%package devel
Summary:     Development files for %{name}
Requires:    %{name} = %{version}-%{release}

%global debug_package %{nil}


%description
%{name} is a graphical client to use with the XiVO Open Source iPBX.
It is used to manage calls and phone book.


%description devel
Development files for %{name}


%prep
%setup -q -n %{gh_project}-%{gh_commit}-%{gh_commit}
%patch0 -p1
%patch1 -p1
#gh_date: git log -1 --pretty=%ct {commit}
sed -i premake.sh \
    -e "s|GIT_DIR=.*|GIT_DIR=$(pwd)|" \
    -e "s/GIT_HASH=.*/GIT_HASH=%{gh_short}/" \
    -e "s/GIT_DATE=.*/GIT_DATE=%{gh_date}/" \
    -e "s/XC_VERSION=.*/XC_VERSION=%{version}/"

%build
qmake-qt5
make %{_smp_mflags}

%install
%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__mkdir_p} %{buildroot}%{_libdir}/%{name}/plugins
%{__mkdir_p} %{buildroot}%{_datadir}/applications

%{__install} -m755 %SOURCE2 %{buildroot}/%{_bindir}
sed -i %{buildroot}/%{_bindir}/xivoclient \
    -e "s|%libdir|%{_libdir}|g"
%{__install} -m755 bin/xivoclient %{buildroot}%{_libdir}/%{name}/xivoclient-qt
%{__install} -m755 bin/*.so* %{buildroot}%{_libdir}/%{name}
%{__install} -m755 bin/plugins/*.so* %{buildroot}%{_libdir}/%{name}/plugins
%{__install} -m644 xivoclient/images/xivoicon.ico %{buildroot}%{_datadir}/%{name}/
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %SOURCE1
chmod 0755 %{buildroot}%{_libdir}/%{name}/*.so*
chmod 0755 %{buildroot}%{_libdir}/%{name}/plugins/*.so*


%clean
rm -rf %{buildroot}


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CODING.md README.md
%{_bindir}/xivoclient

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/xivoclient-qt
%{_libdir}/%{name}/*.so.*
%{_libdir}/%{name}/plugins
%{_datadir}/applications/%{name}.desktop


%files devel
%{_libdir}/%{name}/libxivoclient.so
%{_libdir}/%{name}/libxivoclientxlets.so


%changelog
* Tue Jul 03 2018 Johan Cwiklinski <jcwiklinski AT teclib DOT com> 2018.01-2.git1399a27
- Add quick and dirty patch for f28
* Mon Jan 08 2018 Johan Cwiklinski <jcwiklinski AT teclib DOT com> 2018.01-1.git1399a27
- Update to 2018.01
* Wed Aug 09 2017 Johan Cwiklinski <jcwiklinski AT teclib DOT com> 2017.02-git9dc5591f
- Update to 2017.02
* Wed Aug 10 2016 Johan Cwiklinski <johan AT x-tnd DOT be> 16.10.1.git4ace739
- Update to 16.10
* Mon Jul 04 2016 Johan Cwiklinski <johan AT x-tnd DOT be> 16.08.1.git1cf7719
- Last upstream release
* Thu Jun 16 2016 Johan Cwiklinski <jcwiklinski AT teclib DOT com> 16.07.git9dc5591
- Update to 16.07
* Thu Jan 10 2013 Kévin Raymond <shaiton@fedoraproject.org> 12.24-1.gite157025
- Update to the 12.24 latest release
- Clean dependancies
- Typo in the application group
* Wed Dec 19 2012 Kévin Raymond <shaiton@fedoraproject.org> 12.22-2.gitdf471e3
- Removing the libs subpackage
- Adding the binary wrapper
* Sun Dec 16 2012 Kévin Raymond <shaiton@fedoraproject.org> 12.22-1.gitdf471e3
- initial packing
