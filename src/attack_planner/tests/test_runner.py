'''
run this directly from terminal as such:
 py -m src.attack_planner.tests.test_runner

'''

import os
import json
from src.attack_planner.distribution_network import DistributionNetwork
def run_tests(test_folder="src/attack_planner/tests/test_cases"):
    print(f"{'TEST CASE':<30} | {'STATUS':<10} | {'MESSAGE'}")
    print("-" * 75)

    passed = 0
    test_files = [f for f in os.listdir(test_folder) if f.endswith('.json')]

    for file_name in test_files:
        path = os.path.join(test_folder, file_name)
        with open(path, 'r') as f:
            test_data = json.load(f)

        try:
            network = DistributionNetwork.from_json(test_data)
            result = network.plan_attack()
            
            # 1. handle missing expected_result (stress tests)
            expected = test_data.get("expected_result")
            if expected is None:
                print(f"{file_name:<30} | PASS       | No expected result provided (Stress Test)")
                passed += 1
                continue

            # 2. validate consumption
            actual_before = result.get("total_consumption_before", 0.0)
            exp_before = expected.get("total_consumption_before", 0.0)
            
            if abs(actual_before - exp_before) > 1e-5:
                raise ValueError(f"Flow mismatch: Got {actual_before}, expected {exp_before}")

            # 3. validate pipeline name
            actual_name = result.get("pipeline_name")
            exp_name = expected.get("pipeline_name")
            
            if actual_name != exp_name:
                raise ValueError(f"Target mismatch: Hit {actual_name}, expected {exp_name}")

            print(f"{file_name:<30} | \033[92mPASS\033[0m       | OK")
            passed += 1

        except Exception as e:
            # this prints the actual error message clearly
            print(f"{file_name:<30} | \033[91mFAIL\033[0m       | {str(e)}")

    print("-" * 75)
    print(f"Final Score: {passed}/{len(test_files)} passed.")
if __name__ == "__main__":
    run_tests()
    print('tests finished')