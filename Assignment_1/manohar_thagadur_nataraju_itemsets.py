import MapReduce
import sys
import re

"""
frequent itemsets
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    length = len(record)
    for i in range(len(record)):
        for j in range(i+1, len(record)):
            key = (record[i], record[j])
            mr.emit_intermediate(key, 1)

def reducer(key, list_of_values):
    total = 0
    for v in list_of_values:
      total += v
    if total >= 100:
        mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
