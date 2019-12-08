from random import uniform
from math import sqrt
from operator import itemgetter

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



def forward_search():
    with open("smalldata/CS170_SMALLtestdata__1.txt", "r") as f:
        data = [line.split() for line in f.readlines()]
    f.close
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

def backward_search():
    with open("smalldata/CS170_SMALLtestdata__1.txt", "r") as f:
        data = [line.split() for line in f.readlines()]
    f.close
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


def iterative_deepening():
    with open("data/CS170_SMALLtestdata__1.txt", "r") as f:
        data = [line.split() for line in f.readlines()]
    f.close
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

#forward_search()
#backward_search()
iterative_deepening()