from importlib.resources import files, contents
from typing import List

PACKAGE_NAME = 'src.data'

class ProblemDataClient:
    def get_problem_statement(self, problem_id: str) -> str:
        md_str = files(PACKAGE_NAME).joinpath(f'{problem_id}.md').read_text()
        return md_str
    
    def list_problems(self) -> List[str]:
        problem_list = []
        for resource in contents(PACKAGE_NAME):
            if resource.endswith('.md'):
                problem_list.append(resource[:-3])
        return problem_list