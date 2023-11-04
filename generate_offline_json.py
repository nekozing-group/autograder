import sys
from pathlib import Path
from src.models import GetProblemStatementResponse,GradeProblemResponse,ListProblemsResponse
from pydantic import BaseModel

'''
test_pass: bool
    error_message: Optional[str] = None
    input: Any
    actual_output: Any
    expected_output: Any
'''

def iter_response_models():
    get_problem_resp = GetProblemStatementResponse(problem_id='problem_id_mock-a', problem_statement='problem_statement_mock')
    list_problems_resp = ListProblemsResponse(problem_id_list=['problem_id_mock-a', 'problem_id_mock-b', 'problem_id_mock-c'])
    
    grade_problem_resp = GradeProblemResponse.model_validate({
        'session_id': 'session_id_mock',
        'error': None,
        'llm_guidance': 'this is something llm said',
        'test_results': {
            'session_id': 'session_id_mock',
            'test_outputs': [
                {
                    'test_pass': True,
                    'input': 5,
                    'actual_output': 5,
                    'expected_output': 5,
                },
                {
                    'test_pass': False,
                    'error_message': 'mock error message',
                    'input': 6,
                    'actual_output': 5,
                    'expected_output': 6,
                }
            ],
            'num_total_tests': 2,
            'num_tests_passed': 1
        }
    })

    for resp in [get_problem_resp, grade_problem_resp, list_problems_resp]:
        yield resp

# this class generates json files for use in the front end
def generate_json_files(folder):
    model: BaseModel
    for model in iter_response_models():
        file_name = f'{type(model).__name__}.json'
        with open(folder / file_name, 'w', encoding='utf-8') as file:
            file.write(model.model_dump_json())

if __name__ == '__main__':
    folder = Path('json')
    folder.mkdir(exist_ok=True)
    generate_json_files(folder)