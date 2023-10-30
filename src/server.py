from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from .clients.testrunner_client import TestrunnerClient
from .clients.data_client import DataClient
import logging
import uuid

log = logging.getLogger(__name__)

app = FastAPI()

testrunner_client = TestrunnerClient()
data_client = DataClient()

class CodePayload(BaseModel):
    code: str


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get('/problem_statement/{problem_id}')
async def problem_statement(problem_id: str):
    problem_statement = data_client.get_problem_statement(problem_id)
    return {
        'problem_id': problem_id,
        'problem_statement': problem_statement
    }

@app.post('/grade/{problem_id}')
async def grade_problem(problem_id: str, payload: CodePayload):
    code = payload.code
    log.info(code)
    session_id = str(uuid.uuid4())
    result = testrunner_client.execute_code(session_id, code, problem_id)
    return {"message": f"Code for problem {problem_id} received!", "content": code, "exec_result": result}
