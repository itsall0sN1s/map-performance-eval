import java.io.File;
import java.io.IOException;
import java.text.MessageFormat;
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;

public class Benchmark {
    static ObjectMapper objectmapper = new ObjectMapper();
    static long start_time;
    static long end_time;
    static long time_in_milliseconds;
    public static void main(String[] args) {
        //run_static_problem_benchmark(300);
        //run_dynamic_problem_benchmark(300);
        run_memory_usage_benchmark();
    }
    public static void run_memory_usage_benchmark() {
        for (int n=1; n<11; n++) {
            File setup_set_json = new File(MessageFormat.format("C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\setup_set_{0}.json", n));
            HashMap<Integer, Integer> setup_set = load_setup_data(setup_set_json);
            System.out.println();
        }
    }
    static HashMap<Integer, Integer> load_setup_data(File setup_set_json) {
        HashMap<Integer, Integer> setup_set;
        try {
            setup_set = objectmapper.readValue(setup_set_json, HashMap.class);
            // Put break point here to measure memory usage
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return setup_set;
    }
    static void run_static_problem_test(HashMap<Integer, Integer> setup_set, ArrayList<Integer> static_problem_set) {
        for (Integer key : static_problem_set) {
            setup_set.containsKey(key);
        }
    }
    static void run_static_problem_benchmark(int iterations) {
        for (int n=1; n<11; n++) {
            File setup_set_json = new File(MessageFormat.format("C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\setup_set_{0}.json", n));
            HashMap<Integer, Integer> setup_set = load_setup_data(setup_set_json);
            File static_problem_set_json = new File(MessageFormat.format("C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\static_problem_set_{0}.json", n));
            ArrayList<Integer> static_problem_set;
            ArrayList<Long> exec_times = new ArrayList<>();
            try {
                static_problem_set = objectmapper.readValue(static_problem_set_json, ArrayList.class);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            for (int i=0; i<=iterations; i++) {
                run_static_problem_test(setup_set, static_problem_set);
            }
            for (int i=0; i<10; i++) {
                start_time = System.currentTimeMillis();
                run_static_problem_test(setup_set, static_problem_set);
                end_time = System.currentTimeMillis();
                time_in_milliseconds = end_time - start_time;
                exec_times.add(time_in_milliseconds);
            }
            try {
                objectmapper.writeValue(new File(MessageFormat.format("java_static_problem_results_{0}", n)), exec_times);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }
    static void run_dynamic_problem_test(HashMap<Integer, Integer> setup_set, ArrayList<ArrayList<Object>> dynamic_problem_set) {
        for (ArrayList<Object> instruction : dynamic_problem_set) {
            switch ((String) instruction.get(0)) {
                case "delete":
                    setup_set.remove((int) instruction.get(1));
                    break;
                case "insert":
                    setup_set.put((int) instruction.get(1), (int) instruction.get(2));
                    break;
                case "isMember":
                    setup_set.containsKey((int) instruction.get(1));
                    break;
            }
        }
    }
    static void run_dynamic_problem_benchmark(int iterations) {
        for (int n=1 ; n<11; n++) {
            File setup_set_json = new File(MessageFormat.format("C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\setup_set_{0}.json", n));
            HashMap<Integer, Integer> setup_set = load_setup_data(setup_set_json);
            File dynamic_problem_set_json = new File(MessageFormat.format("C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\dynamic_problem_set_{0}.json", n));
            ArrayList<ArrayList<Object>> dynamic_problem_set;
            ArrayList<Long> exec_times = new ArrayList<>();
            try {
                dynamic_problem_set = objectmapper.readValue(dynamic_problem_set_json, ArrayList.class);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            for (int i=0; i<=iterations;i++){
                run_dynamic_problem_test(setup_set, dynamic_problem_set);
                setup_set = load_setup_data(setup_set_json);
            }
            for (int i=0; i<10; i++) {
                start_time = System.currentTimeMillis();
                run_dynamic_problem_test(setup_set, dynamic_problem_set);
                end_time = System.currentTimeMillis();
                time_in_milliseconds = end_time - start_time;
                exec_times.add(time_in_milliseconds);
                setup_set = load_setup_data(setup_set_json);
            }
            try {
                objectmapper.writeValue(new File(MessageFormat.format("java_dynamic_problem_results_{0}", n)), exec_times);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }
}
