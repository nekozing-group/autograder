from src.clients.problem_data_client import ProblemDataClient

def test_problem_client():
    client = ProblemDataClient()
    problem_list = client.list_problems()
    assert 'sort' in problem_list
    
    problem_statement = client.get_problem_description('sort')
    assert 'sort' in problem_statement