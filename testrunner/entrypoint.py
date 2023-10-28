import sys
import subprocess
import os
import logging

log = logging.getLogger(__name__)

def run_test(test_path):
    result = None
    try:
        result = subprocess.run(['pytest', test_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}")
        print("Standard Output:")
        print(e.stdout)
        print("Standard Error:")
        print(e.stderr)
        return

    print(result.stdout)

# TODO better encapsulation
# TODO resolve problem id to test cases
def get_test_cases(problem_id: str):
    if problem_id == 'hello_world':
        return ['hello world', 'hello world']
    else:
        raise KeyError(f'test case definition for {problem_id} not found')

# TODO load test case and run it agains input code path. get input code path output
def run_native_test(input_code_path: str, problem_id: str):
    test_cases = get_test_cases(problem_id)
    try:
        for test_case in test_cases:
            result = subprocess.run(['python', input_code_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            code_output = result.stdout.strip()
            assert code_output == test_case
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}")
        print("Standard Output:")
        print(e.stdout)
        print("Standard Error:")
        print(e.stderr)
        return
    print('all tests successful')


if __name__ == "__main__":
    # Check if both arguments are provided
    if len(sys.argv) != 3:
        print("You must provide exactly 2 arguments: <input_file>, <problem_id>")
        sys.exit(1)

    # Extract arguments
    input_file_path = sys.argv[1] # the file to execute. this requires mount to be at the same path
    problem_id = sys.argv[2]
    print(input_file_path, problem_id)

    if not os.path.isfile(input_file_path):
        print(f'could not get code to run: {input_file_path}')
        sys.exit(1)

    run_native_test(input_file_path, problem_id)