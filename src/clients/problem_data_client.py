from importlib.resources import files, contents
import tomllib
from typing import List

PACKAGE_NAME = 'src.data'

class ProblemDataClient:
    def get_problem_description(self, problem_id: str) -> str:
        toml = tomllib.loads(files(PACKAGE_NAME).joinpath(f'{problem_id}.toml').read_text())
        return toml['metadata']['problem_description']
    
    def list_problems(self) -> List[str]:
        problem_list = []
        for resource in contents(PACKAGE_NAME):
            if resource.endswith('.toml'):
                problem_list.append(resource[:-5])
        return problem_list