from knn import knn
from naive_base import naive_base
from ID3 import *

attributes_dict = {}


def decision_tree(f, tree, is_root, number_of_tabs):
    if tree.attribute == "yes" or tree.attribute == "no":
        f.write(": " + tree.attribute + "\n")
        return
    elif not is_root:
        number_of_tabs += 1
        f.write("\n")
    for subtree in tree.subtree:
        if not is_root:
            f.write("\t" * number_of_tabs + '|')
        f.write(tree.attribute + " = " + subtree[0])
        decision_tree(f, subtree[1], False, number_of_tabs)


def save_tree(tree, file_name):
    f = open(file_name, "w")
    decision_tree(f, tree, True, 0)
    if file_name == "output.txt":
        f.write('\n')
    f.close()


def set_dict_attributes(attributes):
    for idx, attribute in enumerate(attributes[:-1]):
        attributes_dict.update({attribute: idx})


# This function read the dataset from a text file
def get_dataset(file_name):
    file = open(file_name, "r")
    set_dict_attributes(file.readline().split())
    dataset = [line.split() for line in file]
    file.close()
    return dataset


def split_dataset(dataset):
    n = int(len(dataset) * (1 / 5))
    return dataset[:n], dataset[n:]


# This function writes the accuracy to a file
def save_accuracy(file_name, dt, knn, nb):
    file = open(file_name, "a")
    file.write("{}  {}  {}".format(dt, knn, nb))
    file.close()


def cross_validation(k, dataset):
    knn_result = 0
    nb_result = 0
    id3_result = 0
    dataset_len = len(dataset)
    for i in range(k):
        x, y = int((i / k) * dataset_len), int(((i + 1) / k) * dataset_len)
        test = dataset[x:y]
        train = (dataset[:x] + (dataset[y:]))
        knn_result += knn(train, test, 5)
        nb_result += naive_base(train, test)
        tree = tree_generator(train, attributes_dict)
        id3_result += get_ID3_result(test, tree, attributes_dict)
    save_accuracy("accuracy.txt", id3_result / k, knn_result / k, nb_result / k)


def main():
    dataset = get_dataset("dataset.txt")
    # cross_validation(5, dataset)
    tree = tree_generator(dataset, attributes_dict)
    save_tree(tree, "tree.txt")

    # test, train = split_dataset(dataset)
    # train = get_dataset("train.txt")
    # test = get_dataset("test.py")
    # knn_result = knn(train, test, 5)
    # nb_result = naive_base(train, test)
    # tree = tree_generator(train, attributes_dict)
    # id3_result = get_ID3_result(test, tree, attributes_dict)

    # save_tree(tree, "output.txt")
    # save_accuracy("output.txt", id3_result, knn_result, nb_result)


if __name__ == '__main__':
    main()
