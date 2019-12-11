from random import uniform
from math import sqrt
from operator import itemgetter
from timeit import default_timer
import cProfile
import sys

def calc_distance(instance1, instance2, features):
    sum = 0
    for feature in features:
        sum = sum + (float(instance1[feature]) - float(instance2[feature]))**2
    distance = sqrt(sum)
    return distance

def cross_validation(data, current_features, added_feature, method = "add"):
    features = current_features.copy()
    if added_feature != 0:
        if method == "add":
            features.append(added_feature)
        elif method == "remove":
            features.remove(added_feature)
    correct_classifications = 0
    for i in range (len(data)):
        nearest_neighbor = data[i-1]
        nearest_distance = calc_distance(data[i], nearest_neighbor, features)
        for j in range (len(data)):
            if i != j:
                distance = calc_distance(data[i], data[j], features)
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_neighbor = data[j]
        if data[i][0] == nearest_neighbor[0]:
            correct_classifications = correct_classifications + 1
    
    return correct_classifications/len(data)



def forward_search(data):

    features_accuracy_at_each_level = []
    current_features = []

    for i in range(1,len(data[0])):
        print(f"Currently in level {i}")
        added_feature = []
        highest_accuracy = 0
        for j in range(1,len(data[0])):
            if j not in current_features:
                accuracy = cross_validation(data,current_features, j)
                print(f"\tConsidering adding feature {j}: {accuracy}")
                

                if accuracy > highest_accuracy:
                    highest_accuracy = accuracy
                    added_feature = j
        current_features.append(added_feature)
        features_accuracy_at_each_level.append((current_features.copy(),highest_accuracy))
        print(f"Level {i}: added {added_feature} to feature set")

    best_features = features_accuracy_at_each_level[0]
    for features, accuracy in features_accuracy_at_each_level:
        #print(f"{features}: {accuracy}")
        if accuracy > best_features[1]:
            best_features = (features, accuracy)
    print(f"The best feature set is {best_features[0]} with an accuracy of {best_features[1]}")

def backward_search(data):

    features_accuracy_at_each_level = []
    current_features = [num for num in range(1,len(data[0]))]
    #print(current_features)
    for i in range(len(data[0])-1,0,-1):
        print(f"Currently in level {i}")
        remove_feature = []
        highest_accuracy = 0
        for j in range(len(data[0]),0,-1):
            if j in current_features:
                accuracy = cross_validation(data,current_features, j, method="remove")
                print(f"\tConsidering removing feature {j}: {accuracy}")
                

                if accuracy > highest_accuracy:
                    highest_accuracy = accuracy
                    remove_feature = j
        current_features.remove(remove_feature)
        features_accuracy_at_each_level.append((current_features.copy(),highest_accuracy))
        print(f"Level {i}: removed {remove_feature} from feature set")

    best_features = features_accuracy_at_each_level[0]
    for features, accuracy in features_accuracy_at_each_level:
        #print(f"{features}: {accuracy}")
        if accuracy > best_features[1]:
            best_features = (features, accuracy)
    print(f"The best feature set is {best_features[0]} with an accuracy of {best_features[1]}")


def combinational_search(data):

    best_of_one_feature = ([],0)
    print("Checking all single features")
    for i in range(1,len(data[0])):
        accuracy = cross_validation(data,[i], 0)
        if accuracy > best_of_one_feature[1]:
            best_of_one_feature = ([i],accuracy)
        print(f"\tChecking Feature {i}: {accuracy}")

    best_of_two_features = ([],0) 
    print("Checking all combinations of two features")
    for i in range(1,len(data[0])):
        for j in range(1,len(data[0])):
            if i != j:    
                features = [i,j]
                accuracy = cross_validation(data,features, 0)
                if accuracy > best_of_two_features[1]:
                    best_of_two_features = (features,accuracy)
                print(f"\tChecking Feature {features}: {accuracy}")
    
    #print(best_of_one_feature)
    #print(best_of_two_features)
    best_features = max([best_of_one_feature, best_of_two_features], key=itemgetter(1))
    print(f"The best feature set is {best_features[0]} with an accuracy of {best_features[1]}")


def open_file(path = "smalldata/CS170_SMALLtestdata__1.txt"):
    with open(path, "r") as f:
        data = [line.split() for line in f.readlines()]
    f.close
    return data

search = ""
file_path = ""
stop = False
if len(sys.argv) > 1:
    search = sys.argv[1]
    if len(sys.argv) == 3:
        file_path = sys.argv[2]
        stop = True
while True:
    if not file_path:
        file_path = input("Enter the dataset you want to run.\n\n")
    data = open_file(file_path)
    if not search:
        search = input("""Enter the number to select the function\n\t 1: Forward Search\n\t 2: Backwards Search\n\t 3: Combinational Search\n\t 4: Change File\n\t 5: Exit\n""")
    search = int(search)
    if search == 1:
        profile1 = cProfile.Profile()
        profile1.enable()
        forward_search(data)
        profile1.disable()
        path = f"{file_path[:-4]}_forward_search"
        profile1.dump_stats(path)
        #print(f"\nForward Search time: {end - start} seconds\n")
    elif search == 2:
        profile2 = cProfile.Profile()
        profile2.enable()
        backward_search(data)
        profile2.disable()
        path = f"{file_path[:-4]}_backward_search"
        profile2.dump_stats(path)
        #print(f"\nBackward Search time: {end - start} seconds\n")
    elif search == 3:
        start = default_timer()
        profile3 = cProfile.Profile()
        profile3.enable()
        combinational_search(data)
        profile3.disable()
        path = f"{file_path[:-4]}_combin_search"
        profile3.dump_stats(path)
        #print(f"\nCombinational Search time: {end - start} seconds\n")
    elif search == 4:
        file_path = input("Enter the dataset you want to run.\n\n")
    elif search == 5:
        break
    search = ""
    if stop:
        break
