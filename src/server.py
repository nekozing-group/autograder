from typing import Union
from subprocess import CalledProcessError
import subprocess
import tempfile
import sys
from pydantic import BaseModel
from fastapi import FastAPI
from .clients.testrunner_client import TestrunnerClient


app = FastAPI()

testrunner_client = TestrunnerClient()

class CodePayload(BaseModel):
    code: str


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



@app.post('/grade/{problem_id}')
async def grade_problem(problem_id: str, payload: CodePayload):
    code = payload.code.encode()
    # docker run -v /path/on/host:/path/in/container testrunner /path/in/container/filename.txt test1
    
    result = testrunner_client.execute_code(problem_id, code)
    return {"message": f"Code for problem {problem_id} received!", "content": code, "exec_result": result}


'''
import subprocess
import tempfile

with tempfile.NamedTemporaryFile(suffix=".py", delete=True) as tmp:
    tmp.write(code_str.encode())
    tmp.flush()  
    output = subprocess.check_output(["python", tmp.name])
print(output)
'''