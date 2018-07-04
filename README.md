# nginx-rpmbuild-arm7
rpmbuild for nginx 1.14.0 on arm7 architecture

## Start the build by executing the following command
`cd SPECS`
`rpmbuild -ba nginx-1.14.0.spec`

The rpm is already generated for arm7 architecture (centos7).
The rpm can be rebuilt for any architecture.
Dependencies are not sorted out quite well while the rpm is installed.

The directories "BUILDROOT" and "BUILD" needs to be created before 
running the rpmbuild command.

Note: Development Tools should be installed before running the rpmbuild
