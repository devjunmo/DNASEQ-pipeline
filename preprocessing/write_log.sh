#!/bin/bash -e

if [ $# -lt 2 ]
then
    echo usage: $0 [errorMsg] [output]
    exit 1
fi



echo $1 >> $2