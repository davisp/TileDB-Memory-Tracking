#!/usr/bin/env bash

dsdgen -table customer -dir . -delimiter '|' -scale 10000 -distributions /opt/dsdgen/tpcds.idx -suffix .csv
