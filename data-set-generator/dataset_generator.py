import json
import copy
from scipy.stats import randint
from numpy.random import SeedSequence
from numpy.random import default_rng
import numpy as np


number_of_queries = 2 ** 20

def generate_setup_set(n):
    setup_set_size = ((2**20)//10) * n # we chose the setup size to take values of "n times a tenth of 2^20"
    rng = default_rng(32254990002318088069556011570970575698)  # using custom seed of the random number generator to make the results reproducible
    setup_set_values = randint.rvs(10 ** 5, 2 * 10 ** 5, size=setup_set_size,
                                   random_state=rng).tolist()  # generating a set of 2^20 random integers between 100k and 200k that will be used as values for the setup set
    setup_set_keys = np.arange(1, (setup_set_size) + 1, 1).tolist()

    print(
        "Number of keys is the same as number of values before we start merging them into a key:value pairs - {}".format(
            len(setup_set_keys) == len(setup_set_values)))

    rng = default_rng(206466621666963313970457261653727091860)
    iterations = len(
        setup_set_keys) - 1  # We need total number of keys - 1 iterations because scipy raises an exception if we try to get a rndint with low=0 and high=0, which is the case in the last iteration (only 1 key is left in the list).
    setup_set_dict = {}

    for i in range(iterations):
        index = randint.rvs(low=0, high=len(setup_set_keys) - 1, random_state=rng)
        key = setup_set_keys.pop(index)
        value = setup_set_values.pop()  # no need to pop a value at specific index since they are already unsorted and randomized.
        setup_set_dict[key] = value

    # poping last key and value and adding them to the dict as pair.
    key = setup_set_keys.pop()
    value = setup_set_values.pop()
    setup_set_dict[key] = value

    print("Setup_set_dict length = {}".format(len(setup_set_dict)))

    with open("setup_set_{}.json".format(n), "w") as file:
        json.dump(setup_set_dict, file)

    return len(setup_set_dict)

def generate_static_problem_set(setup_set_size, n):
    global number_of_queries

    rng = default_rng(323220876805334095988239417329540186256)
    upper_bound = setup_set_size + setup_set_size // 2
    isMember_set_static = randint.rvs(low=1, high=upper_bound, random_state=rng, size=number_of_queries).tolist()

    with open("static_problem_set_{}.json".format(n), "w") as file:
        json.dump(isMember_set_static, file)

    print("Size of static problem isMember set = {}".format(len(isMember_set_static)))


def generate_dynamic_problem_set(setup_set_size, n):

    rng = default_rng(221968154327335442400956208460406460092)
    delete_set = []
    isMember_set = []
    number_del_operations = (setup_set_size) // 3
    number_isMember_operations = 2 * setup_set_size // 9
    iterations = number_del_operations + number_isMember_operations
    setup_set_keys = np.arange(1, (setup_set_size) + 1, 1).tolist()
    for i in range(iterations):
        index = randint.rvs(low=0, high=len(setup_set_keys) - 1, random_state=rng)
        if i < number_del_operations:
            delete_set.append(["delete", setup_set_keys.pop(index)])
        else:
            isMember_set.append(["isMember", setup_set_keys.pop(index)])

    print("Number of delete operations is correct - {}".format((setup_set_size) // 3 == len(delete_set)))
    print("Number of legal isMember operations is correct - {}".format(2 * setup_set_size // 9 == len(isMember_set)))

    rng = default_rng(81768862057879993526170376212426307869)
    rng_2 = default_rng(155676108167050145510153885484907278655)
    number_isMember_operations_unexisting_key = setup_set_size // 9
    number_insert_operations = number_del_operations
    upper_bound = setup_set_size + number_insert_operations + number_isMember_operations_unexisting_key
    unexisting_keys = np.arange(setup_set_size + 1, upper_bound + 1, 1).tolist()
    iterations = len(unexisting_keys) - 1
    print("Range for generating unexisting keys is correct - {}".format(
        iterations + 1 == setup_set_size // 3 + setup_set_size // 9))
    insert_set = []

    for i in range(iterations):
        index = randint.rvs(low=0, high=len(unexisting_keys) - 1, random_state=rng)
        if i < number_insert_operations:
            key = unexisting_keys.pop(index)
            value = randint.rvs(low=2 * 10 ** 5, high=3 * 10 ** 5, random_state=rng_2)
            insert_set.append(["insert", key, value])
        else:
            key = unexisting_keys.pop(index)
            isMember_set.append(["isMember", key])
    isMember_set.append(["isMember", unexisting_keys.pop()])

    rng = default_rng(294493996120424975969415788972525135884)
    isMember_set_shuffled = []
    for i in range(len(isMember_set) - 1):
        index = randint.rvs(low=0, high=len(isMember_set) - 1, random_state=rng)
        isMember_set_shuffled.append(isMember_set.pop(index))
    isMember_set_shuffled.append(isMember_set.pop())

    print("unexisting_keys list length - {}".format(len(unexisting_keys)))
    print("Number of insert operations is correct - {}".format(setup_set_size // 3 == len(insert_set)))
    print(
        "Number of total isMember operations is correct - {}".format(setup_set_size // 3 == len(isMember_set_shuffled)-1))
    print("Size of delete set = {}".format(len(delete_set)))
    print("Size of insert set = {}".format(len(insert_set)))
    print("Size of isMember set = {}".format(len(isMember_set_shuffled)))

    dynamic_problem_experimental_set = []
    dynamic_problem_experimental_set.extend(delete_set)
    dynamic_problem_experimental_set.extend(isMember_set_shuffled)
    dynamic_problem_experimental_set.extend(insert_set)

    dynamic_problem_experimental_set_shuffled = []
    for i in range(len(dynamic_problem_experimental_set) - 1):
        index = randint.rvs(low=0, high=len(dynamic_problem_experimental_set) - 1, random_state=rng)
        dynamic_problem_experimental_set_shuffled.append(dynamic_problem_experimental_set.pop(index))
    dynamic_problem_experimental_set_shuffled.append(dynamic_problem_experimental_set.pop())

    with open("dynamic_problem_set_{}.json".format(n), "w") as file:
        json.dump(dynamic_problem_experimental_set_shuffled, file)

    print("Size of dynamic problem experimental set = {}".format(len(dynamic_problem_experimental_set_shuffled)))

def main():
    for n in range(1,10):
        set_size = generate_setup_set(n)
        generate_static_problem_set(set_size, n)
        generate_dynamic_problem_set(set_size, n)


if __name__ == "__main__":
    main()