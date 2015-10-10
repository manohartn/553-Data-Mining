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


def get_candidate_item_list(sampled_input, prob, support, k, freq_item_list):
    
    candidate_item_freq_list = []
    count_dict = {}
    current_freq_list = []

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
   
    else:
        cand_singleton = get_singleton(freq_item_list)
        k_subsets = get_k_subsets(cand_singleton, k)
        if k == 2:
            pass
    candidate_item_freq_list = sorted(candidate_item_freq_list)
    print "cand:"
    print candidate_item_freq_list
    #print candidate_item_list
    #print len(candidate_item_list)

    all_candidate_list = []
    for k,v in count_dict.iteritems():
       all_candidate_list.append(k)
    all_candidate_list = sorted(all_candidate_list)
    return (candidate_item_freq_list, all_candidate_list)
               
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

def find_freq_item_list(input_path, sampled_input, probability, scaled_support, original_support, k, freq_item_list):
    candidate_freq_item_list, all_candidate_list = get_candidate_item_list(sampled_input, probability, scaled_support, k, freq_item_list)
    
    #Compute Negative border
    neg_border_list = []
    for itemA in all_candidate_list:
        flag = 1
        if itemA not in candidate_freq_item_list:
	    if k == 1:
	        neg_border_list.append(itemA)
	    else:
	        k_minus_one_subset = get_k_subsets(itemA, k-1)
	        flag = 1
	        for itemB in k_minus_one_subset:
	            if itemB not in candidate_freq_item_list:
	                flag = 0
                if flag == 1:
	            neg_border_list.append(itemA)

    #print neg_border_list
    
    #compute for whole data set
    inputFileObj = open(input_path)
    whole_data_set_freq_items = []
    count_dict = {}

    for line in inputFileObj:
        line = tokenize(line)
       
	k_subset = get_k_subsets(line, k)
	if k == 1:
	    for itemA in k_subset:
	        checkItem = list(itemA)
	        if checkItem[0] in neg_border_list or checkItem[0] in candidate_freq_item_list:
	            count_dict.setdefault(checkItem[0], 0)
	            count_dict[checkItem[0]] = count_dict[checkItem[0]] + 1
	            if count_dict[checkItem[0]] >= original_support:
	                if checkItem[0] not in whole_data_set_freq_items:
	                    whole_data_set_freq_items.append(checkItem[0])

    repeat = 0
    for item in neg_border_list:
        if item in whole_data_set_freq_items:
            repeat = 1

    whole_data_set_freq_items = sorted(whole_data_set_freq_items)
    print "neg" 
    print neg_border_list
    print whole_data_set_freq_items

    return (candidate_freq_item_list, repeat)

def get_random_list(req_range, total_sample_size):
    random_list = random.sample(xrange(1, req_range), total_sample_size)
    return random_list

def main():
    args_len = len(sys.argv)
    if (args_len !=3):
        print "Usage: python <source_file> <input_file> <SUPPORT>"
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
    freq_item_list = []
    repeat = 0
    total_iter = 1
    scaled_support = 0.8*probability*support
    #while k == 1 or len(freq_item_list) > 0:
    while k == 1 or repeat:
        if repeat or k == 1:
            total_iter = total_iter + 1
            k = 1
            _sampled_input = []
            freq_item_list = []
            random_list = get_random_list(req_range, total_sample_size)
            _sampled_input = get_sampled_input(input_path, random_list)
            #print _sampled_input
        freq_item_list, repeat = find_freq_item_list(input_path, _sampled_input, probability, scaled_support, support, k, freq_item_list)
        if repeat == 0:
            pass
            #print freq_item_list
        k = k + 1

if __name__ == '__main__':
    main()
