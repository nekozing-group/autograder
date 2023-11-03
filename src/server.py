from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from .clients.problem_data_client import ProblemDataClient
from .models import GetProblemStatementResponse, GradeProblemRequest, GradeProblemResponse, ListProblemsResponse
from .grader import Grader
import logging
import uuid

log = logging.getLogger(__name__)

app = FastAPI()

grader = Grader()

@app.get('/problems')
async def list_problems() -> ListProblemsResponse:
    problem_id_list = ProblemDataClient.list_problems()
    return ListProblemsResponse(problem_id_list=problem_id_list)

@app.get('/problems/{problem_id}')
async def get_problem_statement(problem_id: str) -> GetProblemStatementResponse:
    data_client = ProblemDataClient(problem_id)
    problem_statement = data_client.get_problem_description()
    return GetProblemStatementResponse(
        problem_id=problem_id, 
        problem_statement=problem_statement
    )

@app.post('/grade/{problem_id}')
async def grade_problem(problem_id: str, payload: GradeProblemRequest) -> GradeProblemResponse:
    code = payload.code
    log.info('received payload %s', payload.model_dump_json())
    session_id = str(uuid.uuid4())
    result = grader.grade_code(session_id, code, problem_id)
    response = GradeProblemResponse.model_validate(result.model_dump())
    return response
