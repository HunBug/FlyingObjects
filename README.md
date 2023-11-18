# FlyingObjects
Simulation of flying objects

# Instructions
create folder for postgres data:
```
mkdir postgres-data
```

build docker image:
```
docker compose build
```

run docker container:
```
docker compose up
```

# Ideas for the project
 - one-by-one simulation vs multiple objects
 - single-threaded vs multi-threaded
 - float boundaries equality check (floats are not precise)
 - add unit test (angle normalization, regexp, etc)
 - bezier path
 - random init seed
 - all the TODOs in the code
 - consistent code style
 - read db config from env or config file
 - assuming queried data can be fit into memory. Pagination is not implemented
 - async in flask

Check whether all requirements are met. https://trackdeep.ai/back-end-developer-test-task/

!!!!  add indeices to db with sqlalchemy !!!!