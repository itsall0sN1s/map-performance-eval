import json
import time
#import platform # Module to check platform. Current platform is CPython
from pympler import asizeof # Module to measure object size


#dynamic_problem_set_json = open("C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\dynamic_problem_set_{}.json".format(n))



def load_setup_set(setup_set_json):
    setup_set = {}
    setup_set_raw = json.load(setup_set_json)
    for key, value in setup_set_raw.items():
        key = int (key)
        setup_set[key] = value

    return setup_set
def run_memory_usage_benchmark():
    memory_usage_results = []
    for n in range(1,11):
        setup_set = load_setup_set(open(
            "C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\setup_set_{}.json".format(n)))
        memory_usage_results.append(asizeof.asizeof(setup_set))

    with open("py_memory_usage_results.json", "w") as file:
        json.dump(memory_usage_results, file)


def run_dynamic_problem_test():
    global setup_set, dynamic_problem_set
    start_time = time.time()
    for instruction in dynamic_problem_set:
        match instruction[0]:
            case "delete":
                del setup_set[instruction[1]]
            case "insert":
                setup_set[instruction[1]] = instruction[2]
            case "isMember":
                instruction[1] in setup_set
    end_time = time.time()
    exec_time = (end_time - start_time) * 1000

    return exec_time
def run_dynamic_problem_benchmark():
    global setup_set, dynamic_problem_set
    setup_set = {}
    dynamic_problem_set = []
    for n in range(1, 11):
        setup_set = load_setup_set(open(
            "C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\setup_set_{}.json".format(n)))
        dynamic_problem_set = json.load(open(
            "C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\dynamic_problem_set_{}.json".format(n)))

        exec_times = []
        for i in range(10):
            exec_times.append(run_dynamic_problem_test())
            setup_set = load_setup_set(open(
                "C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\setup_set_{}.json".format(n)))
        with open("py_dynamic_problem_results_{}.json".format(n), "w") as file:
            json.dump(exec_times, file)


def run_static_problem_test():
    global setup_set, static_problem_set

    start_time = time.time()
    for key in static_problem_set:
        key in setup_set
    end_time = time.time()
    exec_time = (end_time - start_time) * 1000

    return exec_time
def run_static_problem_benchmark():
    global setup_set, static_problem_set
    static_problem_set = []
    setup_set = {}
    for n in range(1, 11):
        setup_set = load_setup_set(open(
            "C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\setup_set_{}.json".format(n)))
        static_problem_set = json.load(open(
            "C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\static_problem_set_{}.json".format(n)))

        exec_times = []
        for i in range(10):
            exec_times.append(run_static_problem_test())
        with open("py_static_problem_results_{}.json".format(n), "w") as file:
            json.dump(exec_times, file)


def main():
    #run_static_problem_benchmark()
    #run_dynamic_problem_benchmark()
    run_memory_usage_benchmark()


if __name__ == "__main__":
    main()