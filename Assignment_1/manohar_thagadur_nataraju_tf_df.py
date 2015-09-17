import MapReduce
import sys
import re

"""
Document frequency and term frequency
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    doc_id = record[0]
    document = record[1]
    #words = value.split()
    #convert all characters in the document to their lowercase
    document = document.lower()
    #remove non alphanumeric characters in document
    document = re.findall(r"[\w]+", document)
    for word in document:
        word = str(word)
        doc_tuple = (str(doc_id), 1)
        mr.emit_intermediate(word, doc_tuple)

def reducer(key, doc_tuple_list):
    # key: word
    # value: list of occurrence counts
    term_list = []
    doc_dict = {}
    for doc_id, val in doc_tuple_list:
        doc_dict.setdefault(doc_id, 0)
        doc_dict[doc_id] += 1
    document_freq = len(doc_dict)

    for docId, tf in doc_dict.iteritems():
        docIdList = []
        docIdList.append(docId)
        docIdList.append(tf)
        term_list.append(docIdList)
    result_list = [key, document_freq, term_list]
    mr.emit(result_list)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
