#!/usr/bin/env python3

import json
import sys

def collapse_cols():
  return [
    ("timestamp", [
      "timestamp"
    ]),
    ("fragment_metadata", [
      "Enumeration",
      "Footer",
      "MaxBuffer",
      "MinBuffer",
      "NullCounts",
      "RTree",
      "Sums",
      "TileOffsets",
      "TileValidityOffsets",
      "TileVarOffsets",
      "TileVarSizes",
    ]),
    ("reader", [
      "AttributeTiles",
      "CoordinateTiles",
      "DeleteConditionTiles",
      "DeleteTimestampTiles",
      "TimestampTiles"
    ]),
    ("writer", [
      "WriterFixedData",
      "WriterVarData"
    ])
  ]

def print_cols(cols):
  row = []
  for (name, _) in cols:
    row.append(name)
  print("\t".join(row))

def print_row(cols, data):
  combined = {}
  for key in data:
    bits = key.split(".")
    if len(bits) == 1:
      combined[key] = data[key]
    elif len(bits) == 2:
      combined.setdefault(bits[1], 0)
      combined[bits[1]] += data[key]
  row = []
  for (_, cnames) in cols:
    total = 0
    for cname in cnames:
      total += combined.get(cname, 0)
    row.append(str(total))
  print("\t".join(row))

def main():
  if len(sys.argv) != 2:
    print("usage:", sys.argv[0], "JSON_LOGS")
    exit(1)
  cols = collapse_cols()
  print_cols(cols)
  with open(sys.argv[1]) as handle:
    for line in handle:
      data = json.loads(line)
      print_row(cols, data)



if __name__ == "__main__":
  main()
