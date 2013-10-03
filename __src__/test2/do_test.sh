#!/bin/sh
HOWMANY=$1
time ab -n 10000 -c 100 -g test_data_$HOWMANY.txt http://127.0.0.1:8002/ > timming.$HOWMANY
