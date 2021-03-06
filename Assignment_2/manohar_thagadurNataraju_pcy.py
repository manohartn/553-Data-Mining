import sys
import itertools

def get_hash_value(itemTuple, hashBucketSize):
    #hashFunc = sum of all the values of chars in the tuple % 20
    sum = 0
    for i in range(0, len(itemTuple)):
        sum = sum + ord(itemTuple[i]) - 96
    hash_val = sum % hashBucketSize
    return hash_val

def generate_hash_table(itemTuple, hashBucketSize, hash_dict):
    bucketNo = get_hash_value(itemTuple, hashBucketSize)
    hash_dict[bucketNo] = hash_dict[bucketNo] + 1

def find_freq_singletons(input_path, support):
    inputFileObj = open(input_path)
    singleton_dict = {}
    freq_singleton_list = []
    all_singleton_list = []
    
    for line in inputFileObj:
        line = line.rstrip('\n')
        line = sorted(line.split(','))

        for item in line:
            singleton_dict.setdefault(item, 0)
            count = singleton_dict[item]
            singleton_dict[item] = count+1
            if singleton_dict[item] >= support:
                 if item not in freq_singleton_list:
                     freq_singleton_list.append(item)

    freq_singleton_list = sorted(freq_singleton_list)

    #print singleton_dict
    inputFileObj.close()
    return freq_singleton_list
       
def get_k_subsets(inputList, k):
    k_subsets = itertools.combinations(inputList, k)
    return k_subsets

def get_candidate_item_list(input_path, k, freq_item_list, hash_bucket_size, bitmap):
    inputFileObj = open(input_path)

    candidate_item_list = []
    for line in inputFileObj:
        line = line.rstrip('\n')
        line = sorted(line.split(','))

        k_subsets = get_k_subsets(line, k)

        for itemA in k_subsets:
            k_minus_one_subset = get_k_subsets(list(itemA), k-1)
            flag = 1
            for itemB in k_minus_one_subset:
                listItem = list(itemB)
                if len(listItem) == 1:
                    if listItem[0] not in freq_item_list:
                        flag = 0
                else:
                    if listItem not in freq_item_list:
                        flag = 0
            if flag == 1:
                hash_val = get_hash_value(itemA, hash_bucket_size)
                if bitmap[hash_val] == 1:
                    append_item = list(itemA)
                    #print append_item
                    if append_item not in candidate_item_list:
                        candidate_item_list.append(list(itemA))
    candidate_item_list = sorted(candidate_item_list)
    #print candidate_item_list
    #print len(candidate_item_list)
    return candidate_item_list
               
def get_truly_freq_list(input_path, support, k, candidate_item_list):

    inputFileObj = open(input_path)
    candidate_item_dict = {}
    truly_freq_list = []

    for line in inputFileObj:
        line = line.rstrip('\n')
        line = sorted(line.split(','))

        k_subsets = get_k_subsets(line, k)
        for item in k_subsets:
            if list(item) in candidate_item_list:
                candidate_item_dict.setdefault(item, 0)
                candidate_item_dict[item] = candidate_item_dict[item] + 1

                if candidate_item_dict[item] >= support:
                    if list(item) not in truly_freq_list:
                        #print "y" 
                        truly_freq_list.append(list(item))
    truly_freq_list = sorted(truly_freq_list)
    #print truly_freq_list
    return truly_freq_list

def find_freq_item_list(input_path, support, k, freq_item_list, hash_bucket_size, hash_dict):
    inputFileObj = open(input_path)

    for i in range(0, hash_bucket_size):
        hash_dict.setdefault(i, 0)

    for line in inputFileObj:
        line = line.rstrip('\n')
        line = sorted(line.split(','))

        k_subsets = get_k_subsets(line, k)
        for item in k_subsets:
            generate_hash_table(item, hash_bucket_size, hash_dict)
    inputFileObj.close()

    hash_dict_copy = dict(hash_dict)
    bitmap = hash_dict_copy

    for i in range(0, hash_bucket_size):
        if bitmap[i] >= support:
            bitmap[i] = 1
        else:
            bitmap[i] = 0
           
    #print hash_dict
    #print bitmap

    # Now read the file again 
    # 1. Generate k-1 subsets
    # 2. Check if each of the items are there in freq_item_list
    # 3. And hash k_subsets of the given input line and see if it falls to frequent hash bucket

    candidate_item_list = get_candidate_item_list(input_path, k, freq_item_list, hash_bucket_size, bitmap)
    
    truly_freq_list = get_truly_freq_list(input_path, support, k, candidate_item_list)

    # print the output 
    # 1. print hash dictionary
    # 2. print frequent items

    if len(truly_freq_list) > 0:
        print
        print hash_dict
        print truly_freq_list

    #reset to be ready for the next iteration

    freq_item_list = truly_freq_list
    truly_freq_list = []
    hash_dict = {}
    hash_dict_copy = {}
    return freq_item_list
    
def main():
    args_len = len(sys.argv)
    if (args_len !=4):
        print "Usage: python <source_file> <input_file> <SUPPORT> <HASH_BUCKET_SIZE>"
        sys.exit()

    input_path = sys.argv[1]
    support = sys.argv[2]
    hash_bucket_size = sys.argv[3]

    support = int(support)
    hash_bucket_size = int(hash_bucket_size)
    #print "Arguments list:", sys.argv

    hash_dict = {}
    freq_item_list = find_freq_singletons(input_path, support)
    print freq_item_list

    #start from k=2
    k = 2
    while len(freq_item_list) > 0:
        freq_item_list = find_freq_item_list(input_path, support, k, freq_item_list, hash_bucket_size, hash_dict)
        k = k+1

if __name__ == '__main__':
    main()
