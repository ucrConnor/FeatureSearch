from random import uniform

def cross_validation(data, current_features, added_feature):
    return uniform(0,100)

def search():
    with open("smalldata/CS170_SMALLtestdata__1.txt", "r") as f:
        data = [line.split() for line in f.readlines()]
    f.close

    current_features = []

    for i in range(1,len(data[0])):
        print(f"Currently in level {i}")
        added_feature = []
        highest_accuracy = 0
        for j in range(1,len(data[0])):
            if j not in current_features:
                accuracy = cross_validation(data,current_features, j + 1)
                print(f"\tConsidering adding feature {j}: {accuracy}")
                

                if accuracy > highest_accuracy:
                    highest_accuracy = accuracy
                    added_feature = j
        current_features.append(added_feature)
        print(f"Level {i}: added {added_feature} to feature set")
search()