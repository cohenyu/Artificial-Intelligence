# This function arranges the data in an efficient data structure
def pre_processing(train):
    attributes_num = len(train[0]) - 1
    # Create a list of dictionaries, one dictionary for each attribute
    yes = [{} for i in range(attributes_num)]
    no = [{} for i in range(attributes_num)]

    yes_num = 0
    no_num = 0

    for example in train:
        # if the example tag is "yes" -> add 1 to the yes counter
        if example[-1] == "yes":
            yes_num += 1
        # else add 1 to the no counter
        else:
            no_num += 1

        # loop over the attributes in the example
        for cell, attribute in enumerate(example[:-1]):
            # if the attribute not in the dictionary -> add this attribute with counter = 0
            if attribute not in yes[cell]:
                yes[cell][attribute] = 0
            if attribute not in no[cell]:
                no[cell][attribute] = 0

            # add 1 to the attribute in the right dictionary
            if example[-1] == "yes":
                yes[cell][attribute] += 1
            else:
                no[cell][attribute] += 1

    # check what is the most common tag
    majority = "yes" if yes_num > no_num else "no"
    return yes_num, yes, no_num, no, majority


# This function runs the naive base algorithm
def naive_base(train, test):
    correct = 0
    yes_num, yes_list, no_num, no_list, majority = pre_processing(train)
    all_counter = len(train)
    # get the number of yes/no from the total number of examples
    yes_counter = yes_num / all_counter
    no_counter = no_num / all_counter

    for test_ex in test:
        yes = yes_counter if yes_counter != 0 else 1
        no = no_counter if no_counter != 0 else 1
        #  loop over the attributes in the test example
        for idx, attribute in enumerate(test_ex[:-1]):
            # if the attribute in the dictionary and his value not 0 -> multiply the probability of seeing this feature
            if attribute in yes_list[idx] and yes_list[idx][attribute] != 0:
                yes *= (yes_list[idx][attribute] / yes_num)

            if attribute in no_list[idx] and no_list[idx][attribute] != 0:
                no *= (no_list[idx][attribute] / no_num)

        tag = nb_get_tag(yes, no, majority)
        correct += 1 if tag == test_ex[-1] else 0

    return correct / len(test)


# This function find the correct classification
def nb_get_tag(yes, no, majority):
    if yes > no:
        return "yes"
    elif no > yes:
        return "no"
    return majority