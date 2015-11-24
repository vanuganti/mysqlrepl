MySQL Multi source replication demo
===================================
Docker based environment to test MySQL 5.7 multi source replication from multiple servers to single MySQL server. The test uses 4 MySQL 5.6 servers as master database servers and one 5.7 server as slave; which aggregates data from all databases to single database.

## Requirements:
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)
* [Rakefile](http://docs.seattlerb.org/rake/)
* [Python](https://www.python.org/)
* [Python MySQL connector](https://dev.mysql.com/downloads/connector/python/2.1.html)

## Build the containers

```
rake build
```

## Run the containers
```
rake start
rake init
rake test
```

Or simply run:
```
rake demo
```
which will build, start and load the test data


