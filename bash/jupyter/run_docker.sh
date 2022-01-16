#!/bin/bash

export c=mp2i_jupyter;
docker container start $c;
while (( 1 - $(docker container ls | grep -c "$c") )); do sleep 1; done;
google-chrome $(docker logs $c 2>&1 | grep -Eo "http://127.0.0.1[^ ]*token[^ ]*" | tail -n1)
