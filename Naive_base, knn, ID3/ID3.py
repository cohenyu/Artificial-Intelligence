import math
import copy


class Node:
    def __init__(self, attribute):
        self.attribute = attribute
        self.subtree = []

    def add_branch(self, value, subtree):
        self.subtree.append([value, subtree])


attribute_values_dict = {}


def same_class(examples):
    tag = examples[0][-1]
    for e in examples:
        if e[-1] != tag:
            return False, None
    return True, tag


def tag_count(examples):
    yes = 0
    no = 0
    for e in examples:
        if e[-1] == "yes":
            yes += 1
        else:
            no += 1
    return yes, no


def common_class(examples):
    yes,no = tag_count(examples)
    return "yes" if yes > no else "no"


def entropy(examples):
    yes, no = tag_count(examples)
    all_ex = yes + no
    e1 = ((yes / all_ex) * math.log(yes / all_ex, 2)) if yes != 0 else 0
    e2 = ((no / all_ex) * math.log(no / all_ex, 2)) if no != 0 else 0
    return -1 * (e1 + e2)


def get_values_dict(examples, attribute_idx):
    values_dict = {}
    for val in attribute_values_dict[attribute_idx]:
        values_dict.update({val: []})

    for e in examples:
        values_dict[e[attribute_idx]].append(e)
    return values_dict


def choose_attribute(examples, attributes):
    ig_list = []
    examples_size = len(examples)
    for att_name in attributes:
        ig = 0
        value_dict = get_values_dict(examples, attributes[att_name])
        for value in value_dict:
            cur_entropy = entropy(value_dict[value])
            ig += (len(value_dict[value]) / examples_size) * cur_entropy
        ig_list.append([ig, att_name, value_dict])
    ig_list.sort(key=lambda x: x[0])
    best = ig_list[0]
    return best[1], best[2]


def values_per_attribute(examples, attributes):
    for idx in attributes.values():
        if idx not in attribute_values_dict:
            attribute_values_dict.update({idx: []})

        for ex in examples:
            if ex[idx] not in attribute_values_dict[idx]:
                attribute_values_dict[idx].append(ex[idx])


def DTL(examples, attributes, default_tag):
    if not examples:
        return Node(default_tag)
    same, tag = same_class(examples)
    if same:
        return Node(tag)
    elif not attributes:
        return Node(common_class(examples))
    else:
        best, values_dict = choose_attribute(examples, attributes)
        tree = Node(best)
        temp = copy.deepcopy(attributes)
        del temp[best]
        values_dict = dict(sorted(values_dict.items(), key=lambda x: x[0]))
        for value, new_examples in values_dict.items():
            subtree = DTL(new_examples, temp, common_class(examples))
            tree.add_branch(value, subtree)
        return tree


def classify(example, tree, attributes):
    if tree.attribute == "yes" or tree.attribute == "no":
        return tree.attribute

    idx = attributes[tree.attribute]
    for subtree in tree.subtree:
        if example[idx] == subtree[0]:
            return classify(example, subtree[1], attributes)


def get_ID3_result(examples, tree, attributes):
    correct = 0
    for ex in examples:
        tag = classify(ex, tree, attributes)
        correct += 1 if tag == ex[-1] else 0
    return correct / len(examples)


def tree_generator(examples, attributes):
    values_per_attribute(examples, attributes)
    return DTL(examples, attributes, "yes")
