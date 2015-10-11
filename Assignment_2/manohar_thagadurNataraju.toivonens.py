import sys
import itertools
import random

def get_hash_value(itemTuple, hashBucketSize):
    #hashFunc = sum of all the values of chars in the tuple % 20
    sum = 0
    for i in range(0, len(itemTuple)):
        sum = sum + ord(itemTuple[i]) - 96
    hash_val = sum % hashBucketSize
    return hash_val

def get_sampled_input(inputPath, random_list):
    sampled_input = []
    inputFileObj = open(inputPath)
   
    i = 1
    for line in inputFileObj:
        inputList = tokenize(line)
        if i in random_list: 
            sampled_input.append(inputList)
        i = i + 1
    return sampled_input

def tokenize(text):
    text = text.rstrip('\n')
    text = text.split(',')
    text = sorted(text)
    return text

def find_freq_singletons(input_path, support):
    inputFileObj = open(input_path)
    singleton_dict = {}
    freq_singleton_list = []
    all_singleton_list = []
    
    for line in inputFileObj:
        line = tokenize(line)

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


def get_all_cand_from_sample(sampled_input, support, k):
    #print "scaled_support", support
    count_dict = {}
    all_cand_from_sample = []

    for subList in sampled_input:
        k_subsets = get_k_subsets(subList, k)
        for itemA in k_subsets:
            count_dict.setdefault(itemA, 0)
            count_dict[itemA] = count_dict[itemA] + 1
            if count_dict[itemA] >= support:
                if itemA not in all_cand_from_sample:
                    all_cand_from_sample.append(itemA)
    #print count_dict

    '''for k, v in count_dict.iteritems():
        print k, " : ", v'''
    return all_cand_from_sample

def get_candidate_item_list(sampled_input, prob, support, k, prev_Lk_list):
    
    candidate_item_freq_list = []
    count_dict = {}
    CK_list = []

    if k == 1:
        for subList in sampled_input:
            k_subsets = get_k_subsets(subList, k)

            for itemA in k_subsets:
                appendItem = list(itemA)
                count_dict.setdefault(appendItem[0], 0)
                count_dict[appendItem[0]] = count_dict[appendItem[0]] + 1
                if count_dict[appendItem[0]] >= support:
                    if appendItem[0] not in candidate_item_freq_list:
                        candidate_item_freq_list.append(appendItem[0])
   
        for k,v in count_dict.iteritems():
            CK_list.append(k)
        CK_list = sorted(CK_list)
    else:
        if k > 2:
            cand_singleton = get_singleton_from_list(prev_Lk_list)
        else:
            cand_singleton = prev_Lk_list
        #print "cand singleton "
        #print cand_singleton
        k_subsets = get_k_subsets(cand_singleton, k)
        for itemA in k_subsets:
            k_minus_1_subsets = get_k_subsets(list(itemA), k-1)
            flag = 1
            for itemB in k_minus_1_subsets:
                checkItem = list(itemB)
                if len(checkItem) == 1:
                    appendItem = checkItem[0] 
                else:
                    appendItem = itemB
                if appendItem not in prev_Lk_list:
                    flag = 0
            if flag == 1:
                CK_list.append(itemA)

        CK_list = sorted(CK_list)
        #print "CK"
        #print CK_list
        all_cand_sample_list = get_all_cand_from_sample(sampled_input, support, k)
        for item in all_cand_sample_list:
            if item in CK_list:
                candidate_item_freq_list.append(item)

    candidate_item_freq_list = sorted(candidate_item_freq_list)
    #print candidate_item_freq_list
    #print candidate_item_list
    #print len(candidate_item_list)

    #print "CK : ", CK_list
    #print
    #print "LK : ", candidate_item_freq_list
    return (candidate_item_freq_list, CK_list)
               
def get_truly_freq_list(input_path, support, k, probability, candidate_item_list):

    inputFileObj = open(input_path)
    candidate_item_dict = {}
    truly_freq_list = []

    for line in inputFileObj:
        line = tokenize(line, probability)

        k_subsets = get_k_subsets(line, k)
        for item in k_subsets:
            if list(item) in candidate_item_list:
                candidate_item_dict.setdefault(item, 0)
                candidate_item_dict[item] = candidate_item_dict[item] + 1

                if candidate_item_dict[item] >= support:
                    if list(item) not in truly_freq_list:
                        truly_freq_list.append(list(item))

    truly_freq_list = sorted(truly_freq_list)
    #print truly_freq_list
    return truly_freq_list

def find_freq_item_list(input_path, sampled_input, probability, scaled_support, original_support, k, prev_Lk_list):
    candidate_freq_item_list, CK_list = get_candidate_item_list(sampled_input, probability, scaled_support, k, prev_Lk_list)
   

    whole_data_set_freq_item_list = []

    #Compute Negative border
    neg_border_list = []
    for itemA in CK_list:
        flag = 1
        if itemA not in candidate_freq_item_list:
            #print "pnbl ", itemA
	    if k == 1:
	        neg_border_list.append(itemA)
	    else:
	        k_minus_one_subset = get_k_subsets(itemA, k-1)
	        for itemB in k_minus_one_subset:
                    if k-1 == 1:
                        listItem = list(itemB)
                        checkItem = listItem[0]
                    else:
                        checkItem = itemB
	            if checkItem not in prev_Lk_list:
	                flag = 0
                if flag == 1:
	            neg_border_list.append(itemA)

    #print "NBL : ", neg_border_list
    
    #compute for whole data set
    inputFileObj = open(input_path)
    count_dict = {}
    whole_data_set_freq_items = []

    for line in inputFileObj:
        line = tokenize(line)
       
	k_subset = get_k_subsets(line, k)
	for itemA in k_subset:
	    checkItem = list(itemA)
            if k == 1:
                actual_append_item = checkItem[0]
            else:
                actual_append_item = itemA                

	    if actual_append_item in neg_border_list or actual_append_item in candidate_freq_item_list:
	        count_dict.setdefault(actual_append_item, 0)
	        count_dict[actual_append_item] = count_dict[actual_append_item] + 1
	        if count_dict[actual_append_item] >= original_support:
	                if actual_append_item not in whole_data_set_freq_items:
	                    whole_data_set_freq_items.append(actual_append_item)

    repeat = 0
    for item in neg_border_list:
        if item in whole_data_set_freq_items:
            repeat = 1

    whole_data_set_freq_items = sorted(whole_data_set_freq_items)

    #print "neg" 
    #print neg_border_list
    #print "whole"
    #print whole_data_set_freq_items

    return (whole_data_set_freq_items, repeat, candidate_freq_item_list)

def get_random_list(req_range, total_sample_size):
    random_list = random.sample(xrange(1, req_range), total_sample_size)
    return random_list

def get_singleton_from_list(Lk_list):
    singleton = []
    for itemA in Lk_list:
        list_itemA = list(itemA)
        for itemB in list_itemA:
            if itemB not in singleton:
                singleton.append(itemB)
    singleton = sorted(singleton)
    return singleton

def main():
    args_len = len(sys.argv)
    if (args_len !=3):
        print "Usage: python <source_5file> <input_file> <SUPPORT>"
        sys.exit()

    input_path = sys.argv[1]
    support = sys.argv[2]

    support = int(support)
    #print "Arguments list:", sys.argv

    probability = 0.5
    _sampled_input = []

    hash_dict = {}

    with open(input_path) as f:
        total_baskets = sum(1 for _ in f)

    #print "total lines : ", total_baskets


    total_sample_size = int(probability * total_baskets)
    #print "samp size ", total_sample_size
    #for sample, determine the range
    req_range = total_baskets
    random_list = get_random_list(req_range, total_sample_size)
    #print "rand list : ", random_list
    #start from k=2
    k = 1
    _whole_data_freq_item_list = []
    whole_data_set_freq_items = []
    repeat = 0
    total_iter = 1
    scaled_support = 0.8*probability*support
    while k == 1 or len(whole_data_set_freq_items) > 0:
        if repeat or k == 1:
            total_iter = total_iter + 1
            k = 1
            _sampled_input = []
            prev_Lk_list = []
            whole_data_set_freq_items = []
            _whole_data_freq_item_list = []
            random_list = get_random_list(req_range, total_sample_size)
            _sampled_input = get_sampled_input(input_path, random_list)
            #print _sampled_input
        whole_data_set_freq_items = []
        whole_data_set_freq_items, repeat, prev_Lk_list = find_freq_item_list(input_path, _sampled_input, probability, scaled_support, support, k, prev_Lk_list)
        if repeat == 1:
            k = 1
            #print freq_item_list
        else:
            k = k + 1
            if len(whole_data_set_freq_items) > 0:
        #copy all items in whole_data to _whole_data list to be used for printing later
                for item in whole_data_set_freq_items:
                    list_item = list(item)
                    _whole_data_freq_item_list.append(list_item)
    
    #print "=== whole === "

    # === print the required output ====
    print total_iter
    print probability

    #start printing from size=1
    size = 1
    print_list = []
    while size == 1 or len(print_list) > 0:
        print_list = []
        for item in _whole_data_freq_item_list:
            if len(item) == size:
                print_list.append(item)
        if len(print_list) > 0:
            print print_list
            print
        size = size + 1

if __name__ == '__main__':
    main()
