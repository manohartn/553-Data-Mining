import MapReduce
import sys
import re

"""
Two phase map reduce matrix multipication -- PHASE 2
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    i = record[0]
    j = record[1]
    value = record[2]

    mr.emit_intermediate((i,j), value)

def reducer(key, list_of_values):
    total = 0
    for v in list_of_values:
      total += v
    mr.emit([key[0], key[1], total])

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
