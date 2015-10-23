import sys
import math

def predict_rating(user, item, k_nearest_neighbours, user_item_dict):
    numerator = 0.0
    denominator = 0.0
    for neighbour in k_nearest_neighbours:
        neighbour_user_id = neighbour[0]
        neighbour_similarity_val = neighbour[1]
        neighbour_user_movie_rating_dict = user_item_dict[neighbour_user_id]
        if item in neighbour_user_movie_rating_dict.keys():
            numerator += (neighbour_similarity_val * neighbour_user_movie_rating_dict[item])
            denominator += neighbour_similarity_val

    predicted_rating = float(numerator/denominator)

    return predicted_rating

def get_K_nearest_neighbours(pearson_coeff_dict, K):
    otherUsers_list = pearson_coeff_dict.keys()
    otherUsers_pearsonValue_list = pearson_coeff_dict.values()

    user_pearsonVal_list = zip(otherUsers_pearsonValue_list, otherUsers_list)

    #user_pearsonVal_list_sorted = sorted(user_pearsonVal_list)

    user_pearsonVal_list_sorted = sorted(user_pearsonVal_list, key=lambda x:(-x[0], x[1]))

    neighbour_list = [(user,val) for val,user in user_pearsonVal_list_sorted]

    # print val and user in user_pearsonVal_list
    '''
    for val, user in user_pearsonVal_list:
        print user, " : " , val
    '''
    #get top k neighbour_list
    # list is sorted in descending order, so to get top k
    k_nearest_neighbour_list = neighbour_list[:K]
    return k_nearest_neighbour_list

def get_pearson_coefficient_util(userA, userA_avgRating, userA_movie_rating_dict, userB, userB_avgRating, userB_movie_rating_dict):
    numerator = 0.0
    denominator_part1 = 0.0
    denominator_part2 = 0.0

    for movie, userA_rating in userA_movie_rating_dict.iteritems():
        
        if movie in userB_movie_rating_dict:
            userA_rating_normalize = userA_rating - userA_avgRating
            userB_rating = userB_movie_rating_dict[movie]
            userB_rating_normalize = userB_rating - userB_avgRating

            numerator += (userA_rating_normalize * userB_rating_normalize)

            denominator_part1 += math.pow(userA_rating_normalize, 2)
            denominator_part2 += math.pow(userB_rating_normalize, 2)

    denominator = math.sqrt(denominator_part1) * math.sqrt(denominator_part2)
    pearson_coeff_val = float(numerator/denominator)

    return pearson_coeff_val

def get_pearson_coeff_dict(input_user, user_item_dict, user_avg_rating_dict):
    numerator = 0.0
    denominator = 0.0
    pearson_coeff_dict = {}
    for otherUser, otherUserAvgRating in user_avg_rating_dict.iteritems():
        if otherUser != input_user:
            input_user_avg_rating = user_avg_rating_dict[input_user]

            input_user_movie_rating_dict = user_item_dict[input_user]
            otherUser_movie_rating_dict = user_item_dict[otherUser]
            pearson_coeff_val = get_pearson_coefficient_util(input_user, input_user_avg_rating, input_user_movie_rating_dict, otherUser, otherUserAvgRating, otherUser_movie_rating_dict)
            pearson_coeff_dict.setdefault(otherUser, pearson_coeff_val)

    return pearson_coeff_dict

def print_required_output(k_nearest_neighbour_list, predicted_rating):

    for user_name, pearson_val in k_nearest_neighbour_list:
        print user_name, pearson_val
    print "\n"
    print predicted_rating
            

def get_from_file_to_list(ratings_file):
    inputFileObj = open(ratings_file)

    input_list = []
    for line in inputFileObj:
        line = line.rstrip('\n')
        entry_in_list = line.split('\t')

        input_list.append(entry_in_list)

    inputFileObj.close()
    return input_list

def get_user_item_dict(input_list):
    user_item_dict = {}
    user_avg_rating_dict = {} 
    map_user_avgRating = {}

    for item in input_list:
        user_id = item[0]
        rating = float(item[1])
        movie_name = item[2]

        item_aggr_dict = {}
        user_item_dict.setdefault(user_id, item_aggr_dict)
        user_item_dict[user_id].setdefault(movie_name, rating)

        rating_itemCount_list = [0, 0]
        user_avg_rating_dict.setdefault(user_id, rating_itemCount_list)
        
        rating_sum = user_avg_rating_dict[user_id][0]
        rating_sum += rating
        movie_count = user_avg_rating_dict[user_id][1]
        movie_count += 1

        user_avg_rating_dict[user_id][0] = rating_sum
        user_avg_rating_dict[user_id][1] = movie_count

    for key,val in user_avg_rating_dict.iteritems():
        map_user_avgRating.setdefault(key, 0.0)
        avg = float(val[0]/val[1])
        map_user_avgRating[key] = avg
    return (user_item_dict, map_user_avgRating)

def main():
    args_len = len(sys.argv)
    if args_len != 5:
        print "Usage: python <source_file> <ratings_input_file> <user_id> <item_name_to_calculate_prediction_for> <no_of_neighbours>"
        sys.exit()
    
    ratings_file = sys.argv[1]
    input_user_id = sys.argv[2]
    item_name = sys.argv[3]
    neighbours_count = int(sys.argv[4])

    # print the arguments
    '''
    print "input params are"
    print "ratings_file :", ratings_file
    print "user_id :", input_user_id
    print "item_name :", item_name
    print "neighbours_count :", neighbours_count

    '''
    input_list = get_from_file_to_list(ratings_file)

    # print the input list
    
    '''
    print "size :", len(input_list)
    for item in input_list:
        print item
    '''

    user_item_dict, user_avg_rating_dict = get_user_item_dict(input_list)

    #user item dict - {user_id: {movie_name:rating, ...}}

    '''
    print user_item_dict
    print user_avg_rating_dict

    '''
    pearson_coeff_dict = get_pearson_coeff_dict(input_user_id, user_item_dict, user_avg_rating_dict)

    # pearson coeff dict for given/input user
    '''
    print pearson_coeff_dict
    '''
    
    k_nearest_neighbour_list = get_K_nearest_neighbours(pearson_coeff_dict, neighbours_count)

    # print k nearest neighbours to input_user

    #print k_nearest_neighbour_list
    '''
    for user_name, pearson_val in k_nearest_neighbour_list:
        print user_name, " ", pearson_val
    '''

    predicted_rating = predict_rating(input_user_id, item_name, k_nearest_neighbour_list, user_item_dict) 

    # print predicted_rating
    '''
    print predicted_rating
    '''

    print_required_output(k_nearest_neighbour_list, predicted_rating)

if __name__ == "__main__":
    main()
