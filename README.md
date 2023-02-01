# Performance evaluation of Map implementations in Java, Python and CS
## BSc. Thesis 2023
## Kristian Nedelchev

This respository contains the code needed to reproduce the experiments conducted in my BSc. thesis. The paper itself can be found in `Performance evaluation of Map implementations in Java, Python and CS.pdf`. Description of the files below:
- `data-set-generator\dataset_generator.py`. contains the source code that generates the data sets with which the experiments will be conducted.
- `python-benchmarks\Benchmark.py` contains the source code that evaluates the performance of Python's dict.
- `java-benchmarks\Benchmark.java` contains the source code that evaluates the performance of Java's HashMap.
- `cs-benchmarks\Benchmark.cs` contains the source code that evaluates the performance of C#'s Dictionary.
- `graph-generator\main.py` contains the Python script that generates the graphs from the results of the experiments.
- `Data-sets` contains the data sets that were used to perform the experiments
- `Results` contains the results of the experiments
