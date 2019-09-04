#! /bin/bash

root=$(git rev-parse --show-toplevel)
cd $root/testing
cram *.t
