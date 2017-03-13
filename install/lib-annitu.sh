#!/bin/sh
cd "$(dirname "$0")"
. ./_ins_utilities.sh

ins_deb_require swig libboost-dev &&
  ins_git_get https://github.itu.dk/maau/ann-filters &&
  mkdir build &&
  cd build &&
  cmake -DCMAKE_BUILD_TYPE=Release .. &&
  make -j4
