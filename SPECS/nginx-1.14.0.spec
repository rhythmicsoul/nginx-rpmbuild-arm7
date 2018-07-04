Name:		nginx
Version:	1.14.0
Release:	1%{?dist}
Summary:	Nginx Web Server

Group:		Applications/Webserver
License:	GPL
URL:		http://nginx.org/download/%{name}-%{version}.tar.gz
Source0:	http://nginx.org/download/%{name}-%{version}.tar.gz
Source1:	nginx.service

BuildRequires:	perl-ExtUtils-Embed,systemd
Requires:	openssl, perl-ExtUtils-Embed
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Nginx Webserver


%prep
%setup -q -n %{name}-%{version}


%build
./configure --prefix="/usr/local/nginx" --sbin-path="/usr/sbin/nginx" --conf-path="/etc/nginx/nginx.conf" --pid-path="/var/run/nginx.pid" --lock-path="/var/run/nginx.lock" --user="nginx" --group="nginx" --with-threads --with-file-aio --with-http_ssl_module --with-http_v2_module --with-http_gzip_static_module --with-http_gunzip_module --with-http_auth_request_module --with-http_perl_module=dynamic --http-log-path="/var/log/nginx/access.log" --with-pcre --error-log-path="/var/log/nginx/error.log"
make -j4


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
make install DESTDIR=%{buildroot}

#Install the service file
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -m644 %SOURCE1 $RPM_BUILD_ROOT%{_unitdir}/nginx.service


%files
%doc
%defattr(-,root,root)
/etc/nginx/fastcgi.conf
/etc/nginx/fastcgi.conf.default
/etc/nginx/fastcgi_params
/etc/nginx/fastcgi_params.default
/etc/nginx/koi-utf
/etc/nginx/koi-win
/etc/nginx/mime.types
/etc/nginx/mime.types.default
/etc/nginx/nginx.conf
/etc/nginx/nginx.conf.default
/etc/nginx/scgi_params
/etc/nginx/scgi_params.default
/etc/nginx/uwsgi_params
/etc/nginx/uwsgi_params.default
/etc/nginx/win-utf
/usr/lib/perl5/perllocal.pod
/usr/local/lib/perl5/auto/nginx/.packlist
/usr/local/lib/perl5/auto/nginx/nginx.bs
/usr/local/lib/perl5/auto/nginx/nginx.so
/usr/local/lib/perl5/nginx.pm
/usr/local/nginx/html/50x.html
/usr/local/nginx/html/index.html
/usr/local/nginx/modules/ngx_http_perl_module.so
/usr/local/nginx/modules/ngx_http_perl_module.so.old
/usr/local/share/man/man3/nginx.3pm
/usr/sbin/nginx
/usr/sbin/nginx.old
%{_unitdir}/nginx.service



%changelog


%post
if [ $1 -eq 1 ]; then
	# Add the "nginx" user
	getent group nginx >/dev/null || groupadd -r nginx
	getent passwd nginx >/dev/null || \
	useradd -r -m -g nginx -s /sbin/nologin \
	-d /var/cache/nginx -c "nginx user"  nginx

	/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
	exit 0
fi

%preun
if [ $1 -eq 0 ]; then
	/usr/bin/systemctl stop nginx.service
	/usr/bin/systemctl --no-reload disable nginx.service >/dev/null 2>&1 ||:
fi


%postun
if [ $1 -eq 0 ]; then
	getent group nginx >/dev/null && groupdel nginx
	getent passwd nginx >/dev/null && userdel -r nginx
	/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
fi

