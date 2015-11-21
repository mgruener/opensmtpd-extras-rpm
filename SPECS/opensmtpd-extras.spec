%if (0%{?rhel} >= 7) || (0%{?fedora})
%global luaver luajit
%global mysqlver mariadb
%else
%global luaver lua
%global mysqlver mysql
%endif

Name:		opensmtpd-extras
Version:	5.7.1
Release:	3%{?dist}
Summary:	addons for the OpenSMTPD SMTP server

Group:		System Environment/Daemons
License:	ISC
URL:		http://www.opensmtpd.org/
Source0:	http://www.opensmtpd.org/archives/%{name}-%{version}.tar.gz

Patch0: 01_install_man.diff
Patch1: 02_table_sqlite.5.diff

BuildRequires: automake
BuildRequires: libtool
BuildRequires: openssl-devel
BuildRequires: libevent-devel
BuildRequires: libasr-devel
BuildRequires: %{luaver}-devel
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: python-devel
BuildRequires: postgresql-devel
BuildRequires: %{mysqlver}-devel
BuildRequires: sqlite-devel
BuildRequires: hiredis-devel

%description
OpenSMTPD is a FREE implementation of the server-side SMTP protocol as defined
by RFC 5321, with some additional standard extensions. It allows ordinary
machines to exchange e-mails with other systems speaking the SMTP protocol.
Started out of dissatisfaction with other implementations, OpenSMTPD nowadays
is a fairly complete SMTP implementation. OpenSMTPD is primarily developed
by Gilles Chehade, Eric Faurot and Charles Longeau; with contributions from
various OpenBSD hackers. OpenSMTPD is part of the OpenBSD Project.
The software is freely usable and re-usable by everyone under an ISC license.
.
This package provides addons for OpenSMTPD, including experimental ones.
 * Tables:
   + ldap: support lookup against LDAP
   + passwd: support lookup in passwd-format tables
   + socketmap: support lookups against sockets
 * Filters: 
   + clamav: filter mail through clamd [clamav-daemon]
   + dkim-signer: add DKIM signatures to headers
   + monkey: randomly accept mail with a probability of 70%
   + pause: pause on new connections to avoid "slamming" attacks
   + regex: filter mail using regex
   + spamassassin: filter mail through SpamAssassin's spamd [spamassassin]
   + trace: trace SMTP sessions
   + void: accepts all mails, without doing anything
 * Queues:
   + null:
   + ram:
 * Schedulers:
   + ram:

%package filter-dnsbl
Summary: This package provides the dnslbl filter addon for OpenSMTPD.
%description filter-dnsbl
 * Filters:
   + dnsbl: perform DNSBL checks

%package filter-lua
Summary: This package provides the lua filter addon for OpenSMTPD.
%description filter-lua
 * Filters:
   + lua: filter mail using lua

%package filter-perl
Summary: This package provides the perl filter addon for OpenSMTPD.
%description filter-perl
 * Filters:
   + perl: filter mail using perl

%package table-mysql
Summary: This package provides the MySQL table addon for OpenSMTPD.
%description table-mysql
 * Tables:
   + mysql: support lookup against MySQL

%package table-postgres
Summary: This package provides the postgresql table addon for OpenSMTPD.
%description table-postgres
 * Tables:
   + postgres: support lookup against PostgreSQL

%package table-redis
Summary: This package provides the redis table addon for OpenSMTPD.
%description table-redis
 * Tables:
   + redis: support lookup against a Redis server

%package table-sqlite
Summary: This package provides the sqlite table addon for OpenSMTPD.
%description table-sqlite
 * Tables:
   + sqlite: support lookup in SQLite tables

%package python
Summary: This package provides the python addons for OpenSMTPD.
%description python
 * Filters:
   + python: filter mail using python
 * Table:
   + python: support lookup in python tables
 * Queues:
   + python:
 * Schedulers:
   + python:

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# necessary because we are patching makefiles
aclocal -I m4
autoconf

%build
export CFLAGS="%{optflags}"
export LDFLAGS=-L%{_libdir}/mysql

%configure \
    --sysconfdir=%{_sysconfdir}/opensmtpd \
    --with-mantype=man \
    --with-privsep-user=smtpd \
    --with-privsep-path=%{_localstatedir}/empty/smtpd \
    --with-lua-type=%{luaver} \
    --with-filter-clamav \
    --with-filter-dkim-signer \
    --with-filter-dnsbl \
    --with-filter-lua \
    --with-filter-monkey \
    --with-filter-pause \
    --with-filter-perl \
    --with-filter-python \
    --with-filter-regex \
    --with-filter-spamassassin \
    --with-filter-trace \
    --with-filter-void \
    --with-queue-null \
    --with-queue-python \
    --with-queue-ram \
    --with-table-ldap \
    --with-table-mysql \
    --with-table-postgres \
    --with-table-redis \
    --with-table-socketmap \
    --with-table-passwd \
    --with-table-python \
    --with-table-sqlite \
    --with-scheduler-ram \
    --with-scheduler-python

make %{?_smp_mflags}


%install
%make_install


%files
%{_libexecdir}/opensmtpd/queue-ram
%{_libexecdir}/opensmtpd/table-socketmap
%{_libexecdir}/opensmtpd/filter-trace
%{_libexecdir}/opensmtpd/table-passwd
%{_libexecdir}/opensmtpd/filter-monkey
%{_libexecdir}/opensmtpd/scheduler-ram
%{_libexecdir}/opensmtpd/queue-null
%{_libexecdir}/opensmtpd/filter-void
%{_libexecdir}/opensmtpd/filter-pause
%{_libexecdir}/opensmtpd/filter-clamav
%{_libexecdir}/opensmtpd/filter-spamassassin
%{_libexecdir}/opensmtpd/filter-regex
%{_libexecdir}/opensmtpd/table-ldap
%{_libexecdir}/opensmtpd/filter-dkim-signer
%{_mandir}/man3/filter_api.3.gz
%{_mandir}/man5/table_passwd.5.gz
%{_mandir}/man5/table_socketmap.5.gz
%{_mandir}/man8/filter-clamav.8.gz
%{_mandir}/man8/filter-monkey.8.gz
%{_mandir}/man8/filter-pause.8.gz
%{_mandir}/man8/filter-regex.8.gz
%{_mandir}/man8/filter-spamassassin.8.gz
%{_mandir}/man8/filter-trace.8.gz
%{_mandir}/man8/filter-void.8.gz

%files filter-dnsbl
%{_libexecdir}/opensmtpd/filter-dnsbl
%{_mandir}/man8/filter-dnsbl.8.gz

%files filter-lua
%{_libexecdir}/opensmtpd/filter-lua

%files filter-perl
%{_libexecdir}/opensmtpd/filter-perl

%files table-mysql
%{_libexecdir}/opensmtpd/table-mysql

%files table-postgres
%{_libexecdir}/opensmtpd/table-postgres

%files table-redis
%{_libexecdir}/opensmtpd/table-redis

%files table-sqlite
%{_libexecdir}/opensmtpd/table-sqlite
%{_mandir}/man5/table_sqlite.5.gz

%files python
%doc extras/wip/queues/queue-python/scripts
%{_libexecdir}/opensmtpd/filter-python
%{_libexecdir}/opensmtpd/table-python
%{_libexecdir}/opensmtpd/queue-python
%{_libexecdir}/opensmtpd/scheduler-python

%changelog
* Sat Nov 21 2015 Michael Gruener <michael.gruener@chaosmoon.net> - 5.7.1-3
- add compatibility to CentOS / RHEL 6

* Sat Nov 21 2015 Michael Gruener <michael.gruener@chaosmoon.net> - 5.7.1-2
- ensure autotools compatibility by calling aclocal / autoconf
- remove comment with macro (fixes warning)

* Sat Nov 21 2015 Michael Gruener <michael.gruener@chaosmoon.net> - 5.7.1-1
- Initial release
