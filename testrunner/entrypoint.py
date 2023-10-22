import sys
import subprocess
import os

# def run_test1(filepath):
#     with open(filepath, 'r') as file:
#         content = file.read()
#     print(f"Running test1 on: {content}")

# def run_test2(filepath):
#     with open(filepath, 'r') as file:
#         content = file.read()
#     print(f"Running test2 on: {content}")


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

if __name__ == "__main__":
    # Check if both arguments are provided
    if len(sys.argv) != 2:
        print("You must provide exactly 1 argument: <test_name>")
        sys.exit(1)

    # Extract arguments
    test_name = sys.argv[1]
    print(test_name)
    test_path = os.path.join('tests', f'{test_name}.py')

    if not os.path.isfile(test_path):
        print(f'could not find grader for {test_name}')
        sys.exit(1)

    run_test(test_path)