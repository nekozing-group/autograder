from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from .clients.testrunner_client import TestrunnerClient
from .clients.problem_data_client import ProblemDataClient
from .grader import Grader
import logging
import uuid

log = logging.getLogger(__name__)

app = FastAPI()

grader = Grader()

class GradeProblemPayload(BaseModel):
    user_id: Optional[str] = 'testuser'
    code: str

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get('/problems')
async def list_problems():
    return ProblemDataClient.list_problems()

@app.get('/problems/{problem_id}')
async def problem_statement(problem_id: str):
    data_client = ProblemDataClient(problem_id)
    problem_statement = data_client.get_problem_description()
    return {
        'problem_id': problem_id,
        'problem_statement': problem_statement
    }

@app.post('/grade/{problem_id}')
async def grade_problem(problem_id: str, payload: GradeProblemPayload):
    code = payload.code
    log.info('received payload %s', payload.model_dump_json())
    session_id = str(uuid.uuid4())
    result = grader.grade_code(session_id, code, problem_id)
    return {"message": f"Code for problem {problem_id} received!", "exec_result": result}
