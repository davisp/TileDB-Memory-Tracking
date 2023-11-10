#!/usr/bin/env python3

import json
import os
import sys
import threading
import time

import numpy as np
import tiledb

STAT_PREFIX = "Context.StorageManager.MemoryTracker."

tiledb.stats_enable()

def stats_monitor(ctx):
  while True:
    time.sleep(1)
    stats = ctx.get_stats(print_out = False)
    if not stats:
      continue
    counters = json.loads(stats)["counters"]
    to_dump = {}
    for c in counters:
      if c.startswith(STAT_PREFIX):
        to_dump[c[len(STAT_PREFIX):]] = counters[c]
    to_dump["timestamp"] = int(time.time() * 1000.0)
    print(json.dumps(to_dump, sort_keys=True))

def start_stats_monitor(ctx):
  t = threading.Thread(target=stats_monitor, args=(ctx,))
  t.daemon = True
  t.start()

def ingest(dataset, array_path, ctx):
    columns = {
      "c_customer_sk": np.uint64,
      "c_customer_id": np.str_,
      "c_current_cdemo_sk": np.uint64,
      "c_current_hdemo_sk": np.uint64,
      "c_current_addr_sk": np.uint64,
      "c_first_shipto_date_sk": np.uint64,
      "c_first_sales_date_sk": np.uint64,
      "c_salutation": np.str_,
      "c_first_name": np.str_,
      "c_last_name": np.str_,
      "c_preferred_cust_flag": np.str_,
      "c_birth_day": np.uint64,
      "c_birth_month": np.uint64,
      "c_birth_year": np.uint64,
      "c_birth_country": np.str_,
      "c_login": np.str_,
      "c_email_address": np.str_,
      "c_last_review_date_sk": np.uint64,
      "ignore": np.uint64
    }

    tiledb.from_csv(
      array_path,
      dataset,
      chunksize = 650000,
      ctx = ctx,
      capacity = 100000,
      sparse = True,
      full_domain = True,
      index_col = ['c_customer_sk'],
      fillna = {
        'c_login': '',
        "c_salutation": "",
        "c_first_name": "",
        "c_last_name": "",
        "c_preferred_cust_flag": "",
        "c_birth_country": "",
        "c_email_address": ""
      },
      usecols = list(columns.keys())[:-1],
      sep = "|",
      encoding = "iso-8859-1",
      column_types = columns,
      names = list(columns.keys()),
      dim_filters = tiledb.FilterList([tiledb.ZstdFilter(level=-1)]),
      attr_filters = tiledb.FilterList([tiledb.ZstdFilter(level=-1)]))

def main():
  if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "CSV_FILE", "ARRAY_DIR")
    exit(1)

  dataset = sys.argv[1]
  array_path = sys.argv[2]

  config = {
      'py.alloc_max_bytes': str(12 * pow(1024, 3)), #64GB,
      'py.init_buffer_bytes': str(12 * pow(1024, 3)),
      'sm.compute_concurrency_level': '16',
      'sm.io_concurrency_level': '16',
  }

  ctx = tiledb.Ctx(config)
  start_stats_monitor(ctx)
  array_path = ingest(dataset, array_path, ctx)


if __name__ == "__main__":
  main()
