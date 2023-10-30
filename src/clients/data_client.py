from importlib.resources import files 

class DataClient:
    def get_problem_statement(self, problem_id: str) -> str:
        md_str = files('src.data').joinpath(f'{problem_id}.md').read_text()
        return md_str