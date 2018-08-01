#! /bin/bas

root=$(git rev-parse --show-toplevel)
cd $root/testing
cram *.t
