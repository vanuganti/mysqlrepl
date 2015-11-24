#
# MySQL generic Dockerfile
# 
FROM ubuntu:14.04
MAINTAINER Venu Anugati<venu@venublog.com>

RUN apt-get update && apt-get install -y --no-install-recommends mysql-server-5.6 

RUN rm -rf /etc/mysql/conf.d/mysqld_safe_syslog.cnf && \
  /bin/bash -c "echo -e '[mysqld]\nbind-address=0.0.0.0'" > /etc/mysql/conf.d/listen.cnf

# expose the port
EXPOSE 3306

# Start mysql server
CMD ["/usr/bin/mysqld_safe"]
