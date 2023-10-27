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

def run_native_test(input_code_path, test_case):
    # for now test_case == eval(input_code)
    result = None
    try:
        result = subprocess.run(['python', input_code_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}")
        print("Standard Output:")
        print(e.stdout)
        print("Standard Error:")
        print(e.stderr)
        return
    print(result)
    assert result.stdout.strip() == test_case


if __name__ == "__main__":
    # Check if both arguments are provided
    if len(sys.argv) != 3:
        print("You must provide exactly 2 arguments: <input_file>, <test_case>")
        sys.exit(1)

    # Extract arguments
    input_file = sys.argv[1]
    test_case = sys.argv[2]
    print(input_file)
    input_code_path = os.path.join('/input', f'{input_file}.py')

    if not os.path.isfile(input_code_path):
        print(f'could not get code to run: {input_code_path}')
        sys.exit(1)

    run_native_test(input_code_path, test_case)