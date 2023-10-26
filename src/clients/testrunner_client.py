import subprocess
import tempfile
import sys
from kubernetes import client, config

class TestrunnerClient:
    def execute_code(self, problem_id: str, code: str):
        result = None
        with tempfile.NamedTemporaryFile(suffix='.py', delete=True) as tmp:
            tmp.write(code)
            print(code)
            tmp.flush()
            try:
                result = subprocess.check_output(['docker', 'run', '-v', f'{tmp.name}:/input/solution.py', 'testrunner', problem_id])
            except subprocess.CalledProcessError as e:
                print(e.output, file=sys.stderr)
                raise e    
        result = subprocess.check_output(['docker', 'run', '-v', f'{tmp.name}:/input/solution.py', 'testrunner', problem_id])
        return result