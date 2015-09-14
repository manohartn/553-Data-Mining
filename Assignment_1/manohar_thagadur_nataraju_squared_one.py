import MapReduce
import sys
import re

"""
Matrix multiplication in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    # 5x5 matrix
    rows = 5
    cols = 5

    i = record[0]
    j = record[1]
    Aij = record[2]
    #for matrix "A"
    for k in range(0, cols):
      value_list = ["A", j, Aij]
      mr.emit_intermediate((i,k), value_list)
      #print (i,k), value_list
    #for matrix "B"
    j = record[0]
    k = record[1]
    Bjk = record[2]
    for i in range(0, rows):
        value_list = ["B", j, Bjk]
        mr.emit_intermediate((i,k), value_list)
        #print (j,k), value_list

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    j_list = []
    j_dict = {}

    for val in list_of_values:
        j_val = val[1]
        element = val[2]
        #if key not already in dictionary, set value to empty list
        j_dict.setdefault(j_val, [])
        #add value to list associated with key
        j_dict[j_val].append(element)
    j_list.append(j_dict)

    res_addition_list = []
    for j_dict in j_list:
        for k, value in j_dict.iteritems():
            if len(value) == 2:
                res_addition_list.append(value[0] * value[1])

    res_element = 0
    for element in res_addition_list:
        res_element += element

    mr.emit([key[0], key[1], res_element])
    #mr.emit((key, total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
