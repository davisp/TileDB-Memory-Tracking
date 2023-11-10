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

def main():
  if len(sys.argv) != 2:
    print("usage:", sys.argv[0], "ARRAY")
    exit(1)

  config = tiledb.Config()
  config["sm.consolidation.mode"] = "fragments"
  config["sm.consolidation.step_max_frags"] = 5
  config["sm.consolidation.step_min_frags"] = 1
  config["sm.mem.total_budget"] = sys.maxsize
  ctx = tiledb.Ctx(config)

  start_stats_monitor(ctx)
  tiledb.cc.Array.consolidate(ctx, sys.argv[1], None)

if __name__ == "__main__":
  main()
