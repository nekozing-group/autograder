from importlib.resources import files, contents
import tomllib
from typing import List

PACKAGE_NAME = 'shared.data'

class ProblemDataClient:

    def __init__(self, problem_id: str):
        self.problem_id = problem_id
        self.toml = tomllib.loads(files(PACKAGE_NAME).joinpath(f'{problem_id}.toml').read_text())

    def get_problem_description(self) -> str:
        return self.toml['metadata']['problem_description']
    
    def get_reference_implementation(self) -> str:
        return self.toml['metadata']['reference_implementation']
    
    @staticmethod
    def list_problems() -> List[str]:
        problem_list = []
        for resource in contents(PACKAGE_NAME):
            if resource.endswith('.toml'):
                problem_list.append(resource[:-5])
        return problem_list