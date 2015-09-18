import MapReduce
import sys
import re

"""
Two Phase Matrix Multiplication -- PHASE 1
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    i = record[0]
    j = record[1]
    Aij = record[2]

    mr.emit_intermediate(j, ['A', i, Aij])

    j = record[0]
    k = record[1]
    Bjk = record[2]
    mr.emit_intermediate(j, ['B', k, Bjk])

def reducer(key, list_of_lists):
   
    list_len = len(list_of_lists)
    for i in range(0, list_len-1):
        for j in range(i+1, list_len):
            if list_of_lists[i][0] != list_of_lists[j][0]:
                mult_val = list_of_lists[i][2] * list_of_lists[j][2]
                if list_of_lists[i][0] == 'A':
                    mr.emit([list_of_lists[i][1], list_of_lists[j][1], mult_val])
                else:
                    mr.emit([list_of_lists[j][1], list_of_lists[i][1], mult_val])
    
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
