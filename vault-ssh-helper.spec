#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	tests		# build without tests

Summary:	Vault SSH Agent is used to enable one time keys and passwords
Name:		vault-ssh-helper
Version:	0.1.2
Release:	0.1
License:	MPL v2.0
Group:		Base
Source0:	https://github.com/hashicorp/vault-ssh-helper/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d81009708ddf16d4aa9cd2e51f352ac8
URL:		https://github.com/hashicorp/vault-ssh-helper
Source1:	config.hcl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0
%define		gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%define		gopath		%{_libdir}/golang
%define		import_path		github.com/hashicorp/vault-ssh-helper

%description
Vault SSH Agent is a counterpart to Vault's SSH backend. It enables
creation of One-Time-Passwords (OTP) by Vault servers. OTPs will be
used as client authentication credentials while establishing SSH
connections with remote hosts.

%prep
%setup -q

mkdir -p src/github.com/hashicorp
ln -s ../../../ src/github.com/hashicorp/vault-ssh-helper

%build
export GOPATH=$(pwd):%{gopath}
%gobuild -o bin/%{name} %{import_path}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name}.d,%{_bindir}}
install -p bin/%{name} $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d/config.hcl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.d/config.hcl
