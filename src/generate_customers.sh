#!/usr/bin/env bash

dsdgen \
  -table customer \
  -dir data/ \
  -delimiter '|' \
  -scale 10000 \
  -distributions /opt/dsdgen/tpcds.idx \
  -suffix .csv
