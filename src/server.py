from typing import Union
from subprocess import CalledProcessError
import subprocess
import tempfile
import sys
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

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
    code = payload.code
    # docker run -v /path/on/host:/path/in/container testrunner /path/in/container/filename.txt test1
    result = None
    with tempfile.NamedTemporaryFile(suffix='.py', delete=True) as tmp:
        tmp.write(code.encode())
        print(code.encode())
        tmp.flush()
        try:
            result = subprocess.check_output(['docker', 'run', '-v', f'{tmp.name}:/input/solution.py', 'testrunner', problem_id])
        except CalledProcessError as e:
            print(e.output, file=sys.stderr)
            raise e
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