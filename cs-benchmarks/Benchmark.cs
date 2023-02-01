using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using System.IO;
using System.Diagnostics;

namespace Dictionary_Benchmark
{
    internal class Benchmark
    {
        static void Main(string[] args)
        {
            //run_static_problem_benchmark();
            //run_dynamic_problem_benchmark();
            memory_benchmark();
        }

        static Dictionary<int, int> load_setup_set(string setup_set_json)
        {
            Dictionary<int, int> setup_set = JsonConvert.DeserializeObject<Dictionary<int, int>>(setup_set_json);
            return setup_set;
        }
        static void run_static_problem_benchmark()
        {
            for (int n = 1; n < 11; n++)
            {
                string setup_set_json = File.ReadAllText($"C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\setup_set_{n}.json");
                Dictionary<int, int> setup_set = load_setup_set(setup_set_json);
                string static_problem_set_json = File.ReadAllText($"C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\static_problem_set_{n}.json");
                List<int> static_problem_set = JsonConvert.DeserializeObject<List<int>>(static_problem_set_json);
                List<long> exec_times = new List<long>();
                for(int i=0; i < 10; i++)
                {
                    exec_times.Add(run_static_problem_test(setup_set, static_problem_set));
                }
                string exec_times_json = JsonConvert.SerializeObject(exec_times);
                File.WriteAllText($"C:\\Users\\chris\\Desktop\\C#\\cs_static_problem_results_{n}.json", exec_times_json);
            }
        }
        static long run_static_problem_test(Dictionary<int, int> setup_set, List<int> static_problem_set)
        {
            long start_time = DateTimeOffset.Now.ToUnixTimeMilliseconds();
            foreach (int key in static_problem_set)
            {
                setup_set.ContainsKey(key);
            }
            long end_time = DateTimeOffset.Now.ToUnixTimeMilliseconds();
            long exec_time = end_time - start_time;

            return exec_time;
        }
        static void run_dynamic_problem_benchmark()
        {
            for(int n=1; n<11; n++)
            {
                string setup_set_json = File.ReadAllText($"C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\setup_set_{n}.json");
                Dictionary<int, int> setup_set = load_setup_set(setup_set_json);
                string dynamic_problem_set_json = File.ReadAllText($"C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\dynamic_problem_set_{n}.json");
                List<List<Object>> dynamic_problem_set = JsonConvert.DeserializeObject<List<List<Object>>>(dynamic_problem_set_json);
                List<long> exec_times= new List<long>();
                for(int i=0; i<10; i++)
                {
                    exec_times.Add(run_dynamic_problem_test(setup_set, dynamic_problem_set));
                    setup_set = load_setup_set(setup_set_json);
                }
                string exec_times_json = JsonConvert.SerializeObject(exec_times);
                File.WriteAllText($"C:\\Users\\chris\\Desktop\\C#\\cs_dynamic_problem_results_{n}.json", exec_times_json);
            }
        }
        static long run_dynamic_problem_test(Dictionary<int, int> setup_set, List<List<Object>> dynamic_problem_set)
        {
            long start_time = DateTimeOffset.Now.ToUnixTimeMilliseconds();
            foreach (List<Object> instruction in dynamic_problem_set)
            {
                switch ((string)instruction[0])
                {
                    case "delete":
                        setup_set.Remove(Convert.ToInt32(instruction[1]));
                        break;
                    case "insert":
                        setup_set.Add(Convert.ToInt32(instruction[1]), Convert.ToInt32(instruction[2]));
                        break;
                    case "isMember":
                        setup_set.ContainsKey(Convert.ToInt32(instruction[1]));
                        break;
                }
            }
            long end_time = DateTimeOffset.Now.ToUnixTimeMilliseconds();
            long exec_time = end_time-start_time;

            return exec_time;
        }
        static void memory_benchmark()
        {
            for (int n = 1; n < 11; n++)
            {
                string setup_set_json = File.ReadAllText($"C:\\Users\\chris\\PycharmProjects\\dataset_generator\\venv\\Source\\setup_set_{n}.json");
                Dictionary<int, int> setup_set = load_setup_set(setup_set_json);
            }
        }
    }
}
