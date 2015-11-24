Multi source replication test from multiple mysql servers  
=========================================================
Docker based environment to test MySQL 5.7 multi source replication from multiple servers to single servers

## Requirements:
* [Docker](https://www.docker.com/) setup
* [Rakefile](http://docs.seattlerb.org/rake/)
* Python
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


