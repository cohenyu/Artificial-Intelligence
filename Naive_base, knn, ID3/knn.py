# This function calculate the hemming distance of 2 examples
def hemming_distance(a, b):
    dis = 0
    # check if the features is different of each cell
    for i in range(len(a) - 1):
        dis += 1 if a[i] != b[i] else 0
    return dis


# This function find the correct classification
def knn_get_tag(topk):
    yes = 0
    no = 0
    # check how many tags of the topk examples is "yes" or "no"
    for example in topk:
        if example[1] == 'no':
            no += 1
        else:
            yes += 1
    # the classification is by the majority
    return "yes" if yes > no else "no"


# This function runs the knn algorithm
def knn(train, test, k):
    correct = 0
    for test_ex in test:
        # get the needed data from the train set
        data = [[hemming_distance(test_ex, train_ex), train_ex[-1]] for train_ex in train]
        # sort the data by the hemming_distance
        data.sort(key=lambda x: x[0])
        # take the top k (the k min hemming_distance)
        topk = data[:k]
        # get the tag (classification)
        tag = knn_get_tag(topk)
        # check if this classification is correct
        correct += 1 if tag == test_ex[-1] else 0
    return correct / len(test)


