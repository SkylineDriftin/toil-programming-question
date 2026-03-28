'''
run this directly from terminal as such:
 py -m src.attack_planner.tests.test_generator

'''


import json
import os
import random

# helper to save json to test_cases folder
def save_test(name, data, folder="src/attack_planner/tests/test_cases"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, f"{name}.json")
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"generated: {path}")

def generate_bottleneck_case():
    # simple case where one pipe is the absolute bottleneck
    data = {
        "facilities": [
            {"name": "Producer_A", "max_production": 500},
            {"name": "Consumer_B", "max_consumption": 500}
        ],
        "pipelines": [
            {"name": "Thin_Pipe", "capacity": 50, "facilities": ["Producer_A", "Consumer_B"]}
        ],
        "expected_result": {
            "total_consumption_before": 50.0,
            "pipeline_name": "Thin_Pipe"
        }
    }
    save_test("bottleneck_simple", data)

def generate_random_stress_test(num_facilities=50, num_pipelines=20):
    # generates a large random network to test igraph performance
    facilities = []
    for i in range(num_facilities):
        fac = {"name": f"Fac_{i}"}
        rtype = random.random()
        if rtype < 0.3:
            fac["max_production"] = random.randint(100, 1000)
        elif rtype < 0.6:
            fac["max_consumption"] = random.randint(100, 1000)
        facilities.append(fac)

    pipelines = []
    fac_names = [f["name"] for f in facilities]
    for i in range(num_pipelines):
        # random facility strings for pipelines
        path_len = random.randint(2, 5)
        path = random.sample(fac_names, path_len)
        pipelines.append({
            "name": f"Route_{i}",
            "capacity": random.randint(50, 500),
            "facilities": path
        })

    data = {
        "facilities": facilities,
        "pipelines": pipelines
    }
    save_test("stress_test_large", data)

def generate_reroute_test():
    # test if flow re-routes when the primary path is cut
    data = {
        "facilities": [
            {"name": "Supply", "max_production": 1000},
            {"name": "Hub", "max_consumption": 0},
            {"name": "Demand", "max_consumption": 1000}
        ],
        "pipelines": [
            {"name": "Short_Path", "capacity": 400, "facilities": ["Supply", "Demand"]},
            {"name": "Long_Path_A", "capacity": 300, "facilities": ["Supply", "Hub"]},
            {"name": "Long_Path_B", "capacity": 300, "facilities": ["Hub", "Demand"]}
        ],
        "expected_result": {
            "total_consumption_before": 700.0, # 400 + 300
            "pipeline_name": "Short_Path" 
        }
    }
    save_test("reroute_test", data)

def generate_dead_end_case():
    # test where a producer has no path to any consumer
    data = {
        "facilities": [
            {"name": "Isolated_Producer", "max_production": 1000},
            {"name": "Isolated_Consumer", "max_consumption": 1000}
        ],
        "pipelines": [], # no pipelines at all
        "expected_result": {
            "total_consumption_before": 0.0,
            "pipeline_name": None
        }
    }
    save_test("dead_end_island", data)

def generate_cycle_reroute():
    # tests a triangle of facilities where flow can swap directions
    data = {
        "facilities": [
            {"name": "A", "max_production": 100},
            {"name": "B", "max_consumption": 0},
            {"name": "C", "max_consumption": 100}
        ],
        "pipelines": [
            {"name": "Direct", "capacity": 10, "facilities": ["A", "C"]},
            {"name": "Loop_Part1", "capacity": 100, "facilities": ["A", "B"]},
            {"name": "Loop_Part2", "capacity": 100, "facilities": ["B", "C"]}
        ],
        "expected_result": {
            "total_consumption_before": 100.0,
            "pipeline_name": "Loop_Part1" 
        }
    }
    save_test("triangle_cycle", data)

def generate_oversupply_case():
    # test where production far exceeds pipe capacity
    data = {
        "facilities": [
            {"name": "Super_Source", "max_production": 999999},
            {"name": "Small_Sink", "max_consumption": 10}
        ],
        "pipelines": [
            {"name": "Huge_Pipe", "capacity": 999999, "facilities": ["Super_Source", "Small_Sink"]}
        ],
        "expected_result": {
            "total_consumption_before": 10.0,
            "pipeline_name": "Huge_Pipe"
        }
    }
    save_test("oversupply_bottleneck", data)

def generate_parallel_pipes():
    # tests if two separate pipelines between same nodes add up
    data = {
        "facilities": [
            {"name": "S", "max_production": 100},
            {"name": "T", "max_consumption": 100}
        ],
        "pipelines": [
            {"name": "Pipe_1", "capacity": 30, "facilities": ["S", "T"]},
            {"name": "Pipe_2", "capacity": 40, "facilities": ["S", "T"]}
        ],
        "expected_result": {
            "total_consumption_before": 70.0,
            "pipeline_name": "Pipe_2"
        }
    }
    save_test("parallel_pipes", data)


if __name__ == "__main__":
    generate_bottleneck_case()
    generate_reroute_test()
    generate_random_stress_test(num_facilities=1000, num_pipelines=500)
    generate_dead_end_case()
    generate_cycle_reroute()
    generate_oversupply_case()
    generate_parallel_pipes()