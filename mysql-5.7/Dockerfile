#
# MySQL generic Dockerfile
# 
FROM ubuntu:14.04
MAINTAINER Venu Anugati<venu@venublog.com>

RUN apt-key adv --keyserver ha.pool.sks-keyservers.net --recv-keys A4A9406876FCBD3C456770C88C718D3B5072E1F5

RUN echo "deb http://repo.mysql.com/apt/ubuntu/ trusty mysql-5.7" > /etc/apt/sources.list.d/mysql.list

RUN apt-get update && apt-get install -y --no-install-recommends mysql-server-5.7

RUN rm -rf /etc/mysql/conf.d/mysqld_safe_syslog.cnf && \
  /bin/bash -c "echo -e '[mysqld]\nbind-address=0.0.0.0'" > /etc/mysql/conf.d/listen.cnf

# expose the port
EXPOSE 3306

# Start mysql server
CMD ["/usr/bin/mysqld_safe"]
